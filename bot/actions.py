import os

import owm_helpers
import cities_game_helpers as cithelp
import wordcount_helpers as wordhelp
from messages_helpers import send_text_to_user


cur_dir = os.path.dirname(os.path.abspath(__file__))
cities_data = os.path.join(os.path.split(cur_dir)[0], 'cities_data')


def start_comand_handler(bot, update):
    """ Функция отправляет ответ на команду /start. """
    answ_text = """
Я умею:
1. /weather Москва - узнать температуру в городе
2. /wordcount привет, как дела? - узнать количество слов в введенном сообщении
3. А можете просто мне написать и я отвечу вам вашим же сообщением :-)
"""
    send_text_to_user(update, answ_text)


def send_mirror_message_handler(bot, update):
    """ Функция отправляет пользователю его же сообщение. """
    answ_text = '{first_name}, ты написал: {msg}'.format(
        first_name=update.message.chat.first_name,
        msg=update.message.text,
    )
    send_text_to_user(update, answ_text)


def weather_comand_handler(bot, update, args):
    """ Функция отправляет температуру в указанном городе. """
    city = args[0] if args else None

    if city is None:
        answ_text = 'Необходимо указать город. Пример: /weather Москва'
        send_text_to_user(update, answ_text)
        return

    resp = owm_helpers.get_weather(city)

    if resp is not None:
        answ_text = owm_helpers.process_owm_response(resp)
        send_text_to_user(update, answ_text)
        return

    answ_text = 'Ошибка соединения с сервером openweathermap.org'
    send_text_to_user(update, answ_text)


def wordcount_comand_handler(bot, update, args):
    """ Функция отправляет количество слов в пользовательском сообщении. """
    word_count = wordhelp.get_word_count(args)
    answ_text = wordhelp.get_answer_text(word_count)
    send_text_to_user(update, answ_text)


def cities_comand_handler(bot, update, args):
    """ Функция игры в города, отправляет город в ответ. """
    username = update.message.chat.username
    user_filename = os.path.join(cities_data, f'{username}_cities_base.json')
    cities_base = os.path.join(cities_data, user_filename)

    # если пользователь не ввел название города, то выход
    user_city = cithelp.concat_words(args)
    if not user_city:
        answ_text = 'Необходимо указать город. Пример: /cities Москва'
        send_text_to_user(update, answ_text)
        return

    # создаем и/или загружаем файл с базой городов для пользователя
    user_db_obj = cithelp.prepare_user_db(cities_base,
                                          user_filename,
                                          cithelp.get_etalon_cities_list())

    # заполняем рабочие переменные сведениями из файла игрока
    cities = user_db_obj['cities']
    last_symbol = user_db_obj['symbol']

    # выполняем проверки для переменной user_city
    uc_validation = cithelp.user_city_validation(user_city, cities, last_symbol)
    if uc_validation is not None:
        answ_text = cithelp.user_city_validation(user_city, cities, last_symbol)
        send_text_to_user(update, answ_text)
        return

    # получаеv город от бота или None
    city = cithelp.get_city_from_bot(cities, user_city)
    if city is not None:
        bot_city_last_symbol = city[-2] if cithelp.is_invalid_end_symbol(city) else city[-1]
        cithelp.save_user_db(user_filename, cities, bot_city_last_symbol)
        answ_text = f'{city}, твоя очередь.'
        send_text_to_user(update, answ_text)
        return

    # если мы дошли сюда, то у бота кончились города
    cithelp.delete_user_db(user_filename)
    answ_text = 'Я больше не знаю городов, давай начнем сначала'
    send_text_to_user(update, answ_text)


def cities_stop_comand_handler(bot, update):
    """ Функция останавливает игру в города, удаляет БД пользователя. """
    username = update.message.chat.username
    user_filename = os.path.join(cities_data, f'{username}_cities_base.json')
    cithelp.delete_user_db(user_filename)
    answ_text = 'Как скажешь, в следующий раз начнем сначала'
    send_text_to_user(update, answ_text)
