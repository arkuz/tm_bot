import os
import json


cur_dir = os.path.dirname(os.path.abspath(__file__))
cities_data = os.path.join(os.path.split(cur_dir)[0], 'cities_data')
etalon_base = os.path.join(cities_data, 'etalon_base.json')


def read_json(path):
    """ Функция возвращает json объект из файла. """
    with open(path, 'r', encoding='UTF-8') as f:
        data = f.read()
    return json.loads(data)


def get_etalon_cities_list():
    """ Функция возвращает эталонный список городов, которые знает бот, из файла. """
    return read_json(etalon_base)['cities']


def create_user_db(cities_base, user_filename, cities_list):
    """ Функция записывает словарь в json файл, для стартовой инициализации. """
    user_data = {}
    user_data['symbol'] = None
    user_data['cities'] = cities_list
    with open(user_filename, 'w', encoding='UTF-8') as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)


def prepare_user_db(cities_base, user_filename, cities_list):
    """ Функция создает или загружает пользовательскую БД"""
    if not os.path.exists(cities_base):
        create_user_db(cities_base, user_filename, cities_list)

    return load_user_db(user_filename)


def delete_user_db(user_filename):
    """ Функция удаляет файл БД городов пользователя. """
    if os.path.exists(user_filename):
        os.remove(user_filename)


def save_user_db(user_filename, cities_list, symbol):
    """ Функция записывает словарь в json файл, сохраняет текущее состояние игры. """
    user_data = {}
    user_data['symbol'] = symbol
    user_data['cities'] = cities_list
    with open(user_filename, 'w', encoding='UTF-8') as f:
        json.dump(user_data, f, indent=4, ensure_ascii=False)


def load_user_db(user_filename):
    """ Функция возвращает json из файла, текущее игровое состояние. """
    return read_json(user_filename)


def is_invalid_end_symbol(city_name):
    """ Функция проверяет заканчивается ли слово на ['ь', 'ъ', 'ы', 'й']. """
    return True if city_name.lower()[-1] in ['ь', 'ъ', 'ы', 'й'] else False


def concat_words(words_list):
    """ Функция переводит каждое слово в нижний регистр, затем собирает все слова в одну строку и возвращает. """
    all_words_string = ''
    if words_list:
        for arg in words_list:
            all_words_string += f' {arg.lower()}'
    all_words_string = all_words_string.strip()
    return all_words_string


def get_city_from_bot(cities, user_city):
    """ Функция возвращает элемент списка (город) или None. """
    for city in cities:
        user_city_last_symbol = user_city[-2] if is_invalid_end_symbol(user_city) else user_city[-1]
        if city[0] == user_city_last_symbol:
            delete_cities_in_list(cities, city, user_city)
            return city
    return None


def delete_cities_in_list(cities, city, user_city):
    """ Функция удаляет из списка cities значения city, user_city. """
    try:  # на случай, когда user_city нет в списке
        user_city_index = cities.index(user_city)
        cities.pop(user_city_index)
    except ValueError:
        pass
    city_index = cities.index(city)
    cities.pop(city_index)


def user_city_validation(user_city, cities, last_symbol):
    """ Функция выполняет проверки для user_city. """

    # проверка, что введенный город есть в эталонном списке бота
    if user_city not in get_etalon_cities_list():
        return 'Я не знаю такого города.'

    # бот проверяет, что наш город начинается на последнюю букву его города
    if user_city[0].lower() != last_symbol and last_symbol is not None:
        return f'Опять жульничаешь? Тебе на "{last_symbol.capitalize()}"'

    # проверка, что введенный город уже был назван
    if user_city not in cities:
        return f'Кто-то из нас уже называл город "{user_city}".'

    return None
