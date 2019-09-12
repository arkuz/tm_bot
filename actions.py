import logging
import tools


def start_comand_handler(bot, update):
    """ Функция отправляет ответ на команду /start. """
    text = 'Вызвана команда /start'
    logging.info(text)
    update.message.reply_text(text)


def send_mirror_message_handler(bot, update):
    """ Функция отправляет пользователю его же сообщение. """
    user_text = 'Привет, {first_name}. Ты написал: {text}'.format(
        first_name=update.message.chat.first_name,
        text=update.message.text,
    )
    logging.info('Пользователь: {user}, Чат ID: {chat_id}, Сообщение: {msg}'.format(
        user=update.message.chat.username,
        chat_id=update.message.chat.id,
        msg=update.message.text,
    ))
    update.message.reply_text(user_text)


def weather_comand_handler(bot, update, args):
    """ Функция отправляет температуру в указанном городе. """
    text = update.message.text
    if not args:
        msg_text = 'Необходимо указать город. Пример: /weather Москва'
        logging.info('{0} - {1}'.format(text, msg_text))
    else:
        resp = tools.get_weather(args[0])
        if resp is None:
            return
        msg_text = tools.process_owm_response(text, resp)
    update.message.reply_text(msg_text)
