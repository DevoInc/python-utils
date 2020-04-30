# -*- coding: utf-8 -*-
"""Syslog raw sender provider"""
from .realtime_fake_generator import RealtimeFakeGenerator


class SyslogRawFakeGenerator(RealtimeFakeGenerator):
    """Generate a lot of events from/for Syslog"""
    def __init__(self, engine=None, template=None, **kwargs):
        RealtimeFakeGenerator.__init__(self, engine=engine, template=template,
                                       **kwargs)

    def send_raw(self, message=None):
        """Class to call function devo.sender.send_raw() with raw data"""
        if message[-1:] != "\n":
            message += "\n"
        self.engine.send_raw(message)

    def run(self):
        """Run function for cli or call function to send de raw data"""
        self.realtime_iteration(
            write_function=lambda message: self.send_raw(str(message)))
