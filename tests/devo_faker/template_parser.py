"""Main file for devoutils.faker test"""
import unittest
import re
import os
from dateutil import parser
from devoutils.faker import BatchFakeGenerator
from devoutils.faker import TemplateParser


class TestTemplateParser(unittest.TestCase):
    """Main class for tests"""
    def __init__(self, *args, **kwargs):
        super(TestTemplateParser, self).__init__(*args, **kwargs)


    def setUp(self):
        os.chdir("{!s}{!s}".format(os.path.dirname(os.path.abspath(__file__)),
                                   os.sep))

    def test_simple(self):
        with open("./template01") as content_file:
            text = content_file.read()
        template_parser = TemplateParser(template=text)
        result = template_parser.process(text)
        self.assertTrue(result == 'test1\ntest2')

    def test_with_faker(self):
        with open("./template02") as content_file:
            text = content_file.read()
        template_parser = TemplateParser(template=text)
        result = template_parser.process(text)
        self.assertTrue(re.match("test\d+", result))

    def test_with_faker_from_file(self):
        with open("./template03") as content_file:
            text = content_file.read()
        template_parser = TemplateParser(template=text)
        result = template_parser.process(text)
        self.assertTrue(re.match("test\d+", result))

    def test_with_faker_more_complicated(self):
        with open("./template04") as content_file:
            text = content_file.read()
        start_date = parser.parse("01-01-2018 00:00:00")
        end_date = parser.parse("01-01-2018 00:05:00")

        template_parser = TemplateParser(template=text)
        result = \
            template_parser.process(date_generator=
                                    BatchFakeGenerator.date_range(start_date,
                                                                  end_date,
                                                                  (1, 10),
                                                                  50))
        self.assertTrue('test' in result)


if __name__ == '__main__':
    unittest.main()
