import os
import re

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload
from dotenv import load_dotenv

from FSM import *
from db.models import Account, Component, Entry
from keyboard import *
from phrases import *
from core import settings
from schemes import ComponentScheme

admin_router = Router(name='auth')


@admin_router.message(F.text == 'Компоненты')
async def components_handler(message: Message, state: FSMContext, telegram_id: int):
    if str(telegram_id) in settings.admin_id.split():
        component_scheme = ComponentScheme()
        await message.answer(text=components_text, reply_markup=ComponentsMainKeyboard(component_scheme.groups))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'main_components'))
async def main_components_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AuthCallback):
    component_scheme = ComponentScheme()
    await callback.message.edit_text(text=components_text, reply_markup=ComponentsMainKeyboard(component_scheme.groups))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'group_components'))
async def group_components_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    group = callback_data.params
    components = await Component.get_group(group=group)
    await callback.message.edit_text(text=group_components_text, reply_markup=GroupComponentsKeyboard(components))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'view_component'))
async def view_component_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    component_id = callback_data.params
    component = await Component(id=component_id).get()

    await callback.message.edit_text(text=view_component_text(component), reply_markup=ViewComponentKeyboard(component))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'hide_component'))
async def hide_component_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    component_id = callback_data.params
    component = await (await Component(id=component_id).update(hide=True)).get()
    print(component.hide)
    await callback.message.edit_text(text=view_component_text(component), reply_markup=ViewComponentKeyboard(component))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'show_component'))
async def show_component_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    component_id = callback_data.params
    component = await (await Component(id=component_id).update(hide=False)).get()
    await callback.message.edit_text(text=view_component_text(component), reply_markup=ViewComponentKeyboard(component))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'edit_component_name'))
async def edit_component_name_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    component_id = callback_data.params
    await state.set_state(ComponentUpdate.name)
    await state.update_data(component_id=component_id)
    await callback.message.edit_text(text=edit_component_name_text)


@admin_router.message(ComponentUpdate.name)
async def final_edit_component_name_handler(message: Message, state: FSMContext, telegram_id: int):
    name = message.text
    data = await state.get_data()
    component_id = data['component_id']
    component = await (await Component(id=component_id).update(name=name)).get()
    await message.answer(text=view_component_text(component), reply_markup=ViewComponentKeyboard(component))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'edit_component_price'))
async def edit_component_price_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    component_id = callback_data.params
    await state.set_state(ComponentUpdate.price)
    await state.update_data(component_id=component_id)
    await callback.message.edit_text(text=edit_component_price_text)


@admin_router.message(ComponentUpdate.price)
async def final_edit_component_price_handler(message: Message, state: FSMContext, telegram_id: int):
    price = int(message.text)
    data = await state.get_data()
    component_id = data['component_id']
    component = await (await Component(id=component_id).update(price=price)).get()
    await message.answer(text=view_component_text(component), reply_markup=ViewComponentKeyboard(component))


@admin_router.message(F.text == 'Добавить компонент')
async def select_group_handler(message: Message, state: FSMContext, telegram_id: int):
    component_scheme = ComponentScheme()
    await message.answer(text=select_group_text, reply_markup=SelectGroupKeyboard(component_scheme.groups))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'select_group'))
async def select_name_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    group = callback_data.params
    await state.set_state(ComponentForm.group)
    await state.update_data(group=group)
    await callback.message.edit_text(text=select_name_text)


@admin_router.message(ComponentForm.group)
async def select_price_handler(message: Message, state: FSMContext, telegram_id: int):
    name = message.text
    await state.set_state(ComponentForm.name)
    await state.update_data(name=name)
    await message.answer(text=select_price_text)


@admin_router.message(ComponentForm.name)
async def create_component_handler(message: Message, state: FSMContext, telegram_id: int):
    price = message.text
    data = await state.get_data()
    component = await Component(name=data['name'], price=price, group=data['group']).create()
    component_scheme = ComponentScheme()
    await message.answer(text=create_text(component), reply_markup=SelectGroupKeyboard(component_scheme.groups))
    await state.clear()


