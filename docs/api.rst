==============
The begins API
==============

.. module:: begin
    :noindex:

The :mod:`begin` module provides the bulk of *begins* decorator API.

.. decorator:: start(auto_convert=False, cmd_delim=None, short_args=True, lexical_order=False, env_prefix=None, config_file=None, config_section=None, sub_group=None, collector=None)

   Annotates the decorated function as the programs main function. If the
   module is run, the function will be automatically called after processing
   options from the command line.

   If *auto_convert* is ``True`` the decorated function will also be decorated
   by :func:`begin.convert` with automatic type conversion enabled.

   If *cmd_delim* is provided, it will be used as a separator on the command
   line between multiple sub-commands that are to be called in sequence.

   If *short_args* is ``False`` (default is ``True``) the use of short, single
   character options on the command line is suppressed.

   If *lexical_order* is ``True`` (default is ``False``) command line options
   in help output will be in alphabetical order rather than the order in which
   they appear in the function signature.

   If *env_prefix* is provided, the use of environment variables for changing
   the default value of command line options is enabled. The value of
   *env_prefix* is used as a prefix in front of environment variables. An empty
   string my be provided to indicate no prefix but still enable the use of
   environment variables.

   If *config_file* is provided, it's the name of a file in the current and
   user's home directory from which configuration options will be loaded to
   change the default values of command line options.

   If *config_section* is provided it overrides the decorated function name as
   the configuration file section from which to load command line option
   defaults.

   The *sub_group* changes the collector name used to load sub-commands from.
   The *sub_group* name must match the *group* name provdided to the
   :func:`begin.subcommand` decorator.

   The *collector* allows a :class:`begin.subcommand.Collector` of sub-commands
   to be provided instead of a named collector.

Sub-commands
============

.. decorator:: subcommand(name=None, group=None, collector=None)

   TODO

TODO

Type conversion
===============

.. decorator:: convert(**kwargs)

   TODO

.. module:: begin.utils
