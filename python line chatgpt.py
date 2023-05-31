from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   
import json
import functions_framework
import requests
import openai
@functions_framework.http
def linebot(request):
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi('Channel access token')
        handler = WebhookHandler('Channel secret')
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        ai_msg = msg
        reply_msg = ''
        if ai_msg :
            openai.api_key = 'open ai api key'
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg,
                max_tokens=2000,
                temperature=0.5,
                )
            reply_msg = response["choices"][0]["text"].replace('\n','')
        text_message = TextSendMessage(text=reply_msg)          # 設定回傳同樣的訊息
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息
    except:
        print('error')
    return 'OK'