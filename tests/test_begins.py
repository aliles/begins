from __future__ import absolute_import, division, print_function
import atexit
import mock

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import doctest

import begin


class TestTouchstone(unittest.TestCase):

    def test_has_version(self):
        self.assertTrue(begin.__version__)

    @mock.patch('atexit.register')
    def test_readme(self, register):
        doctest.testfile('../README.rst')


if __name__ == '__main__':
    unittest.begin()
