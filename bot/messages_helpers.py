import logging


def send_text_to_user(update, answ_text):
    """ Функция отправляет пользователю сообщение и дублирует его в лог. """
    log_text = 'Пользователь: {user}, Чат ID: {chat_id}, Сообщение: {msg}, Ответ: {answ}'
    logging.info(log_text.format(
        user=update.message.chat.username,
        chat_id=update.message.chat.id,
        msg=update.message.text,
        answ=answ_text,
    ))
    update.message.reply_text(answ_text)
