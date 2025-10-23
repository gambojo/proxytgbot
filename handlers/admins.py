from aiogram import Router, types, F
from aiogram.filters import Command
from config import is_admin
from keyboards.admins import (
    get_admin_menu,
    get_admin_stats_menu,
    get_admin_users_menu,
    get_admin_test_menu
)
from utils.admin_stats import AdminStatsService
from utils.admin_users import AdminUsersService
from utils.admin_protocols import AdminProtocolsService
from utils.admin_system import AdminSystemService


router = Router()


# Фильтр для проверки админа
async def admin_filter(message: types.Message | types.CallbackQuery) -> bool:
    user_id = message.from_user.id
    return is_admin(user_id)


# Команда админ-панели
@router.message(Command("admin"), admin_filter)
async def admin_handler(message: types.Message):
    keyboard = get_admin_menu()
    await message.answer("👨‍💻 Панель администратора:", reply_markup=keyboard)


# Главное меню админ-панели
@router.callback_query(F.data == "admin_panel", admin_filter)
async def admin_panel_handler(callback: types.CallbackQuery):
    keyboard = get_admin_menu()
    await callback.message.edit_text("👨‍💻 Панель администратора:", reply_markup=keyboard)
    await callback.answer()


# Статистика
@router.callback_query(F.data == "admin_stats", admin_filter)
async def admin_stats_handler(callback: types.CallbackQuery):
    stats = await AdminStatsService.get_basic_stats()
    text = await AdminStatsService.format_basic_stats(stats)

    keyboard = get_admin_stats_menu()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# Детальная статистика
@router.callback_query(F.data == "admin_stats_detailed", admin_filter)
async def admin_stats_detailed_handler(callback: types.CallbackQuery):
    stats = await AdminStatsService.get_detailed_stats()
    text = await AdminStatsService.format_detailed_stats(stats)

    keyboard = get_admin_stats_menu()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# Управление пользователями
@router.callback_query(F.data == "admin_users", admin_filter)
async def admin_users_handler(callback: types.CallbackQuery):
    text = "👥 **Управление пользователями**\n\nВыберите действие для работы с пользователями:"

    keyboard = get_admin_users_menu(page=1)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# Список пользователей с пагинацией
@router.callback_query(F.data.startswith("admin_users_list_"), admin_filter)
async def admin_users_list_handler(callback: types.CallbackQuery):
    # Извлекаем номер страницы из callback_data
    page_str = callback.data.replace("admin_users_list_", "")
    try:
        page = int(page_str)
    except ValueError:
        page = 1

    users_data = await AdminUsersService.get_users_list(page=page)
    text = await AdminUsersService.format_users_list(users_data)

    keyboard = get_admin_users_menu(page=page)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# Тестирование протоколов
@router.callback_query(F.data == "admin_test", admin_filter)
async def admin_test_handler(callback: types.CallbackQuery):
    text = (
        "🔧 **Тестирование протоколов**\n\n"
        "Протестируйте работу протоколов:\n"
        "Будут созданы тестовые конфиги для проверки"
    )

    keyboard = get_admin_test_menu()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# Тест протоколов (общий хендлер)
@router.callback_query(F.data.startswith("admin_test_"), admin_filter)
async def admin_test_protocol_handler(callback: types.CallbackQuery):
    protocol = callback.data.replace("admin_test_", "")
    user_id = str(callback.from_user.id)

    test_result = await AdminProtocolsService.test_protocol(protocol, user_id)
    text = await AdminProtocolsService.format_test_result(test_result)

    keyboard = get_admin_test_menu()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# Настройки
@router.callback_query(F.data == "admin_settings", admin_filter)
async def admin_settings_handler(callback: types.CallbackQuery):
    settings = await AdminSystemService.get_system_settings()
    text = await AdminSystemService.format_system_settings(settings)

    keyboard = get_admin_menu()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# Защита от не-админов
@router.message(Command("admin"))
async def admin_not_allowed(message: types.Message):
    await message.answer("❌ У вас нет доступа к админ-панели")


@router.callback_query(F.data.startswith("admin_"))
async def admin_not_allowed_callback(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Доступ запрещен", show_alert=True)
