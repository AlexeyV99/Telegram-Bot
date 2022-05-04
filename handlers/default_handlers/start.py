from telebot.types import Message
from loader import bot
from config_data.config import DEFAULT_COMMANDS
from handlers.default_handlers.help import bot_help


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    bot_help(message)
    
