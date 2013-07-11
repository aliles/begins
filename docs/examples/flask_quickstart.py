from flask import Flask
import begin

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@begin.start(env_prefix='WEB_')
@begin.convert(port=int, debug=begin.utils.tobool)
def main(host='127.0.0.1', port=8080, debug=False):
    app.run(host=host, port=port, debug=debug)
