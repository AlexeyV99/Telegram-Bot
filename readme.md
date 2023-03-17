# Описание проекта
Телеграм-бот для работы с API стороннего сайта.

# Установка
1. Клонируйте репозиторий с GitHub, создайте виртуальное окружение
и активируйте его:

$ git clone https://github.com/username/foobar.git
$ python3 -m venv env
$ source env/bin/activate


2. Установите библиотеки из файла requirements.txt:

$ pip install -r requirements.txt
или
$ python -m pip install -r requirements.txt


3. Переименуйте файл .env.template в .env и укажите в нем Ваш токен для бота
и ключ от API по образцу:

BOT_TOKEN = "Ваш токен для бота, полученный от @BotFather"
RAPID_API_KEY = "Ваш ключ полученный от API по адресу rapidapi.com/apidojo/api/hotels4/"

