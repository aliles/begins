"""Utility functions for begins"""
from distutils.util import strtobool as tobool
from argparse import FileType as tofile

def tolist(value=None, sep=',', empty_strings=False):
    """Convert a string to a list.

    The input string is split on the separator character. The default separator
    is ','. An alternative separator may be passed as the 'sep' keyword. If no
    string value is provided a function is returned that splits a string on the
    provided separator, or default if none was provided. Any empty strings are
    removed from the resulting list. This behaviour can be changed by passing
    True as the 'empty_strings' keyword argument.
    """
    def tolist(value):
        result = value.split(sep)
        if not empty_strings:
            return [r for r in result if len(r) > 0]
        return result
    if value is None:
        return tolist
    return tolist(value)
