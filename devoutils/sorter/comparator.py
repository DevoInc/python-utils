"""
Module with the comparators to use in the ordering.
The comparators are functions that return the comparison functions.
To be able to compare properly, you have to indicate the event parser
that you will get the field you want to compare
"""
from datetime import datetime
from .cmp_compatible import cmp


def compare_date(date_format, parser):
    """
    Returns a date comparator based on a given format according to
    https://docs.python.org/3.5/library/datetime.html#strftime-and-strptime-behavior
    :param date_format: the format to use in the date parse
    :param parser: the event parser that retrieves the date to apply the format
    :return: the comparator to use in the ordination
    """
    return lambda x, y = None: datetime.strptime(parser(x), date_format) \
        if y is None else cmp(datetime.strptime(parser(x), date_format),
                              datetime.strptime(parser(y), date_format))


def compare_num(parser):
    """
    Compare two numbers
    :param parser: the event parser that retrieves the date to apply the format
    :return: the comparator to use in the ordination
    """
    return lambda x, y = None: float(parser(x)) if y is None \
        else cmp(float(parser(x)), float(parser(y)))


def compare_str(parser):
    """
    Compara dos strings
    :param parser: the event parser that retrieves the date to apply the format
    :return: the comparator to use in the ordination
        """
    return lambda x, y = None: parser(x) if y is None \
        else cmp(parser(x), parser(y))
