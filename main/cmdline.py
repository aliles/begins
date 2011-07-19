"Simple command line parsing using argparse."
from collections import namedtuple
from functools import partial
import argparse

__all__ = ['Argument', 'parse_cmdline']


class Argument(namedtuple('BaseArgument', 'short full default help')):
    """Command line argument option for command line parser.

    If both short and full are None the argument is a positional argument.
    Otherwise short is a single character opton and full is a long name
    option.
    """

    def __new__(self, short=None, full=None, default=None, help=None):
        return super(Argument, self).__new__(Argument,
                short, full, default, help)


def parse_cmdline(arguments, description=None, epilog=None,
        known_args=False, cmdline=None):
    """Parse a command line using the arguments dictionary.

    The arguments dictionary keys are the option names. Values are either
    an Argument instance or a string. If the value is a string it's used for
    the option flag, short or long depending on length.
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    for name in sorted(arguments):
        if isinstance(arguments[name], Argument):
            _add_advanced_argument(parser, name, arguments[name])
        else:
            _add_simple_argument(parser, name, arguments[name])
    if known_args:
        return parser.parse_known_args(cmdline)
    return parser.parse_args(cmdline)


def _type_not_none(obj):
    "Return type of all object exception None"
    if obj is None:
        return None
    return type(obj)


def _add_simple_argument(parser, name, default):
    "Add an argument using simple options"
    flag = '--' + name if len(name) > 1 else '-' + name
    if not isinstance(default, bool):
        parser.add_argument(flag, default=default,
                type=_type_not_none(default))
    else:
        action = 'store_true' if not default else 'store_false'
        parser.add_argument(flag, action=action, default=default)


def _add_advanced_argument(parser, name, args):
    "Add an argument using an Argument object"
    flags = []
    if args.short:
        flags.append('-' + args.short[:1])
    if args.full:
        flags.append('--' + args.full)
    default = args.default
    if not isinstance(default, bool):
        parser.add_argument(*flags, dest=name, default=default,
                type=_type_not_none(default), help=args.help)
    else:
        action = 'store_true' if not default else 'store_false'
        parser.add_argument(*flags, dest=name, action=action,
                default=default, help=args.help)
