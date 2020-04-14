# -*- coding: utf-8 -*-
"""File Sender provider"""
from .realtime_fake_generator import RealtimeFakeGenerator
from datetime import datetime


class FileFakeGenerator(RealtimeFakeGenerator):
    """Generate a lot of events from file"""
    def __init__(self, template, **kwargs):
        RealtimeFakeGenerator.__init__(self, None, template, **kwargs)
        self.last_flush = int(datetime.now().timestamp())
        self.file_name = kwargs.get('file_name', "safestream.log")
        self.f = None

    def write_row(self, message):
        self.f.write(message)
        self.f.write('\n')
        now = int(datetime.now().timestamp())
        # flush every 5 secs
        if now - self.last_flush > 5:
            self.last_flush = now
            self.f.flush()

    def run(self):
        """Run function for cli or call function"""
        with open(self.file_name, "a") as self.f:
            self.realtime_iteration(self.write_row)
