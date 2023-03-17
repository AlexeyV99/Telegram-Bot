from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMLowprice(StatesGroup):
    city_dict = State()
    city = State()
    hotel_num = State()
    foto = State()
