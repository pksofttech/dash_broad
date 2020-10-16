
from bottle import Bottle, run, template, debug, static_file
from bottle import get, post, request, response

from bottle.ext.websocket import GeventWebSocketServer
from bottle.ext.websocket import websocket

import os, sys, socket

import json
import imutils
import numpy as np

from ftplib import FTP

try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

dirname = os.path.dirname(sys.argv[0])
service_port    = 80;

app = Bottle()
debug(False)


@app.route('/')
def index():
    data = {"developer_name":"Ahmedur Rahman Shovon",
            "developer_organization":"Datamate Web Solutions"}
    return template('index', data = data)

# ! ------------------------------------------------------------------------------------------------------------------------ #

run(app);
