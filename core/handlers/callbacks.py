from aiogram import Router
from aiogram.types import CallbackQuery

from core.keyboards import dynamic as kd, static as ks
from core.keyboards.static import get_main_menu_inline  # 🔹 ЭТО НУЖНО
from core.plugins.registry import get_registered_plugins
from databases.crud import get_user_by_telegram_id

router = Router(name="core_callbacks")

@router.callback_query(lambda c: c.data == "menu_main")
async def handle_main_menu(callback: CallbackQuery):
    await callback.message.edit_text("🏠 Главное меню", reply_markup=get_main_menu_inline())

@router.callback_query(lambda c: c.data == "menu_services")
async def handle_services(callback: CallbackQuery):
    plugin_names = list(get_registered_plugins().keys())
    keyboard = kd.get_services_keyboard(plugin_names)
    await callback.message.edit_text("📦 Выберите услугу:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "menu_profile")
async def handle_profile(callback: CallbackQuery):
    user = await get_user_by_telegram_id(callback.from_user.id)
    text = f"👤 {user.first_name} @{user.username or '—'}\nРоль: {user.role}"
    await callback.message.edit_text(text, reply_markup=get_main_menu_inline())

@router.callback_query(lambda c: c.data == "confirm")
async def handle_confirm(callback: CallbackQuery):
    await callback.message.edit_text("✅ Действие подтверждено.")

@router.callback_query(lambda c: c.data == "cancel")
async def handle_cancel(callback: CallbackQuery):
    await callback.message.edit_text("❌ Действие отменено.")

@router.callback_query(lambda c: c.data == "back")
async def handle_back(callback: CallbackQuery):
    await callback.message.edit_text("🔙 Назад", reply_markup=get_main_menu_inline())
