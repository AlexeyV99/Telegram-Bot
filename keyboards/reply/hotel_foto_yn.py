from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def request_hotel_foto_yn() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(KeyboardButton('Да'))
    keyboard.add(KeyboardButton('Нет'))
    return keyboard
