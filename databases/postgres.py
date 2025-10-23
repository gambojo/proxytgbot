import asyncpg
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def init_db(self):
        """Инициализация подключения к базе данных"""
        try:
            from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

            self.pool = await asyncpg.create_pool(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            logger.info("✅ PostgreSQL подключена успешно")

            # Создаем таблицу если не существует
            await self._create_tables()

        except Exception as e:
            logger.error(f"❌ Ошибка подключения к PostgreSQL: {e}")
            raise

    async def _create_tables(self):
        """Создание таблиц если они не существуют"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            username VARCHAR(32),
            first_name VARCHAR(64),
            last_name VARCHAR(64),
            is_bot BOOLEAN DEFAULT FALSE,
            is_premium BOOLEAN DEFAULT FALSE,
            language_code VARCHAR(10),
            balance DECIMAL(10, 2) DEFAULT 0,
            referral_owner BIGINT,
            referral_invited BIGINT[] DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_referral_owner ON users(referral_owner);
        CREATE INDEX IF NOT EXISTS idx_username ON users(username);
        CREATE INDEX IF NOT EXISTS idx_created_at ON users(created_at);
        """

        async with self.pool.acquire() as conn:
            await conn.execute(create_table_query)
        logger.info("✅ Таблицы созданы/проверены")

    async def save_user(self, user_data: Dict[str, Any]) -> bool:
        """
        Сохраняет или обновляет пользователя
        Args:
            user_data: словарь с данными пользователя
        Returns:
            bool: успешность операции
        """
        try:
            query = """
            INSERT INTO users (
                telegram_id, username, first_name, last_name, 
                is_bot, is_premium, language_code
            ) VALUES ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT (telegram_id) 
            DO UPDATE SET
                username = EXCLUDED.username,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name,
                is_premium = EXCLUDED.is_premium,
                language_code = EXCLUDED.language_code,
                updated_at = CURRENT_TIMESTAMP
            """

            async with self.pool.acquire() as conn:
                await conn.execute(
                    query,
                    user_data['telegram_id'],
                    user_data.get('username'),
                    user_data.get('first_name'),
                    user_data.get('last_name'),
                    user_data.get('is_bot', False),
                    user_data.get('is_premium', False),
                    user_data.get('language_code')
                )
            return True

        except Exception as e:
            logger.error(f"❌ Ошибка сохранения пользователя {user_data.get('telegram_id')}: {e}")
            return False

    async def get_user(self, telegram_id: int) -> Optional[Dict[str, Any]]:
        """
        Получает все данные пользователя по telegram_id
        Args:
            telegram_id: ID пользователя в Telegram
        Returns:
            Dict с данными пользователя или None если не найден
        """
        try:
            query = "SELECT * FROM users WHERE telegram_id = $1"

            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(query, telegram_id)

            if row:
                return dict(row)
            return None

        except Exception as e:
            logger.error(f"❌ Ошибка получения пользователя {telegram_id}: {e}")
            return None

    async def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Получает список всех пользователей
        Returns:
            List[Dict]: список всех пользователей
        """
        try:
            query = "SELECT * FROM users ORDER BY created_at DESC"

            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query)

            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"❌ Ошибка получения всех пользователей: {e}")
            return []

    async def get_users_with_active_clients(self) -> List[int]:
        """
        Получает список telegram_id пользователей с активными клиентами
        Note: Эта функция будет дополнена когда появится таблица клиентов
        Returns:
            List[int]: список telegram_id
        """
        try:
            # Временная реализация - возвращаем всех пользователей
            # Позже можно будет добавить JOIN с таблицей клиентов
            query = "SELECT telegram_id FROM users"

            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query)

            return [row['telegram_id'] for row in rows]

        except Exception as e:
            logger.error(f"❌ Ошибка получения пользователей с активными клиентами: {e}")
            return []

    async def get_users_count(self) -> int:
        """
        Получает общее количество пользователей
        Returns:
            int: количество пользователей
        """
        try:
            query = "SELECT COUNT(*) as count FROM users"

            async with self.pool.acquire() as conn:
                result = await conn.fetchval(query)

            return result

        except Exception as e:
            logger.error(f"❌ Ошибка получения количества пользователей: {e}")
            return 0

    async def get_new_users_today(self) -> int:
        """
        Получает количество новых пользователей за сегодня
        Returns:
            int: количество новых пользователей
        """
        try:
            query = """
            SELECT COUNT(*) as count FROM users 
            WHERE DATE(created_at) = CURRENT_DATE
            """

            async with self.pool.acquire() as conn:
                result = await conn.fetchval(query)

            return result

        except Exception as e:
            logger.error(f"❌ Ошибка получения новых пользователей за сегодня: {e}")
            return 0

    async def update_balance(self, telegram_id: int, amount: float) -> bool:
        """
        Обновляет баланс пользователя
        Args:
            telegram_id: ID пользователя
            amount: сумма для изменения (может быть отрицательной)
        Returns:
            bool: успешность операции
        """
        try:
            query = """
            UPDATE users 
            SET balance = balance + $1, updated_at = CURRENT_TIMESTAMP
            WHERE telegram_id = $2
            """

            async with self.pool.acquire() as conn:
                await conn.execute(query, amount, telegram_id)

            return True

        except Exception as e:
            logger.error(f"❌ Ошибка обновления баланса пользователя {telegram_id}: {e}")
            return False

    async def add_referral(self, owner_id: int, referral_id: int) -> bool:
        """
        Добавляет реферала пользователю
        Args:
            owner_id: ID пользователя-владельца
            referral_id: ID приглашенного пользователя
        Returns:
            bool: успешность операции
        """
        try:
            # Обновляем referral_invited у владельца
            query_owner = """
            UPDATE users 
            SET referral_invited = array_append(referral_invited, $1),
                updated_at = CURRENT_TIMESTAMP
            WHERE telegram_id = $2
            """

            # Устанавливаем referral_owner у реферала
            query_referral = """
            UPDATE users 
            SET referral_owner = $1,
                updated_at = CURRENT_TIMESTAMP
            WHERE telegram_id = $2 AND referral_owner IS NULL
            """

            async with self.pool.acquire() as conn:
                await conn.execute(query_owner, referral_id, owner_id)
                await conn.execute(query_referral, owner_id, referral_id)

            return True

        except Exception as e:
            logger.error(f"❌ Ошибка добавления реферала {referral_id} для {owner_id}: {e}")
            return False

    async def get_referrals(self, owner_id: int) -> List[Dict[str, Any]]:
        """
        Получает список рефералов пользователя
        Args:
            owner_id: ID пользователя-владельца
        Returns:
            List[Dict]: список рефералов
        """
        try:
            query = """
            SELECT * FROM users 
            WHERE referral_owner = $1 
            ORDER BY created_at DESC
            """

            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query, owner_id)

            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"❌ Ошибка получения рефералов для {owner_id}: {e}")
            return []

    async def get_top_referrers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Получает топ рефереров по количеству приглашенных
        Args:
            limit: количество возвращаемых записей
        Returns:
            List[Dict]: список топ рефереров
        """
        try:
            query = """
            SELECT 
                telegram_id,
                username,
                first_name,
                array_length(referral_invited, 1) as referrals_count
            FROM users 
            WHERE array_length(referral_invited, 1) > 0
            ORDER BY referrals_count DESC
            LIMIT $1
            """

            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query, limit)

            return [dict(row) for row in rows]

        except Exception as e:
            logger.error(f"❌ Ошибка получения топ рефереров: {e}")
            return []

    async def close(self):
        """Закрывает соединение с базой данных"""
        if self.pool:
            await self.pool.close()
            logger.info("✅ Соединение с PostgreSQL закрыто")


# Глобальный экземпляр базы данных
db = Database()
