# coding=utf-8
"""Number provider"""
import sys
from faker.generator import random
from faker.providers import BaseProvider


class NumbersProvider(BaseProvider):
    """Main class for number provider"""
    @staticmethod
    def hex(min=0, max=sys.maxsize):
        """Return hex random number"""
        return hex(random.randint(min, max))

    @staticmethod
    def int(min=0, max=sys.maxsize):
        """Return int random number"""
        return random.randint(min, max)
