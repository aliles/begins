from __future__ import absolute_import, division, print_function
import cgitb
import logging
import mock
import os
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import pkg_resources

import begin


class TestStart(unittest.TestCase):

    def tearDown(self):
        for collector in begin.subcommands.COLLECTORS.values():
            collector.clear()

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

    def test_decorate_true(self):
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1]
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            def main():
                target()
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], tuple())
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_decorate_callable(self):
        target = mock.Mock()
        @begin.start
        def main():
            target()
        main()
        self.assertTrue(target.called)

    def test_entry_point(self):
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1]
            @begin.start
            def main():
                target()
            main.start()
            self.assertTrue(target.called)
        finally:
            sys.argv = orig_argv

    def test_command_line(self):
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['A']
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

    def test_env_disabled(self):
        target = mock.Mock()
        try:
            orig_env = os.environ
            os.environ = {'ALPHA_': 'A'}
            orig_argv= sys.argv
            sys.argv = orig_argv[:1]
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            def main(alpha_='Z', b=Ellipsis):
                target(alpha_, b)
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], ('Z', Ellipsis))
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
            sys.argv = orig_argv[:1]
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start(env_prefix='X_')
            def main(alpha_='Z', b=Ellipsis):
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
            sys.argv = orig_argv[:1] + ['-a', '1']
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

    @mock.patch('cgitb.enable')
    def test_tracebacks(self, enable):
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['--tracebacks']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            @begin.tracebacks
            def main():
                pass
            self.assertTrue(enable.called)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    @mock.patch('logging.getLogger')
    def test_logging(self, getlogger):
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1]
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            @begin.logging
            def main():
                pass
            self.assertTrue(getlogger.called)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_subcommand(self):
        epilogue = mock.Mock()
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['subcmd']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.subcommand
            def subcmd():
                target()
            @begin.start
            def main():
                epilogue()
            self.assertTrue(epilogue.called)
            self.assertTrue(target.called)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_subcommand_group(self):
        epilogue = mock.Mock()
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['subcmd']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.subcommand(group='named.collector')
            def subcmd():
                target()
            @begin.start(sub_group='named.collector')
            def main():
                epilogue()
            self.assertTrue(epilogue.called)
            self.assertTrue(target.called)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_multiple_subcommand(self):
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['subcmd', '--', 'subcmd', '--', 'subcmd']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.subcommand
            def subcmd():
                target()
            @begin.start(cmd_delim='--')
            def main():
                pass
            self.assertEqual(target.call_count, 3)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    @mock.patch('pkg_resources.iter_entry_points')
    def test_plugins(self, iep):
        epilogue = mock.Mock()
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['subcmd']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            def subcmd():
                target()
            def entry_points(group, *args):
                yield subcmd
            iep.side_effect = entry_points
            @begin.start(plugins='entry.points')
            def main():
                epilogue()
            self.assertTrue(epilogue.called)
            self.assertTrue(target.called)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    @mock.patch('sys.exit')
    def test_keyboard_interrupt_main(self, exit):
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1]
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start
            def main():
                raise KeyboardInterrupt
            self.assertTrue(exit.called)
            self.assertGreater(exit.call_args[0][0], 0)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    @mock.patch('sys.exit')
    def test_keyboard_interrupt_subcommand(self, exit):
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['subcmd']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.subcommand
            def subcmd():
                raise KeyboardInterrupt
            @begin.start
            def main():
                pass
            self.assertTrue(exit.called)
            self.assertGreater(exit.call_args[0][0], 0)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_context(self):
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['one', '--', 'two', '--', 'three']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.subcommand
            def one():
                self.assertIs(begin.context.return_value, None)
                self.assertEqual(len(begin.context.opts_previous), 0)
                self.assertEqual(len(begin.context.opts_next), 2)
                return 1
            @begin.subcommand
            def two():
                self.assertEqual(begin.context.return_value, 1)
                self.assertEqual(len(begin.context.opts_previous), 1)
                self.assertEqual(len(begin.context.opts_next), 1)
                return 2
            @begin.subcommand
            def three():
                self.assertEqual(begin.context.return_value, 2)
                self.assertEqual(len(begin.context.opts_previous), 2)
                self.assertEqual(len(begin.context.opts_next), 0)
                return 3
            @begin.start(cmd_delim='--')
            def main():
                pass
            self.assertEqual(begin.context.return_value, 3)
            self.assertEqual(len(begin.context.opts_previous), 3)
            self.assertEqual(len(begin.context.opts_next), 0)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name

    def test_automatic_convert(self):
        target = mock.Mock()
        try:
            orig_argv= sys.argv
            sys.argv = orig_argv[:1] + ['-a', '-b', '1', '-c', 'x,y', '-d', '*']
            orig_name = globals()['__name__']
            globals()['__name__'] = "__main__"
            @begin.start(auto_convert=True)
            def main(a=False, b=0, c=(), d=''):
                target(a, b, c, d)
            self.assertTrue(target.called)
            self.assertEqual(target.call_args[0], (True, 1, ['x', 'y'], '*'))
            self.assertIsInstance(target.call_args[0][0], bool)
            self.assertIsInstance(target.call_args[0][1], int)
            self.assertIsInstance(target.call_args[0][2], list)
        finally:
            sys.argv = orig_argv
            globals()['__name__'] = orig_name


if __name__ == '__main__':
    unittest.begin()
