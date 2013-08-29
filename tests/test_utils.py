from __future__ import absolute_import, division, print_function
import mock
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from begin import utils


class TestToList(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(utils.tolist(''), [])

    def test_default_list(self):
        self.assertEqual(utils.tolist('a,b'), ['a', 'b'])

    def test_empty_strings(self):
        self.assertEqual(utils.tolist(',', empty_strings=True), ['', ''])

    def test_custom_separator(self):
        self.assertEqual(utils.tolist('a|b', sep='|'), ['a', 'b'])

    def test_function_generator(self):
        func = utils.tolist()
        self.assertEqual(utils.tolist('a,b'), ['a', 'b'])
