from __future__ import absolute_import, division, print_function
import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from begin import cmdline


class TestCommandLine(unittest.TestCase):

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

    def test_keyword_argument(self):
        def main(opt=Ellipsis):
            pass
        parser = cmdline.create_parser(main)
        self.assertEqual(len(parser.option_list), 2)
        self.assertIs(parser.option_list[0].default, Ellipsis)

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
    self.assertEqual(parser.option_list[0].help, 'help string')
""")


if __name__ == "__main__":
    unittest.begin()
