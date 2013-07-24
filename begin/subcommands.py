"Subcommand support for command lines"

try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping


class Collector(dict):
    """Collect functions for use as subcommands"""

    def commands(self):
        for name in sorted(self):
            yield self[name]

    def register(self, func):
        if func.__name__ in self:
            msg = "Function named '{0}' already registered".format(func.__name__)
            raise ValueError(msg)
        self[func.__name__] = func


def subcommand(func=None, collector=None):
    """Register function as a program's subcommand

    Functions are registered with the default subcommand collector, unless a
    custom collector is provided through the 'collector' argument. Subcommands
    will automatically be included in the generated command line support.
    """
    collector = DEFAULT if collector is None else collector
    def wrapper(func):
        collector.register(func)
        return func
    if func is not None:
        return wrapper(func)
    return wrapper


DEFAULT = Collector()
