# coding=utf-8
"""Number provider"""
import sys
from faker.generator import random
from faker.providers import BaseProvider


class NumbersProvider(BaseProvider):
    """Main class for number provider"""
    @staticmethod
    def hex(min_value=0, max_value=sys.maxsize):
        """Return hex random number"""
        return hex(random.randint(min_value, max_value))

    @staticmethod
    def int(min_value=0, max_value=sys.maxsize):
        """Return int random number"""
        return random.randint(min_value, max_value)
