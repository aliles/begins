import sys
import unittest

import begin

if sys.version_info > (3, 0):
    unicode = lambda s: s


class TestCmdline(unittest.TestCase):

    def test_cmdline_simple(self):
        # begin.parse_cmdline() with simple arguments
        args = {
                'natural': 1,
                'r': 1.0,
                'hello': 'world',
                'japanese':
                    unicode('\u30cf\u30ed\u30fc\u30ef\u30fc\u30eb\u30c9'),
                'verbose': False,
        }
        cmdline = ['-r', '10.0', '--verbose']
        opts = begin.parse_cmdline(args, cmdline=cmdline)
        self.assertEqual(opts.natural, 1)
        self.assertEqual(opts.r, 10.0)
        self.assertEqual(opts.hello, 'world')
        self.assertEqual(opts.japanese,
                unicode('\u30cf\u30ed\u30fc\u30ef\u30fc\u30eb\u30c9'))
        self.assertEqual(opts.verbose, True)

    def test_cmdline_advanced(self):
        # begin.parse_cmdline() with advanced arguments
        args = {
                'natural': begin.Argument('n', None, 1, 'a natural number'),
                'real': begin.Argument('f', 'float', 1.0, 'a real number'),
                'hello': begin.Argument(None, 'name', 'world', 'a name'),
                'japanese': begin.Argument('j', 'japanese',
                    unicode('\u30cf\u30ed\u30fc\u30ef\u30fc\u30eb\u30c9'),
                    None),
                'verbose': begin.Argument('v', None, False, 'verbosity flag'),
                'target': begin.Argument(None, None, None, 'a file name'),
        }
        cmdline = ['-n', '100', '--float', '0.0', '-v', 'filename']
        opts = begin.parse_cmdline(args, cmdline=cmdline)
        self.assertEqual(opts.natural, 100)
        self.assertEqual(opts.real, 0.0)
        self.assertEqual(opts.hello, 'world')
        self.assertEqual(opts.japanese,
                unicode('\u30cf\u30ed\u30fc\u30ef\u30fc\u30eb\u30c9'))
        self.assertEqual(opts.verbose, True)
        self.assertEqual(opts.target, 'filename')

if __name__ == '__main__':
    unittest.begin()
