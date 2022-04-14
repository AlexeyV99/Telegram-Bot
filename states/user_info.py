from telebot.handler_backends import State, StatesGroup

'''
UserInfoState:
    [user_country]      страна
    [user_city]         город
    [user_hotel_num]    кол-во отелей
    [user_foto]         фото
'''


class UserInfoState(StatesGroup):
    user_country = State()
    user_city = State()
    user_hotel_num = State()
    user_foto = State()
