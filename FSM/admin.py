from aiogram.fsm.state import StatesGroup, State


class ComponentForm(StatesGroup):
    group = State()
    name = State()
    price = State()


class ComponentUpdate(StatesGroup):
    component_id = State()
    name = State()
    price = State()