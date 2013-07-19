from __future__ import absolute_import, division, print_function
import cgitb
import mock
import os
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from begin import cmdline
from begin import extensions


class Options(object):
    pass


class TestCreateParser(unittest.TestCase):

    def test_void_function(self):
        def main():
            pass
        parser = cmdline.create_parser(main)
        self.assertIs(parser, None)

    def test_positional_arguments(self):
        def main(a, b, c):
            pass
        parser = cmdline.create_parser(main)
        self.assertEqual(len(parser._optionals._actions), 4)
        self.assertIs(parser._optionals._actions[1].default, cmdline.NODEFAULT)

    def test_keyword_argument(self):
        def main(opt=Ellipsis):
            pass
        parser = cmdline.create_parser(main)
        self.assertEqual(len(parser._optionals._actions), 2)
        self.assertIs(parser._optionals._actions[1].default, Ellipsis)

    def test_variable_arguments(self):
        def main(*variable_arguments):
            pass
        parser = cmdline.create_parser(main)
        self.assertIn('variable_arguments', parser.format_help())

    def test_function_description(self):
        def main(a):
            'program description'
        parser = cmdline.create_parser(main)
        self.assertEqual(parser.description, main.__doc__)

    if sys.version_info[0] > 2:
        exec("""
def test_positional_with_annotation(self):
    def main(opt:'help string'):
        pass
    parser = cmdline.create_parser(main)
    self.assertEqual(len(parser._optionals._actions), 2)
    self.assertEqual(parser._optionals._actions[1].help, 'help string')

def test_positional_with_annotation_and_default(self):
    def main(opt:'help string'='default'):
        pass
    parser = cmdline.create_parser(main)
    self.assertEqual(len(parser._optionals._actions), 2)
    self.assertEqual(parser._optionals._actions[1].help,
        'help string (default: %(default)s)')

def test_variable_positional_with_annotation(self):
    def main(*opts:'help string'):
        pass
    parser = cmdline.create_parser(main)
    self.assertEqual(len(parser._optionals._actions), 2)
    self.assertEqual(parser._optionals._actions[1].help, 'help string')
""")

    def test_variable_keyword_arguments(self):
        def main(**args):
            pass
        with self.assertRaises(ValueError):
            cmdline.create_parser(main)

    def test_env_disabled(self):
        def main(one, two):
            pass
        try:
            original = os.environ
            os.environ = {'ONE': 1}
            parser = cmdline.create_parser(main)
            self.assertEqual(parser._optionals._actions[1].default, cmdline.NODEFAULT)
            self.assertIs(parser._optionals._actions[2].default, cmdline.NODEFAULT)
        finally:
            os.environ = original

    def test_env_prefixes(self):
        def main(one, two):
            pass
        try:
            original = os.environ
            os.environ = {'X_ONE': 1, 'TWO': 2}
            parser = cmdline.create_parser(main, env_prefix='X_')
            self.assertEqual(parser._optionals._actions[1].default, 1)
            self.assertIs(parser._optionals._actions[2].default, cmdline.NODEFAULT)
        finally:
            os.environ = original

    @mock.patch('os.path.expanduser')
    def test_configfile(self, expanduser):
        def main(arg, unk):
            pass
        expanduser.return_value = os.path.join(os.curdir, 'tests')
        parser = cmdline.create_parser(main, config_file='config_test.cfg')
        self.assertEqual(parser._optionals._actions[1].default, 'value')
        self.assertEqual(parser._optionals._actions[2].default, cmdline.NODEFAULT)

    def test_help_strings(self):
        def main(a, b=None):
            pass
        parser = cmdline.create_parser(main)
        self.assertIs(parser._optionals._actions[1].help, None)
        self.assertEqual(parser._optionals._actions[2].help, '(default: %(default)s)')

    def test_tracebacks(self):
        @extensions.Tracebacks
        def main():
            pass
        parser = cmdline.create_parser(main)
        self.assertEqual(len(parser._action_groups), 3)
        self.assertEqual(len(parser._optionals._actions), 3)


class TestApplyOptions(unittest.TestCase):

    def setUp(self):
        self.opts = Options()

    def test_void_function(self):
        def main():
            return Ellipsis
        value = cmdline.apply_options(main, self.opts)
        self.assertIs(value, Ellipsis)

    def test_positional_argument(self):
        def main(a, b,c):
            return (a, b, c)
        self.opts.a = 1
        self.opts.b = 2
        self.opts.c = 3
        value = cmdline.apply_options(main, self.opts)
        self.assertTupleEqual(value, (1, 2, 3))

    def test_keyword_argument(self):
        def main(a=None, b=None, c=None):
            return (a, b, c)
        self.opts.a = 1
        self.opts.b = 2
        self.opts.c = 3
        value = cmdline.apply_options(main, self.opts)
        self.assertEqual(value, (1, 2, 3))

    def test_variable_arguments(self):
        def main(*args):
            return tuple(args)
        self.opts.args = [1, 2, 3]
        value = cmdline.apply_options(main, self.opts)
        self.assertTupleEqual(value, (1, 2, 3))

    def test_variable_keywords(self):
        def main(**kwargs):
            return dict(args)
        with self.assertRaises(cmdline.CommandLineError):
            value = cmdline.apply_options(main, self.opts)

    def test_positional_with_variable_arguments(self):
        def main(a, *b):
            return (a, b)
        self.opts.a = 1
        self.opts.b = [2]
        value = cmdline.apply_options(main, self.opts)
        self.assertTupleEqual(value, (1, (2,)))

    def test_missing_option(self):
        def main(a):
            return a
        with self.assertRaises(cmdline.CommandLineError):
            value = cmdline.apply_options(main, self.opts)

    @mock.patch('sys.stderr')
    @mock.patch('sys.exit')
    def test_missing_required(self, exit, stderr):
        def main(a):
            pass
        self.opts.a = cmdline.NODEFAULT
        cmdline.apply_options(main, self.opts)
        self.assertTrue(exit.called)

    if sys.version_info[0] > 2:
        exec("""
def test_keyword_only(self):
    def main(*, a=None):
        return a
    self.opts.a = 1
    value = cmdline.apply_options(main, self.opts)
    self.assertEqual(value, 1)
""")

    @mock.patch('cgitb.enable')
    def test_tracebacks(self, enable):
        @extensions.tracebacks
        def main():
            return
        self.opts.tracebacks = True
        self.opts.tbdir = None
        cmdline.apply_options(main, self.opts)
        enable.assert_called_one(format='txt', logdir=None)


if __name__ == "__main__":
    unittest.begin()
