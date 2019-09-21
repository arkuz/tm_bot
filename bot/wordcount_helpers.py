import os
import re


def get_word_count(text):
    """ Функция возвращает количество слов в пользовательском сообщении. """
    if not text:
        return -1

    word_count = 0
    for word in text:
        word = re.sub(r'([^a-zA-zа-яА-Я]+)', '', word)  # удаляем все, кроме букв
        if len(word) >= int(os.getenv('WORD_LEN','2')):  # минимальное кол-во букв в слове, определяется переменной окружения WORD_LEN
            word_count += 1
    return word_count


def get_answer_text(code):
    """ Функция возвращает текст сообщения для ответа. """
    msg_dict = {
        -1: 'Вы ввели пустую строку',
        0: 'Я не вижу слов в вашем предложении',
    }
    if code in msg_dict:
        return msg_dict[code]
    return f'Количество слов в вашем предложении = {code}'

