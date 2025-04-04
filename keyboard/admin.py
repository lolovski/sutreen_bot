from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from callbacks import *


def AdminMenuKeyboard():
    buttons = [
        [
            KeyboardButton(text="Компоненты", callback_data=NavigationCallback(menu="components").pack()),
            KeyboardButton(text="Добавить компонент", callback_data=NavigationCallback(menu="add_component").pack()),
        ],
        [
            KeyboardButton(text="Заказы в очереди", callback_data=NavigationCallback(menu="admin_entries").pack()),
            KeyboardButton(text="Завершенные заказы", callback_data=NavigationCallback(menu="admin_completed_entries").pack())
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def ComponentsMainKeyboard(groups):
    buttons = []
    for group in groups:
        buttons.append([InlineKeyboardButton(text=group, callback_data=AdminCallback(menu="group_components", params=group).pack())])
    return InlineKeyboardMarkup(inline_keyboard=buttons,)

def GroupComponentsKeyboard(components):
    buttons = []
    for component in components:
        buttons.append([InlineKeyboardButton(text=component.name, callback_data=AdminCallback(menu="view_component", params=component.id).pack())])
    buttons.append([InlineKeyboardButton(text="◀️Назад", callback_data=AdminCallback(menu="main_components").pack())])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def ViewComponentKeyboard(component):
    buttons = [
        [InlineKeyboardButton(text='Скрыть', callback_data=AdminCallback(menu="hide_component", params=component.id).pack())] if not component.hide
        else [InlineKeyboardButton(text='Показать', callback_data=AdminCallback(menu="show_component", params=component.id).pack())],
        [InlineKeyboardButton(text="Изменить название", callback_data=AdminCallback(menu="edit_component_name", params=component.id).pack())],
        [InlineKeyboardButton(text="Изменить цену", callback_data=AdminCallback(menu="edit_component_price", params=component.id).pack())],
        [InlineKeyboardButton(text="◀️Назад", callback_data=AdminCallback(menu="group_components", params=component.group).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def SelectGroupKeyboard(groups):
    buttons = []
    for group in groups:
        buttons.append([InlineKeyboardButton(text=group, callback_data=AdminCallback(menu="select_group", params=group).pack())])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def MainEntriesKeyboard(entries, page=1, row_page=3, total_pages=1):
    buttons = []
    i = min(page * row_page, len(entries))
    for entry in entries[(page - 1) * row_page:i]:
        buttons.append([InlineKeyboardButton(text=f'{entry.id}: {entry.client.first_name}', callback_data=AdminCallback(menu='view_entry', params=entry.id).pack())])

    if len(entries) > 0:
        buttons.append([
            InlineKeyboardButton(text=f'⬅️', callback_data=AdminCallback(menu='main_entries', params=page-1).pack()),
            InlineKeyboardButton(text=f'{page}/{total_pages}', callback_data=AdminCallback(menu='main_entries', params=-1).pack()),
            InlineKeyboardButton(text=f'➡️', callback_data=AdminCallback(menu='main_entries', params=page+1).pack())

        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def AdminViewEntryKeyboard(entry_id):
    buttons = [
        [InlineKeyboardButton(text='Завершить', callback_data=AdminCallback(menu='complete_entry', params=entry_id).pack()),],
        [InlineKeyboardButton(text='Отменить', callback_data=AdminCallback(menu='delete_entry', params=entry_id).pack()),],
        [InlineKeyboardButton(text='Назад', callback_data=AdminCallback(menu='main_entries', params=1).pack())],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def AdminCompletedEntriesKeyboard(entries, page=1, row_page=3, total_pages=1):
    buttons = []
    i = min(page * row_page, len(entries))
    for entry in entries[(page - 1) * row_page:i]:
        buttons.append([InlineKeyboardButton(text=f'{entry.id}: {entry.client.first_name}', callback_data=AdminCallback(menu='view_completed_entry', params=entry.id).pack())])
    if len(entries) > 0:
        buttons.append([
            InlineKeyboardButton(text=f'⬅️', callback_data=AdminCallback(menu='completed_entries', params=page-1).pack()),
            InlineKeyboardButton(text=f'{page}/{total_pages}', callback_data=AdminCallback(menu='completed_entries', params=-1).pack()),
            InlineKeyboardButton(text=f'➡️', callback_data=AdminCallback(menu='completed_entries', params=page+1).pack())

        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def AdmimViewCompletedEntryKeyboard():
    buttons = [[InlineKeyboardButton(text='Назад', callback_data=AdminCallback(menu='completed_entries', params=1).pack())]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

