from flask import Flask, request
import requests
import config
from utils import append_row, search_by_column
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == config.VERIFY_TOKEN:
        return challenge
    return "Invalid verification token"

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data.get('entry', []):
        for message_event in entry.get('messaging', []):
            sender_id = message_event['sender']['id']
            if 'message' in message_event:
                message_text = message_event['message'].get('text', '')
                handle_message(sender_id, message_text)
    return "ok", 200

def handle_message(sender_id, text):
    if text.lower().startswith("tra cứu"):
        keyword = text[7:].strip()
        results = search_by_column("ThongTinCacDichVu", 0, keyword)
        if results:
            reply = "\n".join([", ".join(row) for row in results])
        else:
            reply = "Không tìm thấy thông tin."
        send_message(sender_id, reply)
    elif text.lower().startswith("thêm"):
        parts = text[4:].split('|')
        if len(parts) >= 2:
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = parts + [sender_id, now]
            append_row("NhapThongTinDichVu", data)
            send_message(sender_id, "Đã lưu thông tin.")
        else:
            send_message(sender_id, "Vui lòng nhập theo định dạng: thêm tên|sdt|dịch vụ")
    else:
        send_message(sender_id, "Chào bạn! Gõ 'tra cứu <sdt>' hoặc 'thêm tên|sdt|dịch vụ'.")

def send_message(recipient_id, message_text):
    params = {
        "access_token": config.PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post("https://graph.facebook.com/v18.0/me/messages", params=params, headers=headers, json=data)

if __name__ == '__main__':
    app.run()
