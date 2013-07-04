Roadmap for Begins
==================

This is a rough roadmap for the first beta release of *begins*.

0.3
---
* Environment variable parsing require explicit enabling by passing
  ``env_prefix`` argument to ``begin.start()``.
* Use *argparse* module over *optparse* internally for command line parsing.
* Remove vendored *funcsigs* package from *begin* package.
* Add external *argparse* dependency for Python 2.6.
* Add external *funcsigs* dependency for Python 2.6, 2.7 and 3.2.

0.4
---
* Add optional boilerplate decorators:
   * ``begin.logging()`` to configure *logging* module.
   * ``begin.traceback()`` to configure *cgitb* moudle.
* Support optional configuration file to read option values from.

0.5
---
* Support sub commands using a sub command deocorate:
   * ``begin.subcommand()`` registers function with default collector.
   * ``begin.start()`` checks default collector for registered sub commands.
   * Additonal collectors may be defined explicitly.

0.6
---
* User manual hosted on `Read the Docs <https://begins.readthedocs.org>`_.
* First beta release.
