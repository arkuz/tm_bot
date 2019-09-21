import pytest

import wordcount_helpers as wh


@pytest.mark.parametrize('text,word_count', [
    ([], -1),
    (['4355345' '*&%(*%', '0', 'р45345'], 0),
    (['привет', 'как', 'дела?'], 3),
])
def test_get_word_count(text, word_count):
    assert wh.get_word_count(text) == word_count


@pytest.mark.parametrize('code,text', [
    (-1, 'Вы ввели пустую строку'),
    (0, 'Я не вижу слов в вашем предложении'),
])
def test_get_answer_text_static_code(code, text):
    assert wh.get_answer_text(code) == text


@pytest.mark.parametrize('code', [
    1, 55, 999,
])
def test_get_answer_text_dynamic_code(code):
    assert wh.get_answer_text(code) == f'Количество слов в вашем предложении = {code}'
