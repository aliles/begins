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
volume of code I am writting.

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
listed in the package configurtion.
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
and therfore
the API or behaviour
could change.

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

   usage: example.py [-h] [-n NAME] [-q QUEST] [-c COLOUR]
                     [knights [knights ...]]

   tis but a scratch!

   positional arguments:
     knights

   optional arguments:
     -h, --help            show this help message and exit
     -n NAME, --name NAME  (default: Arther)
     -q QUEST, --quest QUEST
                           (default: Holy Grail)
     -c COLOUR, --colour COLOUR
                           (default: blue)

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

If a paramater
does not have a default,
failing to pass a value
on the command line
will cause running the program to
print an error and exit.

For programs that have
a large number of options
it may be preferrable to
only use long options.
To suppress short options,
pass ``False`` as the
``short_args`` keyword argument to
the ``begin.start`` decorator::

    >>> import begin
    >>> @begin.start(short_args=False)
    ... def run(name='Arther', quest='Holy Grail', colour='blue', *knights):
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

------------
Sub-Commands
------------

*begins* supports
using functions as
`sub-commands`_ with the
``begin.subcommand()`` decorator::

    >>> import begin
    >>> @begin.subcommand                                    # doctest: +SKIP
    ... def name(answer):
    ...     "What is your name?"
    ...
    >>> @begin.subcommand                                    # doctest: +SKIP
    ... def quest(answer):
    ...     "What is your quest?"
    ...
    >>> @begin.subcommand                                    # doctest: +SKIP
    ... def colour(answer):
    ...     "What is your favourite colour?"
    ...
    >>> @begin.start
    ... def main():
    ...     pass

This example registers
three sub-commands for
the program::

   usage: subcommands.py [-h] {colour,name,quest} ...

   optional arguments:
     -h, --help           show this help message and exit

   Available subcommands:
     {colour,name,quest}
       colour             What is your favourite colour?
       name               What is your name?
       quest              What is your quest?

The main function will
always be called with
the provided command line arguments.
If a sub-command was chosen
the associated function will
also be called.

Sub-commands can be
registered with a
specific named group by
passing a ``group`` argument to
the ``begin.subcommand`` decorator.
The ``begin.start()`` decorator can
use sub-commands from
a named group by
passing it a ``sub_group`` argument.

Similarily, sub-commands can be
load from `entry points`_ by
passing the name
of the entry point
through the ``plugins`` argument
to the ``begin.start()`` decorator::

    >>> import begin
    >>> @begin.start(plugins='begins.plugin.demo')
    ... def main():
    ...     pass

Any functions from
installed packages
that are registered with
the ``begins.plugin.demo`` entry point
will be loaded as sub-commands.

---------------------
Environment Variables
---------------------

