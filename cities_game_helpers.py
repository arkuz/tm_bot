import os
import json


cur_dir = os.path.dirname(os.path.abspath(__file__))
cities_data = os.path.join(cur_dir, 'cities_data')
etalon_base = os.path.join(cities_data, 'etalon_base.json')


def read_json(path):
    """ Функция возвращает json объект из файла. """
    with open(path, 'r', encoding='UTF-8') as f:
        data = f.read()
    return json.loads(data)


def get_etalon_cities_list():
    """ Функция возвращает эталонный список городов, которые знает бот, из файла. """
    return read_json(etalon_base)['cities']


def create_user_db(user_filename, cities_list, symbol=None):
    """ Функция записывает словарь в json файл, для стартовой инициализации. """
    user_data = {}
    user_data['symbol'] = symbol
    user_data['cities'] = cities_list
    with open(user_filename, 'w', encoding='UTF-8') as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)


def save_user_db(user_filename, cities_list, symbol):
    """ Функция записывает словарь в json файл, сохраняет текущее состояние игры. """
    create_user_db(user_filename, cities_list, symbol)


def load_user_db(user_filename):
    """ Функция возвращает json из файла, текущее игровое состояние. """
    return read_json(user_filename)


def is_invalid_end_symbol(city_name):
    """ Функция проверяет заканчивается ли слово на ['ь','ъ','ы']. """
    return True if city_name.lower()[-1] in ['ь', 'ъ', 'ы'] else False


def concat_words(words_list):
    """ Функция собирает слова из списка в одну строку, форматирует и возвращает. """
    all_words_string = ''
    if words_list:
        for arg in words_list:
            all_words_string += f' {arg.capitalize()}'
    all_words_string = all_words_string.strip()
    return all_words_string


def get_city_from_bot(cities, user_city):
    """ Функция возвращает город или None. """
    for city in cities:
        user_city_last_symbol = user_city[-2] if is_invalid_end_symbol(user_city) else user_city[-1]
        if city.lower()[0] == user_city_last_symbol:
            try:  # на случай, когда город введенный пользователем уже удален из списка
                user_city_index = cities.index(user_city)
                cities.pop(user_city_index)
            except ValueError:
                pass
            city_index = cities.index(city)
            cities.pop(city_index)
            return city
    return None
