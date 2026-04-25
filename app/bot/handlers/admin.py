from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select, func
from datetime import datetime, timezone, timedelta

from app.config import settings
from app.repositories.user_repo import UserRepository
from app.db.models.user import User
from app.db.models.payment import Payment

router = Router()


def _is_admin(user_id: int) -> bool:
    admin_ids = [int(x.strip()) for x in settings.ADMIN_IDS.split(",") if x.strip()]
    return user_id in admin_ids


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="adm:stats")],
        [InlineKeyboardButton(text="🗑 Foydalanuvchini o'chirish", callback_data="adm:deleteuser_info")],
        [InlineKeyboardButton(text="📢 Broadcast xabar", callback_data="adm:broadcast_info")],
        [InlineKeyboardButton(text="✅ Obuna berish", callback_data="adm:giveaccess_info")],
    ])


@router.message(Command("admin"))
async def admin_menu_handler(message: Message, session):
    if not _is_admin(message.from_user.id):
        return
    await message.answer(
        "<b>🛠 Admin panel</b>\n\nQuyidagi amallardan birini tanlang:",
        reply_markup=admin_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "adm:stats")
async def admin_stats_callback(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    result = await session.execute(
        select(User.status, func.count().label("cnt")).group_by(User.status)
    )
    status_counts = {row.status: row.cnt for row in result.fetchall()}

    result = await session.execute(
        select(User.language, func.count().label("cnt")).group_by(User.language)
    )
    lang_counts = {row.language: row.cnt for row in result.fetchall()}

    result = await session.execute(select(func.count()).select_from(User))
    total = result.scalar() or 0

    result = await session.execute(
        select(func.count()).select_from(User).where(User.questions_used > 0)
    )
    active_users = result.scalar() or 0

    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    result = await session.execute(
        select(func.count()).select_from(User).where(User.created_at >= week_ago)
    )
    new_this_week = result.scalar() or 0

    result = await session.execute(
        select(func.count()).select_from(Payment).where(Payment.payment_status == "pending")
    )
    pending_payments = result.scalar() or 0

    result = await session.execute(
        select(func.count()).select_from(Payment).where(Payment.payment_status == "approved")
    )
    total_paid = result.scalar() or 0

    trial = status_counts.get("trial", 0)
    active = status_counts.get("active", 0)
    expired = status_counts.get("expired", 0)
    blocked = status_counts.get("blocked", 0)

    conversion = round(active / total * 100, 1) if total > 0 else 0
    engagement = round(active_users / total * 100, 1) if total > 0 else 0
    lang_str = " | ".join(f"{k}: {v}" for k, v in sorted(lang_counts.items()))

    text = (
        f"📊 <b>Statistika</b>\n\n"
        f"<b>👥 Foydalanuvchilar:</b>\n"
        f"  Jami: {total}\n"
        f"  Trial: {trial}\n"
        f"  Aktiv: {active}\n"
        f"  Tugagan: {expired}\n"
        f"  Bloklangan: {blocked}\n\n"
        f"<b>📈 Konversiya:</b>\n"
        f"  Trial → Obuna: {conversion}%\n"
        f"  Savol berganlar: {active_users} ({engagement}%)\n"
        f"  Bu hafta yangilar: +{new_this_week}\n\n"
        f"<b>💳 To'lovlar:</b>\n"
        f"  Kutilmoqda: {pending_payments}\n"
        f"  Tasdiqlangan: {total_paid}\n\n"
        f"<b>🌐 Tillar:</b> {lang_str}"
    )

    await callback.answer()
    await callback.message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "adm:deleteuser_info")
async def admin_deleteuser_info(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await callback.answer()
    await callback.message.answer(
        "🗑 <b>Foydalanuvchini o'chirish</b>\n\n"
        "Buyruq: <code>/deleteuser TELEGRAM_ID</code>\n\n"
        "Misol: <code>/deleteuser 123456789</code>",
        parse_mode="HTML",
    )


@router.message(Command("deleteuser"))
async def admin_deleteuser_handler(message: Message, session):
    if not _is_admin(message.from_user.id):
        return

    parts = message.text.strip().split()
    if len(parts) < 2:
        await message.answer("Foydalanish: <code>/deleteuser TELEGRAM_ID</code>", parse_mode="HTML")
        return

    try:
        target_id = int(parts[1])
    except ValueError:
        await message.answer("❌ Noto'g'ri ID format")
        return

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(target_id)
    if not user:
        await message.answer(f"❌ Foydalanuvchi topilmadi: {target_id}")
        return

    await session.delete(user)
    await session.commit()
    await message.answer(f"✅ Foydalanuvchi {target_id} o'chirildi")


@router.callback_query(F.data == "adm:broadcast_info")
async def admin_broadcast_info(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await callback.answer()
    await callback.message.answer(
        "📢 <b>Broadcast xabar yuborish</b>\n\n"
        "Buyruq: <code>/broadcast Xabar matni</code>\n\n"
        "Misol: <code>/broadcast Yangi daraja qo'shildi!</code>\n\n"
        "⚠️ Barcha foydalanuvchilarga yuboriladi.",
        parse_mode="HTML",
    )


@router.message(Command("broadcast"))
async def admin_broadcast_handler(message: Message, session):
    if not _is_admin(message.from_user.id):
        return

    text = message.text.strip()[len("/broadcast"):].strip()
    if not text:
        await message.answer("Foydalanish: <code>/broadcast Xabar matni</code>", parse_mode="HTML")
        return

    result = await session.execute(select(User.telegram_id))
    all_ids = [row.telegram_id for row in result.fetchall()]

    sent = 0
    failed = 0
    for uid in all_ids:
        try:
            await message.bot.send_message(chat_id=uid, text=text)
            sent += 1
        except Exception:
            failed += 1

    await message.answer(f"✅ Yuborildi: {sent}\n❌ Xato: {failed}")


@router.callback_query(F.data == "adm:giveaccess_info")
async def admin_giveaccess_info(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await callback.answer()
    await callback.message.answer(
        "✅ <b>Obuna berish</b>\n\n"
        "Buyruq: <code>/giveaccess TELEGRAM_ID PLAN</code>\n\n"
        "Planlar: <code>10_days</code> | <code>1_month</code>\n\n"
        "Misol: <code>/giveaccess 123456789 1_month</code>",
        parse_mode="HTML",
    )


@router.message(Command("giveaccess"))
async def admin_giveaccess_handler(message: Message, session):
    if not _is_admin(message.from_user.id):
        return

    parts = message.text.strip().split()
    if len(parts) < 3:
        await message.answer("Foydalanish: <code>/giveaccess TELEGRAM_ID PLAN</code>", parse_mode="HTML")
        return

    try:
        target_id = int(parts[1])
    except ValueError:
        await message.answer("❌ Noto'g'ri ID")
        return

    plan = parts[2]
    if plan not in ("10_days", "1_month"):
        await message.answer("❌ Plan: 10_days yoki 1_month")
        return

    from app.services.subscription_service import SubscriptionService
    sub_service = SubscriptionService(session)
    await sub_service.activate_plan(telegram_id=target_id, plan_type=plan)
    await session.commit()
    await message.answer(f"✅ {target_id} ga {plan} obuna berildi")
