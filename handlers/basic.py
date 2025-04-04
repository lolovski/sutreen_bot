import os

from aiogram import Router, Bot
from dotenv import load_dotenv
from core import settings

basic_router = Router(name='basic')


@basic_router.startup()
async def on_startup(bot: Bot):
    from core.commands import set_commands
    await set_commands(bot)
    for admin_id in settings.admin_id.split():
        await bot.send_message(admin_id, text=f'Бот запустился в работу!')


@basic_router.shutdown()
async def on_shutdown(bot: Bot):
    for admin_id in settings.admin_id.split():
        await bot.send_message(admin_id, text=f'БОТ ЛЁГ!')
    ...