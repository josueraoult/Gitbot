from flask import Flask, request
import requests
from googletrans import Translator

app = Flask(__bot__)

PAGE_ACCESS_TOKEN = "EAAJ3opZCZBh4MBO4PQgzmxYllgslFvVXYsZApczTQWnfYAZCUXpAF1HZBiw7dZAovZBBCvAx9wCZB5J8AFq9Xtx2xCM4j2sQULYRFbUnt5Wdt9wbB6ajVA0SWs1y0sgtdE84L9tsMxv7WOmS2WoRTab4pSZBUgWSDv1hwg42BTfwLQsfbxGlmIZBwe6tPjN0R6FPqe"
VERIFY_TOKEN = "2c361288a69c0c40ef760e2c4aa007f4"

translator = Translator()

def send_message(recipient_id, message):
    params = {
        "access_token": PAGE_ACCESS_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    response = requests.post("https://graph.facebook.com/v13.0/me/messages", params=params, headers=headers, json=data)
    if response.status_code != 200:
        print("Unable to send message: " + response.text)

def translate_message(message, target_language):
    translated_message = translator.translate(message, dest=target_language).text
    return translated_message

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('message'):
                    sender_id = messaging_event['sender']['id']
                    message_text = messaging_event['message']['text']
                    translated_message = translate_message(message_text, 'fr')  # Change 'fr' to target language code
                    send_message(sender_id, translated_message)
    return "ok", 200

if __name__ == '__main__':
    app.run(debug=True)
