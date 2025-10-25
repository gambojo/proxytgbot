from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_vpn_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛡 Создать VPN", callback_data="vpn:create")],
            [InlineKeyboardButton(text="📄 Мои VPN", callback_data="vpn:list")],
            [InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu_main")]
        ]
    )

def get_duration_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 день", callback_data="vpn:duration:1d")],
            [InlineKeyboardButton(text="7 дней", callback_data="vpn:duration:7d")],
            [InlineKeyboardButton(text="30 дней", callback_data="vpn:duration:30d")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )

def get_vpn_confirm_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="vpn:confirm")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel")]
        ]
    )
