from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from core.keyboards.static import get_main_menu_inline

router = Router(name="start")

@router.message(CommandStart())
async def handle_start(msg: Message):
    await msg.answer("👋 Добро пожаловать!", reply_markup=get_main_menu_inline())
