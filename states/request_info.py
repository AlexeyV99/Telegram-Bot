from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMLowprice(StatesGroup):
    city = State()
    hotel_num = State()
    foto = State()
