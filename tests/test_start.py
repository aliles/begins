from __future__ import absolute_import, division, print_function
import mock
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import begin


class TestStart(unittest.TestCase):

    def test_start_false(self):
        # begin.start() return false outside __main__
        self.assertFalse(begin.start())

    def test_start_true(self):
        # mock globals to mimic __main__
        try:
            original = globals()['__name__']
            globals()['__name__'] = "__main__"
            self.assertTrue(begin.start())
        finally:
            globals()['__name__'] = original

    def test_decorate_false(self):
        target = mock.Mock()
        @begin.start
        def main():
            target()
        self.assertFalse(target.called)
        self.assertTrue(callable(main))

    def test_decorate_true(self):
        target = mock.Mock()
        try:
            original = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            def main():
                target()
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], tuple())
        finally:
            globals()['__name__'] = original

    def test_command_line(self):
        target = mock.Mock()
        try:
            original = sys.argv
            sys.argv = ['', '-a', 'A']
            original = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            def main(a, b=Ellipsis):
                target(a, b)
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], ('A', Ellipsis))
        finally:
            sys.argv = original
            globals()['__name__'] = original

    def test_not_callable(self):
        target = mock.Mock
        with self.assertRaises(ValueError):
            begin.start(Ellipsis)


if __name__ == '__main__':
    unittest.begin()
