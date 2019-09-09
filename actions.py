import os
import logging
import requests
import config


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


def weather_comand_handler(bot, update):
    """ Функция отправляет температуру в указанном городе """
    text = update.message.text
    length_cmd = update.message.entities[0].length  # узнаем длину сообщения
    city = text[length_cmd + 1:].replace(' ','')    # забираем все после /weather и удаляем пробелы
    params = {
        'q': city,
        'APPID': os.environ['WEATHER_API_KEY'],
    }
    url = 'http://api.openweathermap.org/data/2.5/weather'

    try:
        resp = requests.get(url, params=params)
    except (requests.ConnectionError,
            requests.ConnectTimeout,
            ) as e:
        logging.error('Ошибка {0}'.format(e.message))
        return  # выходим из функции если ошибка соединения

    if resp.status_code == 200:
        kelvin = resp.json()['main']['temp']
        degree = round(kelvin - 273)
        msg_text = 'Сейчас {0} °C'.format(degree)
        logging.info('{0} - {1}'.format(text, msg_text))
    elif resp.status_code == 404 and resp.json()['message'] == 'city not found':
        msg_text = 'Я не знаю такого города.'
        logging.info('{0} - {1}'.format(text, msg_text))
    elif resp.status_code == 400:
        msg_text = 'Нужно указать город. Например /weather Moscow'
        logging.info('{0} - {1}'.format(text, msg_text))
    else:
        logging.error('Ошибка. Сервер вернул код {0}'.format(resp.status_code))

    update.message.reply_text(msg_text)

