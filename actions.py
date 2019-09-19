import owm_helpers
import re
from messages_helpers import send_text_to_user


def start_comand_handler(bot, update):
    """ Функция отправляет ответ на команду /start. """
    answ_text = 'Я умею:\n' \
                '1. /weather Москва - узнать температуру в городе\n' \
                '2. /wordcount привет, как дела? - узнать количество слов в введенном сообщении\n' \
                '3. А можете просто мне написать и я отвечу вам вашим же сообщением :-)'
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
        count = 0
        for arg in args:
            arg = re.sub(r'([^a-zA-zа-яА-Я]+)', '', arg) # удаляем все, кроме букв
            if len(arg) > 1: # если в длина строки в arg больше 1 буквы, то считать словом
                count += 1
        if count != 0:
            answ_text = f'Количество слов в вашем предложении = {count}'
        else:
            answ_text = 'Я не вижу слов в вашем предложении'
    else:
        answ_text = 'Вы ввели пустую строку'

    send_text_to_user(update, answ_text)

