
# coding: utf-8

import json
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from linebot.exceptions import LineBotApiError
import requests
import Twitter

app = Flask(__name__)

line_bot_api = LineBotApi('yourKey')
handler = WebhookHandler('yourKey')

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userText = request.json["events"][0]["message"]["text"]
    twitterMessage = Twitter.twitterGetMessage(userText)
    line_bot_api.push_message('yourBotId', TextSendMessage(text=twitterMessage))

if __name__ == "__main__":
    app.run()
