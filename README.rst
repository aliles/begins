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

|pypi_version| |build_status| |coverage|

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
volume of code I am writing.

Begins was implemented to
remove the boilerplate code
from these Python programs.
It's not intended to replace
the rich command line processing
needed for larger applications.

------------
Requirements
------------

For Python versions earlier
than Python 3.3,
the `funcsigs`_ package from the
`Python Package Index`_ is
required.

For Python version 2.6,
the `argparse`_ package from the
`Python Package Index`_ is
also required.

Both of these dependencies are
listed in the package configuration.
If using `Pip`_ to
install *begins* then
the required dependencies will
be automatically installed.

------------
Installation
------------

*begins* is available
for download from
the `Python Package Index`_.
To install using `Pip`_ ::

$ pip install begins

Alternatively, the latest
development version can be
installed directly
from `Github`_. ::

$ pip install git+https://github.com/aliles/begins.git

Please note that
*begins* is still in
an alpha state 
and therefore
the API or behaviour
could change.

---------------------------------
Setting a programs starting point
---------------------------------

The ``begin.start()`` function can be
used as a function call
or a decorator.
If called as a function
it returns ``True`` when
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

By deferring the execution
of the function until after
the remainder of the module has loaded
ensures the main function doesn't fail
if depending on something
defined in later code.

----------------------------
Parsing command line options
----------------------------

If ``begin.start()`` decorates a
function accepts parameters
``begin.start()`` will
process the command for
options to pass as
those parameters::

    >>> import begin
    >>> @begin.start
    ... def run(name='Arthur', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

The decorated function above
will generate the following
command line help::

   usage: example.py [-h] [-n NAME] [-q QUEST] [-c COLOUR]
                     [knights [knights ...]]

   tis but a scratch!

   positional arguments:
     knights

   optional arguments:
     -h, --help            show this help message and exit
     -n NAME, --name NAME  (default: Arthur)
     -q QUEST, --quest QUEST
                           (default: Holy Grail)
     -c COLOUR, --colour COLOUR
                           (default: blue)

In Python 3, any `function annotations`_
for a parameter become
the command line option help.
For example::

    >>> import begin
    >>> @begin.start                                         # doctest: +SKIP
    ... def run(name: 'What, is your name?',
    ...         quest: 'What, is your quest?',
    ...         colour: 'What, is your favourite colour?'):
    ...     pass

Will generate command help like::

   usage: holygrail_py3.py [-h] -n NAME -q QUEST -c COLOUR

   optional arguments:
     -h, --help            show this help message and exit
     -n NAME, --name NAME  What, is your name?
     -q QUEST, --quest QUEST
                           What, is your quest?
     -c COLOUR, --colour COLOUR
                           What, is your favourite colour?

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

If a parameter
does not have a default,
failing to pass a value
on the command line
will cause running the program to
print an error and exit.

For programs that have
a large number of options
it may be preferable to
only use long options.
To suppress short options,
pass ``False`` as the
``short_args`` keyword argument to
the ``begin.start`` decorator::

    >>> import begin
    >>> @begin.start(short_args=False)
    ... def run(name='Arthur', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

This program will not
accept ``-n``, ``-q`` or ``-c``
as option names.

Similarity, a large number of
command line options may
be better displayed in
alphabetical order.
This can be achieved
by passing ``lexical_order``
as ``True``::

    >>> import begin
    >>> @begin.start(lexical_order=True)
    ... def main(charlie=3, alpha=1, beta=2):
    ...     pass

This program will list
the command line options as
``alpha``, ``beta``, ``charlie``
instead of the order
in which the function
accepts them.

---------------
Further Reading
---------------

A walk-through tutorial,
the remainder of this guide
and API documentation can
are all part of the
official *begins* documentation
hosted on `Read The Docs`_.

------
Issues
------

Any bug reports or
feature requests can
be made using GitHub's `issues system`_.

.. _Github: https://github.com/aliles/begins
.. _Read The Docs: http://begins.readthedocs.org
.. _Python: http://python.org
.. _Python Package Index: https://pypi.python.org/pypi
.. _Pip: http://www.pip-installer.org
.. _argparse: https://pypi.python.org/pypi/argparse
.. _issues system: https://github.com/aliles/begins/issues
.. _funcsigs: https://pypi.python.org/pypi/funcsigs
.. _function annotations: http://www.python.org/dev/peps/pep-3107/

.. |build_status| image:: https://secure.travis-ci.org/aliles/begins.png?branch=master
   :target: https://travis-ci.org/aliles/begins
   :alt: Current build status

.. |coverage| image:: https://coveralls.io/repos/aliles/begins/badge.png?branch=master
   :target: https://coveralls.io/r/aliles/begins?branch=master
   :alt: Latest PyPI version

.. |pypi_version| image:: https://pypip.in/v/begins/badge.png
   :target: https://crate.io/packages/begins/
   :alt: Latest PyPI version
