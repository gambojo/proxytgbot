class AdminSystemService:
    @staticmethod
    async def get_system_settings():
        """Получение системных настроек"""
        return {
            "config_lifetime": 30,
            "max_connections": 5,
            "notifications": True,
            "auto_backup": "Каждые 24 часа"
        }

    @staticmethod
    async def format_system_settings(settings: dict) -> str:
        """Форматирование настроек системы"""
        return (
            "⚙️ **Настройки системы**\n\n"
            f"• Время жизни конфигов: {settings['config_lifetime']} дней\n"
            f"• Максимум подключений: {settings['max_connections']} на пользователя\n"
            f"• Уведомления: {'Включены' if settings['notifications'] else 'Выключены'}\n"
            f"• Авто-бэкап: {settings['auto_backup']}\n\n"
            "Изменить настройки можно в config.py"
        )
