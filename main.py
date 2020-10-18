
from bottle import Bottle, run, template, debug, static_file
from bottle import get, post, request, response

#from bottle.ext.websocket import GeventWebSocketServer
#from bottle.ext.websocket import websocket

import os, sys, socket


app = Bottle(__name__)
debug(False)



@app.route('/')
def index():
    data = {"developer_name":"Ahmedur Rahman Shovon",
            "developer_organization":"Datamate Web Solutions"}
    return (data)



# ! ------------------------------------------------------------------------------------------------------------------------ #

import os
if __name__ == "__main__":
    print(os.name);
    app.run(host='0.0.0.0',port=os.environ['PORT'])