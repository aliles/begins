from __future__ import print_function
import begin

@begin.subcommand
def name(answer):
    "What is your name?"
    print(answer)

@begin.subcommand
def quest(answer):
    "What is your quest?"
    print(answer)

@begin.subcommand
def colour(answer):
    "What is your favourite colour?"
    print(answer)

@begin.start(cmd_delim='--')
def main():
    pass