Environment variables can
be used to override the
default values for
command line options.
To use environment variables
pass a prefix string to
the ``begin.start()`` decorator through
the ``env_prefix`` paramater::

    >>> import begin
    >>> @begin.start(env_prefix='MP_')
    ... def run(name='Arther', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

In the example above,
if an environment variable
``MP_NAME`` existed,
it's value would be
used as the default for
the ``name`` option.
The options value can
still be set by
explicitly passing a
new value as
a command line option.

-------------------
Configuration files
-------------------

Configuration files can
also be used to
override the default values of
command line options.
To use configuration files
pass a base file name to
the ``begin.start()`` decorator through
the ``config_file`` paramater::

    >>> import begin
    >>> @begin.start(config_file='.camelot.cfg')
    ... def run(name='Arther', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

This example will
look for config files named
``.camelot.cfg`` in
the current directory and/or
the user's home directory.
A command line option's
default value can be
changed by an
option value in
a config file.
The config section
used matches the
decorated function's name
by default.
This can be changed by
passing a ``config_section``
paramater to ``begin.start()``::

    >>> import begin
    >>> @begin.start(config_file='.camelot.cfg', config_section='camelot')
    ... def run(name='Arther', quest='Holy Grail', colour='blue', *knights):
    ...     "tis but a scratch!"

In this second example
the section ``camelot``
will be used instead of
a section named ``run``.

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

    >>> import begin
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

    >>> import begin
    >>> @begin.start
    ... @begin.convert(port=int, debug=begin.utils.tobool)
    ... def main(host='127.0.0.1', port=8080, debug=False):
    ...    "Run web application"

The module ``begin.utils`` contains
useful functions for
converting argument types.

-----------------------
Command Line Extensions
-----------------------

There are behaviours that
are common to many
command line applications,
such as configuring the
``logging`` and
``cgitb`` modules.
*begins* provides
function decorators that
extend a program's
command line arguments to
configure these modules.

* ``begin.tracebacks()``
* ``begin.logging()``

To use these decorators
they need to decorate
the main function
before ``begin.start()``
is applied.

Tracebacks
----------

The ``begin.tracebacks()`` decorator
adds command line options for
extended traceback reports to
be generated for
unhandled exceptions::

   >>> import begin
   >>> @begin.start
   ... @begin.tracebacks
   ... def main(*message):
   ...     pass

The example above will
now have the following
additional argument group::

   tracebacks:
     Extended traceback reports on failure

     --tracebacks   Enable extended traceback reports
     --tbdir TBDIR  Write tracebacks to directory

Passing ``--tracebacks`` will
cause extended traceback reports
to be generated for
unhandled exceptions.

Traceback options may
also be set using
config files,
if `Configuration files`_
are supported.
The follow options
are used.

* ``enabled``: use any of ``true``, ``t``, ``yes``, ``y``, ``on`` or ``1``
  to enable tracebacks.
* ``directory``: write tracebacks to this directory.

Options are expected to
be in a ``tracebacks`` section.

Logging
-------

The ``begin.logging()`` decorator
adds command line options for
configuring the logging module::

   >>> import logging
   >>> import begin
   >>> @begin.start
   ... @begin.logging
   ... def main(*message):
   ...     for msg in message:
   ...         logging.info(msg)

The example above will
now have two additional
optional arguments as well as
an additional argument group::

   optional arguments:
     -h, --help            show this help message and exit
     -v, --verbose         Increse logging output
     -q, --quiet           Decrease logging output

   logging:
     Detailed control of logging output

     --loglvl {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                           Set explicit log level
     --logfile LOGFILE     Ouput log messages to file
     --logfmt LOGFMT       Log message format

The logging level
defaults to ``INFO``.
It can be adjusted
by passing ``--quiet``,
``--verbose`` or
explicity using ``--loglvl``.

The default log format
depends on whether
log output is
being directed to
standard out or file.
The raw log text
is written to
standard out.
The log message written
to file output includes:

* Time
* Log level
* Filename and line number
* Message

The message format can
be overridden using
the ``--logfmt`` option.

Logging options may
also be set using
config files,
if `Configuration files`_
are supported.
The follow options
are used.

* ``level``: log level, must be one of ``DEBUG``, ``INFO``, ``WARNING``,
  ``ERROR`` or ``CRITICAL``.
* ``file``: output log messages to this file.
* ``format``: log message format.

Options are expected to
be in a ``logging`` section.

------------
Entry Points
------------

The `setuptools`_ package supports
`automatic script creation`_ to
automatically create
command line scripts.
These command line scripts
use the `entry points`_ system
from setuptools.

To support the
use of entry points,
functions decorated by
``begin.start()`` have
an instance method called
``start()`` that must be
used to configure the
entry point::

    setup(
        # ...
        entry_points = {
            'console_scripts': [
                'program = package.module:main.start'
            ]
        }

Use of the ``start()`` method is
required because the
main function is not
called from the ``__main__`` module
by the entryp points system.

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
.. _argparse: https://pypi.python.org/pypi/argparse
.. _automatic script creation: http://peak.telecommunity.com/DevCenter/setuptools#automatic-script-creation
.. _issues system: https://github.com/aliles/begins/issues
.. _entry points: http://peak.telecommunity.com/DevCenter/setuptools#dynamic-discovery-of-services-and-plugins
.. _funcsigs: https://pypi.python.org/pypi/funcsigs
.. _function annotations: http://www.python.org/dev/peps/pep-3107/
.. _setuptools: https://pypi.python.org/pypi/setuptools
.. _sub-commands: http://docs.python.org/dev/library/argparse.html#sub-commands

.. |build_status| image:: https://secure.travis-ci.org/aliles/begins.png?branch=master
   :target: https://travis-ci.org/aliles/begins
   :alt: Current build status

.. |coverage| image:: https://coveralls.io/repos/aliles/begins/badge.png?branch=master
   :target: https://coveralls.io/r/aliles/begins?branch=master
   :alt: Latest PyPI version

.. |pypi_version| image:: https://pypip.in/v/begins/badge.png
   :target: https://crate.io/packages/begins/
   :alt: Latest PyPI version
