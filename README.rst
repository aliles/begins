====
main
====

--------
Overview
--------
Convenience functions for Python main programs.

-------
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
>>> @main.execute
... def run():
...     pass

By defering the execution of the function until after the remainder of the
module has loaded ensures the main function doesn't fail if depending on
something defined in the later code.

-------------
parse_cmdline
-------------
This is a simple wrapper over the ``argparse`` module. Configuration of the
expected command line arguments is done through a ``dict`` object passed to the
function. Each items in the ``dict`` is a different command line option, in
either a simple of advanced format.

It's not possible to do everything with ``parse_cmdline`` that can be done with
``argparse``. It's intended to make doing the most common things simple.

simple arguments
----------------
These a simple key vaue pairs. The key is the option flag (without the '-' or
'--' prefix) and the value is the default. The exception to this is if the
value is a ``bool``. In that case the flag will store the opposite boolean
value of the default.

advanced arguments
------------------
These are an instance of main.Argument. Uses advanced arguments both short and
long options can be specified. The options are different to the attribute on
the return object which stores the value. And a help string can be provided.

If both the short and long option are None then this option is assumed to be a
positional argument.

usage
-----
Using ``parse_cmdline`` looks like.

>>> import main
>>> args = {
...     'hello': 'world',
...     'natural': main.Argument('n', None, 1, 'a natural number'),
...     'real': main.Argument('f', 'float', 1.0, 'a real number'),
...     'verbose': False,
... }
>>> opts = main.parse_cmdline(args, 'This is a program')
>>> opts.hello == 'world'
True
>>>
