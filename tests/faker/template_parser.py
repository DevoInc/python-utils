import unittest
import re
from dateutil import parser
from devoutils.faker import BatchSender
from devoutils.faker import TemplateParser


class TestTemplateParser(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTemplateParser, self).__init__(*args, **kwargs)
        self.parser = TemplateParser()

    def test_simple(self):
        with open('template01', 'r') as content_file:
            text = content_file.read()
        result = self.parser.process(text)
        self.assertTrue(result == 'test1\ntest2')

    def test_with_faker(self):
        with open('template02', 'r') as content_file:
            text = content_file.read()
        result = self.parser.process(text)
        self.assertTrue(re.match("test\d+", result))

    def test_with_faker_from_file(self):
        with open('template03', 'r') as content_file:
            text = content_file.read()
        result = self.parser.process(text)
        self.assertTrue(re.match("test\d+", result))
        
    def test_with_faker_more_complicated(self):
        with open('template04', 'r') as content_file:
            text = content_file.read()
        start_date = parser.parse("01-01-2018 00:00:00")
        end_date = parser.parse("01-01-2018 00:05:00")
        result = self.parser.process(text,
                                     date_generator=
                                     BatchSender.date_range(start_date,
                                                            end_date,
                                                            (1, 10),
                                                            50))
        self.assertTrue('test' in result)


if __name__ == '__main__':
    unittest.main()
