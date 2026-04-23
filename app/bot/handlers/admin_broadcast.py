import asyncio
import time
from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.config import settings
from app.repositories.user_repo import UserRepository
from app.bot.fsm.admin_broadcast import BroadcastStates
from app.bot.keyboards.admin_broadcast import broadcast_panel_keyboard, broadcast_confirm_keyboard

router = Router()


def _is_admin(user_id: int) -> bool:
    admin_ids = [int(x.strip()) for x in settings.ADMIN_IDS.split(",") if x.strip()]
    return user_id in admin_ids


def _panel_text(
    lang_filter: Optional[str],
    status_filter: Optional[str],
    level_filter: Optional[str],
) -> str:
    lang_label = lang_filter.upper() if lang_filter else "Hammasi"
    status_label = {"active": "Active", "trial": "Trial", "free": "Expired"}.get(
        status_filter, "Hammasi"
    )
    level_label = level_filter.upper() if level_filter else "Hammasi"
    return (
        "📢 <b>Broadcast paneli</b>\n\n"
        f"Til: <b>{lang_label}</b> | Status: <b>{status_label}</b> | Daraja: <b>{level_label}</b>\n\n"
        "Filtrlarni tanlang, so'ng ✏️ Matn kiritish tugmasini bosing."
    )


async def _redraw_panel(callback: CallbackQuery, data: dict) -> None:
    lang_filter = data.get("lang_filter")
    status_filter = data.get("status_filter")
    level_filter = data.get("level_filter")
    try:
        await callback.message.edit_text(
            _panel_text(lang_filter, status_filter, level_filter),
            reply_markup=broadcast_panel_keyboard(lang_filter, status_filter, level_filter),
            parse_mode="HTML",
        )
    except Exception:
        pass


# ── /broadcast ──────────────────────────────────────────────────────────────

@router.message(Command("broadcast"))
async def broadcast_command(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return

    await state.clear()
    await state.update_data(lang_filter=None, status_filter=None, level_filter=None)

    sent = await message.answer(
        _panel_text(None, None, None),
        reply_markup=broadcast_panel_keyboard(None, None, None),
        parse_mode="HTML",
    )
    await state.update_data(panel_msg_id=sent.message_id, panel_chat_id=sent.chat.id)


# ── Filter toggles ───────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("bc:lang:"))
async def bc_lang_filter(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    val = callback.data.split(":")[2]
    data = await state.get_data()
    data["lang_filter"] = None if val == "all" else val
    await state.update_data(lang_filter=data["lang_filter"])
    await _redraw_panel(callback, data)
    await callback.answer()


@router.callback_query(F.data.startswith("bc:status:"))
async def bc_status_filter(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    val = callback.data.split(":")[2]
    data = await state.get_data()
    data["status_filter"] = None if val == "all" else val
    await state.update_data(status_filter=data["status_filter"])
    await _redraw_panel(callback, data)
    await callback.answer()


@router.callback_query(F.data.startswith("bc:level:"))
async def bc_level_filter(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    val = callback.data.split(":")[2]
    data = await state.get_data()
    data["level_filter"] = None if val == "all" else val
    await state.update_data(level_filter=data["level_filter"])
    await _redraw_panel(callback, data)
    await callback.answer()


# ── Text entry ───────────────────────────────────────────────────────────────

@router.callback_query(F.data == "bc:enter_text")
async def bc_enter_text(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    await state.set_state(BroadcastStates.waiting_for_text)
    await callback.answer()
    await callback.message.answer("✏️ Xabar matnini yuboring:")


@router.message(BroadcastStates.waiting_for_text)
async def bc_receive_text(message: Message, state: FSMContext, session):
    if not _is_admin(message.from_user.id):
        return

    text = message.text or message.caption
    if not text:
        await message.answer("Faqat matn xabar yuboring.")
        return

    await state.set_state(None)
    await state.update_data(broadcast_text=text)

    data = await state.get_data()
    user_repo = UserRepository(session)
    users = await user_repo.get_filtered_users(
        language=data.get("lang_filter"),
        status=data.get("status_filter"),
        level=data.get("level_filter"),
    )
    count = len(users)

    preview = text[:200] + ("..." if len(text) > 200 else "")
    confirm_text = (
        f"📢 <b>Broadcast tasdiqlash</b>\n\n"
        f"<i>{preview}</i>\n\n"
        f"👥 <b>{count} ta</b> userga yuboriladi.\n\n"
        "Tasdiqlaysizmi?"
    )

    panel_msg_id = data.get("panel_msg_id")
    panel_chat_id = data.get("panel_chat_id")

    if panel_msg_id and panel_chat_id:
        try:
            await message.bot.edit_message_text(
                text=confirm_text,
                chat_id=panel_chat_id,
                message_id=panel_msg_id,
                reply_markup=broadcast_confirm_keyboard(),
                parse_mode="HTML",
            )
            return
        except Exception:
            pass

    sent = await message.answer(
        confirm_text,
        reply_markup=broadcast_confirm_keyboard(),
        parse_mode="HTML",
    )
    await state.update_data(panel_msg_id=sent.message_id, panel_chat_id=sent.chat.id)


# ── Confirm / Cancel ─────────────────────────────────────────────────────────

@router.callback_query(F.data == "bc:confirm")
async def bc_confirm(callback: CallbackQuery, state: FSMContext, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    await callback.answer()

    data = await state.get_data()
    broadcast_text = data.get("broadcast_text", "")
    await state.clear()

    if not broadcast_text:
        await callback.message.edit_text("❌ Xabar matni topilmadi.")
        return

    user_repo = UserRepository(session)
    users = await user_repo.get_filtered_users(
        language=data.get("lang_filter"),
        status=data.get("status_filter"),
        level=data.get("level_filter"),
    )
    total = len(users)

    await callback.message.edit_text(f"⏳ Yuborilmoqda... (0/{total})")

    sent_count = 0
    failed_count = 0
    last_update = time.monotonic()

    for i, user in enumerate(users, start=1):
        try:
            await callback.bot.send_message(user.telegram_id, broadcast_text)
            sent_count += 1
        except Exception:
            failed_count += 1
        await asyncio.sleep(0.05)

        now = time.monotonic()
        if now - last_update >= 2 or i == total:
            try:
                await callback.message.edit_text(f"⏳ Yuborilmoqda... ({i}/{total})")
                last_update = now
            except Exception:
                pass

    await callback.message.edit_text(
        f"✅ Yuborildi: {sent_count}, ❌ Xato: {failed_count}"
    )


@router.callback_query(F.data == "bc:cancel")
async def bc_cancel(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    await state.clear()
    await callback.answer()
    await callback.message.edit_text("❌ Broadcast bekor qilindi.")
