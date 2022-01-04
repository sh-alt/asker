from flask import Flask, request 
import config 
import telegram
from telegram.update import Update
import logging
import uuid
from update_processor import Update_processor 

app = Flask(__name__) 

bot = telegram.Bot(token=config.token)

logging.basicConfig(filename='/var/log/projects/askeradmin_bot/production.log', level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s in %(module)s:  %(message)s')


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
