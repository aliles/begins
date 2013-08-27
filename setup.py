#!/usr/bin/env python
from setuptools import setup
import re
import sys


def load_version(filename='begin/version.py'):
    "Parse a __version__ number from a source file"
    with open(filename) as source:
        text = source.read()
        match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", text)
        if not match:
            msg = "Unable to find version number in {}".format(filename)
            raise RuntimeError(msg)
        version = match.group(1)
        return version

PYTHON3K = sys.version_info[0] > 2

requires = ['funcsigs'] if sys.version_info[:2] < (3, 3) else []
requires += ['argparse'] if sys.version_info[:2] < (2, 7) else []

setup(
    name="begins",
    version=load_version(),
    packages=['begin'],
    zip_safe=False,
    author="Aaron Iles",
    author_email="aaron.iles@gmail.com",
    url="http://begins.readthedocs.org",
    description="Command line programs for busy developers",
    long_description=open('README.rst').read(),
    license="ASL",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=requires,
    tests_require=['mock'] + [] if PYTHON3K else ['unittest2'],
    test_suite="tests" if PYTHON3K else "unittest2.collector"
)
