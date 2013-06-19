from __future__ import absolute_import, division, print_function
import mock
import os
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
            orig_argv= sys.argv
            sys.argv = ['', '-a', 'A']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            def main(a, b=Ellipsis):
                target(a, b)
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], ('A', Ellipsis))
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_env_defaults(self):
        target = mock.Mock()
        try:
            orig_env = os.environ
            os.environ = {'ALPHA_': 'A'}
            orig_argv= sys.argv
            sys.argv = []
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            def main(alpha_, b=Ellipsis):
                target(alpha_, b)
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], ('A', Ellipsis))
        finally:
            os.environ = orig_env
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_env_prefixes(self):
        target = mock.Mock()
        try:
            orig_env = os.environ
            os.environ = {'X_ALPHA_': 'A'}
            orig_argv= sys.argv
            sys.argv = []
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start(env_prefix='X_')
            def main(alpha_, b=Ellipsis):
                target(alpha_, b)
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], ('A', Ellipsis))
        finally:
            os.environ = orig_env
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_not_callable(self):
        target = mock.Mock
        with self.assertRaises(ValueError):
            begin.start(Ellipsis)

    def test_convert(self):
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = ['', '-a', '1']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            @begin.convert(a=int)
            def main(a=0):
                target(a)
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], (1,))
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name


if __name__ == '__main__':
    unittest.begin()
