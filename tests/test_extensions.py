from __future__ import absolute_import, division, print_function
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


if __name__ == '__main__':
    unittest.begin()
