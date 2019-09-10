import os
import requests
import logging


def get_weather(city):
    """ Функция для получения температуры в городе city. """
    params = {
        'q': city,
        'APPID': os.environ['WEATHER_API_KEY'],
    }
    url = 'http://api.openweathermap.org/data/2.5/weather'
    try:
        return requests.get(url, params=params)
    except (requests.ConnectionError,
            requests.ConnectTimeout,
            ) as e:
        logging.error('Ошибка {0}'.format(e.message))
        return None


def process_owm_response(text, response):
    """ Функция для разбора результата функции get_weather. """
    if response.status_code in [200, 404]:
        resp_json_dict = response.json()

    if response.status_code == 200:
        kelvin = resp_json_dict['main']['temp']
        degree = round(kelvin - 273)
        msg_text = 'Сейчас {0} °C'.format(degree)
        logging.info('{0} - {1}'.format(text, msg_text))
    elif response.status_code == 404 and resp_json_dict['message'] == 'city not found':
        msg_text = 'Я не знаю такого города.'
        logging.info('{0} - {1}'.format(text, msg_text))
    elif response.status_code == 400:
        msg_text = 'Нужно указать город. Например /weather Moscow'
        logging.info('{0} - {1}'.format(text, msg_text))
    else:
        logging.error('Ошибка. Сервер вернул код {0}'.format(response.status_code))

    return msg_text

