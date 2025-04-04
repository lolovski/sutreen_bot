import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from fastapi import FastAPI

from core import settings
from middleware import UserMiddleware
from handlers import main_router

dp = Dispatcher()
bot = Bot(token=settings.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp.update.middleware.register(UserMiddleware(bot=bot))


async def main() -> None:
    # wait async_main()
    dp.include_router(main_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
