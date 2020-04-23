# -*- coding: utf-8 -*-
"""File Sender provider"""
from datetime import datetime
from .realtime_fake_generator import RealtimeFakeGenerator


class FileFakeGenerator(RealtimeFakeGenerator):
    """Generate a lot of events from file"""
    def __init__(self, template=None, **kwargs):
        RealtimeFakeGenerator.__init__(self, template=template, **kwargs)
        self.last_flush = int(datetime.now().timestamp())
        self.file_name = kwargs.get('file_name', "safestream.log")
        self.file = None

    def write_row(self, message=None):
        """Write row to file"""
        self.file.write(message)
        self.file.write('\n')
        now = int(datetime.now().timestamp())
        # flush every 5 secs
        if now - self.last_flush > 5:
            self.last_flush = now
            self.file.flush()

    def run(self):
        """Run function for cli or call function"""
        with open(self.file_name, "a") as self.file:
            self.realtime_iteration(write_function=self.write_row)
