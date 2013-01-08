"Generate command line parsers from function signatures"
import optparse

try:
    from inspect import signature
except ImportError:
    from begin.funcsigs import signature


def create_parser(func):
    """Create and OptionParser object from a function definition.

    Use the function's signature to generate an OptionParser object. Default
    values are honoured, argument annotations are used as help strings and the
    functions docstring becomes the parser description.
    """
    sig = signature(func)
    option_list = []
    for param in sig.parameters.values():
        if param.kind == param.POSITIONAL_OR_KEYWORD or \
                param.kind == param.KEYWORD_ONLY:
            attrs = {}
            if param.default is not param.empty:
                attrs['default'] = param.default
            if param.annotation is not param.empty:
                attrs['help'] = param.annotation
            option = optparse.make_option('-' + param.name[0],
                    '--' + param.name, **attrs)
            option_list.append(option)
    attrs = {'conflict_handler': 'resolve'}
    if func.__doc__ is not None:
        attrs['description'] = func.__doc__
    return optparse.OptionParser(option_list=option_list, **attrs)
