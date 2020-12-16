from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)
from pprint import pprint 
import json 
app = Flask(__name__)

# ? หมายเหตุ: LineBotApi(ใส่ Channel Access Token ของตัวเองนะ) และ WebhookHandler(ใส่ Channel Secret ของตัวเองนะ) ดูข้อมูลได้ที่หน้า LINE Developer นะ

line_bot_api = LineBotApi('ljuJWWhDu8nCahD0zsoqtPWV9GpZSKX45HVqNGmaZ47Pr/wjDWAFTdXmyd6nB+4bqCnXt+oJTeXJJv1G+FcigupmkMnmOKN4xYbLHCrbCdTr2UbECunPIBqafSQrUuPiqaVJW+uwYFAMHiiA8sIOVAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1cfcfb0f93bcf292a4c46579fd087e52')

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="ทดสอบข้อความตอบกลับ .. {}".format(event.message.text)))


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/webhook", methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    res = json.loads(body)
    app.logger.info("Request body: " + body)
    print(signature)
    pprint(res)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        print(e);
        abort(400)

    return 'OK'
    

import os
if __name__ == "__main__":
    print(os.name);
    #app.run(host='0.0.0.0',port=os.environ['PORT'])
    app.run(host='0.0.0.0',port=8000)