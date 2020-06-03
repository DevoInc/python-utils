"""
Module with classes for file management
- File reader
- Writer in files
- Reader and join of several ordered files
"""
import os
from devoutils.fileio.file_reader import FileReader


class FileSortedJoin:
    """
   From several ordered files returns an iterator that returns the
     content of all the files ordered.
     The arguments it receives are:
       - The list of files to join
       - if the order is in reverse
       - The comparator to use
    """
    def __init__(self, part_files, **kwargs):
        self.__files = []
        self.__reverse = kwargs.get('reverse', False)
        self.__reverse_mod = -1 if self.__reverse else 1
        kwargs['is_gzip'] = True
        for tmp_file in part_files:
            self.__files.append(FileReader(tmp_file, **kwargs))
        self.__last_sorted_list = []

        self.__comparator = kwargs.get('comp', lambda a, b: (a > b) - (a < b))
        for file in self.__files:
            self.__in_sort(self.__last_sorted_list, (file.next(), file))

    def __in_sort(self, sorted_list, item):
        """
        Insert item in list 'sorted_list', and keep it sorted assuming
        'sorted_list' is sorted. If item is already in 'sorted_list',
        insert it to the right of the rightmost item.
        """
        lowest = 0
        highest = len(sorted_list)
        while lowest < highest:
            mid = (lowest + highest) // 2
            if (self.__reverse_mod * self.__comparator(item[0],
                                                       sorted_list[mid][0]))\
                    < 0:
                highest = mid
            else:
                lowest = mid + 1
        sorted_list.insert(lowest, item)

    def __iter__(self):
        return self

    def next(self):
        """
        Iterate the elements of the files ordered by returning the element
         suitable for ordination.
         When it reaches the end of all the files it launches a StopIteration
         :return: next element
        """
        if self.__last_sorted_list:
            data = self.__last_sorted_list.pop(0)
            try:
                self.__in_sort(self.__last_sorted_list, (data[1].next(),
                                                         data[1]))
            except StopIteration:
                os.remove(data[1].file_name)
            return data[0]
        raise StopIteration

    def __next__(self):
        return self.next()

    def __getitem__(self, position):
        return self.next()
