"""Batch sender provider"""
import datetime
import os.path
import random
import sys
import click

from .base_fake_generator import BaseFakeGenerator


class BatchFakeGenerator(BaseFakeGenerator):
    """
    Generates a lot of events in a single batch without any waits, it
    supports generating events from the past
    """

    GENERATION_ENDED_TOKEN = '###END###'

    def __init__(self, template=None, start_date=None, end_date=None,
                 **kwargs):

        BaseFakeGenerator.__init__(self, template=template, **kwargs)

        self._start_date = start_date
        self._end_date = end_date
        self.date_format = kwargs.get('date_format', "%Y-%m-%d %H:%M:%S.%f")
        self.dont_remove_microseconds = kwargs.get('dont_remove_microseconds',
                                                   False)
        self.file_name = kwargs.get("file_name") if kwargs.get("file_name") \
            else "eventbatch.log"

    @staticmethod
    def date_range(start_date=None, end_date=None, frequency=None,
                   probability=None,
                   date_format="%Y-%m-%d %H:%M:%S.%f",
                   dont_remove_microseconds=True):
        """
        Generates date range
        :param start_date:me objects between a start date and an end date with
        some given frequency,
        Some events can be piled up in the same millisecond, this happens
        sometimes with real data.
        :param end_date:
        :param start_date:
        :param frequency:
        :param probability:
        :param date_format:
        :param dont_remove_microseconds:
        :return:
        """

        # Control how fast events are spaced between them with a
        # frequency (--frequency argument)
        millis = 0
        idx = 0
        while True:

            millis_increment = random.uniform(frequency[0],
                                              frequency[1]) * 1000

            # Add some randomness to the event generation with
            # the --probability argument
            k = random.randint(0, 100)
            if k <= int(probability):
                millis += millis_increment

            idx += 1
            next_date = start_date + datetime.timedelta(milliseconds=millis)

            if next_date > end_date:
                yield BatchFakeGenerator.GENERATION_ENDED_TOKEN
            else:
                if dont_remove_microseconds:
                    yield next_date.strftime(date_format)
                else:
                    yield next_date.strftime(date_format)[:-3]

    def run(self):
        """Run function for cli or call function"""
        if os.path.exists(self.file_name):
            raise ValueError('an {} file already exists, remove it before'
                             ' generating new events'.format(self.file_name))

        counter = 0
        date_generator = self.date_range(
            self._start_date, self._end_date, self.freq, self.prob,
            self.date_format, self.dont_remove_microseconds)
        with open(self.file_name, "w") as f:
            while True:
                lines = self.process(date_generator=date_generator).split('\n')
                for line in lines:
                    if BatchFakeGenerator.GENERATION_ENDED_TOKEN in line:
                        print("Wrote {} events in {}".format(counter,
                                                             self.file_name),
                              file=sys.stdout)
                        return
                    if counter % 100 == 0:
                        click.echo('Wrote {} lines'.format(counter),
                                   file=sys.stderr)
                        click.echo(line[:40], file=sys.stderr)
                    if self.verbose:
                        print(line, file=sys.stdout)
                    f.write(line+"\n")
                    counter += 1
