# -*- coding: utf-8 -*-
"""Syslog sender provider"""
from datetime import datetime
from builtins import input
from .base_sender import BaseSender


class SyslogSender(BaseSender):
    """Generate a lot of events from/for Syslog"""
    def __init__(self, engine, template, **kwargs):
        BaseSender.__init__(self, engine, template, **kwargs)
        self.tag = kwargs.get('tag', 'test.keep.free')

    def run(self):
        """Run function for cli or call function"""
        while True:
            lines = self.process(date_generator=self.date_generator).split('\n')
            for line in lines:
                if self.probability():
                    if not self.simulation:
                        self.engine.send(tag=self.tag, msg=str(line))
                    now = datetime.utcnow().ctime()
                    print('{0} => {1}'.format(now, str(line)))
                else:
                    now = datetime.utcnow().ctime()
                    print('{0} => Skipped by prob.'.format(now))

                if self.interactive:
                    input("» Press Enter for next iteration «")
                else:
                    self.wait()
