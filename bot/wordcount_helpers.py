import os
import re


def get_word_count(word_list):
    """ Функция возвращает количество слов в пользовательском сообщении. """
    if not word_list:
        return -1

    word_count = 0
    for word in word_list:
        # удаляем все, кроме букв
        word = re.sub(r'([^a-zA-zа-яА-Я]+)', '', word)
        # минимальное кол-во букв в слове, определяется переменной окружения WORD_LEN
        if len(word) >= int(os.getenv('WORD_LEN', '2')):
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
