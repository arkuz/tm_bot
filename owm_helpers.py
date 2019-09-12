import os
import requests
import logging


def get_weather(city):
    """ Функция для получения ответа от сервиса openweathermap.org. """
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
        logging.error('Ошибка {0}'.format(e))
        return None


def process_owm_response(response):
    """ Функция для разбора результата функции get_weather. """
    if response.status_code in [200, 404]:
        resp_json_dict = response.json()

    if response.status_code == 200:
        kelvin = resp_json_dict['main']['temp']
        degree = round(kelvin - 273)
        msg_text = 'Сейчас {0} °C'.format(degree)
    elif response.status_code == 404 and resp_json_dict['message'] == 'city not found':
        msg_text = 'Я не знаю такого города.'
    elif response.status_code == 400:
        msg_text = 'Нужно указать город. Например /weather Moscow'
    else:
        logging.error('Ошибка. Сервер вернул код {0}'.format(response.status_code))

    return msg_text
