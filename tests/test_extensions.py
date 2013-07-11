from __future__ import absolute_import, division, print_function
import argparse
import cgitb
import mock
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from begin import extensions


def target():
    "target"
    return Ellipsis


class Options(object):
    pass


class TestExtension(unittest.TestCase):

    def setUp(self):
        self.extension = extensions.Extension(target)

    def test_call(self):
        self.assertIs(self.extension(), Ellipsis)

    def test_add_arguments(self):
        self.assertRaises(NotImplementedError, self.extension.add_arguments, mock.Mock())

    def test_run(self):
        self.assertRaises(NotImplementedError, self.extension.run, mock.Mock())

    def test_property_wrapped(self):
        self.assertIs(self.extension.__wrapped__, target)

    def test_property_doc(self):
        self.assertIs(self.extension.__doc__, target.__doc__)

    def test_property_module(self):
        self.assertIs(self.extension.__module__, target.__module__)

    def test_property_name(self):
        self.assertIs(self.extension.__name__, target.__name__)

    if sys.version_info[0] > 2:
        exec("""
def test_property_annotations(self):
    self.assertIs(self.extension.__annotations__, target.__annotations__)
""")


class TestTracebacks(unittest.TestCase):

    def setUp(self):
        self.tracebacks = extensions.Tracebacks(target)

    def test_add_arguments(self):
        parser = argparse.ArgumentParser()
        self.assertEqual(len(parser._action_groups), 2)
        self.assertEqual(len(parser._optionals._actions), 1)
        self.tracebacks.add_arguments(parser)
        self.assertEqual(len(parser._action_groups), 3)
        self.assertEqual(len(parser._optionals._actions), 3)

    @mock.patch('cgitb.enable')
    def test_run_disabled(self, enable):
        opts = Options()
        opts.tracebacks = False
        self.tracebacks.run(opts)
        self.assertFalse(enable.called)

    @mock.patch('cgitb.enable')
    def test_run_stdout(self, enable):
        opts = Options()
        opts.tracebacks = True
        opts.tbdir = None
        self.tracebacks.run(opts)
        enable.assert_called_once_with(format='txt', logdir=None)

    @mock.patch('cgitb.enable')
    def test_run_directory(self, enable):
        opts = Options()
        opts.tracebacks = True
        opts.tbdir = '/dev/null'
        self.tracebacks.run(opts)
        enable.assert_called_once_with(format='txt', logdir='/dev/null')


if __name__ == '__main__':
    unittest.begin()
