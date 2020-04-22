# -*- coding: utf-8 -*-
"""Base Sender, father of all other providers"""
import random
import threading
import time
from datetime import datetime, timedelta
from pycron import is_now
from .template_parser import TemplateParser


class BaseFakeGenerator(threading.Thread):
    """Base provider main class"""

    def __init__(self, engine=None, template=None, **kwargs):
        threading.Thread.__init__(self)
        self.engine = engine
        self.template = str(template)

        if kwargs.get('time_rules', None) is not None:
            self.time_rules = kwargs.get("time_rules")
            self.set_last_time_rule()

            self.cron_child = threading.Thread(
                target=self.check_time_rules
            )
            self.cron_child.setDaemon(True)
            self.cron_child.start()
        else:
            self.prob = kwargs.get('probability', 100)
            self.freq = kwargs.get('frequency', (1, 1))

        self.interactive = kwargs.get('interactive', False)
        self.simulation = kwargs.get('simulation', False)
        self.verbose = kwargs.get('verbose', False)
        self.parser = TemplateParser()
        self.date_generator = kwargs.get('date_generator', None)
        self.providers = kwargs.get('providers', {})

    def process(self, date_generator=None, **kwargs):
        """Process template"""
        return self.parser.process(self.template, date_generator,
                                   **self.providers, **kwargs)

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

    def set_last_time_rule(self):
        now = datetime.now()
        try:
            for _ in range(0, 525600):
                for item in self.time_rules:
                    if is_now(item["rule"], now):
                        self.prob = item['probability']
                        self.freq = item['frequency']
                        raise Exception('found')
                now = now - timedelta(minutes=1)
        except Exception as inst:
            if inst.args[0] != "found":
                raise Exception(inst)

    def check_time_rules(self):
        while True:
            for item in self.time_rules:
                if is_now(item["rule"]):
                    self.prob = item['probability']
                    self.freq = item['frequency']
                    break
            time.sleep(60)

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

