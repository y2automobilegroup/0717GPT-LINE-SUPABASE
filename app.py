
from flask import Flask, request
from linebot.v3.webhook import WebhookHandler
from modules.gpt_logic import process_message
from modules.supabase_client import query_supabase
from modules.utils import is_human_mode, save_message, switch_mode
import os

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.get_json()
    user_id = body['events'][0]['source']['userId']
    message_text = body['events'][0]['message']['text']

    if message_text == "人工客服您好":
        switch_mode(user_id, True)
        return "OK"
    elif message_text == "人工客服結束":
        switch_mode(user_id, False)
        return "OK"

    if is_human_mode(user_id):
        save_message(user_id, message_text)
        return "OK"

    gpt_query = process_message(message_text)
    result = query_supabase(gpt_query)

    reply_text = result if result else "亞鈺汽車AI智能客服您好，感謝您的詢問，目前您的問題需要專人回覆您，請稍後馬上有人為您服務！😄"

    from linebot.v3.messaging import MessagingApi, ReplyMessageRequest, TextMessage
    line_bot_api = MessagingApi(channel_access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
    reply_token = body['events'][0]['replyToken']
    line_bot_api.reply_message(ReplyMessageRequest(reply_token, [TextMessage(text=reply_text)]))

    return "OK"
