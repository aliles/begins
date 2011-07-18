main
====

Overview
--------
Convenience functions for Python main programs.

execute
-------
This can be used as a function call or a decorator. If called as a function is
returns True if called from the ``__main__`` module. To do this is inspects the
stack frame of the caller, checking the ``__name__`` global.

This allows the following Python pattern:

>>> if __name__ == '__main__':
...     pass

To be replace with:

>>> import main
>>> if main.execute():
...    pass

If used as a decorate to annotate a function it will register the function to
run after the module as been loaded if the module is the ``__main__`` module.
This uses the ``atexit`` module so may not work correctly with code that uses
``sys.exitfunc``.

Usage of ``execute`` as a decorator looks like:

>>> import main
>>> @execute
... def main():
...     pass

By defering the execution of the function until after the remainder of the
module has loaded ensures the main function doesn't fail if depending on
something defined in the later code.
