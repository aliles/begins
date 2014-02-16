from __future__ import absolute_import, division, print_function
import argparse
import mock
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from begin import formatters


class TestCompose(unittest.TestCase):

    def make_parser(self, formatter_class):
        parser = argparse.ArgumentParser(description='A test parser',
                formatter_class=formatter_class)
        parser.add_argument('test', help='Test argument')
        subparsers = parser.add_subparsers(title='Available subcommands')
        subparser = subparsers.add_parser('command', help='Test Subcommand',
                formatter_class=formatter_class)
        subparser.add_argument('test', help='Test argument')
        return parser

    def test_zero_mixins(self):
        formatter_class = formatters.compose()

    def test_all_mixins(self):
        formatter_class = formatters.compose(
                formatters.RawArguments,
                formatters.RawDescription,
                formatters.ArgumentDefaults,
                formatters.RemoveSubcommandsLine)

    def test_with_name(self):
        name = '__HelpFormatterForTesting'
        formatter_class = formatters.compose(formatters.RawDescription,
                name=name)
        self.assertEqual(formatter_class.__name__, name)

    def test_invalid_keyword(self):
        with self.assertRaises(TypeError):
            formatters.compose(invalid=None)

    def test_raw_argument(self):
        formatter_class = formatters.compose(formatters.RawArguments)
        parser = self.make_parser(formatter_class)
        clihelp = parser.format_help()

    def test_raw_description(self):
        formatter_class = formatters.compose(formatters.RawDescription)
        parser = self.make_parser(formatter_class)
        clihelp = parser.format_help()

    def test_argument_defaults(self):
        formatter_class = formatters.compose(formatters.ArgumentDefaults)
        parser = self.make_parser(formatter_class)
        clihelp = parser.format_help()

    def test_remove_subcommands_line(self):
        formatter_class = formatters.compose(formatters.RemoveSubcommandsLine)
        parser = self.make_parser(formatter_class)
        clihelp = parser.format_help()
