import owm_helpers
from messages_helpers import send_text_to_user


def start_comand_handler(bot, update):
    """ Функция отправляет ответ на команду /start. """
    answ_text = 'Вот такой командой можно узнать погоду: /weather Москва'
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
