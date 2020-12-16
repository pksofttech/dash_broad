
from flask import Flask
import os
app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))
print("RUN TEST")
@app.route("/")
def hello():
    return "Hello World!"
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
    
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
run(app, port = service_port);

"""