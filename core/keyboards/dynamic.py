from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_services_keyboard(plugin_names: list[str]) -> InlineKeyboardMarkup:
    """
    Строит клавиатуру с кнопками для зарегистрированных плагинов.
    """
    buttons = [
        [InlineKeyboardButton(text=name, callback_data=f"plugin:{name}")]
        for name in plugin_names
    ]
    buttons.append([InlineKeyboardButton(text="🏠 Главное меню", callback_data="menu_main")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
