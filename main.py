
from sys import intern
from bottle import Bottle, run, template, debug, static_file
from bottle import get, post, request, response

#from bottle.ext.websocket import GeventWebSocketServer
#from bottle.ext.websocket import websocket

import os, sys, socket
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

#line_bot_api = LineBotApi('43398846c9d56769235d6876bb879bba')
#handler = WebhookHandler('1653361761')
line_bot_api = LineBotApi('43398846c9d56769235d6876bb879bba')

app = Bottle(__name__)
debug(False)

from pprint import pprint


@app.route('/')
def index():
    data = {"developer_name":"Ahmedur Rahman Shovon",
            "developer_organization":"Datamate Web Solutions"}
    return (data)

@app.post('/')
def index():

    print("-------------------------------------------------- POST INDEX ---------------------------------------------------------------");
    try :
        _data = unquote(request.body.read().decode('utf-8'));
        #_data = json.load(_data);
        pprint(_data,indent=2);
        rey_tk = _data["events"]["replyToken"]
        line_bot_api.reply_message(rey_tk, TextSendMessage(text='Hello World!'))
    except Exception as identifier:
        print("post Error : " + str(identifier));
    
    print("------------------------------------------------------------------------------------------------------------------------\n");
    

    return("POST OK")

@app.post('/<post>')
def index(post):
    print("-------------------------------------------------- POST ---------------------------------------------------------------");
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> POST " + post);
    try :
        _data = unquote(request.body.read().decode('utf-8'));
        #_data = json.load(_data);
        print(_data);
    except Exception as identifier:
        print("post Error : " + str(identifier));
    
    
    print("------------------------------------------------------------------------------------------------------------------------\n");



# ! ------------------------------------------------------------------------------------------------------------------------ #

import os
if __name__ == "__main__":
    print(os.name);
    app.run(host='0.0.0.0',port=os.environ['PORT'])