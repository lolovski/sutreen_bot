import os
import re

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload
from dotenv import load_dotenv
from sqlalchemy.util import await_only

from FSM import *
from db.models import Account, Component, Entry
from keyboard import *
from phrases import *
from core import settings
from schemes import ComponentScheme

entry_router = Router(name='entry')


@entry_router.message(F.text == 'Актуальные заказы')
async def actuality_entries_handler(message: Message, state: FSMContext, telegram_id: int):
    actuality_entries = await Entry(client_id=telegram_id).get_client()
    row_page = 3
    total_pages = len(actuality_entries) // row_page + 1 if len(actuality_entries) % row_page != 0 else len(actuality_entries) // row_page
    if len(actuality_entries) == 0:
        return await message.answer(text=not_actuality_entries_text)
    await message.answer(text=actuality_entries_text, reply_markup=ActualityEntriesKeyboard(actuality_entries, row_page=row_page, total_pages=total_pages, page=1))


@entry_router.message(F.text == 'Выполненные заказы')
async def completed_entries_handler(message: Message, state: FSMContext, telegram_id: int):
    completed_entries = await Entry(client_id=telegram_id).get_client(completed=True)
    row_page = 3
    total_pages = len(completed_entries) // row_page + 1 if len(completed_entries) % row_page != 0 else len(
        completed_entries) // row_page
    if len(completed_entries) == 0:
        return await message.answer(text=not_completed_entries_text)
    await message.answer(text=completed_entries_text, reply_markup=CompletedEntriesKeyboard(completed_entries, row_page=row_page, total_pages=total_pages, page=1))


@entry_router.callback_query(EntryCallback.filter(F.menu == 'view_entry'))
async def view_entry_handler(callback: CallbackQuery, callback_data: EntryCallback, state: FSMContext):
    entry = await Entry(id=callback_data.params).get()
    place = await entry.get_place()
    component_dict = await entry.get_components_dict()
    await callback.message.edit_text(text=view_entry_text(entry, place, component_dict), reply_markup=ViewEntryKeyboard(entry))


@entry_router.callback_query(EntryCallback.filter(F.menu == 'completed_entries'))
async def completed_entries_callback_handler(callback: CallbackQuery, callback_data: EntryCallback, state: FSMContext, telegram_id: int):
    row_page = 3
    completed_entries = await Entry(client_id=telegram_id).get_client(completed=True)
    page = int(callback_data.params)
    total_pages = len(completed_entries) // row_page + 1 if len(completed_entries) % row_page != 0 else len(completed_entries) // row_page
    if page < 1 or page > total_pages:
        return await callback.answer()
    if len(completed_entries) == 0:
        return await callback.message.edit_text(text=not_completed_entries_text)
    await callback.message.edit_text(text=completed_entries_text, reply_markup=CompletedEntriesKeyboard(completed_entries, row_page=row_page, total_pages=total_pages, page=1))


@entry_router.callback_query(EntryCallback.filter(F.menu == 'view_completed_entry'))
async def view_completed_entry_handler(callback: CallbackQuery, callback_data: EntryCallback, state: FSMContext):
    completed_entry = await Entry(id=callback_data.params).get()
    component_dict = await completed_entry.get_components_dict()
    await callback.message.edit_text(text=view_completed_entry_text(completed_entry, component_dict), reply_markup=ViewCompletedEntryKeyboard())


@entry_router.callback_query(EntryCallback.filter(F.menu == 'actuality_entries'))
async def actuality_entries_callback_handler(callback: CallbackQuery, callback_data: EntryCallback, state: FSMContext, telegram_id: int):
    row_page = 3
    actuality_entries = await Entry(client_id=telegram_id).get_client()
    page = int(callback_data.params)
    total_pages = len(actuality_entries) // row_page + 1 if len(actuality_entries) % row_page != 0 else len(actuality_entries) // row_page
    if page < 1 or page > total_pages:
       return await callback.answer()
    if len(actuality_entries) == 0:
        return await callback.message.edit_text(text=not_actuality_entries_text)
    await callback.message.edit_text(text=actuality_entries_text, reply_markup=ActualityEntriesKeyboard(actuality_entries, page=page, total_pages=total_pages, row_page=row_page))


@entry_router.callback_query(EntryCallback.filter(F.menu == 'delete_entry'))
async def delete_entry_handler(callback: CallbackQuery, callback_data: EntryCallback, state: FSMContext, telegram_id: int, bot: Bot):
    entry = await Entry(id=callback_data.params).get()
    await entry.delete()
    row_page = 3
    actuality_entries = await Entry(client_id=telegram_id).get_client()
    page = 1
    total_pages = len(actuality_entries) // row_page + 1 if len(actuality_entries) % row_page != 0 else len(
        actuality_entries) // row_page
    await bot.send_message(chat_id=settings.admin_id, text=entry_deleted_text(entry))
    if len(actuality_entries) == 0:
        return await callback.message.edit_text(text=entry_deleted_text(entry))
    await callback.message.edit_text(text=entry_deleted_text(entry),
                                     reply_markup=ActualityEntriesKeyboard(actuality_entries, page=page,
                                                                           total_pages=total_pages, row_page=row_page))

