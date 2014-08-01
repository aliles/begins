from flask import Flask
import begin

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@begin.start(auto_convert=True, env_prefix='WEB_')
@begin.logging
def main(host='127.0.0.1', port=8080, debug=False):
    app.run(host=host, port=port, debug=debug)
