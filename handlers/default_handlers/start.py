from telebot.types import Message
from loader import bot
from database.sqlite_db_loader import db_loader


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
