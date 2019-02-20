# -*- coding: utf-8 -*-
"""File Sender provider"""
from datetime import datetime
from builtins import input
from .base_sender import BaseSender


class FileSender(BaseSender):
    """Generate a lot of events from file"""
    def __init__(self, template, **kwargs):
        BaseSender.__init__(self, None, template, **kwargs)

    def run(self):
        """Run function for cli or call function"""
        with open("safestream.log", "a") as file:
            lines = self.process().split('\n')
            while True:
                for line in lines:
                    if self.probability():
                        file.write(line + "\n")
                        now = datetime.utcnow().ctime()
                        print('{0} => {1}'.format(now, str(line)))
                    else:
                        now = datetime.utcnow().ctime()
                        print('{0} => Skipped by prob.'.format(now))

                    if self.interactive:
                        input("» Press Enter for next iteration «")
                    else:
                        self.wait()
