import logging
import requests
import datetime


def start_comand_handler(bot, update):
    """ Функция отправляет ответ на команду /start. """
    text = 'Вызвана команда /start'
    logging.info(text)
    update.message.reply_text(text)


def send_mirror_message_handler(bot, update):
    """ Функция отправляет пользователю его же сообщение. """
    user_text = 'Привет, {first_name}. Ты написал: {text}'.format(
        first_name=update.message.chat.first_name,
        text=update.message.text
    )
    logging.info('Пользователь: {user}, Чат ID: {chat_id}, Сообщение: {msg}'.format(
        user=update.message.chat.username,
        chat_id=update.message.chat.id,
        msg=update.message.text
    ))
    update.message.reply_text(user_text)


def get_datetime_comand_handler(bot, update):
    """ Функция отправляет пользователю время и дату в Москве. """
    try:
        resp = requests.get('https://time100.ru/api.php')
        if resp.status_code == 200:
            text = 'Вызвана команда /now'
            value = datetime.datetime.fromtimestamp(int(resp.text))
            cur_date = value.strftime('%d.%m.%Y')
            cur_time = value.strftime('%H:%M:%S')
            msg_text = 'Сейчас в Москве:\n     Время: {time}\n     Дата: {date}'.format(
                time=cur_time,
                date=cur_date
            )
            logging.info('{0} - {1}'.format(text, msg_text))
            update.message.reply_text(msg_text)
        else:
            logging.error('Ошибка. Код ответа %s', resp.status_code)
    except Exception:
        logging.error('Ошибка - %s', Exception.message)

