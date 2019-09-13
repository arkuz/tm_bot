import os
import requests


def get_weather(city):
    """ Функция для получения ответа от сервиса openweathermap.org. """
    params = {
        'q': city,
        'APPID': os.environ['WEATHER_API_KEY'],
    }
    url = 'http://api.openweathermap.org/data/2.5/weather'
    return requests.get(url, params=params)


def process_owm_response(response):
    """ Функция для разбора результата функции get_weather. """
    if response.status_code in [200, 404]:
        resp_json_dict = response.json()

        if response:
            kelvin = resp_json_dict['main']['temp']
            degree = round(kelvin - 273)
            answ_text = 'Сейчас {0} °C'.format(degree)

        if response.status_code == 404 and resp_json_dict['message'] == 'city not found':
            answ_text = 'Я не знаю такого города.'

    else:
        answ_text = ('Ошибка. Сервер вернул код {0}'.format(response.status_code))

    return answ_text
