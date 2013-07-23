import begin

@begin.subcommand
def name(answer):
    "What is your name?"

@begin.subcommand
def quest(answer):
    "What is your quest?"

@begin.subcommand
def colour(answer):
    "What is your favourite colour?"

@begin.start
def main():
    pass
