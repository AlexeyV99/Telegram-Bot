from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config_data.config import DEFAULT_COMMANDS


#Генератор кравиатуры из списка
def inline_keyboard_generator(commands_list) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for item in commands_list:
        inline_kb.add(InlineKeyboardButton(text=item[1], callback_data=item[0]))
    return inline_kb


def inline_keyboard_help() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Команды бота', callback_data='/help'))
    return inline_kb


def inline_keyboard_default() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()
    for item in DEFAULT_COMMANDS:
        inline_kb.add(InlineKeyboardButton(text=item[1], callback_data="/" + item[0]))
    return inline_kb


def inline_keyboard_history(history) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for item in history:
        inline_kb.add(InlineKeyboardButton(text=item[1], callback_data=item[0]))
    return inline_kb


def kb_cities(cities) -> InlineKeyboardMarkup:
    """
    Клавиатура городов
    :param cities:
    :return:
    """
    inline_kb = InlineKeyboardMarkup()
    for i_code, i_city in cities.items():
        i_button = InlineKeyboardButton(i_city, callback_data=i_code)
        inline_kb.add(i_button)
    return inline_kb



def inline_keyboard_yn() -> InlineKeyboardMarkup:
    '''Клавиатура да/нет'''
    inline_kb = InlineKeyboardMarkup(row_width=2)
    key_yes = InlineKeyboardButton('Да', callback_data='True')
    key_no = InlineKeyboardButton('Нет', callback_data='False')
    inline_kb.add(key_yes, key_no)
    return inline_kb

