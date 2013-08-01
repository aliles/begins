"Generate command line parsers and apply options using function signatures"
import argparse
import os
import sys

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

try:
    from inspect import signature
except ImportError:
    from funcsigs import signature

from begin import extensions
from begin import subcommands

__all__ = ['create_parser', 'populate_parser',
           'apply_options', 'call_function']


NODEFAULT = object()


class CommandLineError(ValueError):
    """Error in command line processing"""


class DefaultsManager(object):
    """Manage default values for command line options

    Inspects environment variables and default argument values to determine the
    correct default for command line option.
    """

    def __init__(self, env_prefix=None, config_file=None, config_section=None):
        self._use_env = env_prefix is not None
        self._prefix = '' if not self._use_env else env_prefix
        self._parser = configparser.ConfigParser()
        self._section = config_section
        if config_file is not None:
            self._parser.read([config_file,
                os.path.join(os.path.expanduser('~'), config_file)])

    def metavar(self, name):
        "Generate meta variable name for parameter"
        metavar = (self._prefix + name).upper()
        return metavar

    def from_param(self, param, default=NODEFAULT):
        "Get default value from signature paramater"
        if param.default is not param.empty:
            default = param.default
        default = self.from_name(param.name, default)
        return default

    def from_name(self, name, default=NODEFAULT, section=None):
        "Get default value from argument name"
        if len(self._parser.sections()) > 0:
            section = self._section if section is None else section
            try:
                default = self._parser.get(section, name)
            except (configparser.NoSectionError, configparser.NoOptionError):
                pass
        if self._use_env:
            default = os.environ.get(self.metavar(name), default)
        return default

    def set_config_section(self, section):
        self._section = section


def populate_parser(parser, defaults, funcsig):
    """Populate parser according to function signature

    Use the parameters accepted by the source function, according to the
    functions signature provided, to populating a corresponding command line
    argument parser.
    """
    for param in funcsig.parameters.values():
        if param.kind == param.POSITIONAL_OR_KEYWORD or \
                param.kind == param.KEYWORD_ONLY or \
                param.kind == param.POSITIONAL_ONLY:
            args = {
                    'default': defaults.from_param(param),
                    'metavar': defaults.metavar(param.name),
            }
            if param.annotation is not param.empty:
                args['help'] = param.annotation
            if args['default'] is NODEFAULT:
                args['required'] = True
            else:
                if 'help' not in args:
                    args['help'] = '(default: %(default)s)'
                else:
                    args['help'] += ' (default: %(default)s)'
            parser.add_argument('-' + param.name[0],
                    '--' + param.name, **args)
        elif param.kind == param.VAR_POSITIONAL:
            args = {'nargs': '*'}
            if param.annotation is not param.empty:
                args['help'] = param.annotation
            parser.add_argument(param.name, **args)
        elif param.kind == param.VAR_KEYWORD:
            msg = 'Variable length keyword arguments not supported'
            raise ValueError(msg)
    return parser


def create_parser(func, env_prefix=None, config_file=None, config_section=None,
        sub_group=None, plugins=None, collector=None):
    """Create and OptionParser object from a function definition.

    Use the function's signature to generate an OptionParser object. Default
    values are honoured, argument annotations are used as help strings and the
    functions docstring becomes the parser description. Environment variables
    can alter the default values of options. Variable positional arguments are
    ingored but will alter the program's usage string. Variable keyword
    arguments will raise a ValueError exception. A prefix on expected
    environment variables can be added using the env_prefix argument.
    """
    defaults = DefaultsManager(env_prefix, config_file, func.__name__)
    parser = argparse.ArgumentParser(
            argument_default=NODEFAULT,
            conflict_handler='resolve',
            description = func.__doc__
    )
    collector = collector if collector is not None else subcommands.COLLECTORS[sub_group]
    if plugins is not None:
        collector.load_plugins(plugins)
    if len(collector) > 0:
        subparsers = parser.add_subparsers(title='Available subcommands',
                dest='_subcommand')
        for subfunc in collector.commands():
            funcsig  = signature(subfunc)
            subparser = subparsers.add_parser(subfunc.__name__,
                    conflict_handler='resolve', help=subfunc.__doc__)
            defaults.set_config_section(subfunc.__name__)
            populate_parser(subparser, defaults, funcsig)
    have_extensions = False
    while hasattr(func, '__wrapped__') and not hasattr(func, '__signature__'):
        if isinstance(func, extensions.Extension):
            func.add_arguments(parser, defaults)
            have_extensions = True
        func = getattr(func, '__wrapped__')
    funcsig = signature(func)
    if len(funcsig.parameters) == 0 and len(collector) == 0 and not have_extensions:
        return None
    populate_parser(parser, defaults, funcsig)
    return parser


def call_function(func, funcsig, opts):
    """Call function using command line options and arguments

    Use the function's signature to extract expected values from the provided
    command line options. The extracted values are used to call the funciton.
    The presence of variable keyword arguments, missing attributes from the
    options object or to failure to use the command line arguments list will
    result in a CommandLineError being raised.
    """
    def getoption(opts, name, default=None):
        if not hasattr(opts, name):
            msg = "Missing command line options '{0}'".format(name)
            raise CommandLineError(msg)
        value = getattr(opts, name)
        if value is NODEFAULT:
            if default is None:
                msg = "'{0}' is a required option{1}".format(name, os.linesep)
                sys.stderr.write(msg)
                sys.exit(1)
            else:
                value = default
        return value
    pargs = []
    kwargs = {}
    for param in funcsig.parameters.values():
        if param.kind == param.POSITIONAL_OR_KEYWORD or \
                param.kind == param.POSITIONAL_ONLY:
            pargs.append(getoption(opts, param.name))
        elif param.kind == param.VAR_POSITIONAL:
            pargs.extend(getoption(opts, param.name, []))
        elif param.kind == param.KEYWORD_ONLY:
            kwargs[param.name] = getoption(opts, param.name)
        elif param.kind == param.VAR_KEYWORD:
            msg = 'Variable length keyword arguments not supported'
            raise CommandLineError(msg)
    return func(*pargs, **kwargs)


def apply_options(func, opts, sub_group=None, collector=None):
    """Apply command line options to function and subcommands

    Call the target function, and any chosen subcommands, using the parsed
    command line arguments.
    """
    ext = func
    collector = collector if collector is not None else subcommands.COLLECTORS[sub_group]
    while hasattr(ext, '__wrapped__') and not hasattr(ext, '__signature__'):
        if isinstance(ext, extensions.Extension):
            ext.run(opts)
        ext = getattr(ext, '__wrapped__')
    result = call_function(func, signature(ext), opts)
    if hasattr(opts, '_subcommand'):
        subfunc = collector.get(opts._subcommand)
        result = call_function(subfunc, signature(subfunc), opts)
    return result
