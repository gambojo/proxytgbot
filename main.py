from aiogram import Bot, Dispatcher
import asyncio
import logging

from handlers.users import router as users_router
from handlers.admins import router as admin_router
from databases.postgres import db
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)


async def main():
    # Инициализируем базу данных
    await db.init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # ПОДКЛЮЧАЕМ ХЕНДЛЕРЫ
    dp.include_router(users_router)
    dp.include_router(admin_router)

    logging.info("Бот запущен!")

    try:
        await dp.start_polling(bot)
    finally:
        await db.close()


if __name__ == "__main__":
    asyncio.run(main())