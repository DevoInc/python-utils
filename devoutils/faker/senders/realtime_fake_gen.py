# -*- coding: utf-8 -*-
"""realtime base sender provider"""
from .base_fake_gen import BaseFakeGen
from datetime import datetime


class RealtimeFakeGen(BaseFakeGen):

    def __init__(self, engine, template, **kwargs):
        BaseFakeGen.__init__(self, engine, template, **kwargs)

    def realtime_iteration(self, write_function):
        while True:
            lines = self.process(date_generator=self.date_generator).split('\n')
            for line in lines:
                if self.probability():
                    if not self.simulation:
                        write_function(line)
                    now = datetime.utcnow().ctime()
                    if self.verbose:
                        print('{0} => {1}'.format(now, str(line)))
                else:
                    now = datetime.utcnow().ctime()
                    if self.verbose:
                        print('{0} => Skipped by prob.'.format(now))

                if self.interactive:
                    input("» Press Enter for next iteration «")
                else:
                    self.wait()
