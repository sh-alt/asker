from flask import Flask, request # Импортируем модули
import askeradmin_bot.config as config
import json
import requests
import telegram
from telegram.update import Update



app = Flask(__name__) # Создаем приложение

bot = telegram.Bot(token=config.token)


@app.route("/") # Говорим Flask, что за этот адрес отвечает эта функция
def hello_world():
    return "It's working"

def get_url(method):
    return "https://api.telegram.org/bot{}/{}".format(config.token, method)


@app.route("/setwebhook")
def set_webhook():
    body = {'url': f'https://{config.ip}'}
    files = {'certificate': (f'{config.sert_pem}', open(f'/etc/ssl/telegram/{config.sert_pem}', 'r'), 'multipart/form-data')}
    r = requests.post(get_url('setwebhook'), body, files=files)
    r = requests.get(get_url("getWebHookInfo"))
    response = str(r.json())
    return response


@app.route("/getwebhook")
def get_webhook():
    r = requests.get(get_url("getWebhookInfo"))
    response = str(r.json())
    return response

@app.route("/", methods=['POST'])
def incoming_message():
    update_json = request.get_json()
    update_obj = Update.de_json(update_json, bot)
    update_processor(update_obj)
    with open('update', 'w') as file:
        file.write(str(update_obj))
    return 'OK'

def update_processor(update):
    if hasattr(update, 'message'):
        if hasattr(update.message, 'entities'):
            if update.message.entities[0].type == 'bot_command':
                command_processor(update)

def command_processor(update):
    if update.message.text == '/start':
        bot.sendMessage(chat_id=update.message.from_user.id,
                        text='Привет!')
