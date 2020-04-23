# -*- coding: utf-8 -*-
"""realtime base sender provider"""
from datetime import datetime
from .base_fake_generator import BaseFakeGenerator


class RealtimeFakeGenerator(BaseFakeGenerator):
    """Realtime fake data generation"""
    def __init__(self, engine=None, template=None, **kwargs):
        """Realtime fake data generation"""
        BaseFakeGenerator.__init__(self, engine=engine, template=template,
                                   **kwargs)

    def realtime_iteration(self, write_function=None):
        """Realtime function for parse and send/show generated data"""
        while True:
            lines = self.process().split('\n')
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
