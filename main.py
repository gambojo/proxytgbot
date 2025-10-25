import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from alembic.config import Config
from alembic import command

# Плагины
from plugins.vpn.handlers import router as vpn_router

# Настройки (если есть config.py)
from core.config import settings
from core.handlers import errors as error_handlers, callbacks as callback_router, start as start_handler
from core.middlewares import user_init_middleware
from databases.init_db import init

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    if settings.db_is_sqlite:
        print("⚠️ SQLite detected — skipping migrations")
    elif settings.db_is_postgres:
        await run_postgres_migrations()

    await init()
    dp = Dispatcher(storage=MemoryStorage())

    # Middleware
    dp.message.middleware(user_init_middleware())

    # Ядро: start
    dp.include_router(start_handler.router)

    # Ядро: системные callback'и
    dp.include_router(callback_router.router)

    # Плагины
    dp.include_router(vpn_router)

    # Обработка ошибок
    dp.include_router(error_handlers.router)

    # Запуск
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
