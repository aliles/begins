======
begins
======

--------
Overview
--------

Command line programs for *lazy* humans.

|build_status| |coverage|

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
it will register the function
to run after the module
has been loaded
if the module is
the ``__main__`` module.
This uses the ``atexit`` module
so may not work correctly with
code that uses ``sys.exitfunc``.

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
    ... def run(name, quest, colour='blue', *knights):
    ...     "tis but a scratch!"

The decorated function above
will generate the following
command line help::

    Usage: run.py [options]

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

    import begin
    @begin.start
    def run(name: 'What, is your name?',
            quest: 'What, is your quest?',
            colour: 'What, is your favourite colour?'):
        pass

Will generate command help like::

    Usage: run.py [options]

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

------
Issues
------

Any bug reports or
freature requests can
be made using GitHub' `issues system`_.

.. _Github: https://github.com/aliles/begins
.. _Python Package Index: http://pypi.python.org/pypi
.. _Pip: http://www.pip-installer.org
.. _issues system: https://github.com/aliles/begins/issues
.. _function annotations: http://www.python.org/dev/peps/pep-3107/

.. |build_status| image:: https://secure.travis-ci.org/aliles/begins.png?branch=master
   :target: https://travis-ci.org/aliles/begins
   :alt: Current build status

.. |coverage| image:: https://coveralls.io/repos/aliles/begins/badge.png?branch=master
   :target: https://coveralls.io/r/aliles/begins?branch=master
   :alt: Latest PyPI version
