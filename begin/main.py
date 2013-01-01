"Convenience function for a programs 'main'."
import atexit
import collections
import inspect

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
    """
    if func is not None:
        if func.__module__ == '__main__':
            atexit.register(func)
    else:
        stack = inspect.stack()
        if len(stack) < 1:
            return False
        frame = stack[1][0]
        if not inspect.isframe(frame):
            return False
        return frame.f_globals['__name__'] == '__main__'
