======
begins
======

--------
Overview
--------

Command line programs for *lazy* humans.

* Decorate a function to be your programs starting point.
* Generate command line parser based on function signature.
* Search system environment for option default values.

|build_status| |coverage|

-----------
Why begins?
-----------

I write a lot of
small programs in `Python`_.
These programs often
accept a small number of
simple command line arguments.
Having to write
command line parsing code
in each of these
small programs both
breaks my train of thought
and greatly increases the
volume of code I am writting.

Begins was implemented to
remove the boilerplate code
from these Python programs.
It's not intended to replace
the rich command line processing
needed for larger applications.

------------
Installation
------------

Currently *begins* is not available
for downloading from the
`Python Package Index`_.
However, if using `Pip`_
you can install directly
from `Github`_. ::

$ pip install git+https://github.com/aliles/begins.git

Please note that
*begins* is still in
an alpha state so
the API and behaviour could
still change.

---------------------------------
Setting a programs starting point
---------------------------------

The ``begin.start()`` function can be
used as a function call
or a decorator.
If called as a function
it returns True when
called from the ``__main__`` module.
To do this it inspects
the stack frame of the caller,
checking the ``__name__`` global.

This allows the following Python pattern::

    >>> if __name__ == '__main__':
    ...     pass

To be replace with::

    >>> import begin
    >>> if begin.start():
    ...    pass

If used as a decorator
to annotate a function
the function will be called
if defined in the ``__main__`` module
as determined by inspecting
the current stack frame.
Any definitions that follow
the decorated function
wont be created until
after the function call
is complete.

Usage of ``begin.start()`` as
a decorator looks like::

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

----------------------------
Parsing command line options
----------------------------

If ``begin.start()`` deocrates a
function accepts parameters
``begin.start()`` will
process the command for
options to pass as
those parameters::

    >>> import begin
    >>> @begin.start
    ... def run(name='Arther', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

The decorated function above
will generate the following
command line help::

    Usage: run.py [knights]

    tis but a scratch!

    Options:
    -n NAME, --name=NAME
    -q QUEST, --quest=QUEST
    -c COLOUR, --colour=COLOUR
    -h, --help            show this help message and exit

In Python3, any `function annotations`_
for a paramter become
the command line option help.
For example::

    >>> import begin
    >>> @begin.start                                         # doctest: +SKIP
    ... def run(name: 'What, is your name?',
    ...         quest: 'What, is your quest?',
    ...         colour: 'What, is your favourite colour?'):
    ...     pass

Will generate command help like::

    Usage: run.py [knights]

    Options:
        -n NAME, --name=NAME  What, is your name?
        -q QUEST, --quest=QUEST
                              What, is your quest?
        -c COLOUR, --colour=COLOUR
                              What, is your favourite colour?
        -h, --help            show this help message and exit

Command line parsing supports:

* positional arguments
* keyword arguments
* default values
* variable length arguments
* annotations

Command line parsing
does not support
variable length keyword arguments,
commonly written as
``**kwargs``.
If variable length keyword arguments
are used by
the decorated function
an exception
will be raised.

If a paramater
does not have a default,
failing to pass a value
on the command line
will cause running the program to
print an error and exit.

---------------------
Environment Variables
---------------------

Default values for
command line options can
be overridden using
envionrment variables.
The presence of an
uppercased version of
a command line option
as an environment variable
will set the default value of
command line options.
In the example above,
if an environment variable
``NAME`` existed,
it's value would be
used as the default for
the ``name`` option.
The options value can
still be set by
explicitly passing a
new value as
a command line option.

If there are concerns of
conflicts with existing
environment variables
a prefix can be provided to
the decorator::

    >>> import begin
    >>> @begin.start(env_prefix='MP_')
    ... def run(name='Arther', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

This example will
use the environment variable
``MP_NAME`` instead of the
preivous ``NAME``.

---------------------
Argument type casting
---------------------

Command line arguments are
always passed as strings.
Sometimes thought it is
more convenient to
receive arguments of
different types.
For example, this is a
possible function for
starting a web application::

    >>> @begin.start
    ... def main(host='127.0.0.1', port='8080', debug='False'):
    ...    port = int(port)
    ...    debug = begin.utils.tobool(debug)
    ...    "Run web application"

Having to convert
the ``port`` argument to
an integer and
the ``debug`` argument to
a boolean is
additional boilerplate code.
To avoid this *begins* provides
the ``begin.convert()`` decorator.
This decorator accepts functions
as keyword arguments where
the argument name matches that of
the decorator function.
These functions are used
to convert the
types of arguments.

Rewritting the example above using
the ``begin.convert()`` decorator::

    >>> @begin.start
    ... @begin.convert(port=int, debug=begin.utils.tobool)
    ... def main(host='127.0.0.1', port=8080, debug=False):
    ...    "Run web application"

The module ``begin.utils`` contains
useful functions for
converting argument types.

------
Issues
------

Any bug reports or
freature requests can
be made using GitHub' `issues system`_.

.. _Github: https://github.com/aliles/begins
.. _Python: http://python.org
.. _Python Package Index: https://pypi.python.org/pypi
.. _Pip: http://www.pip-installer.org
.. _issues system: https://github.com/aliles/begins/issues
.. _function annotations: http://www.python.org/dev/peps/pep-3107/

.. |build_status| image:: https://secure.travis-ci.org/aliles/begins.png?branch=master
   :target: https://travis-ci.org/aliles/begins
   :alt: Current build status

.. |coverage| image:: https://coveralls.io/repos/aliles/begins/badge.png?branch=master
   :target: https://coveralls.io/r/aliles/begins?branch=master
   :alt: Latest PyPI version
