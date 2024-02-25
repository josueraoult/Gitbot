from flask import Flask, request, jsonify
from pymessenger import Bot
import requests
import http.client

# Configurez votre token secret pour la vérification
WEBHOOK_VERIFY_TOKEN = 'nakama'

# Configurez votre clé d'API pour pymessenger
ACCESS_TOKEN = 'EAAPPGL8wMRIBOx3b6igx3apEa6EDOXsqGzGN7mgDkQDOE8ZAZBBbSCVqAAzyTVJZAEZBYOCWYjaQvSJ0s3WGfMIOnqEUclrQEz6CjvwBHAhzyXlZABZANq4fSZBeYTS91AZASmJZA5cBYCRXQeBTf0xZCmBfstIbrHXh2J5AHZCVZCZBkOI4vP00DcnL8AtSUMAkHyJ8p'  # Remplacez par votre propre token

app = Flask(__name__)

# Endpoint pour vérifier le token lors de la configuration du webhook
@app.route("/", methods=['GET'])
def fbverify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == WEBHOOK_VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

# Endpoint pour recevoir les messages du webhook de Messenger
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                if messaging_event.get('postback'):
                    # Si l'utilisateur clique sur "Get Started"
                    if messaging_event['postback']['payload'] == 'GET_STARTED_PAYLOAD':
                        sender_id = messaging_event['sender']['id']
                        send_welcome_messages(sender_id)
                elif messaging_event.get('message') and messaging_event['message'].get('text'):
                    gestionnaire_messages(messaging_event)
    return "OK", 200

def verify_fb_token(token_sent):
    if token_sent == WEBHOOK_VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return 'Token non valide'

def envoyer_message_texte(sender_id, message):
    bot = Bot(ACCESS_TOKEN)
    bot.send_text_message(sender_id, message)

def call_api(text, user_id):
    conn = http.client.HTTPSConnection("aeona3.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': "0aec34de62msh666934268b29f7cp1a34e7jsnc7771e789c31",
        'X-RapidAPI-Host': "aeona3.p.rapidapi.com"
    }
    query_params = f"/?text={text}&userId={user_id}"
    conn.request("GET", query_params, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

# Endpoint pour appeler l'API
@app.route('/call_api', methods=['GET'])
def api_endpoint():
    text = request.args.get('text')
    user_id = request.args.get('userId')
    response = call_api(text, user_id)
    return response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
