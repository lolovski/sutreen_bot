from aiogram import Router

from .auth import auth_router
from .basic import basic_router
from .admin import admin_router
from .entry import entry_router
from .reserve import reserve_router


main_router = Router(name='main')
main_router.include_routers(
    auth_router,
    basic_router,
    admin_router,
    entry_router,
    reserve_router
)