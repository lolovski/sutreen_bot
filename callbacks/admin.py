from aiogram.filters.callback_data import CallbackData


class AdminCallback(CallbackData, prefix='admin'):
    menu: str
    params: str | None | int = None