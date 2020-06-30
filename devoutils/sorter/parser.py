"""
Module with different parsers.

- List, the element is recovered in position
- Delimiter, it is split and element is recovered in position
- Regex retrieves the group x from the given regex
"""
import re


def parser_list(position):
    """
    Returns function that retrieves the element in position `position`
    :param position: position to return
    :return: element
    """
    return lambda x: x[position]


def parser_delimiter(delimiter, position):
    """
    Separate the event with the separator and return the element in the position
     position
    :param delimiter: delimiter
    :param position: position
    :return: the element in the given position
    """
    return lambda x: x.split(delimiter)[position]


def parser_regex(regex, group, ignorecase=False):
    """
    Recovers the group from a regex and returns it
    :param regex: regex
    :param group: the group to recover
    :param ignorecase: False by default
    :return: the group obtained.
    """
    if group == 0:
        if ignorecase:
            return lambda x: re.search(regex, x, re.I).groups()[group]
        return lambda x: re.search(regex, x).groups()[group]
    else:
        if ignorecase:
            return lambda x: re.findall(regex, x, re.I)[group]
        return lambda x: re.findall(regex, x)[group]
