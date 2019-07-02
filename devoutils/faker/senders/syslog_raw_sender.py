# -*- coding: utf-8 -*-
"""Syslog raw sender provider"""
from datetime import datetime
from builtins import input
from .base_sender import BaseSender


class SyslogRawSender(BaseSender):
    """Generate a lot of events from/for Syslog"""
    def __init__(self, engine, template, **kwargs):
        BaseSender.__init__(self, engine, template, **kwargs)
        self.kwargs = kwargs

    def run(self):
        """Run function for cli or call function"""
        while True:
            lines = self.process(**self.kwargs).split('\n')
            for line in lines:
                if self.probability():
                    if not self.simulation and line:
                        if line[-1:] != "\n":
                            line += "\n"
                        self.engine.send_raw(line)
                    now = datetime.utcnow().ctime()
                    print('{0} => {1}'.format(now, str(line)))
                else:
                    now = datetime.utcnow().ctime()
                    print('{0} => Skipped by prob.'.format(now))

                if self.interactive:
                    input("» Press Enter for next iteration «")
                else:
                    self.wait()
