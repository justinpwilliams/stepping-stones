from werkzeug.wrappers import Request, Response
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello world!"


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    run_simple('localhost', 9000, app)
