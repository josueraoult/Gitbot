from flask import Flask, request, jsonify
from pymessenger import Bot
import requests
import openai
import os

# Configurez votre token secret pour la vérification
WEBHOOK_VERIFY_TOKEN = 'mywebhook'

# Configurez votre clé d'API pour pymessenger
ACCESS_TOKEN = 'EAAPPGL8wMRIBOwn8T9Gdjnuvko6sETi7iPfZB8Oq3Ldh1xaFdET4XwWpYgT6kySjPmXogLlOe8aN5qqfcr0QfLgJzZC4hZA8qvovYpRZAehZCEKXya0qhqLlxyUZC2siGtIGimZCvE9rKm559m42SOdr2gnror449RNoftS2jnUsaoKafZCTHNIC8ZAg1xyXBw8ZAf'  # Remplacez par votre propre token

# Configurez votre clé d'API pour OpenAI GPT-3.5-turbo
OPENAI_API_KEY = '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'  # Remplacez par votre propre clé

# Initialisez le client pymessenger
bot = Bot(ACCESS_TOKEN)

# Configurez la clé d'API OpenAI
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Endpoint pour vérifier le token lors de la configuration du webhook
@app.route('/', methods=['GET'])
def verify_token():
    token_sent = request.args.get("hub.verify_token")
    return verify_fb_token(token_sent)

# Endpoint principal pour recevoir les messages du webhook de Messenger
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
                elif messaging_event.get('message'):
                    gestionnaire_messages(messaging_event)
    return "OK", 200
  
def verify_fb_token(token_sent):
    if token_sent == WEBHOOK_VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return 'Token non valide'

def envoyer_message_texte(sender_id, message):
    bot.send_text_message(sender_id, message)

def obtenir_reponse_openai(texte_utilisateur):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": texte_utilisateur},
        ]
                    )
    
