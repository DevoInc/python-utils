import unittest
import string
import random
import os
import re
from datetime import datetime
from devoutils.sorter import Sorter, compare_num, parser_delimiter, \
    compare_date, parser_regex


RE_D5 = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{5})"
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
    return datetime(year, month, day, hour, minute, second, milis) \
        .strftime('%Y-%m-%d %H:%M:%S.%f')


def _create_random_regex_date_file(length, rows, file_source):
    if os.path.isfile(file_source):
        os.remove(file_source)
    with open(file_source, 'wb') as file:
        for _ in range(rows):
            file.write(
                (''.join(
                    random.choice(string.ascii_uppercase) for _ in range(length)
                ) + '##{}##{}\n'.format(_random_date(),
                                        to_str(random.uniform(-1000.0, 1000.0)))
                 ).encode("utf-8")
            )


class TestSimpleSorter(unittest.TestCase):
    __DATAFILE__ = "testData.log"
    __DATAFILE2__ = "testData2.log"
    __TARGETFILE__ = "outputData.log"

    def __init__(self, *args, **kwargs):
        super(TestSimpleSorter, self).__init__(*args, **kwargs)
        self.sorter = Sorter()
        os.chdir("{!s}{!s}".format(os.path.dirname(os.path.abspath(__file__)),
                                   os.sep))

    def test_str_skip_rows(self):
        self.__delete_target_file()
        self._create_random_str_file(1000, 10000)

        self.sorter.sort_file(self.__DATAFILE__,
                              dst_file=self.__TARGETFILE__,
                              rows_to_skip=4)
        with open(self.__TARGETFILE__, 'rb') as file:
            size = 0
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertLessEqual(prev_line, line)
                prev_line = line
                size += 1
            self.assertEqual(9996, size)

    def test_str(self):
        self.__delete_target_file()
        self._create_random_str_file(1000, 10000)
        self.sorter.sort_file(self.__DATAFILE__, dst_file=self.__TARGETFILE__)
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertLessEqual(prev_line, line)
                prev_line = line

    def test_sort_generator(self):
        my_generator = (random.choice(range(100)) for _ in range(100))
        result = self.sorter.sort_iterator(my_generator)

        prev = -1
        for value in result:
            self.assertGreaterEqual(value, prev)
            prev = value

    def __delete_target_file(self):
        if os.path.isfile(self.__TARGETFILE__):
            os.remove(self.__TARGETFILE__)

    def test_str_reverse(self):
        self.__delete_target_file()
        self._create_random_str_file(1000, 10000)
        self.sorter.sort_file(self.__DATAFILE__,
                              dst_file=self.__TARGETFILE__,
                              reverse=True)
        with open(self.__TARGETFILE__, 'rb') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertGreaterEqual(prev_line, line)
                prev_line = line

    def test_number_comma(self):
        self.__delete_target_file()
        self._create_random_comma_file(100, 10000)
        self.sorter.sort_file(self.__DATAFILE__,
                              dst_file=self.__TARGETFILE__,
                              comp=compare_num(parser_delimiter(",", 1)))
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertLessEqual(float(prev_line.split(',')[1]),
                                         float(line.split(',')[1]))
                prev_line = line

    def test_number_comma_reverse(self):
        self.__delete_target_file()
        self._create_random_comma_file(100, 10000)
        self.sorter.sort_file(self.__DATAFILE__,
                              dst_file=self.__TARGETFILE__,
                              reverse=True,
                              comp=compare_num(parser_delimiter(",", 1)))
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertGreaterEqual(float(prev_line.split(',')[1]),
                                            float(line.split(',')[1]))
                prev_line = line
        file.close()

    def test_date_regex(self):
        self.__delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        self.sorter.sort_file(self.__DATAFILE__,
                              dst_file=self.__TARGETFILE__,
                              comp=compare_date('%Y-%m-%d %H:%M:%S.%f',
                                                parser_regex(RE_D6, 0)))
        with open(self.__TARGETFILE__, 'r') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertLessEqual(
                        datetime.strptime(
                            re.search(RE_D5, prev_line).groups()[0],
                            '%Y-%m-%d %H:%M:%S.%f'
                        ),
                        datetime.strptime(re.search(RE_D5, line).groups()[0],
                                          '%Y-%m-%d %H:%M:%S.%f'))
                prev_line = line

    def test_transform(self):
        self.__delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        self.sorter.sort_file(self.__DATAFILE__,
                              dst_file=self.__TARGETFILE__,
                              transform=lambda x: re.search(RE_D6, x).
                              groups()[0] + "##" + x)
        with open(self.__TARGETFILE__, 'rb') as file:
            prev_line = file.readline()
            while prev_line:
                line = file.readline()
                if line:
                    self.assertLessEqual(prev_line, line)
                prev_line = line

    def test_date_regex_no_file(self):
        self.__delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        data = self.sorter.sort_file(self.__DATAFILE__,
                                     comp=compare_date('%Y-%m-%d %H:%M:%S.%f',
                                                       parser_regex(RE_D6, 0)))
        prev_line = None
        for line in data:
            if prev_line:
                self.assertLessEqual(
                    datetime.strptime(
                        re.search(RE_D5, prev_line).groups()[0],
                        '%Y-%m-%d %H:%M:%S.%f'),
                    datetime.strptime(re.search(RE_D5, line).groups()[0],
                                      '%Y-%m-%d %H:%M:%S.%f'))
            prev_line = line

    def test_date_regex_multi_file(self):
        self.__delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        _create_random_regex_date_file(100, 10000, self.__DATAFILE2__)
        data = self.sorter.sort_file("./",
                                     file_pattern="test.*\\.log",
                                     comp=compare_date('%Y-%m-%d %H:%M:%S.%f',
                                                       parser_regex(RE_D6, 0)
                                                       )
                                     )
        prev_line = None
        size = 0
        for line in data:
            size += 1
            if prev_line:
                self.assertLessEqual(
                    datetime.strptime(
                        re.search(RE_D5, prev_line).groups()[0],
                        '%Y-%m-%d %H:%M:%S.%f'),
                    datetime.strptime(
                        re.search(RE_D5, line).groups()[0],
                        '%Y-%m-%d %H:%M:%S.%f'))
            prev_line = line
        self.assertEqual(size, 20000)

    def test_date_regex_multi_file_list(self):
        self.__delete_target_file()
        _create_random_regex_date_file(100, 10000, self.__DATAFILE__)
        _create_random_regex_date_file(100, 10000, self.__DATAFILE2__)
        data = self.sorter.sort_file([self.__DATAFILE__, self.__DATAFILE2__],
                                     comp=compare_date(
                                         '%Y-%m-%d %H:%M:%S.%f',
                                         parser_regex(RE_D6, 0)))
        prev_line = None
        size = 0
        for line in data:
            size += 1
            if prev_line:
                self.assertLessEqual(
                    datetime.strptime(
                        re.search(RE_D5, prev_line).groups()[0],
                        '%Y-%m-%d %H:%M:%S.%f'),
                    datetime.strptime(
                        re.search(RE_D5, line).groups()[0],
                        '%Y-%m-%d %H:%M:%S.%f'))
            prev_line = line
        self.assertEqual(size, 20000)

    def _create_random_str_file(self, length, rows):
        if os.path.isfile(self.__DATAFILE__):
            os.remove(self.__DATAFILE__)
        with open(self.__DATAFILE__, 'w') as file:
            for _ in range(rows):
                file.write(
                    ''.join(random.choice(string.ascii_uppercase +
                                          string.digits)
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
