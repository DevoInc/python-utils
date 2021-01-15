#!/usr/bin/env python
import codecs
import os
import re
from setuptools import setup, find_packages

META_PATH = os.path.join("devoutils", "__version__.py")
HERE = os.path.abspath(os.path.dirname(__file__))
PACKAGES = find_packages()
KEYWORDS = ["devo", "sdk", "developers", "utils"]
CLASSIFIERS = [
    "Programming Language :: Python",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

INSTALL_REQUIRES = ['devo-sdk==3.4.1',
                    'click==7.1.1',
                    'requests==2.23.0',
                    'PyYAML==5.3.1',
                    'Jinja2==2.11.1',
                    'psutil==5.7.0',
                    'python-dateutil==2.8.1',
                    'Faker==4.0.2',
                    'pycron==3.0.0']
CLI = ['devo-faker=devoutils.faker.scripts.faker_cli:cli']


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


META_FILE = read(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author="Devo, Inc.",
    author_email="support@devo.com",
    description="Devo Utils for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license=find_meta("license"),
    name="devo-utils",
    url="https://github.com/DevoInc/python-utils",
    version=find_meta("version"),
    classifiers=CLASSIFIERS,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    # extras_require=EXTRA_REQUIRES,
    entry_points={
            'console_scripts': CLI
        }
)
