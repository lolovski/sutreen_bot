import os
import re

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload
from dotenv import load_dotenv

from FSM import AuthForm
from db.models import Account
from keyboard import *
from phrases import *
from core import settings

auth_router = Router(name='auth')


@auth_router.message(CommandStart())
async def start_handler(message: Message, bot: Bot, command: CommandObject, telegram_id: int, state: FSMContext, first_name: str) -> None:
    await state.clear()
    if str(telegram_id) in settings.admin_id.split():
        return await message.answer(admin_start, reply_markup=AdminMenuKeyboard())
    user = await Account(telegram_id=telegram_id).get_account()
    if user is not None:
        await message.answer_sticker(welcome_sticker, reply_markup=MainMenuKeyboard())
        return await message.answer(start_text(first_name))
    if user is None:
        await message.answer(registration_text(first_name),
                             reply_markup=GetContactKeyboard())
        await state.set_state(AuthForm.contact)


@auth_router.message(AuthForm.contact)
async def get_contact_handler(message: Message, telegram_id: int, state: FSMContext, first_name: str) -> None:
    contact = message.contact.phone_number
    user = await Account(
        telegram_id=telegram_id,
        first_name=first_name,
        telephone=contact
    ).create()
    await message.answer_sticker(welcome_sticker, reply_markup=MainMenuKeyboard())
    await state.clear()
    return await message.answer(welcome_text(first_name))

