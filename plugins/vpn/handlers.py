from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from .fsm import VpnState
from .keyboards import get_vpn_menu, get_duration_keyboard, get_vpn_confirm_keyboard
from core.keyboards.static import get_back_to_main_menu

router = Router(name="vpn_plugin")

@router.callback_query(lambda c: c.data == "plugin:🛡 VPN")
async def entry_point(callback: CallbackQuery):
    await callback.message.edit_text("🛡 VPN меню", reply_markup=get_vpn_menu())

@router.callback_query(lambda c: c.data == "vpn:create")
async def start_vpn_creation(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите имя для нового VPN:")
    await state.set_state(VpnState.AWAITING_NAME)

@router.message(StateFilter(VpnState.AWAITING_NAME))
async def handle_vpn_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text.strip())
    await msg.answer("Выберите срок действия:", reply_markup=get_duration_keyboard())
    await state.set_state(VpnState.AWAITING_DURATION)

@router.callback_query(lambda c: c.data.startswith("vpn:duration:"))
async def handle_duration(callback: CallbackQuery, state: FSMContext):
    duration = callback.data.split(":")[-1]
    await state.update_data(duration=duration)
    data = await state.get_data()
    name = data.get("name")
    await callback.message.edit_text(
        f"Создать VPN:\n\n🔐 Имя: {name}\n⏳ Срок: {duration}",
        reply_markup=get_vpn_confirm_keyboard()
    )
    await state.set_state(VpnState.AWAITING_CONFIRMATION)

@router.callback_query(lambda c: c.data == "vpn:confirm")
async def handle_confirm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    duration = data.get("duration")
    # Здесь можно вызвать create_vpn(name, duration)
    await callback.message.edit_text(f"✅ VPN '{name}' на {duration} создан.",
                                     reply_markup=get_back_to_main_menu())
    await state.clear()
