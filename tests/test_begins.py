from __future__ import absolute_import, division, print_function

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import doctest

import begin


class TestTouchstone(unittest.TestCase):

    def test_has_version(self):
        self.assertTrue(begin.__version__)

    def test_readme(self):
        doctest.testfile('../README.rst')


if __name__ == '__main__':
    unittest.begin()
