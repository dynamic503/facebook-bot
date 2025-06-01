from flask import Flask, request
import requests
from config import VERIFY_TOKEN, PAGE_ACCESS_TOKEN

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # Xác minh webhook từ Facebook
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Verification token mismatch", 403

@app.route('/', methods=['POST'])
def webhook():
    # Xử lý tin nhắn gửi đến
    data = request.get_json()
    
    if data.get('object') == 'page':
        for entry in data.get('entry', []):
            for messaging in entry.get('messaging', []):
                sender_id = messaging['sender']['id']
                if messaging.get('message') and 'text' in messaging['message']:
                    message_text = messaging['message']['text']
                    reply(sender_id, f"Bạn đã gửi: {message_text}")
    return "OK", 200

def reply(recipient_id, message_text):
    # Gửi tin nhắn trả lời lại người dùng
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    print("Response:", response.status_code, response.text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
