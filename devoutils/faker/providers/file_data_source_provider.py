# -*- coding: utf-8 -*-
"""File provider."""
from faker.generator import random
from faker.providers import BaseProvider


class FileDataSourceProvider(BaseProvider):
    """Main class for File provider"""
    cache = {}

    def from_file(self, path):
        """Load random line from file"""
        self._check_cache(path)
        return self._get_random_line(path)

    def _check_cache(self, path):
        """Check cache of file"""
        if path not in self.cache.keys():
            with open(path, 'r') as content_file:
                self.cache[path] = content_file.read()

    def _get_random_line(self, path):
        """Get random line from cache"""
        lines = self.cache[path].split('\n')
        num = random.randint(0, len(lines) - 1)
        return lines[num]
