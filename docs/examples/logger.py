import logging
import begin
@begin.start
@begin.logging
def main(*message):
    for msg in message:
        logging.info(msg)
