#### Описание
Данный репозиторий содержит тестовый проект - телеграм бот. Бот отправляет пользователю его же сообщение. Команда `/weather Moscow` возвращает температуру в указанном городе. Работа бота логируется и сохраняется в файл `bot.log`.

#### Структура проекта
 - bot.py - основной скрипт бота
 - actions.py - описание действий бота
 - tools.py - файл для вспомогательных функций
 
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
```bash
set API_KEY=000000000:AAAAAAAAAAAAAAAAAAAAA
set URL=socks5://testserver.ru:1080
set USERNAME=user
set PASSWORD=pass
set WEATHER_API_KEY=aaaaaaaaaaaaaaaaaaaaaaaa
python bot.py
```
