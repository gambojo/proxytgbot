from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 Услуги", callback_data="menu_services")],
            [InlineKeyboardButton(text="ℹ️ Профиль", callback_data="menu_profile")]
        ]
    )

def get_confirm_cancel_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )

def get_back_to_main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu_main")]
        ]
    )

def get_back_button(callback: str = "back"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data=callback)]
        ]
    )
