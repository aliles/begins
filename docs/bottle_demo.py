from bottle import route, run
import begin

@route('/hello')
def hello():
    return "Hello World!"

@begin.start
@begin.convert(port=int, debug=begin.utils.tobool)
def main(host='127.0.0.1', port=8080, debug=False):
    run(host=host, port=port, debug=debug)
