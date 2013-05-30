"Syntactic sugar for a programs 'main'."
from __future__ import absolute_import, division, print_function
import atexit
import functools
import inspect

from begin import cmdline

__all__ = ['start']


def start(func=None):
    """Return True if called in a module that is executed.

    Inspects the '__name__' in the stack frame of the caller, comparing it
    to '__main__'. Thus allowing the Python idiom:

    >>> if __name__ == '__main__':
    ...     pass

    To be replace with:

    >>> import begin
    >>> if begin.start():
    ...    pass

    Can also be used as a decorator to register a function to run after the
    module has been loaded.

    >>> @begin.start
    ... def main():
    ...     pass

    This uses the atexit module so may not work correctly with code that
    uses sys.exitfunc.

    If used as a decorator, and the decorated function accepts either
    positional or keyword arguments, a command line parser will be generated
    and used to parse command line options.

    >>> @begin.start
    ... def main(first, second=''):
    ...     pass

    This will cause the command line parser to accept two options, the second
    of which defaults to ''.
    """
    if func is None:
        stack = inspect.stack()
        if len(stack) < 1:
            return False
        frame = stack[1][0]
        if not inspect.isframe(frame):
            return False
        return frame.f_globals['__name__'] == '__main__'
    elif not callable(func):
        raise ValueError("Function '{0!r}' is not callable".format(func))
    elif func.__module__ == '__main__':
        parser = cmdline.create_parser(func)
        if len(parser.option_list) > 1:
            opts, args = parser.parse_args()
            func = functools.partial(cmdline.apply_options, func, opts, args)
        atexit.register(func)
    return func
