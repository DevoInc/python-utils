"""
Module with classes for file management
- File reader
- Writer in files
- Reader and join of several ordered fichros
"""
import csv
import gzip


class FileWriter:
    """
    Class that allows writing to a file. Receive the name of the file to
     write and parameters for writing.
     The supported arguments are:
       - is_gzip: write files in gzip format
       - is_cvs: write files in csv format. You can indicate the delimiter and
         the csv quotechar to parse it.
       - mode: file write mode

     When instantiating an object, the file for writing is opened and,
     each write, write a new entry in the file.
    """
    def __init__(self, dest_file, mode='w', **kwargs):
        self.__is_csv = kwargs.get('is_csv', False)
        is_gzip = \
            kwargs.get('is_target_gzip', False) or kwargs.get('is_tmp_gzip',
                                                              False)

        self.__file_desc = gzip.open(dest_file, mode + 't') if is_gzip \
            else open(dest_file, mode, newline='',
                      encoding=kwargs.get("encoding", None))
        if self.__is_csv:
            self.__writer = csv.writer(self.__file_desc,
                                       delimiter=kwargs.get('delimiter', ','),
                                       quotechar=kwargs.get('quotechar', '"'))
        else:
            self.__writer = self.__file_desc

    def write(self, data):
        """
        Write the content in the file
         :param data: data to write in the file
        """
        if self.__is_csv:
            self.__writer.writerow(data)
        else:
            self.__writer.write(data)

    def close(self):
        """
        Could you directly put only __filedesc?
        :return:
        """
        if self.__is_csv:
            self.__file_desc.close()
        else:
            self.__writer.close()
