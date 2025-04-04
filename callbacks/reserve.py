from aiogram.filters.callback_data import CallbackData


class ReserveCallback(CallbackData, prefix='reserve'):
    menu: str
    params: str | None | int = None