from flask import Flask, request # Импортируем модули
import askeradmin_bot.config as config
import json
import requests
import telegram
from telegram.update import Update
import logging
import functools
import uuid


app = Flask(__name__) # Создаем приложение


bot = telegram.Bot(token=config.token)

logging.basicConfig(filename='log.log', level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s in %(module)s: %(uid)s %(message)s')


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
    uid = '[{}]'.format(str(uuid.uuid4())[0:8])
    update_json = request.get_json()
    logging.debug(update_json, extra={'uid': uid})
    update_obj = Update.de_json(update_json, bot)
    logging.debug(f'Создан объект: {update_obj}', extra={'uid': uid})
    logging.debug(f'Запускаю update_processor', extra={'uid': uid})
    update_processor(update_obj, uid)
    return 'OK'


def update_processor(update, uid):
    logging.debug('Проверяю тип обновления', extra={'uid': uid})
    if hasattr(update, 'message'):
        logging.debug('Тип обновления message', extra={'uid': uid})
        logging.debug('Запускаю message_processor', extra={'uid': uid})
        message_processor(update, uid)


def message_processor(update, uid):
    logging.debug('Проверяю количество entities', extra={'uid': uid})
    if len(update.message.entities) > 0:
        logging.debug('Проверяю наличие команд в сообщении', extra={'uid': uid})
        if update.message.entities[0].type == 'bot_command' and update.message.chat.type == 'private':
            logging.debug(f'Найдена команда {update.message.text}, запускаю private_command_processor', 
                            extra={'uid': uid})
            private_command_processor(update, uid)


def private_command_processor(update, uid):
    if update.message.text == '/start':
        logging.debug(f'Отправляю сообщение в ЛС пользователю с id {update.message.from_user.id}',
                        extra={'uid': uid})
        bot.sendMessage(chat_id=update.message.from_user.id,
                        text='Привет!')
