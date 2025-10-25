from typing import Callable

_plugins: dict[str, Callable] = {}

def register_plugin(name: str, entry_callback: Callable):
    """
    Регистрирует плагин с его точкой входа.
    name — название (например, 'VPN')
    entry_callback — функция-хендлер, вызываемая при выборе
    """
    _plugins[name] = entry_callback

def get_registered_plugins() -> dict[str, Callable]:
    return _plugins
