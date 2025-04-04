from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from callbacks import *
from aiogram_inline_paginations.paginator import Paginator


def ActualityEntriesKeyboard(entries, page=1, row_page=3, total_pages=1):
    buttons = []
    i = min(page*row_page, len(entries))
    for entry in entries[(page-1)*row_page:i]:
        buttons.append([InlineKeyboardButton(text=entry.description,
                                             callback_data=EntryCallback(menu='view_entry', params=entry.id).pack())])
    if len(entries) > 0:
        buttons.append([
            InlineKeyboardButton(text=f'⬅️', callback_data=EntryCallback(menu='actuality_entries', params=page-1).pack()),
            InlineKeyboardButton(text=f'{page}/{total_pages}', callback_data=EntryCallback(menu='actuality_entries', params=-1).pack()),
            InlineKeyboardButton(text=f'➡️', callback_data=EntryCallback(menu='actuality_entries', params=page+1).pack())

        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def ViewEntryKeyboard(entry):
    buttons = [
        [InlineKeyboardButton(text='❌Отменить заказ', callback_data=EntryCallback(menu='delete_entry', params=entry.id).pack())],
        [InlineKeyboardButton(text='◀️Назад', callback_data=EntryCallback(menu='actuality_entries', params=1).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def CompletedEntriesKeyboard(entries, page=1, row_page=3, total_pages=1):
    buttons = []
    i = min(page*row_page, len(entries))
    for entry in entries[(page-1)*row_page:i]:
        buttons.append([InlineKeyboardButton(text=entry.description, callback_data=EntryCallback(menu='view_completed_entry', params=entry.id).pack())])
    if len(entries) > 0:
        buttons.append([
            InlineKeyboardButton(text=f'⬅️', callback_data=EntryCallback(menu='completed_entries', params=page - 1).pack()),
            InlineKeyboardButton(text=f'{page}/{total_pages}',
                                 callback_data=EntryCallback(menu='completed_entries', params=-1).pack()),
            InlineKeyboardButton(text=f'➡️', callback_data=EntryCallback(menu='completed_entries', params=page + 1).pack())
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def ViewCompletedEntryKeyboard():
    buttons = [
        [InlineKeyboardButton(text='◀️Назад', callback_data=EntryCallback(menu='completed_entries', params=1).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
