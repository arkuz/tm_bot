import logging
import requests as req
import datetime


def start(bot, update):
    """ Функция отправляет ответ на команду /start. """
    text = 'Вызвана команда /start'
    logging.info(text)
    update.message.reply_text(text)


def talk_to_me(bot, update):
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


def now(bot, update):
    """ Функция отправляет пользователю время и дату в Москве. """
    text = 'Вызвана команда /now'
    ts = req.get('https://time100.ru/api.php').text
    value = datetime.datetime.fromtimestamp(int(ts))
    cur_date = value.strftime('%d.%m.%Y')
    cur_time = value.strftime('%H:%M:%S')
    msg_text = 'Сейчас в Москве:\n     Время: {time}\n     Дата: {date}'.format(
        time=cur_time,
        date=cur_date
    )
    logging.info('{} - {}'.format(text, msg_text))
    update.message.reply_text(msg_text)

