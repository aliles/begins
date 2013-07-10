"Generate command line parsers and apply options using function signatures"
import argparse
import os
import sys

try:
    from inspect import signature
except ImportError:
    from funcsigs import signature


NODEFAULT = object()


class CommandLineError(ValueError):
    """Error in command line processing"""


def create_parser(func, env_prefix=None):
    """Create and OptionParser object from a function definition.

    Use the function's signature to generate an OptionParser object. Default
    values are honoured, argument annotations are used as help strings and the
    functions docstring becomes the parser description. Environment variables
    can alter the default values of options. Variable positional arguments are
    ingored but will alter the program's usage string. Variable keyword
    arguments will raise a ValueError exception. A prefix on expected
    environment variables can be added using the env_prefix argument.
    """
    while hasattr(func, '__wrapped__'):
        func = getattr(func, '__wrapped__')
    sig = signature(func)
    if len(sig.parameters) == 0:
        return None
    meta_prefix = '' if env_prefix is None else env_prefix
    parser = argparse.ArgumentParser(
            argument_default=NODEFAULT,
            conflict_handler='resolve',
            description = func.__doc__
    )
    for param in sig.parameters.values():
        if param.kind == param.POSITIONAL_OR_KEYWORD or \
                param.kind == param.KEYWORD_ONLY or \
                param.kind == param.POSITIONAL_ONLY:
            metavar = (meta_prefix + param.name).upper()
            args = {
                    'default': NODEFAULT,
                    'metavar': metavar,
            }
            if param.annotation is not param.empty:
                args['help'] = param.annotation
            if param.default is not param.empty:
                args['default'] = param.default
                if 'help' not in args:
                    args['help'] = '(default: %(default)s)'
                else:
                    args['help'] += ' (default: %(default)s)'
            if env_prefix is not None:
                args['default'] = os.environ.get(metavar, args['default'])
            if args['default'] is NODEFAULT:
                args['required'] = True
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


def apply_options(func, opts):
    """Apply and call function using command line options and arguments.

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
    sig = signature(func)
    pargs = []
    kwargs = {}
    for param in sig.parameters.values():
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
