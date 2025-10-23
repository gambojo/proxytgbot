from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Главное меню админа
def get_admin_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="👥 Управление пользователями", callback_data="admin_users")],
        [InlineKeyboardButton(text="🔧 Тест протоколов", callback_data="admin_test")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="admin_settings")],
        [InlineKeyboardButton(text="🔙 В главное меню", callback_data="main_menu")]
    ])


# Меню статистики
def get_admin_stats_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Обновить статистику", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📈 Детальная статистика", callback_data="admin_stats_detailed")],
        [InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_panel")]
    ])


# Меню управления пользователями
def get_admin_users_menu(page: int = 1):
    keyboard = [
        [InlineKeyboardButton(text="📋 Список пользователей", callback_data=f"admin_users_list_{page}")],
    ]

    # Кнопки пагинации
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(text="◀️ Назад", callback_data=f"admin_users_list_{page - 1}"))

    pagination_buttons.append(InlineKeyboardButton(text=f"{page}", callback_data="current_page"))

    # Здесь можно добавить кнопку "Вперед" когда будет реализована проверка has_next
    if len(pagination_buttons) > 1:  # Если есть кнопка "Назад"
        keyboard.append(pagination_buttons)

    keyboard.append([InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_panel")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


# Меню тестирования протоколов
def get_admin_test_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔐 Тест VLESS", callback_data="admin_test_vless")],
        [InlineKeyboardButton(text="🔐 Тест VMess", callback_data="admin_test_vmess")],
        [InlineKeyboardButton(text="🔐 Тест Shadowsocks", callback_data="admin_test_shadowsocks")],
        [InlineKeyboardButton(text="🔐 Тест Trojan", callback_data="admin_test_trojan")],
        [InlineKeyboardButton(text="🔙 В админ-панель", callback_data="admin_panel")]
    ])
