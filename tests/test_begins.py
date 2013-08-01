from __future__ import absolute_import, division, print_function
import mock
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import doctest

import begin


class TestBegins(unittest.TestCase):

    def test_has_version(self):
        self.assertTrue(begin.__version__)

    def test_readme(self):
        try:
            original = sys.argv
            sys.argv = ['']
            doctest.testfile('../README.rst')
        finally:
            sys.argv = original
            for collector in begin.subcommands.COLLECTORS.values():
                collector.clear()


if __name__ == '__main__':
    unittest.begin()
