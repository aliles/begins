.. begins documentation master file, created by
   sphinx-quickstart on Fri Apr 20 20:27:52 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================
Introducing begins
==================

*Begins* makes creating
command line applications
in Python easy.

    "The beginning is the most important part of the work."

    -- Plato

Its decorator based API
uses your function's call signatures
to generate command line parsers.
Subcommands,
type conversion,
environment variables
and configuration files
are all supported.
Extensions encapsulate
common patterns
for command line configuration
like logging and tracebacks.

The following short example
demonstrates many
of *begins* features
for both Python2 and Python3.

.. code-block:: python

    import begin
    import logging

    @begin.start(auto_convert=True)
    @begin.logging
    def run(host='127.0.0.1', port=8080, noop=False):
        if noop:
            return
        logging.info("%s:%d", host, port)

========
Features
========

* Small API based on function decorators.
* Generates command line options from function signatures.
* Decorate multiple functions to create sub-commands.
* Automatically convert command line arguments to expected types.
* Use environment variables and command line files to set defaults.
* Pre-packaged to extensions to simplify common tasks.

=================
Table of Contents
=================


.. toctree::
   :maxdepth: 1

   tutorial
   guide
   api

======
Issues
======

If you encounter problems,
please refer to :ref:`issues`
from the guide.
