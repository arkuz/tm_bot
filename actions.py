import logging
import owm_helpers


LOG_STRING = 'Пользователь: {user}, Чат ID: {chat_id}, Сообщение: {msg}, Ответ: {answ}'


def start_comand_handler(bot, update):
    """ Функция отправляет ответ на команду /start. """
    answ_text = 'Вот такой командой можно узнать погоду: /weather Москва'

    logging.info(LOG_STRING.format(
        user=update.message.chat.username,
        chat_id=update.message.chat.id,
        msg=update.message.text,
        answ=answ_text,
    ))

    update.message.reply_text(answ_text)


def send_mirror_message_handler(bot, update):
    """ Функция отправляет пользователю его же сообщение. """
    answ_text = '{first_name}, ты написал: {msg}'.format(
        first_name=update.message.chat.first_name,
        msg=update.message.text,
    )

    logging.info(LOG_STRING.format(
        user=update.message.chat.username,
        chat_id=update.message.chat.id,
        msg=update.message.text,
        answ=answ_text,
    ))

    update.message.reply_text(answ_text)


def weather_comand_handler(bot, update, args):
    """ Функция отправляет температуру в указанном городе. """
    city = ''
    if args:
        city = args[0]

    user = update.message.chat.username
    chat_id = update.message.chat.id
    msg = update.message.text

    if not city:
        answ_text = 'Необходимо указать город. Пример: /weather Москва'
        logging.info(LOG_STRING.format(
            user=user,
            chat_id=chat_id,
            msg=msg,
            answ=answ_text,
        ))
        update.message.reply_text(answ_text)
        return

    try:
        resp = owm_helpers.get_weather(city)
    except (resp.ConnectionError,
            resp.ConnectTimeout,
            ) as e:
        logging.error(LOG_STRING.format(
            user=user,
            chat_id=chat_id,
            msg=msg,
            answ=e,
        ))
        update.message.reply_text('Ошибка соединения с сервером openweathermap.org')
        return

    answ_text = owm_helpers.process_owm_response(resp)
    logging.info(LOG_STRING.format(
        user=user,
        chat_id=chat_id,
        msg=msg,
        answ=answ_text,
    ))
    update.message.reply_text(answ_text)
