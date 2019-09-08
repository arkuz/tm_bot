import logging
import config as conf
import actions as act

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Формат для логирования
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    mybot = Updater(conf.API_KEY, request_kwargs=conf.PROXY)
    logging.info('Стартует БОТ')
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', act.start))
    dp.add_handler(CommandHandler('now', act.now))
    dp.add_handler(MessageHandler(Filters.text, act.talk_to_me))
    mybot.start_polling()
    mybot.idle()


main()

