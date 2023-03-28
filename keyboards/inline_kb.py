from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config_data.config import DEFAULT_COMMANDS


#Генератор кравиатуры из списка
def inline_keyboard_generator(commands_list) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for item in commands_list:
        inline_kb.add(InlineKeyboardButton(text=item[1], callback_data=item[0]))
    return inline_kb


# клавиатура - одна кнопка help
def inline_keyboard_help() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Команды бота', callback_data='/help'))
    return inline_kb


# клавиатура - одна кнопка - ссылка на отель
def inline_keyboard_link(link: str) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup().add(InlineKeyboardButton(text='Ссылка на отель', url=link))
    return inline_kb


# клавиатура команд по умолчанию (из DEFAULT_COMMANDS)
def inline_keyboard_default() -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()
    for item in DEFAULT_COMMANDS:
        inline_kb.add(InlineKeyboardButton(text=item[1], callback_data="/" + item[0]))
    return inline_kb


# клавиатура истории запросов
# def inline_keyboard_history(history: dict) -> InlineKeyboardMarkup:
#     inline_kb = InlineKeyboardMarkup(row_width=2)
#     print(history)
#     for i_code, i_value in history.items():
#         text = f'{i_value["time"]} {i_value["request"]} {i_value["city"]}'
#         inline_kb.add(InlineKeyboardButton(text=text, callback_data='hist_' + str(i_code)))
#     return inline_kb


# Клавиатура городов
def kb_cities(cities) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()
    for i_code, i_city in cities.items():
        i_button = InlineKeyboardButton(i_city, callback_data=i_code)
        inline_kb.add(i_button)
    inline_kb.add(InlineKeyboardButton(text='== ОТМЕНА ==', callback_data='cancel'))
    return inline_kb
