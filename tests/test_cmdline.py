from __future__ import absolute_import, division, print_function
import mock
import os
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from begin import cmdline


class VarObj(object):
    pass


class TestCreateParser(unittest.TestCase):

    def test_void_function(self):
        def main():
            pass
        parser = cmdline.create_parser(main)
        self.assertEqual(len(parser.option_list), 1)

    def test_positional_arguments(self):
        def main(a, b, c):
            pass
        parser = cmdline.create_parser(main)
        self.assertEqual(len(parser.option_list), 4)
        self.assertIs(parser.option_list[0].default, cmdline.NODEFAULT)

    def test_keyword_argument(self):
        def main(opt=Ellipsis):
            pass
        parser = cmdline.create_parser(main)
        self.assertEqual(len(parser.option_list), 2)
        self.assertIs(parser.option_list[0].default, Ellipsis)

    def test_variable_arguments(self):
        def main(*variable_arguments):
            pass
        parser = cmdline.create_parser(main)
        self.assertIn('variable_arguments', parser.usage)

    def test_function_description(self):
        def main():
            'program description'
        parser = cmdline.create_parser(main)
        self.assertEqual(parser.description, main.__doc__)

    if sys.version_info[0] > 2:
        exec("""
def test_annotation(self):
    def main(opt:'help string'):
        pass
    parser = cmdline.create_parser(main)
    self.assertEqual(len(parser.option_list), 2)
    self.assertEqual(parser.option_list[0].help,
        'help string [default: %default]')
""")

    def test_variable_keyword_arguments(self):
        def main(**args):
            pass
        with self.assertRaises(ValueError):
            cmdline.create_parser(main)

    def test_env_defaults(self):
        def main(one, two):
            pass
        try:
            original = os.environ
            os.environ = {'ONE': 1}
            parser = cmdline.create_parser(main)
            self.assertEqual(parser.option_list[0].default, 1)
            self.assertIs(parser.option_list[1].default, cmdline.NODEFAULT)
        finally:
            os.environ = original

    def test_env_prefixes(self):
        def main(one, two):
            pass
        try:
            original = os.environ
            os.environ = {'X_ONE': 1, 'TWO': 2}
            parser = cmdline.create_parser(main, env_prefix='X_')
            self.assertEqual(parser.option_list[0].default, 1)
            self.assertIs(parser.option_list[1].default, cmdline.NODEFAULT)
        finally:
            os.environ = original

    def test_help_strings(self):
        def main(a, b=None):
            pass
        parser = cmdline.create_parser(main)
        self.assertIs(parser.option_list[0].help, None)
        self.assertEqual(parser.option_list[1].help, '[default: %default]')


class TestApplyOptions(unittest.TestCase):

    def setUp(self):
        self.opts = VarObj()
        self.args = []

    def test_void_function(self):
        def main():
            return Ellipsis
        value = cmdline.apply_options(main, self.opts, self.args)
        self.assertIs(value, Ellipsis)

    def test_positional_argument(self):
        def main(a, b,c):
            return (a, b, c)
        self.opts.a = 1
        self.opts.b = 2
        self.opts.c = 3
        value = cmdline.apply_options(main, self.opts, self.args)
        self.assertTupleEqual(value, (1, 2, 3))

    def test_keyword_argument(self):
        def main(a=None, b=None, c=None):
            return (a, b, c)
        self.opts.a = 1
        self.opts.b = 2
        self.opts.c = 3
        value = cmdline.apply_options(main, self.opts, self.args)
        self.assertEqual(value, (1, 2, 3))

    def test_variable_arguments(self):
        def main(*args):
            return tuple(args)
        self.args.append(1)
        self.args.append(2)
        self.args.append(3)
        value = cmdline.apply_options(main, self.opts, self.args)
        self.assertTupleEqual(value, (1, 2, 3))

    def test_variable_keywords(self):
        def main(**kwargs):
            return dict(args)
        with self.assertRaises(cmdline.CommandLineError):
            value = cmdline.apply_options(main, self.opts, self.args)

    def test_positional_with_variable_arguments(self):
        def main(a, *b):
            return (a, b)
        self.opts.a = 1
        self.args.append(2)
        value = cmdline.apply_options(main, self.opts, self.args)
        self.assertTupleEqual(value, (1, (2,)))

    def test_missing_option(self):
        def main(a):
            return a
        with self.assertRaises(cmdline.CommandLineError):
            value = cmdline.apply_options(main, self.opts, self.args)

    def test_missing_arguments(self):
        def main():
            return Ellipsis
        self.args.append(None)
        with self.assertRaises(cmdline.CommandLineError):
            value = cmdline.apply_options(main, self.opts, self.args)

    @mock.patch('sys.stderr')
    @mock.patch('sys.exit')
    def test_missing_required(self, exit, stderr):
        def main(a):
            pass
        self.opts.a = cmdline.NODEFAULT
        cmdline.apply_options(main, self.opts, self.args)
        self.assertTrue(exit.called)


if __name__ == "__main__":
    unittest.begin()
