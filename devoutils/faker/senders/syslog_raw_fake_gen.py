# -*- coding: utf-8 -*-
"""Syslog raw sender provider"""
from .realtime_fake_gen import RealtimeFakeGen


class SyslogRawFakeGen(RealtimeFakeGen):
    """Generate a lot of events from/for Syslog"""
    def __init__(self, engine, template, **kwargs):
        RealtimeFakeGen.__init__(self, engine, template, **kwargs)
        self.kwargs = kwargs

    def send_raw(self, message):
        if message[-1:] != "\n":
            message += "\n"
        self.engine.send_raw(message)

    def run(self):
        """Run function for cli or call function"""
        self.realtime_iteration(
            lambda message: self.send_raw(str(message)))
