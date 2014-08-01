import begin
my_formatter = begin.formatters.compose(begin.formatters.RawDescription)

@begin.subcommand
def sub():
    """Such    text
                Very whitespace
            So exact
    """

@begin.start(formatter_class=my_formatter)
def main():
    """Plain text formatting for this help:
    - how does it look?
    Params:
        foo is yummy... 
    """
