#### Описание
Данный репозиторий содержит тестовый проект - телеграм бот. Бот отправляет пользователю его же сообщение. Команда `/weather Moscow` возвращает температуру в указанном городе. Работа бота логируется и сохраняется в файл `bot.log`.

#### Структура проекта
 - bot.py - основной скрипт бота
 - actions.py - описание действий бота
 - config.py - настройки подключения к боту 
 
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
```bash
python bot.py
```
