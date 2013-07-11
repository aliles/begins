"Command line extension plugins"
import cgitb


class Extension(object):
    """Base class of all command line extensions

    Extension are required to subclass this class and override the
    add_arguments() and run() methods.
    """

    OVERRIDDEN = ('__annotations__', '__doc__', '__module__', '__name__')

    def __init__(self, func):
        self.__wrapped__ = func
        for name in self.OVERRIDDEN:
            setattr(self, name, getattr(func, name, None))

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    def add_arguments(self, parser):
        "Add command line arguments to parser"
        raise NotImplementedError("Command line extension incomplete")

    def run(self, opts):
        "run extension using command line options"
        raise NotImplementedError("Command line extension incomplete")


class Tracebacks(Extension):
    "Manage command line extension for cgitb module"

    def add_arguments(self, parser):
        "Add command line arguments for configuring traceback module"
        group = parser.add_argument_group('tracebacks',
                'Extended traceback reports on failure')
        group.add_argument('--tracebacks', default=False, action='store_true',
                help='Enable extended traceback reports')
        group.add_argument('--tbdir', default=None,
                help='Write tracebacks to directory')

    def run(self, opts):
        "Configure cgitb module if enabled on command line"
        if not opts.tracebacks:
            return
        cgitb.enable(logdir=opts.tbdir, format='txt')


def tracebacks(func):
    "Add command line extension for cgitb module"
    return Tracebacks(func)
