"Generate command line parsers and apply options using function signatures"
import optparse
import os
import sys

try:
    from inspect import signature
except ImportError:
    from begin.funcsigs import signature


NODEFAULT = object()


class CommandLineError(ValueError):
    """Error in command line processing"""


def create_parser(func, env_prefix=''):
    """Create and OptionParser object from a function definition.

    Use the function's signature to generate an OptionParser object. Default
    values are honoured, argument annotations are used as help strings and the
    functions docstring becomes the parser description. Environment variables
    can alter the default values of options. Variable positional arguments are
    ingored but will alter the program's usage string. Variable keyword
    arguments will raise a ValueError exception. A prefix on expected
    environment variables can be added using the env_prefix argument.
    """
    sig = getattr(func, '__signature__', signature(func))
    option_list = []
    attrs = {'conflict_handler': 'resolve'}
    for param in sig.parameters.values():
        if param.kind == param.POSITIONAL_OR_KEYWORD or \
                param.kind == param.KEYWORD_ONLY or \
                param.kind == param.POSITIONAL_ONLY:
            metavar = (env_prefix + param.name).upper()
            args = {
                    'default': os.environ.get(metavar, NODEFAULT),
                    'metavar': metavar
            }
            if param.default is not param.empty:
                args['default'] = param.default
            if param.annotation is not param.empty:
                args['help'] = param.annotation + ' [default: %default]'
            elif args['default'] is not NODEFAULT:
                args['help'] = '[default: %default]'
            option = optparse.make_option('-' + param.name[0],
                    '--' + param.name, **args)
            option_list.append(option)
        elif param.kind == param.VAR_POSITIONAL:
            attrs['usage'] = "%prog [{0}]".format(param.name)
        elif param.kind == param.VAR_KEYWORD:
            msg = 'Variable length keyword arguments not supported'
            raise ValueError(msg)
    if func.__doc__ is not None:
        attrs['description'] = func.__doc__
    return optparse.OptionParser(option_list=option_list, **attrs)


def apply_options(func, opts, args):
    """Apply and call function using command line options and arguments.

    Use the function's signature to extract expected values from the provided
    command line options. The extracted values are used to call the funciton.
    The presence of variable keyword arguments, missing attributes from the
    options object or to failure to use the command line arguments list will
    result in a CommandLineError being raised.
    """
    def getoption(opts, name):
        if not hasattr(opts, name):
            msg = "Missing command line options '{0}'".format(name)
            raise CommandLineError(msg)
        value = getattr(opts, name)
        if value is NODEFAULT:
            msg = "'{0}' is a required option{1}".format(name, os.linesep)
            sys.stderr.write(msg)
            sys.exit(1)
        return value
    sig = signature(func)
    pargs = []
    kwargs = {}
    for param in sig.parameters.values():
        if param.kind == param.POSITIONAL_OR_KEYWORD or \
                param.kind == param.POSITIONAL_ONLY:
            pargs.append(getoption(opts, param.name))
        elif param.kind == param.VAR_POSITIONAL:
            pargs.extend(args)
            args = []
        elif param.kind == param.KEYWORD_ONLY:
            kwargs[param.name] = getoption(opts, param.nmae)
        elif param.kind == param.VAR_KEYWORD:
            msg = 'Variable length keyword arguments not supported'
            raise CommandLineError(msg)
    if len(args) > 0:
        raise CommandLineError('Unused positional arguments')
    return func(*pargs, **kwargs)
