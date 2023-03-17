from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Update


#Генератор кравиатуры из списка

def inline_keyboard_generator(commands_list) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup(row_width=2)
    for item in commands_list:
        inline_kb.add(InlineKeyboardButton(text=item[1], callback_data=item[0]))
    return inline_kb


def inline_keyboard_yn() -> InlineKeyboardMarkup:
    '''Клавиатура да/нет'''

    inline_kb = InlineKeyboardMarkup(row_width=2)
    key_yes = InlineKeyboardButton('Да', callback_data=True)
    key_no = InlineKeyboardButton('Нет', callback_data=False)
    inline_kb.add(key_yes, key_no)
    return inline_kb

