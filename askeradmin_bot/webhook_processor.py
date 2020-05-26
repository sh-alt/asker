from askeradmin_bot.project import bot
import askeradmin_bot.config as config


url = f'https://{config.ip}'
certificate = open(config.sert_pem, 'rb')


def set_webhook():
    bot.set_webhook(url=url, certificate=certificate)

def get_webhook_info():
    webhook_info = bot.get_webhook_info()
    return webhook_info

if __name__ == "__main__":
    wi = get_webhook_info()
    if not wi.url:
        bot.set_webhook()
