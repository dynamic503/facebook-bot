# app.py
from flask import Flask, request
import requests

app = Flask(__name__)

VERIFY_TOKEN = "your_verify_token"
PAGE_ACCESS_TOKEN = "your_page_access_token"

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification token mismatch"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data['entry']:
        for messaging in entry['messaging']:
            sender = messaging['sender']['id']
            if messaging.get('message'):
                text = messaging['message'].get('text')
                reply(sender, f"Bạn đã gửi: {text}")
    return "OK"

def reply(recipient_id, text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    headers = {'Content-Type': 'application/json'}
    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    app.run()
