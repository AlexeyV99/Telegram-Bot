from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMLowprice(StatesGroup):
    step_1 = State()
    step_2 = State()
    step_3 = State()
    step_4 = State()
    step_5 = State()

