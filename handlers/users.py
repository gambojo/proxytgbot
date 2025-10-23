from aiogram import Router, types
from aiogram.filters import Command
from proxy_clients import vless, vmess, shadowsocks, trojan
from utils.qr_code import create_qr_code
from keyboards.users import (
    get_main_menu,
    get_services_menu,
    get_protocol_menu,
    get_qr_menu,
    get_instructions_menu,
    get_back_instructions,
    get_back_button
)

router = Router()


# БЛОК ГЛАВНОГО МЕНЮ
# Старт - главное меню
@router.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = get_main_menu()
    await message.answer("👋 Добро пожаловать! Выберите раздел:", reply_markup=keyboard)


# Назад в главное меню
@router.callback_query(lambda c: c.data == "main_menu")
async def back_to_main(callback: types.CallbackQuery):
    keyboard = get_main_menu()
    await callback.message.edit_text("👋 Главное меню:", reply_markup=keyboard)
    await callback.answer()


# БЛОК УСЛУГ
@router.callback_query(lambda c: c.data == "services")
async def services_handler(callback: types.CallbackQuery):
    keyboard = get_services_menu()
    await callback.message.edit_text("🛒 Выберите услугу:", reply_markup=keyboard)
    await callback.answer()


# Промежуточное меню протоколов
@router.callback_query(lambda c: c.data.startswith("connect_"))
async def protocol_menu_handler(callback: types.CallbackQuery):
    protocol = callback.data.replace("connect_", "")

    text = (
        f"🔐 **{protocol.upper()} подключение**\n\n"
        f"Здесь можно разместить рекламу\n"
        f"или информацию о подключении\n\n"
        f"Выберите действие:"
    )

    keyboard = get_protocol_menu(protocol)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# Получить строку подключения
@router.callback_query(lambda c: c.data.startswith("get_string_"))
async def get_string_handler(callback: types.CallbackQuery):
    protocol = callback.data.replace("get_string_", "")
    user_id = str(callback.from_user.id)

    try:
        if protocol == "vless":
            result = await vless.create_vless_client(user_id)
        elif protocol == "vmess":
            result = await vmess.create_vmess_client(user_id)
        elif protocol == "shadowsocks":
            result = await shadowsocks.create_ss_client(user_id)
        elif protocol == "trojan":
            result = await trojan.create_trojan_client(user_id)
        else:
            await callback.answer("❌ Ошибка протокола")
            return

        connection_string = result["connection_string"]

        text = (
            f"🔐 **Ваш {protocol.upper()} конфиг**\n\n"
            f"**Действует:** {result['expiry_time']} дней\n\n"
            f"```\n{connection_string}\n```\n\n"
            f"⚠️ *Выделите ссылку выше и скопируйте*\n"
        )

        await callback.message.edit_text(text, reply_markup=get_protocol_menu(protocol), parse_mode="Markdown")
        await callback.answer("✅ Строка подключения получена")

    except Exception as e:
        await callback.message.edit_text(
            "❌ Ошибка при получении конфига",
            reply_markup=get_protocol_menu(protocol)
        )
        print(f"Get string error: {e}")
        await callback.answer("❌ Ошибка")


# Получить QR-код
@router.callback_query(lambda c: c.data.startswith("get_qr_"))
async def get_qr_handler(callback: types.CallbackQuery):
    protocol = callback.data.replace("get_qr_", "")
    user_id = str(callback.from_user.id)

    try:
        if protocol == "vless":
            result = await vless.create_vless_client(user_id)
        elif protocol == "vmess":
            result = await vmess.create_vmess_client(user_id)
        elif protocol == "shadowsocks":
            result = await shadowsocks.create_ss_client(user_id)
        elif protocol == "trojan":
            result = await trojan.create_trojan_client(user_id)
        else:
            await callback.answer("❌ Ошибка протокола")
            return

        connection_string = result["connection_string"]
        qr_code = await create_qr_code(connection_string)

        # ✅ РЕДАКТИРУЕМ текущее сообщение, а не создаем новое
        await callback.message.edit_media(
            media=types.InputMediaPhoto(
                media=qr_code,
                caption=(
                    f"📱 **QR-код {protocol.upper()}**\n\n"
                    f"**Действует:** {result['expiry_time']} дней\n\n"
                    f"⚠️ *Отсканируйте QR-код для быстрого подключения*"
                ),
                parse_mode="Markdown"
            ),
            reply_markup=get_qr_menu(protocol)
        )

        await callback.answer("✅ QR-код сгенерирован")

    except Exception as e:
        await callback.answer("❌ Ошибка при создании QR-кода", show_alert=True)
        print(f"Get QR error: {e}")


