from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    user_city = State()
    user_hotel_num = State()
    user_foto = State()
