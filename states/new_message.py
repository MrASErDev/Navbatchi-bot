from aiogram.dispatcher.filters.state import StatesGroup, State

class new_message(StatesGroup):
    msg = State()
    confirm = State()
