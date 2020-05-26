from project import bot
import config as config


url = f'https://{config.ip}'
certificate = open(config.sert_pem, 'rb')


def set_webhook():
    bot.set_webhook(url=url, certificate=certificate)

def get_webhook_info():
    webhook_info = bot.get_webhook_info()
    return webhook_info

def delete_webhook():
    bot.delete_webhook()

if __name__ == "__main__":
    wi = get_webhook_info()
    if not wi.url:
        set_webhook()
