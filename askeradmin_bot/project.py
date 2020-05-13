from flask import Flask # Импортируем модули
import askeradmin_bot.config as config
import json
import requests

app = Flask(__name__) # Создаем приложение

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
