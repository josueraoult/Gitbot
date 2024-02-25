from flask import Flask, request, jsonify
from pymessenger import Bot
import requests
import openai

# Configurez votre token secret pour la vérification
WEBHOOK_VERIFY_TOKEN = 'nakama'

# Configurez votre clé d'API pour pymessenger
ACCESS_TOKEN = 'EAAPPGL8wMRIBO7ZCwR1jMAnEREGrkUymWYYDGCoco2bilnrSlAQsh0ZAFO2DGoZCfZBhwh9nwA9ZCEAgM2SlmXomcP7bZCEgFCAz0NoIhTSxlxYq4Nb2pWQPlq5NYjhRf8xwbr1RYM8hf6t3ehwBZBvg2H4tYQEwQa4ZBve9BpKHjzXdBkbP5ZB9El3PEx57NQiFO'  # Remplacez par votre propre token

# Configurez votre clé d'API pour OpenAI GPT-3.5-turbo
OPENAI_API_KEY = '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'  # Remplacez par votre propre clé

# Initialisez le client pymessenger
bot = Bot(ACCESS_TOKEN)

# Configurez la clé d'API OpenAI
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

#code
@app.route("/", methods=['GET'])
def fbverify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")==WEBHOOK_VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

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
                elif messaging_event.get('message') and messaging_event['message'].get('text'):
                    gestionnaire_messages(messaging_event)
    return "OK", 200

def verify_fb_token(token_sent):
    if token_sent == WEBHOOK_VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return 'Token non valide'

def envoyer_message_texte(sender_id, message):
    bot.send_text_message(sender_id, message)

#open ai 
    def obtenir_reponse_openai(texte_utilisateur):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="You are a helpful assistant.\nUser: " + texte_utilisateur,
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("Une erreur s'est produite lors de la requête OpenAI:", e)
        return "Désolé, je ne peux pas répondre à cela pour le moment."

def repondre_message(sender_id, message_text):
    reponse_openai = obtenir_reponse_openai(message_text)
    envoyer_message_texte(sender_id, reponse_openai)

def gestionnaire_messages(message):
    sender_id = message['sender']['id']
    message_text = message['message']['text']
    repondre_message(sender_id, message_text)

def set_get_started_button():
    url = f'https://graph.facebook.com/v12.0/me/messenger_profile?access_token={ACCESS_TOKEN}'
    payload = {
        "get_started": {
            "payload": "GET_STARTED_PAYLOAD"
        }
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

def send_welcome_messages(user_id):
    envoyer_message_texte(user_id, "Bienvenue, je suis Speed 🤨.")
    envoyer_message_texte(user_id, "Veuillez entrer votre question 😉.")

# Utilisez cette fonction pour définir le bouton "Get Started"
set_get_started_button()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
