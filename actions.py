import owm_helpers
import re
import os

from messages_helpers import send_text_to_user
import cities_game_helpers as cithelp


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

    else:
        answ_text = 'Ошибка соединения с сервером openweathermap.org'
        send_text_to_user(update, answ_text)


def wordcount_comand_handler(bot, update, args):
    """ Функция отправляет количество слов в пользовательском сообщении. """
    if args:
        word_count = 0
        for arg in args:
            arg = re.sub(r'([^a-zA-zа-яА-Я]+)', '', arg)  # удаляем все, кроме букв
            if len(arg) >= int(os.getenv('WORD_LEN', '2')):  # длина слова определяется переменной окружения WORD_LEN
                word_count += 1
        if word_count != 0:
            answ_text = f'Количество слов в вашем предложении = {word_count}'
        else:
            answ_text = 'Я не вижу слов в вашем предложении'
    else:
        answ_text = 'Вы ввели пустую строку'

    send_text_to_user(update, answ_text)


def cities_comand_handler(bot, update, args):
    """ Функция игры в города, отправляет город в ответ. """
    username = update.message.chat.username
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    cities_data = os.path.join(cur_dir, 'cities_data')
    user_filename = os.path.join(cities_data, f'{username}_cities_base.json')
    cities_base = os.path.join(cities_data, user_filename)

    # слово stop для остановки игры и переинициализации пользовательской базы городов
    stop_game = args[0].lower() if args else None
    if stop_game == 'stop':
        answ_text = 'Как скажешь, в следующий раз начнем сначала'
        send_text_to_user(update, answ_text)
        cithelp.create_user_db(user_filename, cithelp.get_etalon_cities_list())
        return

    user_city = cithelp.concat_words(args)
    if user_city is None:
        answ_text = 'Необходимо указать город. Пример: /cities Москва'
        send_text_to_user(update, answ_text)
        return

    # создаем новый файл с городами для пользователя - новая игра
    if not os.path.exists(cities_base):
        cithelp.create_user_db(user_filename, cithelp.get_etalon_cities_list())

    # заполняем рабочие переменные сведениями из файла игрока
    user_db_obj = cithelp.load_user_db(user_filename)
    cities = user_db_obj['cities']
    last_symbol = user_db_obj['symbol']

    if not cities:
        answ_text = 'Я больше не знаю городов, ты победил!'
        send_text_to_user(update, answ_text)
        cithelp.create_user_db(user_filename, cithelp.get_etalon_cities_list())
        return

    # проверка, что введенный город есть в эталонном списке бота
    if user_city not in cithelp.get_etalon_cities_list():
        if user_city not in cities:
            answ_text = 'Я не знаю такого города.'
            send_text_to_user(update, answ_text)
            return

    # бот проверяет, что наш город начинается на последнюю букву его города
    if user_city[0].lower() != last_symbol and last_symbol is not None:
        answ_text = f'Опять жульничаешь? Тебе на "{last_symbol.capitalize()}"'
        send_text_to_user(update, answ_text)
        return

    # проверка, что введенный город уже был назван
    if user_city not in cities:
        answ_text = f'Кто-то из нас уже называл город "{user_city}".'
        send_text_to_user(update, answ_text)
        return

    city = cithelp.get_city_from_bot(cities, user_city)
    if city is not None:
        answ_text = f'{city}, твоя очередь.'
        send_text_to_user(update, answ_text)
        bot_city_last_symbol = city[-2] if cithelp.is_invalid_end_symbol(city) else city[-1]
        cithelp.save_user_db(user_filename, cities, bot_city_last_symbol)
    else:
        answ_text = 'Я больше не знаю городов, давай начнем сначала'
        send_text_to_user(update, answ_text)
        cithelp.create_user_db(user_filename, cithelp.get_etalon_cities_list())
