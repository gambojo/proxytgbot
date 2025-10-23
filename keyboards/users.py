from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню
def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Услуги", callback_data="services")],
        [InlineKeyboardButton(text="👥 Пригласить", callback_data="referral")],
        [InlineKeyboardButton(text="📘 Инструкции", callback_data="instructions")],
        [InlineKeyboardButton(text="ℹ️ О сервисе", callback_data="about")]
    ])

# Меню услуг
def get_services_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔐 Подключить VLESS", callback_data="connect_vless")],
        [InlineKeyboardButton(text="🔐 Подключить VMess", callback_data="connect_vmess")],
        [InlineKeyboardButton(text="🔐 Подключить Shadowsocks", callback_data="connect_shadowsocks")],
        [InlineKeyboardButton(text="🔐 Подключить Trojan", callback_data="connect_trojan")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])

# Меню протокола (промежуточное)
def get_protocol_menu(protocol_name: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Получить строку подключения", callback_data=f"get_string_{protocol_name}")],
        [InlineKeyboardButton(text="📱 Получить QR-код", callback_data=f"get_qr_{protocol_name}")],
        [InlineKeyboardButton(text="🔙 Назад к услугам", callback_data="services")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")]
    ])

# Меню рефералов
def get_referral_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])

# Меню инструкций
def get_instructions_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="VLESS", callback_data="instruction_vless")],
        [InlineKeyboardButton(text="VMess", callback_data="instruction_vmess")],
        [InlineKeyboardButton(text="Shadowsocks", callback_data="instruction_shadowsocks")],
        [InlineKeyboardButton(text="Trojan", callback_data="instruction_trojan")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])

# Простая кнопка назад
def get_back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])

# Кнопка назад к услугам
def get_back_to_services():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад к услугам", callback_data="services")]
    ])
