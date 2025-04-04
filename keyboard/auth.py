from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from callbacks import NavigationCallback, AuthCallback


def MainMenuKeyboard():
    buttons = [
        [
            KeyboardButton(text="Сделать заказ", callback_data=NavigationCallback(menu="reserve").pack()),
        ],
        [
            KeyboardButton(text="Актуальные заказы", callback_data=NavigationCallback(menu="entries").pack()),
            KeyboardButton(text="Выполненные заказы", callback_data=NavigationCallback(menu="entries").pack())
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def GetContactKeyboard():
    buttons = [
        [
            KeyboardButton(text="Отправить контакт", request_contact=True)
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)