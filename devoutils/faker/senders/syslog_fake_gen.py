# -*- coding: utf-8 -*-
"""Syslog sender provider"""
from .realtime_fake_gen import RealtimeFakeGen


class SyslogFakeGen(RealtimeFakeGen):
    """Generate a lot of events from/for Syslog"""
    def __init__(self, engine, template, **kwargs):
        RealtimeFakeGen.__init__(self, engine, template, **kwargs)
        self.tag = kwargs.get('tag', 'test.keep.free')

    def run(self):
        """Run function for cli or call function"""
        self.realtime_iteration(
            lambda message: self.engine.send(tag=self.tag, msg=str(message)))
