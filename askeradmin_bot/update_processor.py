import logging
from telegram import ChatPermissions
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
import texts
from handlers import (Message_handler, Private_message_handler, 
Private_command_handler, New_user_handler, Callback_query_handler, Chat_message_handler,
Left_chat_members_handler)


class Update_processor:


    def update_error_handler(func):
        def wrapped_func(self):
            try:
                func(self)
            except BadRequest as b:
                if str(b) == "Can't remove chat owner":
                    logging.info('Пришел владелец чата')
                elif str(b) == 'Not enough rights to restrict/unrestrict chat member':
                    logging.info(f'[NOT_ENOUGH_RIGHTS] У бота недостаточно прав в чате {self.update.message.chat}')
                    text = 'У бота недостаточно прав в этом чате. Подробнее в лс бота'
                    chat_id = self.update.message.chat.id
                    self.bot.send_message(chat_id=chat_id, text=text)
                else:
                    logging.error(f'[ERROR] Что-то пошло не так: {b} update: {self.update}')
            except Exception as e:
                logging.error(f'[ERROR] {e} update: {self.update}')
        return wrapped_func


    def __init__(self, update, uid, bot):
        self.update = update
        self.bot = bot
        self.extra = {'uid': uid}
        self.update_processor()


    @update_error_handler
    def update_processor(self):
        Private_command_handler(self.update, self.command_processor)
        New_user_handler(self.update, self.new_chat_members_processor)
        Chat_message_handler(self.update, self.chat_message_processor)
        Callback_query_handler(self.update, self.callback_processor)
        Left_chat_members_handler(self.update, self.left_chat_member_processor)


    def chat_message_processor(self):
        logging.info(f'[CHAT_MESSAGE]: chat: {self.update.message.chat}, \
from_user: {self.update.message.from_user} \
text: {self.update.message.text}')


    def left_chat_member_processor(self):
        logging.info(f'[LEFT_MEMBER]: chat: {self.update.message.chat}, \
left_user: {self.update.message.left_chat_member}')

    def command_processor(self):
        text = texts.private_start_message
        if self.update.message.text == '/start':
            self.bot.sendMessage(chat_id=self.update.message.from_user.id,
                            text=text)

        
    @update_error_handler
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
            text = texts.welcome_message.substitute(first_name=first_name)
            reply_keyboard = [[InlineKeyboardButton('Войти', callback_data=f'{user_id}')]]
            reply_markup = InlineKeyboardMarkup(reply_keyboard)
            logging.info(f'[NEW_USER] Новый пользователь {member} в чате {self.update.message.chat}')
            logging.info(f'[RESTRICT] Применяю ограничения для пользователя {member} в чате \
{self.update.message.chat}')
            self.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, permissions=permissions)
            self.bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=message_id, reply_markup=reply_markup)


    @update_error_handler
    def callback_processor(self):
        self.callback_user_id = int(self.update.callback_query.data)
        self.users_list = {}
        for member in self.update.callback_query.message.reply_to_message.new_chat_members: 
            self.users_list[member.id] = member.first_name
        if self.check_user():
            self.promote_user()
        else:
            self.flash_message()
            

    def check_user(self):
        user_initiated = self.update.callback_query.from_user
        if self.callback_user_id == user_initiated.id:
            return True
        else: 
            return False

    @update_error_handler
    def promote_user(self):
        chat_id = self.update.callback_query.message.chat_id
        user_initiated = self.update.callback_query.from_user
        message_id = self.update.callback_query.message.message_id
        callback_query_id = self.update.callback_query.id
        logging.info(f'[PROMOTE] Снимаю ограничения с пользователя {self.update.callback_query.from_user} \
в чате {self.update.callback_query.message.chat}')
        
        text = f'Проверка {self.users_list[self.callback_user_id]} произведена! Поприветствуем! '
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
        self.bot.restrict_chat_member(chat_id=chat_id, user_id=user_initiated.id, permissions=permissions)
        self.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
        self.bot.answer_callback_query(callback_query_id=callback_query_id)

    @update_error_handler
    def flash_message(self):
        callback_query_id = self.update.callback_query.id
        flash_text = f'Нажать клавишу может только {self.users_list[self.callback_user_id]}'
        logging.info(f'Пользователь {self.update.callback_query.from_user} нажал клавишу. \
Callback: {self.update}')
        self.bot.answer_callback_query(callback_query_id=callback_query_id, 
                                            show_alert=True,
                                            text=flash_text)