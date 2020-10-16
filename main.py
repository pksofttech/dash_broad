
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


def get_host_IP():
    try: 
        host_name = socket.gethostname();
        print(host_name);
        host_ip = socket.gethostbyname(host_name);
        return(host_ip);
    except: 
        return("Error");

def get_local_ip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.0.0.8', 1027))
    except socket.error:
        return("Error");
    return s.getsockname()[0]

def ftp_load_img(path) :
    global dirname;
    _path, _imag = os.path.split(path);
    #print(_path);
    _port = _path.split(":")[2].split("/")[0];
    _host = _path.split(":"+ _port)[0];
    _dir   = _path.split(":"+ _port)[1];
    print(_host);
    print(_port);
    print(_dir);
    print(_imag);
    ftp = FTP();
    ftp.connect(_host.split("//")[1], int(_port));
    ftp.login();
    ftp.cwd(_dir)
    #ftp.dir();  
    _path_imge_temp = dirname+ "/imge/"+ _imag;
    with open(_path_imge_temp, 'wb') as f:
        ftp.retrbinary('RETR ' + _imag, f.write)
    
    #ftpResponse = ftp.delete("_imag");

    #print(ftpResponse);
    ftp.close();
    img = cv2.imread(_path_imge_temp,cv2.IMREAD_COLOR)
    cv2.imshow('car',img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    os.remove(_path_imge_temp);
@app.route('/')
def index():
    data = {"developer_name":"Ahmedur Rahman Shovon",
            "developer_organization":"Datamate Web Solutions"}
    return template('index', data = data)

# ! ------------------------------------------------------------------------------------------------------------------------ #

host_ip = get_host_IP();
if(host_ip != "Error") :
    run(app, host = host_ip, port = service_port);
else :
    print("Error Not IP on Device");

