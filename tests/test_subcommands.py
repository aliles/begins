from __future__ import absolute_import, division, print_function
import mock

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import pkg_resources

import begin


class TestSubCommand(unittest.TestCase):

    def tearDown(self):
        begin.subcommands.DEFAULT.clear()

    def test_register_default(self):
        @begin.subcommand
        def one():
            pass
        @begin.subcommand
        def two():
            pass
        self.assertEqual(list(begin.subcommands.DEFAULT.commands()), [one, two])

    def test_register_custom(self):
        collector = begin.subcommands.Collector()
        @begin.subcommand(collector=collector)
        def one():
            pass
        @begin.subcommand(collector=collector)
        def two():
            pass
        self.assertEqual(list(collector.commands()), [one, two])

    def test_double_register(self):
        @begin.subcommand
        def subfunction():
            pass
        with self.assertRaises(ValueError):
            @begin.subcommand
            def subfunction():
                pass

    def test_get_registered(self):
        @begin.subcommand
        def function():
            pass
        self.assertIs(begin.subcommands.DEFAULT.get('function'), function)

    @mock.patch('pkg_resources.iter_entry_points')
    def test_entry_points(self, iep):
        def function():
            pass
        def entry_points(group, name):
            yield function
        iep.side_effect = entry_points
        collector = begin.subcommands.Collector('group.name')
        self.assertEqual(list(collector.commands()), [function])
