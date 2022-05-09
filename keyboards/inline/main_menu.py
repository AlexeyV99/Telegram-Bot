from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Update


 # список кнопок
button_list = [
    InlineKeyboardButton("col1", callback_data=...),
    InlineKeyboardButton("col2", callback_data=...),
    InlineKeyboardButton("row 2", callback_data=...)
]

# сборка клавиатуры из кнопок `InlineKeyboardButton`
reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))