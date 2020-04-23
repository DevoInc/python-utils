# -*- coding: utf-8 -*-
"""Template parser for Faker"""
from datetime import datetime
from jinja2 import Template
from faker import Faker
from faker.providers.internet import Provider as InternetProvider
from ..providers.file_data_source_provider import FileDataSourceProvider
from ..providers.numbers_provider import NumbersProvider


class TemplateParser:
    """Parser for templates, using jinja2 and Faker"""
    fake = None

    def __init__(self, template=None, providers=None, date_generator=None):
        self.fake = Faker()
        self.fake.add_provider(FileDataSourceProvider)
        self.fake.add_provider(NumbersProvider)
        # Ips networks emails etc..
        self.fake.add_provider(InternetProvider)
        self.template = template
        self.providers = {} if providers is None else providers
        self.date_generator = TemplateParser.null_date_generator \
            if date_generator is None else date_generator

    @staticmethod
    def null_date_generator():
        """Generate now date"""
        return str(datetime.now())

    def process(self, date_generator=None, **kwargs):
        """Procces template, parsing it"""
        template = Template(self.template)

        if date_generator is None:
            date_generator = self.date_generator

        # Only the passed objects will be accessible from the template
        # the next built-in needs to be passed for next(date_generator) to work
        return template.render(fake=self.fake, datetime=datetime,
                               date_generator=date_generator,
                               next=next, **self.providers, **kwargs)
