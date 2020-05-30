import logging
from telegram import ChatPermissions
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest

class Update_processor:

    def __init__(self, update, uid, bot):
        self.update = update
        self.bot = bot
        self.extra = {'uid': uid}
        self.update_processor()


    def update_processor(self):
        logging.debug('Проверяю тип обновления', extra=self.extra)
        if self.update.message:
            logging.debug('Тип обновления message', extra=self.extra)
            logging.debug('Запускаю message_processor', extra=self.extra)
            try:
                self.message_processor()
            except BadRequest as b:
                if str(b) == "Can't remove chat owner":
                    logging.info('Пришел владелец чата')
                else:
                    logging.error(f'Что-то пошло не так: {b}')
        elif self.update.callback_query:
            logging.debug('Тип обновления callback_query', extra=self.extra)
            self.callback_processor()           


    def message_processor(self):
        if self.update.message.chat.type == 'private':
            logging.debug('Тип сообщения private')
            if len(self.update.message.entities) > 0:
                logging.debug('Проверяю наличие команд в сообщении', extra=self.extra)
                if self.update.message.entities[0].type == 'bot_command':
                    logging.debug(f'Найдена команда {self.update.message.text}, запускаю private_command_processor', 
                                    extra=self.extra)
                    self.private_command_processor()
        elif self.update.message.chat.type != 'private':
            logging.debug('Тип сообщения не private. Запускаю chat_message_processor')
            self.chat_message_processor()
            
            


    def private_command_processor(self):
        text = 'Привет! \n\n\nЭтот микро-бот создан для того, чтобы отсечь самые глупые спам-боты приходящие в чат, которые \
не в состоянии нажать на клавишу "Войти". Несмотря на то, что бот простейший - развитие продолжается.\
Скоро будут новые функции.\n\n\n\
Для того, чтобы установить бота:\n\
1. Добавьте бота в чат, где Вы можете назначать адинистраторов;\n\
2. Назначьте бота администратором.\n\
Если у Вас возникли какие-либо вопросы или проблемы\
в работе с ботом - напишите об этом в чате @askerchat'
        if self.update.message.text == '/start':
            logging.debug(f'Отправляю сообщение в ЛС пользователю с id {self.update.message.from_user.id}',
                            extra=self.extra)
            self.bot.sendMessage(chat_id=self.update.message.from_user.id,
                            text=text)


    def chat_message_processor(self):
        message_text = self.update.message.text
        logging.debug(f'Текст сообщения: {message_text}')
        if self.update.message.new_chat_members:
            self.new_chat_members_processor()
        
    
    def new_chat_members_processor(self):
        chat_id = self.update.message.chat.id
        #user_id = self.update.message.from_user.id
        message_id = self.update.message.message_id
        permissions = ChatPermissions(
            can_send_messages=False, 
            can_send_media_messages=False, 
            can_send_polls=False, 
            can_send_other_messages=False, 
            can_add_web_page_previews=False, 
            can_change_info=False, 
            can_invite_users=False, 
            can_pin_messages=False
        )
        for member in self.update.message.new_chat_members:
            user_id = member.id
            first_name = member.first_name
            text = f'Привет, {first_name}! Для того, чтобы войти нажми клавишу "Войти"'
            reply_keyboard = [[InlineKeyboardButton('Войти', callback_data=f'{user_id}')]]
            reply_markup = InlineKeyboardMarkup(reply_keyboard)
            self.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=permissions)
            self.bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=message_id, reply_markup=reply_markup)


    def callback_processor(self):
        chat_id = self.update.callback_query.message.chat_id
        user_id = self.update.callback_query.from_user.id
        callback_user_id = int(self.update.callback_query.data)
        message_id = self.update.callback_query.message.message_id
        first_name = self.update.callback_query.message.reply_to_message.from_user.first_name
        text = f'Проверка {first_name} произведена! Поприветствуем!'
        callback_query_id = self.update.callback_query.id
        permissions = ChatPermissions(
            can_send_messages=True, 
            can_send_media_messages=True, 
            can_send_polls=True, 
            can_send_other_messages=True, 
            can_add_web_page_previews=True, 
            can_change_info=False, 
            can_invite_users=True, 
            can_pin_messages=False
        )
        if callback_user_id == user_id:
            self.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=permissions)
            self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
            self.bot.answer_callback_query(callback_query_id=callback_query_id)
        else:
            text = f'Нажать клавишу может только {first_name}'
            self.bot.answer_callback_query(callback_query_id=callback_query_id, 
                                            show_alert=True,
                                            text=text)