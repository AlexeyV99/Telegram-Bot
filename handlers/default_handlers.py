from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Dispatcher
from loader import bot, dp                              # импортируем диспатчер и бота
from config_data.config import DEFAULT_COMMANDS     # импорт команд по умолчанию
from config_data.config import FUNNY_ECHO_ANSWERS   # импорт эхо-команд
import random                                       # для генерации случайных ответов в эхо-хэндлер
from loguru import logger
from keyboards.reply_kb import kb_help
from keyboards.inline_kb import inline_keyboard_help, inline_keyboard_default


# Ответ на команду start
@dp.callback_query_handler(text='/start')
async def bot_start(message: Message):
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "start"')
    await bot.send_message(message.from_user.id,
                           f"Привет, <b>{message.from_user.full_name}</b>!\n"
                           f"Этот бот умеет собирать информацию!",
                           parse_mode='html',
                           reply_markup=inline_keyboard_help())
    # await bot_help(message)


# Ответ на команду help
@dp.callback_query_handler(text='/help')
async def bot_help(message: Message):
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "help"')
    await bot.send_message(message.from_user.id, f"<b><u>Команды бота:</u></b>\n", parse_mode='html',
                           reply_markup=inline_keyboard_default())


# Эхо-хэндлер, куда летят текстовые сообщения без указанного состояния
async def bot_echo(message: Message) -> None:
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) написал {message.text}!')
    answer = FUNNY_ECHO_ANSWERS[random.randint(1, len(FUNNY_ECHO_ANSWERS))]
    await bot.send_message(message.from_user.id, answer, reply_markup=inline_keyboard_help())


# вместо декоратора @dp.message_handler()
def register_default_handlers(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'])
    dp.register_message_handler(bot_help, commands=['help'])
    dp.register_message_handler(bot_echo)

