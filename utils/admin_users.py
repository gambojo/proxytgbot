from databases.postgres import db


class AdminUsersService:
    @staticmethod
    async def get_users_list(limit: int = 10, page: int = 1):
        """Получение списка пользователей из БД с пагинацией"""
        all_users = await db.get_all_users()

        # Пагинация
        total_users = len(all_users)
        total_pages = (total_users + limit - 1) // limit  # Округление вверх
        offset = (page - 1) * limit

        users = all_users[offset:offset + limit]

        return {
            "users": users,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_users": total_users,
                "has_prev": page > 1,
                "has_next": page < total_pages
            }
        }

    @staticmethod
    async def format_users_list(users_data: dict) -> str:
        """Форматирование списка пользователей в текст с пагинацией"""
        users = users_data['users']
        pagination = users_data['pagination']

        if not users:
            return "📋 **Список пользователей**\n\nПользователи не найдены"

        users_text = "\n".join(
            [
                f"{i + 1}. {user.get('username', 'Без username')} (ID: {user['telegram_id']}) - {user.get('first_name', '')}"
                for i, user in enumerate(users)
            ]
        )

        pagination_text = (
            f"\n\n📄 Страница {pagination['current_page']} из {pagination['total_pages']} "
            f"(всего: {pagination['total_users']})"
        )

        return f"📋 **Последние пользователи**\n\n{users_text}{pagination_text}"
