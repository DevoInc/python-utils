"""
Module for the data management of one or several source files.
"""
import os
import sys
import uuid
import re
import json
from types import GeneratorType
from collections import Iterable
from psutil import virtual_memory
from devoutils.fileio import FileReader, FileWriter
from .file_sorted_join import FileSortedJoin
from .cmp_compatible import cmp

DEFAULT_PERC_MEM = 0.4
FILES = 1
ITERATOR = 2


class Sorter:
    """
    Depending on the parameters, you will carry out different management
    strategies allowing arrangements of several files that meet a regex,
    ordinations taking into account the memory of the system to avoid
    have more data in memory than what can be integrated into memory
    """
    def __init__(self):
        self.iterator = None

    def sort_iterator(self, iterator, dst_file=None, **kwargs):
        """
        Order one or more files. Allow the destination to be a unique
        file. If it is not written to a file, it returns an iterable object
        with the result.
        :param iterator: Iterator for sort data
        :param dst_file: (Optional) if you want to save the result in file
        :param kwargs: Variable arguments
        :return: iterator with the data if not recorded in file.
        """
        iterator = [iterator]
        self.iterator = True
        data = self.__read_and_sort(ITERATOR, iterator, kwargs)
        if dst_file:
            self.__write_iterator_dst_file(data, dst_file, **kwargs)
            return True
        return data

    def sort_file(self, src, dst_file=None, **kwargs):
        """
        Order one or more files. Allow the destination to be a unique
        file. If it is not written to a file, it returns an iterable object
        with the result.
        :param src: File, source folder or file list
        :param dst_file: (Optional) if you want to save the result in file
        :param kwargs: Variable arguments
        :return: iterator with the data if not recorded in file.
        """
        if isinstance(src, list):
            files = src
        else:
            files = self.__get_file_list(kwargs.get('file_pattern', None), src)

        self.iterator = False
        data = self.__read_and_sort(FILES, files, kwargs)
        if dst_file:
            self.__write_dst_file(data, dst_file, **kwargs)
            return True
        return data

    @staticmethod
    def __write_iterator_dst_file(data, dst_file, **kwargs):
        """Write to dest file"""
        if not data:
            return None

        writer = FileWriter(dst_file, **kwargs)
        first = ""
        for first in data:
            if first:
                break

        if isinstance(first, dict):
            proc = lambda l: json.dumps(l) + "\n"
        elif isinstance(first, list):
            proc = lambda l: kwargs.get("separator",
                                        ",").join(str(x) for x in l) + "\n"
        elif isinstance(first, (str, bytes)):
            proc = lambda l: l if l[-1:] == "\n" else l + "\n"
        else:
            proc = lambda l: str(l) + "\n"

        if type(data) in [GeneratorType, Iterable]:
            writer.write(proc(first))

        for line in data:
            if line:
                writer.write(proc(line))
        return None

    @staticmethod
    def __write_dst_file(data, dst_file, **kwargs):
        """Write to dest file"""
        writer = FileWriter(dst_file, **kwargs)
        for line in data:
            if line:
                if not line.endswith("\n"):
                    line = line + "\n"
                writer.write(line)

    def __read_and_sort(self, src_type, src, kwargs):
        """Read file and sort it"""
        if kwargs.get('memory_safe', False):
            data = self.__memory_safe(src_type, src, kwargs)
        else:
            data = self.__simple_sort(src_type, src, kwargs)
        return data

    def __simple_sort(self, src_type, src, kwargs):
        """
        Simple ordination in memory
        :param files: list of files to order
        :param kwargs: arguments for ordering parameters
        :return: a list with the data ordered.
        """
        data = []
        transform = kwargs.get('transform', lambda x: x)

        for file in src:
            reader = None
            if src_type == FILES:
                reader = self.get_reader(file, kwargs)
                self.__skip_header_rows(kwargs, reader)
            elif src_type == ITERATOR:
                reader = file
            for line in reader:
                data.append(transform(line))

        if not kwargs.get("comp", None):
            data.sort(reverse=kwargs.get('reverse', False))
        else:
            data.sort(key=kwargs.get('comp', cmp), reverse=kwargs.get('reverse',
                                                                      False))
        return data

    def __memory_safe(self, src_type, src, kwargs):
        """
        Divide the sort into files to return an iterator that allows
        recover all the ordered data
        :param files: list of files to order
        :param kwargs: parameters for ordination
        :return: iterator with ordered data
        """
        tmp_dir = kwargs.get('tmp_dir', 'tmp')
        transform = kwargs.get('transform', lambda x: x)
        tmp_files = []
        total = 0
        data = []

        for file in src:
            reader = None
            if src_type == FILES:
                reader = self.get_reader(file, kwargs)
                self.__skip_header_rows(kwargs, reader)
            elif src_type == ITERATOR:
                reader = file

            iteration = 0
            max_iterations = None
            for line in reader:
                total += 1
                if not max_iterations:
                    max_iterations = int(self.__get_max_mem(kwargs) /
                                         sys.getsizeof(transform(line)))
                iteration += 1
                if iteration > max_iterations:
                    self.__sort_and_save_tmp(data, kwargs, tmp_dir, tmp_files)
                    iteration = 0
                    del data[:]
                data.append(transform(line))
            if data:
                self.__sort_and_save_tmp(data, kwargs, tmp_dir, tmp_files)
            del data[:]
        return FileSortedJoin(tmp_files, **kwargs)

    def __sort_and_save_tmp(self, data, kwargs, tmp_dir, tmp_files):
        """Sort and save one tmp file when has splitted parts"""

        if not kwargs.get("comp", None):
            data.sort(reverse=kwargs.get('reverse', False))
        else:
            data.sort(key=kwargs.get('comp', cmp),
                      reverse=kwargs.get('reverse', False))
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        tmp_file = tmp_dir + "/" + str(uuid.uuid1()) + ".tmp.gz"
        tmp_files.append(tmp_file)
        if self.iterator:
            self.__write_iterator_dst_file(data, tmp_file, is_tmp_gzip=True,
                                           **kwargs)
        else:
            self.__write_dst_file(data, tmp_file, is_tmp_gzip=True, **kwargs)

    @staticmethod
    def get_reader(file, kwargs):
        """Get reader class for file"""
        reader = FileReader(file, **kwargs)
        return reader

    @staticmethod
    def __skip_header_rows(kwargs, reader):
        for _ in range(kwargs.get('rows_to_skip', 0)):
            reader.next()

    def __get_max_mem(self, kwargs):
        return kwargs.get('max_mem', self.__me_by_available(kwargs))

    @staticmethod
    def __me_by_available(kwargs):
        available_mem = virtual_memory().available
        av_mem_perc = kwargs.get('av_mem_perc', DEFAULT_PERC_MEM)
        av_mem_perc = av_mem_perc if 0 > av_mem_perc <= 1 \
            else DEFAULT_PERC_MEM
        return available_mem * av_mem_perc

    @staticmethod
    def __get_file_list(file_pattern, src):
        if file_pattern:
            if not os.path.isdir(src):
                raise ValueError("SRC is not a dir")
            files = [src+"/"+f for f in os.listdir(src) if
                     re.match(file_pattern, f)]
        else:
            files = [src]
        return files
