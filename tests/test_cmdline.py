from __future__ import absolute_import, division, print_function
import cgitb
import mock
import os
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import pkg_resources

from begin import cmdline
from begin import extensions
from begin import subcommands


class Options(object):
    pass


class TestProgramName(unittest.TestCase):

    def setUp(self):
        self.ordir = os.path.abspath(os.curdir)
        os.chdir('./tests')

    def tearDown(self):
        os.chdir(self.ordir)

    def test_simple_script(self):
        def func():
            pass
        prog = cmdline.program_name('main.py', func)
        self.assertEqual(prog, 'main.py')

    def test_main_module(self):
        def func():
            pass
        prog = cmdline.program_name('__main__.py', func)
        self.assertEqual(prog, 'tests')

    @mock.patch('os.path.split')
    def test_unusable_path(self, psplit):
        psplit.return_value = ('', '__main__.py')
        def func():
            pass
        prog = cmdline.program_name('__main__.py', func)
        self.assertEqual(prog, 'func')


class TestCreateParser(unittest.TestCase):

    def tearDown(self):
        for collector in subcommands.COLLECTORS.values():
            collector.clear()

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

    def test_subcommand(self):
        @subcommands.subcommand
        def subcmd():
            pass
        def main():
            pass
        parser = cmdline.create_parser(main)
        self.assertEqual(len(parser._action_groups), 3)
        self.assertIn('subcmd', parser.format_help())

    def test_subcommand_group(self):
        @subcommands.subcommand(group='named.collector')
        def subcmd():
            pass
        def main():
            pass
        parser = cmdline.create_parser(main, sub_group='named.collector')
        self.assertEqual(len(parser._action_groups), 3)
        self.assertIn('subcmd', parser.format_help())

    @mock.patch('pkg_resources.iter_entry_points')
    def test_plugins(self, iep):
        def main():
            pass
        def subcmd():
            pass
        def entry_points(group, *args):
            yield subcmd
        iep.side_effect = entry_points
        parser = cmdline.create_parser(main, plugins='entry.point')
        self.assertEqual(len(parser._action_groups), 3)
        self.assertIn('subcmd', parser.format_help())

    def test_conflict_resoltion(self):
        def main(help):
            pass
        parser = cmdline.create_parser(main)

    def test_subcommand_conflict_resoltion(self):
        @subcommands.subcommand
        def subcmd(help):
            pass
        def main():
            pass
        parser = cmdline.create_parser(main)

    def test_no_short_args(self):
        def main(alpha):
            pass
        parser = cmdline.create_parser(main, short_args=False)
        self.assertNotIn(' -a ', parser.format_help())

    def test_lexical_order(self):
        def main(zeta, alpha, delta):
            pass
        parser = cmdline.create_parser(main, lexical_order=True)
        self.assertEqual(parser._optionals._actions[1].dest, 'alpha')
        self.assertEqual(parser._optionals._actions[2].dest, 'delta')
        self.assertEqual(parser._optionals._actions[3].dest, 'zeta')

    def test_subcommand_description(self):
        @subcommands.subcommand
        def subcmd():
            """SUBCOMMAND_HELP

            SUBCOMMAND_DESC
            """
        def main():
            pass
        parser = cmdline.create_parser(main)
        self.assertIn('SUBCOMMAND_HELP', parser.format_help())
        self.assertNotIn('SUBCOMMAND_DESC', parser.format_help())


class TestApplyOptions(unittest.TestCase):

    def setUp(self):
        self.opts = Options()

    def tearDown(self):
        for collector in subcommands.COLLECTORS.values():
            collector.clear()

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

    def test_subcommand(self):
        @subcommands.subcommand
        def subcmd():
            return 'blue'
        def main():
            return 'red'
        self.opts._subcommand = 'subcmd'
        value = cmdline.apply_options(main, self.opts)
        self.assertEqual('blue', value)

    def test_subcommand_group(self):
        @subcommands.subcommand(group='named.collector')
        def subcmd():
            return 'blue'
        def main():
            return 'red'
        self.opts._subcommand = 'subcmd'
        value = cmdline.apply_options(main, self.opts, sub_group='named.collector')
        self.assertEqual('blue', value)


if __name__ == "__main__":
    unittest.begin()
