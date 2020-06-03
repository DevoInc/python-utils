"""
Module with classes for file management
- File reader
- Writer in files
- Reader and join of several files ordered
"""
import csv
import gzip


class FileReader:
    """
    Class to read a file.
     Receive the name of the file to read and arguments to be able to process
     the file.
     The supported arguments are:
       - is_gzip: read files in gzip format
       - is_cvs: read files in csv format. You can indicate the delimiter and
         the quotechar of the csv to parse it.
       - mode: file reading mode

     When instantiating an object, the file is read and the object returned is a
     iterator that can be used to read the information of the file.
    """
    def __init__(self, src_file, **kwargs):
        self.__is_csv = kwargs.get('is_csv', False)
        is_gzip = kwargs.get('is_gzip', False)
        mode = kwargs.get('mode', 'r')
        self.file_name = src_file
        self.__file_desc = gzip.open(src_file, mode + 't') if is_gzip else \
            open(src_file, mode, newline='',
                 encoding=kwargs.get("encoding", None))
        if self.__is_csv:
            self.__reader = csv.reader(self.__file_desc,
                                       delimiter=kwargs.get('delimiter', ','),
                                       quotechar=kwargs.get('quotechar', '"'))

    def __iter__(self):
        return self

    def next(self):
        """
        Iterate the elements of the file.
        When you reach the end of the file launches a StopIteration
        :return: next element
        """
        if self.__is_csv:
            return self.__reader.next()

        line = self.__file_desc.readline()
        if line:
            return line
        raise StopIteration

    def __next__(self):
        """
        Iterate the elements of the file.
        When you reach the end of the file launches a StopIteration
        :return: next element
        """
        if self.__is_csv:
            try:
                return next(self.__reader)
            except StopIteration:
                self.__file_desc.close()
                raise

        line = self.__file_desc.readline()
        if line:
            return line
        self.__file_desc.close()
        raise StopIteration
