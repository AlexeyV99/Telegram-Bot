from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import Dispatcher
from loader import bot                              # импортируем диспатчер и бота
from config_data.config import FUNNY_ECHO_ANSWERS   # импорт эхо-команд
import random                                       # для генерации случайных ответов в эхо-хэндлер
from loguru import logger
from keyboards.inline_kb import inline_keyboard_help, inline_keyboard_default


# костыль! если это команда - удаляет предыдущее сообщение, если Колбэк - отвечает ))
async def is_command(message: Message):
    if len(dict(message)) == 6:
        await message.delete()
    else:
        await message.answer()


async def bot_start(message: Message):
    """
    Ответ на команду start
    :param message:
    :return:
    """
    await is_command(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "start"')
    await bot.send_message(message.from_user.id,
                           f"Привет, <b>{message.from_user.full_name}</b>!\n"
                           f"Этот бот умеет собирать информацию!",
                           parse_mode='html',
                           reply_markup=inline_keyboard_help())


async def bot_help(message: Message):
    """
    Ответ на команду help
    :param message:
    :return:
    """
    await is_command(message)
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) выполнил команду "help"')
    await bot.send_message(message.from_user.id, f"Команды бота:\n", parse_mode='html',
                           reply_markup=inline_keyboard_default())


async def bot_echo(message: Message) -> None:
    """
    Эхо-хэндлер, куда летят текстовые сообщения без указанного состояния
    :param message:
    :return:
    """
    logger.info(f'Пользователь {message.from_user.full_name}({message.from_user.id}) написал {message.text}!')
    answer = FUNNY_ECHO_ANSWERS[random.randint(1, len(FUNNY_ECHO_ANSWERS))]
    await bot.send_message(message.from_user.id, answer, reply_markup=inline_keyboard_help())


def register_default_handlers(disp: Dispatcher) -> None:
    disp.register_message_handler(bot_start, commands=['start'])
    disp.register_callback_query_handler(bot_start, text=['/start'])
    disp.register_message_handler(bot_help, commands=['help'])
    disp.register_callback_query_handler(bot_help, text=['/help'])
    disp.register_message_handler(bot_echo)

