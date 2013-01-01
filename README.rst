======
begins
======

--------
Overview
--------
Convenience functions for starting Python programs.

-----
Usage
-----
The ``begin.start()`` function can be
used as a function call
or a decorator.
If called as a function
it returns True if
called from the ``__main__`` module.
To do this it inspects
the stack frame of the caller,
checking the ``__name__`` global.

This allows the following Python pattern:

>>> if __name__ == '__main__':
...     pass

To be replace with:

>>> import begin
>>> if begin.start():
...    pass

If used as a decorator
to annotate a function
it will register the function
to run after the module
has been loaded
if the module is
the ``__main__`` module.
This uses the ``atexit`` module
so may not work correctly with
code that uses ``sys.exitfunc``.

Usage of ``begin.start()`` as
a decorator looks like:

>>> import begin
>>> @begin.start
... def run():
...     pass

By defering the execution
of the function until after
the remainder of the module has loaded
ensures the main function doesn't fail
if depending on something
defined in later code.
