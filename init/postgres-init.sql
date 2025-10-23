-- Инициализация базы данных для Telegram Proxy Bot
-- Этот файл создает базу данных, пользователя и таблицы

-- Создаем базу данных если не существует
SELECT 'CREATE DATABASE proxy_bot_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'proxy_bot_db')\gexec

-- Подключаемся к созданной базе данных
\c proxy_bot_db;

-- Создаем пользователя если не существует
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'proxy_bot_user') THEN
        CREATE USER proxy_bot_user WITH PASSWORD 'proxy_bot_password';
    END IF;
END
$$;

-- Даем права пользователю
GRANT ALL PRIVILEGES ON DATABASE proxy_bot_db TO proxy_bot_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO proxy_bot_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO proxy_bot_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO proxy_bot_user;

-- Создаем таблицу пользователей
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

-- Создаем индексы для оптимизации
CREATE INDEX IF NOT EXISTS idx_referral_owner ON users(referral_owner);
CREATE INDEX IF NOT EXISTS idx_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_updated_at ON users(updated_at);
CREATE INDEX IF NOT EXISTS idx_balance ON users(balance);
CREATE INDEX IF NOT EXISTS idx_language_code ON users(language_code);

-- Даем права на таблицу
GRANT ALL PRIVILEGES ON TABLE users TO proxy_bot_user;

-- Создаем функцию для автоматического обновления updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Создаем триггер для автоматического обновления updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Вставляем тестовые данные (опционально)
INSERT INTO users (telegram_id, username, first_name, last_name, is_bot, is_premium, language_code, balance)
VALUES
    (785818468, 'admin_user', 'Admin', 'User', FALSE, TRUE, 'ru', 100.00),
    (123456789, 'test_user1', 'Test', 'User1', FALSE, FALSE, 'en', 50.00),
    (987654321, 'test_user2', 'Test', 'User2', FALSE, TRUE, 'ru', 25.50)
ON CONFLICT (telegram_id) DO NOTHING;

-- Показываем информацию о созданных объектах
\dt
\di

-- Показываем созданных пользователей
SELECT
    telegram_id,
    username,
    first_name,
    balance,
    created_at
FROM users
ORDER BY created_at DESC;

-- Сообщение об успешном завершении
\echo ''
\echo '✅ База данных proxy_bot_db успешно инициализирована!'
\echo '📊 Таблица users создана с индексами и триггерами'
\echo '👤 Пользователь proxy_bot_user создан с правами доступа'
\echo ''