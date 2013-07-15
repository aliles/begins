"Command line extension plugins"
import cgitb
import logging
import logging.handlers
import platform
import sys


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
        group.add_argument('--tracebacks',
                default=False, action='store_true',
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


class Logging(Extension):
    "Manage command line extension for the logging module"

    def add_arguments(self, parser):
        "Add command line arguments for configuring the logging module"
        exclusive  = parser.add_mutually_exclusive_group()
        exclusive.add_argument('-v', '--verbose',
                default=False, action='store_true',
                help='Increse logging output')
        exclusive.add_argument('-q', '--quiet',
                default=False, action='store_true',
                help='Decrease logging output')
        group = parser.add_argument_group('logging',
                'Detailed control of logging output')
        group.add_argument('--loglvl', default=None,
                choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                help='Set explicit log level')
        group.add_argument('--logfile', default=None,
                help='Ouput log messages to file')
        group.add_argument('--logfmt', default=None,
                help='Log message format')

    def run(self, opts):
        "Configure logging module according to command line options"
        # log level
        level = 'INFO'
        if opts.loglvl is not None:
            level = opts.loglvl
        elif opts.verbose:
            level = 'DEBUG'
        elif opts.quiet:
            level = 'WARNING'
        # logger
        logger = logging.getLogger()
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.setLevel(level)
        # handler
        if opts.logfile is None:
            handler = logging.StreamHandler(sys.stdout)
        elif platform.system() != 'Windows':
            handler = logging.handlers.WatchedFileHandler(opts.logfile)
        else:
            handler = logging.FileHandler(opts.logfile)
        logger.addHandler(handler)
        # formatter
        fmt = opts.logfmt
        if fmt is None:
            if opts.logfile is None:
                fmt = '%(message)s'
            else:
                fmt = '[%(asctime)s] [%(levelname)s] [%(pathname)s:%(lineno)s] %(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)


def logger(func):
    "Add command line extension for logging module"
    return Logging(func)
