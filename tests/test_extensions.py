from __future__ import absolute_import, division, print_function
import argparse
import cgitb
import logging
import logging.handlers
import mock
import platform
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from begin import cmdline
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
        self.assertRaises(NotImplementedError, self.extension.add_arguments,
                mock.Mock(), mock.Mock())

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
        self.tracebacks.add_arguments(parser, cmdline.DefaultsManager())
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


class TestLoging(unittest.TestCase):

    def setUp(self):
        self.logs = extensions.Logging(target)
        self.opts = Options()
        self.opts.verbose = False
        self.opts.quiet = False
        self.opts.loglvl = None
        self.opts.logfile = None
        self.opts.logfmt = None

    def test_add_arguments(self):
        parser = argparse.ArgumentParser()
        self.assertEqual(len(parser._action_groups), 2)
        self.assertEqual(len(parser._optionals._actions), 1)
        self.logs.add_arguments(parser, cmdline.DefaultsManager())
        self.assertEqual(len(parser._action_groups), 3)
        self.assertEqual(len(parser._optionals._actions), 6)

    @mock.patch('logging.getLogger')
    def test_run_default(self, getlogger):
        self.logs.run(self.opts)
        self.assertTrue(getlogger.called)
        logger = getlogger.return_value
        logger.setLevel.assert_called_once_with(logging.getLevelName('INFO'))
        self.assertTrue(logger.addHandler.called)
        self.assertIsInstance(logger.addHandler.call_args[0][0],
                logging.StreamHandler)

    @mock.patch('logging.getLogger')
    def test_run_verbose(self, getlogger):
        self.opts.verbose = True
        self.logs.run(self.opts)
        self.assertTrue(getlogger.called)
        logger = getlogger.return_value
        logger.setLevel.assert_called_once_with(logging.getLevelName('DEBUG'))

    @mock.patch('logging.getLogger')
    def test_run_quiet(self, getlogger):
        self.opts.quiet = True
        self.logs.run(self.opts)
        self.assertTrue(getlogger.called)
        logger = getlogger.return_value
        logger.setLevel.assert_called_once_with(logging.getLevelName('WARNING'))

    @mock.patch('logging.getLogger')
    def test_run_loglvl(self, getlogger):
        self.opts.loglvl = 'ERROR'
        self.logs.run(self.opts)
        self.assertTrue(getlogger.called)
        logger = getlogger.return_value
        logger.setLevel.assert_called_once_with(logging.getLevelName('ERROR'))

    @mock.patch('logging.getLogger')
    def test_run_reinitialise(self, getlogger):
        getlogger.return_value.handlers = [Ellipsis]
        self.logs.run(self.opts)
        getlogger.return_value.removeHandler.assert_called_once_with(Ellipsis)

    @mock.patch('logging.open', mock.mock_open(), create=True)
    @mock.patch('platform.system')
    @mock.patch('logging.getLogger')
    def test_run_logfile_linux(self, getlogger, system):
        system.return_value = 'Linux'
        self.opts.logfile = '/dev/null'
        self.logs.run(self.opts)
        logger = getlogger.return_value
        self.assertTrue(logger.addHandler.called)
        self.assertIsInstance(logger.addHandler.call_args[0][0],
                logging.handlers.WatchedFileHandler)

    @mock.patch('logging.open', mock.mock_open(), create=True)
    @mock.patch('platform.system')
    @mock.patch('logging.getLogger')
    def test_run_logfile_windows(self, getlogger, system):
        system.return_value = 'Windows'
        self.opts.logfile = '/dev/null'
        self.logs.run(self.opts)
        logger = getlogger.return_value
        self.assertTrue(logger.addHandler.called)
        self.assertIsInstance(logger.addHandler.call_args[0][0],
                logging.FileHandler)


if __name__ == '__main__':
    unittest.begin()
