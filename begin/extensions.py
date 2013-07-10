"Command line extension plugins"


class Extension(object):
    "Base class of all command line extensions"

    def __init__(self, func):
        self.__wrapped__ = func

    def __call__(self, *args, **kwargs):
        return self.__wrapped__(*args, **kwargs)

    @property
    def __annotations__(self):
        return self.__wrapped__.__annotations__

    @property
    def __doc__(self):
        return self.__wrapped__.__doc__

    @property
    def __module__(self):
        return self.__wrapped__.__module__

    @property
    def __name__(self):
        return self.__wrapped__.__name__

    def add_arguments(self, parser):
        raise NotImplementedError("Command line extension incomplete")

    def run(self, opts):
        raise NotImplementedError("Command line extension incomplete")
