"""
from flask import Flask
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World!"
if __name__ == "__main__":
    app.run()
"""

from bottle import Bottle, run, template, debug, static_file
from bottle import get, post, request, response


service_port    = 5000;

app = Bottle()
debug(False)


@app.route('/')
def index():
    return ("OK")



# ! ------------------------------------------------------------------------------------------------------------------------ #
run(app);

