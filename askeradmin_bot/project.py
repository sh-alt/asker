from flask import Flask, request 
import askeradmin_bot.config as config
import json
import requests
import telegram
from telegram.update import Update
import logging
import uuid
from askeradmin_bot.update_processor import Update_processor 


app = Flask(__name__) 


bot = telegram.Bot(token=config.token)

#logging.basicConfig(filename='log.log', level=logging.DEBUG,
#                    format='[%(asctime)s] %(levelname)s in %(module)s: %(uid)s %(message)s')

logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s in %(module)s:  %(message)s')


@app.route("/") 
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
    uid = '[{}]'.format(str(uuid.uuid4())[0:8])
    update_json = request.get_json()
    logging.debug(update_json, extra={'uid': uid})
    update_obj = Update.de_json(update_json, bot)
    logging.debug(f'Создан объект: {update_obj}', extra={'uid': uid})
    logging.debug(f'Запускаю update_processor', extra={'uid': uid})
    Update_processor(update_obj, uid, bot)
    return 'OK'