# БЛОК ПРИГЛАШЕНИЙ
@router.callback_query(lambda c: c.data == "referral")
async def referral_handler(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)

    # Здесь будет логика создания реферальной ссылки
    referral_link = f"https://t.me/your_bot_username?start=ref{user_id}"

    text = (
        "👥 **Реферальная система**\n\n"
        "Приглашайте друзей и получайте бонусы!\n\n"
        f"**Ваша реферальная ссылка:**\n"
        f"```\n{referral_link}\n```\n\n"
        f"⚠️ *Выделите ссылку выше и скопируйте*\n"
        f"*Поделитесь с друзьями для получения бонусов*"
    )

    keyboard = get_back_button()
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()


# БЛОК ИНСТРУКЦИЙ
@router.callback_query(lambda c: c.data == "instructions")
async def instructions_handler(callback: types.CallbackQuery):
    keyboard = get_instructions_menu()
    await callback.message.edit_text("📘 Выберите протокол для инструкций:", reply_markup=keyboard)
    await callback.answer()


# Инструкции по протоколам
@router.callback_query(lambda c: c.data == "instruction_vless")
async def instruction_vless_handler(callback: types.CallbackQuery):
    text = (
        "📘 Инструкция по VLESS:\n\n"
        "Windows: Скачайте V2RayN\n"
        "Android: Скачайте V2RayNG\n"  
        "iOS: Скачайте Shadowrocket\n"
        "macOS: Скачайте V2RayX"
    )
    await callback.message.edit_text(text, reply_markup=get_back_instructions())
    await callback.answer()


@router.callback_query(lambda c: c.data == "instruction_vmess")
async def instruction_vmess_handler(callback: types.CallbackQuery):
    text = (
        "📘 Инструкция по VMess:\n\n"
        "Windows: Скачайте V2RayN\n"
        "Android: Скачайте V2RayNG\n"
        "iOS: Скачайте Shadowrocket\n"
        "macOS: Скачайте V2RayX"
    )
    await callback.message.edit_text(text, reply_markup=get_back_instructions())
    await callback.answer()


@router.callback_query(lambda c: c.data == "instruction_shadowsocks")
async def instruction_shadowsocks_handler(callback: types.CallbackQuery):
    text = (
        "📘 Инструкция по Shadowsocks:\n\n"
        "Windows: Скачайте Shadowsocks\n"
        "Android: Скачайте Shadowsocks\n"
        "iOS: Скачайте Shadowrocket\n"
        "macOS: Скачайте ShadowsocksX"
    )
    await callback.message.edit_text(text, reply_markup=get_back_instructions())
    await callback.answer()


@router.callback_query(lambda c: c.data == "instruction_trojan")
async def instruction_trojan_handler(callback: types.CallbackQuery):
    text = (
        "📘 Инструкция по Trojan:\n\n"
        "Windows: Скачайте Trojan-Qt5\n"
        "Android: Скачайте Igniter\n"
        "iOS: Скачайте Shadowrocket\n"
        "macOS: Скачайте TrojanX"
    )
    await callback.message.edit_text(text, reply_markup=get_back_instructions())
    await callback.answer()


# БЛОК О СЕРВИСЕ
@router.callback_query(lambda c: c.data == "about")
async def about_handler(callback: types.CallbackQuery):
    text = (
        "ℹ️ О нашем сервисе:\n\n"
        "Мы предоставляем быстрые и надежные прокси-услуги "
        "с поддержкой современных протоколов.\n\n"
        "По всем вопросам: @support"
    )
    await callback.message.edit_text(text, reply_markup=get_back_button())
    await callback.answer()
