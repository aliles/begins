import begin
import logging

@begin.subcommand
def hello(name):
    "Say hello"
    logging.info("Hello {0}".format(name))

@begin.subcommand
def goodbye(name):
    "Say goodbye"
    logging.info("Goodbye {0}".format(name))

@begin.start
@begin.logging
def main():
    "Greetings and salutations"
