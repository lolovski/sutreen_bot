from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from callbacks import *


def ReserveCategoryKeyboard(categories, category_name):
    buttons = []
    for category in categories:
        buttons.append([InlineKeyboardButton(text=category.name, callback_data=ReserveCallback(menu=f'{category_name}', params=category.id).pack())])
    return InlineKeyboardMarkup(inline_keyboard=buttons,)


def ReserveConfirmKeyboard():
    buttons = [
        [InlineKeyboardButton(text='Подтвердить✅', callback_data=ReserveCallback(menu='confirm', params='confirm').pack())],
        [InlineKeyboardButton(text='Отменить❌', callback_data=ReserveCallback(menu='cancel', params='cancel').pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)