@admin_router.message(F.text == 'Заказы в очереди')
async def main_entries_handler(message: Message, state: FSMContext, telegram_id: int):
    if str(telegram_id) in settings.admin_id.split():
        entries = await Entry().get_multi()
        row_page = 3
        total_pages = len(entries) // row_page + 1 if len(entries) % row_page != 0 else len(
            entries) // row_page
        if len(entries) == 0:
            return await message.answer(text=main_not_entries_text)
        await message.answer(text=main_entries_text, reply_markup=MainEntriesKeyboard(entries=entries, row_page=row_page, page=1, total_pages=total_pages))


@admin_router.message(F.text == 'Завершенные заказы')
async def main_completed_entries_handler(message: Message, state: FSMContext, telegram_id: int):
    if str(telegram_id) in settings.admin_id.split():
        entries = await Entry().get_multi(completed=True)
        row_page = 3
        total_pages = len(entries) // row_page + 1 if len(entries) % row_page != 0 else len(
            entries) // row_page
        if len(entries) == 0:
            return await message.answer(text=admin_not_completed_entries_text)
        await message.answer(text=admin_completed_entries_text,
                                         reply_markup=AdminCompletedEntriesKeyboard(entries=entries, row_page=row_page, page=1, total_pages=total_pages))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'view_entry'))
async def view_entry_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    entry = await Entry(id=callback_data.params).get()
    component_dict = await entry.get_components_dict()
    await callback.message.edit_text(text=admin_view_entry_text(entry, component_dict), reply_markup=AdminViewEntryKeyboard(entry.id))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'delete_entry'))
async def delete_entry_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    entry = await Entry(id=callback_data.params).get()
    await entry.delete()
    entries = await Entry().get_multi()
    row_page = 3
    total_pages = len(entries) // row_page + 1 if len(entries) % row_page != 0 else len(
        entries) // row_page
    if len(entries) == 0:
        return await callback.message.edit_text(text=main_not_entries_text)
    await callback.message.edit_text(text=main_entries_text,
                         reply_markup=MainEntriesKeyboard(entries=entries, row_page=row_page, page=1,
                                                          total_pages=total_pages))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'complete_entry'))
async def complete_entry_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    entry = await Entry(id=callback_data.params).get()
    await entry.complete()
    entries = await Entry().get_multi()
    row_page = 3
    total_pages = len(entries) // row_page + 1 if len(entries) % row_page != 0 else len(
        entries) // row_page
    if len(entries) == 0:
        return await callback.message.edit_text(text=main_not_entries_text)
    await callback.message.edit_text(text=main_entries_text,
                                     reply_markup=MainEntriesKeyboard(entries=entries, row_page=row_page, page=1,
                                                                      total_pages=total_pages))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'completed_entries'))
async def completed_entries_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    row_page = 3
    entries = await Entry().get_multi(completed=True)
    page = int(callback_data.params)
    total_pages = len(entries) // row_page + 1 if len(entries) % row_page != 0 else len(
        entries) // row_page
    if page < 1 or page > total_pages:
        return await callback.answer()
    if len(entries) == 0:
        return await callback.message.edit_text(text=admin_not_completed_entries_text)
    await callback.message.edit_text(text=admin_completed_entries_text, reply_markup=AdminCompletedEntriesKeyboard(entries=entries, page=page, total_pages=total_pages, row_page=row_page))


@admin_router.callback_query(AdminCallback.filter(F.menu == 'view_completed_entry'))
async def view_completed_entry_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    entry = await Entry(id=callback_data.params).get()
    component_dict = await entry.get_components_dict()
    await callback.message.edit_text(text=admin_view_completed_entry_text(entry, component_dict), reply_markup=AdmimViewCompletedEntryKeyboard())


@admin_router.callback_query(AdminCallback.filter(F.menu == 'main_entries'))
async def main_entries_handler(callback: CallbackQuery, state: FSMContext, telegram_id: int, callback_data: AdminCallback):
    row_page = 3
    entries = await Entry().get_multi()
    page = int(callback_data.params)
    total_pages = len(entries) // row_page + 1 if len(entries) % row_page != 0 else len(
        entries) // row_page
    if page < 1 or page > total_pages:
        return await callback.answer()
    if len(entries) == 0:
        return await callback.message.edit_text(text=main_not_entries_text)
    await callback.message.edit_text(text=main_entries_text, reply_markup=MainEntriesKeyboard(entries=entries, page=page, total_pages=total_pages, row_page=row_page))


