import os
import unittest

from devoutils.fileio import FileReader, FileWriter


class TestFileIO(unittest.TestCase):
    __DATA = ["id,val", "1,uno", "2,dooss", "3,treeeee"]
    __DATA_CSV = [['id', 'val'],
                  ['1', 'uno'],
                  ['2', 'dooss'],
                  ['3', 'treeeee']]
    __CLEAR_FILE = "".join((os.path.dirname(os.path.abspath(__file__)),
                            os.sep, 'test_lookup.csv'))

    __GZIP_FILE = "".join((os.path.dirname(os.path.abspath(__file__)),
                           os.sep, 'test_lookup.csv.gz'))

    def setUp(self):
        os.chdir("{!s}{!s}".format(os.path.dirname(os.path.abspath(__file__)),
                                   os.sep))

    def test_simple_file(self):
        reader = FileReader(self.__CLEAR_FILE)
        data = []
        for d in reader:
            data.append(d.strip())
        self.assertEqual(data, self.__DATA)

    def test_csv_file(self):
        reader = FileReader(self.__CLEAR_FILE, is_csv=True)
        data = []
        for d in reader:
            data.append(d)
        self.assertEqual(data, self.__DATA_CSV)

    def test_gzip_file(self):
        reader = FileReader(self.__GZIP_FILE, is_gzip=True)
        data = []
        for d in reader:
            data.append(d.strip())
        self.assertEqual(data, self.__DATA)

    def test_gz_csvFile(self):
        reader = FileReader(self.__GZIP_FILE, is_csv=True, is_gzip=True)
        data = []
        for d in reader:
            data.append(d)
        self.assertEqual(data, self.__DATA_CSV)

    def test_write_gz_csv_file(self):
        writer = FileWriter("file.csv.gz", is_csv=True, is_target_gzip=True)
        __DATA_CSV = [['id', 'val'],
                      ['1', 'uno'],
                      ['2', 'dooss'],
                      ['3', 'treeeee']]
        for d in __DATA_CSV:
            writer.write(d)


if __name__ == '__main__':
    unittest.main()
