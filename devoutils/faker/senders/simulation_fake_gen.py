# -*- coding: utf-8 -*-
"""File Sender provider"""
from .realtime_fake_gen import RealtimeFakeGen


class SimulationFakeGen(RealtimeFakeGen):
    """Generate a lot of events from file"""
    def __init__(self, template, **kwargs):
        RealtimeFakeGen.__init__(self, None, template, **kwargs)
        self.verbose = True

    def run(self):
        """Run function for cli or call function"""
        self.realtime_iteration(lambda x: x)
