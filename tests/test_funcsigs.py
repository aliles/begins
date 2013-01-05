from __future__ import absolute_import, division, print_function

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from begin import funcsigs as inspect


class TestFunctionSignatures(unittest.TestCase):

    @staticmethod
    def signature(func):
        sig = inspect.signature(func)
        return (tuple((param.name,
                       (Ellipsis if param.default is param.empty else param.default),
                       (Ellipsis if param.annotation is param.empty
                                                        else param.annotation),
                       str(param.kind).lower())
                                    for param in sig.parameters.values()),
                (Ellipsis if sig.return_annotation is sig.empty
                                            else sig.return_annotation))

    def test_zero_arguments(self):
        def test():
            pass
        self.assertEqual(self.signature(test),
                ((), Ellipsis))

    def test_single_positional_argument(self):
        def test(a):
            pass
        self.assertEqual(self.signature(test),
                (((('a', Ellipsis, Ellipsis, "positional_or_keyword")),), Ellipsis))

    def test_single_keyword_argument(self):
        def test(a=None):
            pass
        self.assertEqual(self.signature(test),
                (((('a', None, Ellipsis, "positional_or_keyword")),), Ellipsis))

    def test_var_args(self):
        def test(*args):
            pass
        self.assertEqual(self.signature(test),
                (((('args', Ellipsis, Ellipsis, "var_positional")),), Ellipsis))

    def test_keywords_args(self):
        def test(**kwargs):
            pass
        self.assertEqual(self.signature(test),
                (((('kwargs', Ellipsis, Ellipsis, "var_keyword")),), Ellipsis))

    def test_multiple_arguments(self):
        def test(a, b=None, *args, **kwargs):
            pass
        self.assertEqual(self.signature(test), ((
            ('a', Ellipsis, Ellipsis, "positional_or_keyword"),
            ('b', None, Ellipsis, "positional_or_keyword"),
            ('args', Ellipsis, Ellipsis, "var_positional"),
            ('kwargs', Ellipsis, Ellipsis, "var_keyword"),
            ), Ellipsis))


if __name__ == "__main__":
    unittest.begin()
