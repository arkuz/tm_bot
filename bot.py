import os
import logging
import actions as act

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Формат для логирования
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log',
                    )


PROXY = {
    'proxy_url': os.environ['URL'],
    'urllib3_proxy_kwargs': {
        'username': os.environ['USERNAME'],
        'password': os.environ['PASSWORD'],
    },
}


def main():
    mybot = Updater(os.environ['API_KEY'], request_kwargs=PROXY)
    logging.info('Стартует БОТ')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', act.start_comand_handler))
    dp.add_handler(CommandHandler('weather', act.weather_comand_handler, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text, act.send_mirror_message_handler))
    mybot.start_polling()
    mybot.idle()


main()
