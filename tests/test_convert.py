from __future__ import absolute_import, division, print_function
import mock
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import begin


class TestConvert(unittest.TestCase):

    def test_positional_as_positional(self):
        target = mock.Mock()
        @begin.convert(b=float)
        def func(a, b, c):
            target(a, b, c)
        func(None, '1.1', None)
        self.assertEqual(target.call_args[0], (None, 1.1, None))
        self.assertIsInstance(target.call_args[0][1], float)

    def test_positional_as_keyword(self):
        target = mock.Mock()
        @begin.convert(b=float)
        def func(a, b, c):
            target(a, b, c)
        func(None, b='1.1', c=None)
        self.assertEqual(target.call_args[0], (None, 1.1, None))
        self.assertIsInstance(target.call_args[0][1], float)

    def test_keyword_as_keyword(self):
        target = mock.Mock()
        @begin.convert(b=float)
        def func(a, b, c):
            target(a, b, c)
        func(None, b='1.1', c=None)
        self.assertEqual(target.call_args[0], (None, 1.1, None))
        self.assertIsInstance(target.call_args[0][1], float)

    def test_variable_positional(self):
        target = mock.Mock()
        @begin.convert(b=float)
        def func(a, *b):
            target(a, b)
        func(None, '1.1', '1.2')
        self.assertEqual(target.call_args[0], (None, (1.1, 1.2)))
        self.assertIsInstance(target.call_args[0][1][0], float)
        self.assertIsInstance(target.call_args[0][1][1], float)

    def test_variable_keyword(self):
        @begin.convert(b=float)
        def func(a, **b):
            target(a, b)
        with self.assertRaises(ValueError):
            func(None, b=None, c=None)

    def test_default_keyword(self):
        target = mock.Mock()
        @begin.convert(b=float)
        def func(a=None, b='x' * 32):
            target(a, b)
        func()
        self.assertEqual(target.call_args[0], (None, 'x' * 32))

    def test_defaults_as_arguments(self):
        target = mock.Mock()
        @begin.convert(port=int, debug=begin.utils.tobool)
        def func(host='0.0.0.0', port=80, debug=False):
            target(host, port, debug)
        func('0.0.0.0', '8080', False)
        self.assertEqual(target.call_args[0], ('0.0.0.0', 8080, False))

    if sys.version_info[0] > 2:
        exec("""
def test_keyword_only(self):
    target = mock.Mock()
    @begin.convert(b=float)
    def func(a, *, b=None):
        target(a, b)
    func(None, b='1.1')
    self.assertEqual(target.call_args[0], (None, 1.1))
    self.assertIsInstance(target.call_args[0][1], float)
""")
