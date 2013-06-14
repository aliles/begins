"Syntactic sugar for a programs 'main'."
from __future__ import absolute_import, division, print_function
import inspect

from begin import cmdline

__all__ = ['start']


def start(func=None, **kwargs):
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

    This also inspects the stack frame of the caller, choosing whether to call
    function immediately. Any definitions following the function wont be
    called until after the main function is complete.

    If used as a decorator, and the decorated function accepts either
    positional or keyword arguments, a command line parser will be generated
    and used to parse command line options.

    >>> @begin.start
    ... def main(first, second=''):
    ...     pass

    This will cause the command line parser to accept two options, the second
    of which defaults to ''.

    Default values for command line options can also be set from the current
    environment, using the uppercased version of an options name. In the
    example above, the environment variable 'FIRST' will set a default value
    for the first argument.

    To use a prefix with expected environment variables (for example, to
    prevent collisions) give an 'env_prefix' argument to the decorator.

    >>> @begin.start(env_prefix='PY_')
    ... def main(first, second=''):
    ...     pass

    The environment variable 'PY_FIRST' will be used instead of 'FIRST'.
    """
    def _start(func):
        if func.__module__ == '__main__':
            parser = cmdline.create_parser(func, **kwargs)
            if len(parser.option_list) > 1:
                opts, args = parser.parse_args()
                cmdline.apply_options(func, opts, args)
            else:
                func()
        return func

    # start() is a decorator factory
    if func is None and len(kwargs) > 0:
        return _start
    # start() is a boolean function
    elif func is None:
        stack = inspect.stack()
        if len(stack) < 1:
            return False
        frame = stack[1][0]
        if not inspect.isframe(frame):
            return False
        return frame.f_globals['__name__'] == '__main__'
    # not correctly used to decorate a function
    elif not callable(func):
        raise ValueError("Function '{0!r}' is not callable".format(func))
    return _start(func)
