import os
import requests
import logging


def get_weather(city):
    """ Функция для получения ответа от сервиса openweathermap.org. """
    params = {
        'q': city,
        'units': 'metric',
        'APPID': os.environ['WEATHER_API_KEY'],
    }
    url = 'http://api.openweathermap.org/data/2.5/weather'
    try:
        resp = requests.get(url, params=params)
        return resp
    except (requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout) as e:
        logging.error(e)
        return None


def process_owm_response(response):
    """ Функция для разбора результата функции get_weather. """
    if response.status_code in [200, 404]:
        resp_json_dict = response.json()

    if response:
        answ_text = 'Сейчас {0} °C'.format(resp_json_dict['main']['temp'])

    elif response.status_code == 404 and resp_json_dict['message'] == 'city not found':
        answ_text = 'Я не знаю такого города.'

    else:
        answ_text = ('Ошибка. Сервер вернул код {0}'.format(response.status_code))

    return answ_text
