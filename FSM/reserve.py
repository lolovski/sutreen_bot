from aiogram.fsm.state import StatesGroup, State


class ReserveForm(StatesGroup):
    client_id = State()
    genre = State()
    canvas = State()
    material = State()
    description = State()
    contact = State()
    price = State