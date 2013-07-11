import begin
@begin.start
@begin.tracebacks
def main(*message):
    raise Exception(' '.join(message))
