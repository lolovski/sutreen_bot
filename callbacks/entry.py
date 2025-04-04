from aiogram.filters.callback_data import CallbackData


class EntryCallback(CallbackData, prefix='entry'):
    menu: str
    params: str | None | int = None