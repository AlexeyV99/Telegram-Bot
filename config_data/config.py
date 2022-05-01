import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('history', 'История запросов'),
    ('lowprice', 'Топ самых дешевых отелей'),
    ('user_info', 'Данные пользователя')
)

DB_NAME = 'bot_base.db'
HISTORY_NUM = 3

