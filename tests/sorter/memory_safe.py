import unittest
import string
import random
import datetime
import os
import re
from devoutils.sorter import Sorter, compare_num, compare_date, parser_regex, \
    parser_delimiter

RE_D5 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{5})"
RE_D56 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})"
RE_D6 = r"(\d{4}\-\d{2}\-\d{2} \d{2}:\d{2}:\d{2}\.\d{6})"


def to_str(my_str):
    return str(my_str).encode("utf-8")


def _random_date():
    year = random.randint(1950, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    milis = random.randint(0, 999999)
    return datetime.datetime(year, month, day, hour, minute, second, milis) \
        .strftime('%Y-%m-%d %H:%M:%S.%f')


def _create_random_regex_date_file(length, rows, file_source):
    if os.path.isfile(file_source):
        os.remove(file_source)
    with open(file_source, 'w') as file:
        for _ in range(rows):
            line = ''.join(random.choice(string.ascii_uppercase)
                           for _ in range(length)) + \
                   '##{}##{}\n'.format(_random_date(),
                                       random.uniform(-1000.0, 1000.0))
            file.write(line)


def _create_fast_pseudo_random_regex_date_file(length, rows, file_source):
    if os.path.isfile(file_source):
        os.remove(file_source)
    with open(file_source, 'w') as file:
        for _ in range(rows):
            line = 'abdcd-f-dejeje-99283ldjjdjeje-af92-8fifn!jfjf^dad##{}#' \
                   '#{}##{}\n'.format((length / 50),
                                      _random_date(),
                                      random.uniform(-1000.0, 1000.0))
            file.write(line)


class TestMemSafeSorter(unittest.TestCase):
    __DATAFILE__ = "testData.log"
    __DATAFILE2__ = "testData2.log"
    __TARGETFILE__ = "outputData.log"

    def __init__(self, *args, **kwargs):
        super(TestMemSafeSorter, self).__init__(*args, **kwargs)
        self.sorter = Sorter()

    def test_str(self):
        self._delete_target_file()
        self._create_random_str_file(1000, 10000)
        self.sorter.sort_file(self.__DATAFILE__, self.__TARGETFILE__,
                              memory_safe=True, max_mem=5000000)
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertTrue(prev_line <= line)
                prev_line = line

    def _delete_target_file(self):
        if os.path.isfile(self.__TARGETFILE__):
            os.remove(self.__TARGETFILE__)

    def test_sort_generator_memory_safe(self):
        self._delete_target_file()
        my_generator = (random.choice(range(100)) for _ in range(100))
        result = self.sorter.sort_iterator(my_generator,
                                           dst_file=self.__TARGETFILE__,
                                           memory_safe=True)

        prev = -1
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line and prev_line:
                    self.assertGreaterEqual(int(line), int(prev_line))
                prev_line = line
        self._delete_target_file()

    def test_str_reverse(self):
        self._delete_target_file()
        self._create_random_str_file(1000, 10000)
        self.sorter.sort_file(self.__DATAFILE__, self.__TARGETFILE__,
                              reverse=True, memory_safe=True, max_men=5000000)
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertTrue(prev_line >= line)
                prev_line = line

    def test_numbercomma(self):
        self._delete_target_file()
        self._create_random_comma_file(100, 10000)
        self.sorter.sort_file(self.__DATAFILE__, self.__TARGETFILE__,
                              comp=compare_num(parser_delimiter(",", 1)),
                              memory_safe=True, max_men=5000000)
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertTrue(float(prev_line.split(',')[1])
                                    <= float(line.split(',')[1]))
                prev_line = line

    def test_numbercomma_reverse(self):
        self._delete_target_file()
        self._create_random_comma_file(100, 10000)
        self.sorter.sort_file(self.__DATAFILE__, self.__TARGETFILE__,
                              reverse=True,
                              comp=compare_num(parser_delimiter(",", 1)),
                              memory_safe=True, max_men=5000000)
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertGreaterEqual(float(prev_line.split(',')[1]),
                                            float(line.split(',')[1]))
                prev_line = line

    def test_dateregex(self):
        self._delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        self.sorter.sort_file(self.__DATAFILE__, self.__TARGETFILE__,
                              comp=compare_date('%Y-%m-%d %H:%M:%S.%f',
                                                parser_regex(RE_D56, 0)),
                              memory_safe=True, max_men=5000000)
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertTrue(
                        datetime.datetime.strptime(
                            re.search(
                                RE_D5,
                                prev_line).groups()[0], '%Y-%m-%d %H:%M:%S.%f')
                        <= datetime.datetime.strptime(
                            re.search(
                                RE_D5,
                                line).groups()[0], '%Y-%m-%d %H:%M:%S.%f'))
                prev_line = line

    def test_transform(self):
        self._delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        self.sorter.sort_file(self.__DATAFILE__, self.__TARGETFILE__,
                              transform=lambda x: re.search(RE_D6, x).groups()[0] + "##" + x,
                              memory_safe=True, max_men=5000000)
        with open(self.__TARGETFILE__, 'rb') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertLessEqual(prev_line, line)
                prev_line = line

    def test_date_regex_no_file(self):
        self._delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        data = self.sorter.sort_file(self.__DATAFILE__,
                                     comp=compare_date('%Y-%m-%d %H:%M:%S.%f',
                                                       parser_regex(RE_D56, 0)),
                                     memory_safe=True, max_men=5000000)
        prev_line = None
        for line in data:
            if prev_line:
                self.assertTrue(
                    datetime.datetime.strptime(
                        re.search(RE_D5,
                                  prev_line).groups()[0], '%Y-%m-%d %H:%M:%S.%f')
                    <= datetime.datetime.strptime(
                        re.search(RE_D5,
                                  line).groups()[0], '%Y-%m-%d %H:%M:%S.%f'))
            prev_line = line

    def test_dateregex_multifile(self):
        self._delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        _create_random_regex_date_file(100, 10000, self.__DATAFILE2__)
        data = self.sorter.sort_file("./", file_pattern="testData.*\\.log",
                                     comp=compare_date('%Y-%m-%d %H:%M:%S.%f',
                                                       parser_regex(RE_D56, 0)),
                                     memory_safe=True, max_men=5000000)
        prev_line = None
        size = 0
        for line in data:
            size += 1
            if prev_line:
                self.assertLessEqual(
                    datetime.datetime.strptime(
                        re.search(RE_D5,
                                  prev_line).groups()[0], '%Y-%m-%d %H:%M:%S.%f')
                    , datetime.datetime.strptime(
                        re.search(
                            RE_D5,
                            line).groups()[0], '%Y-%m-%d %H:%M:%S.%f'))
            prev_line = line
        self.assertEqual(size, 20000)

    def test_dateregex_multifile_list(self):
        self._delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        _create_random_regex_date_file(100, 10000, self.__DATAFILE2__)
        data = self.sorter.sort_file([self.__DATAFILE__, self.__DATAFILE2__],
                                     comp=compare_date('%Y-%m-%d %H:%M:%S.%f',
                                                       parser_regex(RE_D56, 0)),
                                     memory_safe=True,
                                     max_men=5000000)
        prev_line = None
        size = 0
        for line in data:
            size += 1
            if prev_line:
                self.assertLessEqual(
                    datetime.datetime.strptime(
                        re.search(RE_D5,
                                  prev_line).groups()[0],
                        '%Y-%m-%d %H:%M:%S.%f'),
                    datetime.datetime.strptime(
                        re.search(RE_D5,
                                  line).groups()[0], '%Y-%m-%d %H:%M:%S.%f'))
            prev_line = line
        self.assertEqual(size, 20000)

    def test_big_file_custom_size(self):
        self._delete_target_file()
        total_rows = 10000000
        _create_fast_pseudo_random_regex_date_file(1000,
                                                   total_rows,
                                                   self.__DATAFILE__)
        data = self.sorter.sort_file(self.__DATAFILE__,
                                     comp=compare_num(parser_delimiter("##", 3)),
                                     memory_safe=True, max_men=200000000)
        prev_line = None
        size = 0
        for line in data:
            if prev_line:
                self.assertLessEqual(float(prev_line.split('##')[3]),
                                     float(line.split('##')[3]))
            prev_line = line
            size += 1
        self.assertEqual(total_rows, size)
        os.remove(self.__DATAFILE__)

    def test_big_file_custom_size_transfrom(self):
        self._delete_target_file()
        total_rows = 10000000
        _create_fast_pseudo_random_regex_date_file(1000,
                                                   total_rows,
                                                   self.__DATAFILE__)
        data = self.sorter.sort_file(self.__DATAFILE__,
                                     transform=lambda x: re.search(RE_D6, x).groups()[0] + "##" + x,
                                     memory_safe=True,
                                     max_men=200000000)
        prev_line = None
        size = 0
        for line in data:
            if prev_line:
                self.assertLessEqual(prev_line, line)
            prev_line = line
            size += 1
        self.assertEqual(total_rows, size)
        os.remove(self.__DATAFILE__)

    def test_big_file_default(self):
        self._delete_target_file()
        total_rows = 10000000
        _create_fast_pseudo_random_regex_date_file(1000, total_rows,
                                                   self.__DATAFILE__)
        data = self.sorter.sort_file(self.__DATAFILE__,
                                     comp=compare_num(
                                         parser_delimiter("##", 3)),
                                     memory_safe=True)
        prev_line = None
        size = 0
        for line in data:
            if prev_line:
                self.assertLessEqual(float(prev_line.split('##')[1]),
                                     float(line.split('##')[1]))
            prev_line = line
            size += 1
        self.assertEqual(total_rows, size)
        os.remove(self.__DATAFILE__)

    def test_big_file_10_perc(self):
        self._delete_target_file()
        total_rows = 10000000
        _create_fast_pseudo_random_regex_date_file(1000, total_rows,
                                                   self.__DATAFILE__)
        data = self.sorter.sort_file(self.__DATAFILE__,
                                     comp=compare_num(parser_delimiter("##", 3)),
                                     memory_safe=True, avmemperc=0.1)
        prev_line = None
        size = 0
        for line in data:
            if prev_line:
                self.assertLessEqual(float(prev_line.split('##')[1]),
                                     float(line.split('##')[1]))
            prev_line = line
            size += 1
        self.assertEqual(total_rows, size)
        os.remove(self.__DATAFILE__)

    def _create_random_str_file(self, length, rows):
        if os.path.isfile(self.__DATAFILE__):
            os.remove(self.__DATAFILE__)
        with open(self.__DATAFILE__, 'w') as file:
            for _ in range(rows):
                file.write(
                    ''.join(
                        random.choice(string.ascii_uppercase + string.digits)
                        for _ in range(length)) + "\n")

    def _create_random_comma_file(self, length, rows):
        if os.path.isfile(self.__DATAFILE__):
            os.remove(self.__DATAFILE__)
        with open(self.__DATAFILE__, 'w') as file:
            for _ in range(rows):
                file.write(
                    ''.join(random.choice(string.ascii_uppercase)
                            for _ in range(length)) +
                    ',' + str(random.uniform(-1000.0, 1000.0)) + "\n")
