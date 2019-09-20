[![Build Status](https://travis-ci.org/arkuz/tm_bot.svg?branch=master)](https://travis-ci.org/arkuz/tm_bot)
#### Описание
Данный репозиторий содержит тестовый проект - телеграм бот. Бот выполняет несколько простых действий и логирует свою работу в файл `bot.log`.

#### Команды
 - `/weather Москва` - узнать температуру в городе
 - `/wordcount привет, как дела?` - узнать количество слов в введенном сообщении
 - Так же бот умеет Отвечать пользователю его же сообщениями

#### Структура проекта
 - bot.py - основной скрипт бота
 - actions.py - описание действий бота
 - owm_helpers.py - файл для вспомогательных функций owm
 - messages_helpers.py - файл для вспомогательных функций для работы с сообщениями
 
#### Требования к ПО
- Установленный Python 3.7
- Установленный инструмент для работы с виртуальными окружениями virtualenv
```bash
pip install virtualenv
```

#### Установка
```bash
git clone https://github.com/arkuz/tm_bot
cd tm_bot
virtualenv env
env/scripts/activate
pip install -r requirements.txt
```

#### Запуск

Перед запуском бота необходимо заполнить переменные окружения с настройками ключей API и прокси.
 - API_KEY - ключ для телеграм бота
 - URL - адрес прокси
 - USERNAME - имя пользователя для прокси
 - PASSWORD - пароль для прокси
 - WEATHER_API_KEY - ключ для сервиса погоды https://openweathermap.org
 - WORD_LEN - длина слова, используется для `/wordcount`, опциональный параметр, если не указывать, то по умолчанию равен 2
```bash
set API_KEY=000000000:AAAAAAAAAAAAAAAAAAAAA
set URL=socks5://testserver.ru:1080
set USERNAME=user
set PASSWORD=pass
set WEATHER_API_KEY=aaaaaaaaaaaaaaaaaaaaaaaa
set WORD_LEN=3
python bot.py
```
