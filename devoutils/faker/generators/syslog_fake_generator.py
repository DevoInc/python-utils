# -*- coding: utf-8 -*-
"""Syslog sender provider"""
from .realtime_fake_generator import RealtimeFakeGenerator


class SyslogFakeGenerator(RealtimeFakeGenerator):
    """Generate a lot of events from/for Syslog"""
    def __init__(self, engine=None, template=None, **kwargs):
        RealtimeFakeGenerator.__init__(self, engine=engine, template=template,
                                       **kwargs)
        self.tag = kwargs.get('tag', 'test.keep.free')

    def run(self):
        """Run function for cli or call function to send the data"""
        self.realtime_iteration(
            write_function=lambda message:
            self.engine.send(tag=self.tag, msg=str(message)))
