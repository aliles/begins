"Subcommand support for command lines"

class Collector(object):
    """Collect functions for use as subcommands"""

    def __init__(self):
        self._commands = {}

    def clear(self):
        self._commands = {}

    def commands(self):
        for name in sorted(self._commands):
            yield self._commands[name]

    def get(self, name):
        return self._commands[name]

    def register(self, func):
        if func.__name__ in self._commands:
            msg = "Function named '{0}' already registered".format(func.__name__)
            raise ValueError(msg)
        self._commands[func.__name__] = func

    def size(self):
        return len(self._commands)


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
