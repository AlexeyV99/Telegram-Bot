from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Dispatcher
from loader import bot                              # импортируем диспатчер и бота
from config_data.config import DEFAULT_COMMANDS     # импорт команд по умолчанию
from config_data.config import FUNNY_ECHO_ANSWERS   # импорт эхо-команд
import random                                       # для генерации случайных ответов в эхо-хэндлер
from loguru import logger
from keyboards.reply_kb import kb_help


# Ответ на команду start
async def bot_start(message: Message):
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "start"')
    await bot.send_message(message.from_user.id,
                           f"Привет, <b>{message.from_user.full_name}</b>!\n"
                           f"Этот бот умеет собирать информацию!\n"
                           f"Ознакомься с его командами: /help",
                           parse_mode='html',
                           reply_markup=ReplyKeyboardRemove())
    # await bot_help(message)


# Ответ на команду help
async def bot_help(message: Message):
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "help"')
    text = [f'/{command} - {desk}' for command, desk in DEFAULT_COMMANDS]
    text2 = '\n'.join(text)
    await bot.send_message(message.from_user.id, f"<b><u>Команды бота:</u></b>\n{text2}", parse_mode='html', reply_markup=kb_help)


# Эхо-хэндлер, куда летят текстовые сообщения без указанного состояния
async def bot_echo(message: Message) -> None:
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) написал {message.text}!')
    answer = FUNNY_ECHO_ANSWERS[random.randint(1, len(FUNNY_ECHO_ANSWERS))]
    await bot.send_message(message.from_user.id, answer, reply_markup=ReplyKeyboardRemove())
    await bot_help(message)


# вместо декоратора @dp.message_handler()
def register_default_handlers(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
    dp.register_message_handler(bot_help, commands=['help'])
    dp.register_message_handler(bot_echo)

