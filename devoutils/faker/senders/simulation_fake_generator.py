# -*- coding: utf-8 -*-
"""File Sender provider"""
from .realtime_fake_generator import RealtimeFakeGenerator


class SimulationFakeGenerator(RealtimeFakeGenerator):
    """Generate a lot of events from file"""
    def __init__(self, template=None, **kwargs):
        RealtimeFakeGenerator.__init__(self, template=template, **kwargs)
        self.verbose = True

    def run(self):
        """Run function for cli or call function"""
        self.realtime_iteration(write_function=lambda x: x)
