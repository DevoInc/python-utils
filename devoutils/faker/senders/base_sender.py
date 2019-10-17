# -*- coding: utf-8 -*-
"""Base Sender, father of all other providers"""
import random
import threading
import time
from .template_parser import TemplateParser


class BaseSender(threading.Thread):
    """Base provider main class"""
    template = None
    freq = None
    prob = 100
    generator = None

    def __init__(self, engine, template, **kwargs):
        threading.Thread.__init__(self)
        self.engine = engine
        self.template = str(template)
        self.prob = kwargs.get('prob', 100)
        self.freq = kwargs.get('freq', (1, 1))
        self.date_format = kwargs.get('date_format', "%Y-%m-%d %H:%M:%S.%f")
        self.interactive = kwargs.get('interactive', False)
        self.simulation = kwargs.get('simulation', False)
        self.dont_remove_microseconds = kwargs.get('dont_remove_microseconds',
                                                   False)
        self.parser = TemplateParser()
        self.date_generator = kwargs.get('date_generator', None)

    def process(self, date_generator=None, **kwargs):
        """Process template"""
        return self.parser.process(self.template, date_generator, **kwargs)

    def wait(self):
        """Time to wait between events"""
        # freq[0] is the minimum
        # freq[1] is the maximum
        if self.freq[0] == self.freq[1]:
            secs = self.freq[0]
        elif self.freq[1] < self.freq[0]:
            secs = random.uniform(self.freq[1], self.freq[0])
        else:
            secs = random.uniform(self.freq[0], self.freq[1])
        time.sleep(secs)

    def probability(self):
        """Calculate probability"""
        k = random.randint(0, 100)
        if k <= int(self.prob):
            return True
        return False

    def run(self):
        """Run example (for override)"""
        while True:
            if self.probability():
                # Do something
                pass
            self.wait()
