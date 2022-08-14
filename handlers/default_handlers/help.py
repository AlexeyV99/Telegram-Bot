from telebot.types import Message
from config_data.config import DEFAULT_COMMANDS
from loader import bot
from keyboards.inline.inline_kb import inline_keyboard_generator

@bot.callback_query_handler(func=lambda c: c.data == 'help')
def bot_help2(message: Message):
    bot.send_message(message.from_user.id, "/help")



@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    text2 = '\n'.join(text)
    bot.send_message(message.from_user.id, f"Команды бота:\n{text2}", reply_markup = inline_keyboard_generator(DEFAULT_COMMANDS))

