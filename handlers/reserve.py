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
from db.models import Account, Component, Entry, EntryComponent
from keyboard import *
from phrases import *
from core import settings
from schemes import ComponentScheme


reserve_router = Router(name='reserve')


@reserve_router.message(F.text == 'Сделать заказ')
async def reserve_genre_handler(message: Message, state: FSMContext, telegram_id: int):
    await state.update_data(client_id=telegram_id)
    genres = await Component.get_group('Жанр')
    await message.answer(text=reserve_genre_text, reply_markup=ReserveCategoryKeyboard(genres, 'genre'))
    await state.set_state(ReserveForm.genre)


@reserve_router.callback_query(ReserveCallback.filter(F.menu == 'genre'))
async def reserve_canvas_handler(callback: CallbackQuery, callback_data: ReserveCallback, state: FSMContext):
    await state.update_data(genre=callback_data.params)
    canvases = await Component.get_group('Полотно')
    await callback.message.edit_text(text=reserve_canvas_text, reply_markup=ReserveCategoryKeyboard(canvases, 'canvas'))
    await state.set_state(ReserveForm.canvas)


@reserve_router.callback_query(ReserveCallback.filter(F.menu == 'canvas'))
async def reserve_material_handler(callback: CallbackQuery, callback_data: ReserveCallback, state: FSMContext):
    await state.update_data(canvas=callback_data.params)
    material = await Component.get_group('Материал')
    await callback.message.edit_text(text=reserve_material_text, reply_markup=ReserveCategoryKeyboard(material, 'material'))
    await state.set_state(ReserveForm.material)


@reserve_router.callback_query(ReserveCallback.filter(F.menu == 'material'))
async def reserve_description_handler(callback: CallbackQuery, callback_data: ReserveCallback, state: FSMContext):
    await state.update_data(material=callback_data.params)
    await callback.message.edit_text(text=reserve_description_text)
    await state.set_state(ReserveForm.description)


@reserve_router.message(ReserveForm.description)
async def reserve_contact_handler(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text=reserve_contact_text)
    await state.set_state(ReserveForm.contact)


@reserve_router.message(ReserveForm.contact)
async def reserve_confirm_handler(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    price = 0
    components = {}
    for component in ComponentScheme.english_groups:
        db_component = await Component(id=data[component]).get()
        price += db_component.price
        components[component] = db_component.name
    await state.update_data(price=price)
    data['price'] = price
    await message.answer(text=reserve_confirm_text(data=data, components=components), reply_markup=ReserveConfirmKeyboard())


@reserve_router.callback_query(ReserveCallback.filter(F.menu == 'confirm'))
async def reserve_confirm_handler(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    entry = await Entry(**data).create()
    for component in ComponentScheme.english_groups:
        entry_component = await EntryComponent(entry_id=entry.id, component_id=data[component]).create()
    place = await entry.get_place()
    await callback.message.edit_text(text=reserve_final_text(entry, place))
    for admin_id in settings.admin_id.split():
        await bot.send_message(chat_id=admin_id, text=new_reserve_text(data=data))
    await state.clear()



