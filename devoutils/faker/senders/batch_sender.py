"""Batch sender provider"""
import datetime
import os.path
import random
import sys
import click

from .base_sender import BaseSender


class BatchSender(BaseSender):
    """
    Generates a lot of events in a single batch without any waits, it
    supports generating events from the past
    """

    GENERATION_ENDED_TOKEN = '###END###'

    def __init__(self, template, start_date, end_date, **kwargs):
        BaseSender.__init__(self, None, template, **kwargs)

        self._start_date = start_date
        self._end_date = end_date

    @staticmethod
    def date_range(start_date, end_date, freq, prob,
                   date_format="%Y-%m-%d %H:%M:%S.%f",
                   dont_remove_microseconds=True):
        """
        Generates dateti
        :param start_date:me objects between a start date and an end date with
        some given frequency,
        Some events can be piled up in the same millisecond, this happens
        sometimes with real data.
        :param frequency_ms:
        :param end_date:
        :return:
        """

        # Control how fast events are spaced between them with a
        # frequency (--freq argument)
        millis = 0
        idx = 0
        while True:

            millis_increment = random.uniform(freq[0], freq[1]) * 1000

            # Add some randomness to the event generation with
            # the --prob argument
            k = random.randint(0, 100)
            if k <= int(prob):
                millis += millis_increment

            idx += 1
            next_date = start_date + datetime.timedelta(milliseconds=millis)

            if next_date > end_date:
                yield BatchSender.GENERATION_ENDED_TOKEN
            else:
                if dont_remove_microseconds:
                    yield next_date.strftime(date_format)
                else:
                    yield next_date.strftime(date_format)[:-3]

    def run(self):
        """Run function for cli or call function"""
        if os.path.exists("eventbatch.log"):
            raise ValueError('an eventbatch.log file already exists, remove '
                             'it before generating new events')

        counter = 0
        date_generator = self.date_range(
            self._start_date, self._end_date, self.freq, self.prob,
            self.date_format, self.dont_remove_microseconds)
        while True:
            lines = self.process(date_generator=date_generator).split('\n')
            for line in lines:
                if BatchSender.GENERATION_ENDED_TOKEN in line:
                    return
                if counter % 100 == 0:
                    click.echo('Wrote {} lines'.format(counter),
                               file=sys.stderr)
                    click.echo(line[:40], file=sys.stderr)
                print(line, file=sys.stdout)
                counter += 1
