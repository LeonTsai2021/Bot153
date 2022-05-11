from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('rRfClfW1GJ5KPx4ZgfcZwsWDgPPlAoNbqaGLoJy1VBXJjNXBLqLWyYPtCevaJdRctGuFHFUFciM5xHTI0Ssy8KCJFjxf1TX1Pd2tH9rrzaqvnAfOPmnCRi6axiECjQ3Rdqv/6TKv/jRDQqk8sKbFQAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ed1ff2dd179cbfbf6d4c7ad995b40d49')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg=event.message.text
    reply=''
    
    if '你是誰' in msg:
        sticker_message = StickerSendMessage(
            package_id='1070',
            sticker_id='17878'
        )
        
        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return
    
    if msg in ['hi','Hi','嗨']:
        reply='嗨!'
    elif msg == '你在做什麼':
        reply='聊天'
    elif msg == '型號':
        reply='支援型機器人153'
    elif msg == '定位':
        reply='你想定位你目前的位置嗎?'

    else:
        reply='不好意思，你說什麼?'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run()