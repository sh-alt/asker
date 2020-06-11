import logging

class Base_Handler:

    def __init__(self, update, func=None):
        self.update = update
        self.func = func
        self.exec_func()

    def check_update(self):
        pass


    def exec_func(self):
        if self.check_update() and self.func:
            self.func()
    

class Message_handler(Base_Handler):
    
    def check_update(self):
        if self.update.message:
            return True

        
class Private_message_handler(Message_handler):

    def check_update(self):
        if super().check_update():
            if self.update.message.chat.type == 'private':
                message_text = self.update.message.text
                if message_text:
                    logging.info(f'[PRIVATE_MESSAGE]: \
from_user: {self.update.message.from_user} \
text: {message_text}')
                return True



class Private_command_handler(Private_message_handler):

    def check_update(self):
        if super().check_update():
            if self.update.message.entities:
                if self.update.message.entities[0].type == 'bot_command':
                    return True


class Chat_message_handler(Message_handler):

    def check_update(self):
        if super().check_update():
            if self.update.message.text:
                return True


class New_user_handler(Message_handler):

    def check_update(self):
        if super().check_update():
            if self.update.message.new_chat_members:
                return True


class Callback_query_handler(Base_Handler):

    def check_update(self):
        if self.update.callback_query:
            return True


class Left_chat_members_handler(Message_handler):

    def check_update(self):
        if super().check_update():
            if self.update.message.left_chat_member:
                return True