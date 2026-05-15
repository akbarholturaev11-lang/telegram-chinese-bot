from aiogram import Router, F
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select, func
from datetime import datetime, timezone, timedelta
from html import escape

from app.bot.fsm.admin_portfolio import AdminPortfolioStates
from app.config import settings
from app.repositories.user_repo import UserRepository
from app.repositories.course_audio_repo import CourseAudioRepository
from app.db.models.user import User
from app.db.models.payment import Payment
from app.db.models.course_progress import CourseProgress
from app.db.models.referral import Referral
from app.services.ai_usage_budget_service import USD_TO_SOMONI, USD_TO_YUAN
from app.services.portfolio_service import PortfolioService

router = Router()


def _is_admin(user_id: int) -> bool:
    admin_ids = [int(x.strip()) for x in settings.ADMIN_IDS.split(",") if x.strip()]
    return user_id in admin_ids


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Statistika", callback_data="adm:stats")],
        [InlineKeyboardButton(text="💼 Portfel", callback_data="adm:portfolio")],
        [InlineKeyboardButton(text="🗑 Foydalanuvchini o'chirish", callback_data="adm:deleteuser_info")],
        [InlineKeyboardButton(text="📢 Broadcast xabar", callback_data="adm:broadcast_info")],
        [InlineKeyboardButton(text="🎁 Chegirma boshqaruv", callback_data="adm:discount_panel")],
        [InlineKeyboardButton(text="✅ Obuna berish", callback_data="adm:giveaccess_info")],
        [InlineKeyboardButton(text="🎵 Audio boshqaruv", callback_data="adm:audio_panel")],
    ])


def portfolio_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 History", callback_data="adm:portfolio_history")],
        [
            InlineKeyboardButton(text="➕ Foyda qo'shish", callback_data="adm:portfolio_profit_info"),
            InlineKeyboardButton(text="➖ Rasxod qo'shish", callback_data="adm:portfolio_expense_info"),
        ],
        [InlineKeyboardButton(text="⬅️ Admin panel", callback_data="adm:menu")],
    ])


def portfolio_history_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Portfel", callback_data="adm:portfolio")],
    ])


def _usd(value: float) -> str:
    return f"${value:,.2f}"


def _signed_usd(value: float) -> str:
    sign = "+" if value >= 0 else "-"
    return f"{sign}${abs(value):,.2f}"


def _portfolio_type_label(transaction_type: str) -> str:
    return "foyda" if transaction_type == "profit" else "rasxod"


def _portfolio_type_icon(transaction_type: str) -> str:
    return "➕" if transaction_type == "profit" else "➖"


def _parse_amount_currency(text: str) -> tuple[float, str] | None:
    parts = (text or "").strip().split(maxsplit=2)
    if len(parts) < 2:
        return None
    try:
        amount = float(parts[0].replace(",", "."))
    except ValueError:
        return None
    if amount <= 0:
        return None
    return amount, parts[1]


async def _start_portfolio_flow(
    *,
    state: FSMContext,
    respond,
    transaction_type: str,
) -> None:
    await state.clear()
    await state.update_data(portfolio_transaction_type=transaction_type)
    await state.set_state(AdminPortfolioStates.waiting_amount)
    icon = _portfolio_type_icon(transaction_type)
    label = _portfolio_type_label(transaction_type)
    await respond(
        f"{icon} <b>{label.capitalize()} qo'shish</b>\n\n"
        "Avval summa va currency yuboring:\n"
        "<code>50 usd</code>\n"
        "<code>120 somoni</code>\n"
        "<code>200 ¥</code>\n\n"
        "Keyingi xabarda bot sababini so'raydi.",
        parse_mode="HTML",
    )


async def _ask_portfolio_reason(
    *,
    state: FSMContext,
    message: Message,
    transaction_type: str,
    amount: float,
    currency: str,
) -> None:
    if PortfolioService(None).amount_to_usd(amount, currency) is None:
        await message.answer("❌ Currency noto'g'ri. Faqat usd, somoni yoki ¥ ishlat.")
        return

    await state.update_data(
        portfolio_transaction_type=transaction_type,
        portfolio_amount=amount,
        portfolio_currency=currency,
    )
    await state.set_state(AdminPortfolioStates.waiting_reason)
    icon = _portfolio_type_icon(transaction_type)
    label = _portfolio_type_label(transaction_type)
    await message.answer(
        f"{icon} <b>{amount:g} {escape(currency)}</b> {label} uchun sababini yozing.\n\n"
        "Masalan:\n"
        "<code>OpenAI to'lov</code>\n"
        "<code>Reklama tushumi</code>\n"
        "<code>Railway oylik to'lov</code>",
        parse_mode="HTML",
    )


async def _start_portfolio_command_flow(
    *,
    message: Message,
    state: FSMContext,
    transaction_type: str,
) -> None:
    parts = message.text.strip().split(maxsplit=3)
    if len(parts) < 3:
        command = "/portfolio_profit" if transaction_type == "profit" else "/portfolio_expense"
        await message.answer(
            f"Foydalanish: <code>{command} 50 usd</code>\n\n"
            "Sababini keyingi xabarda bot o'zi so'raydi.",
            parse_mode="HTML",
        )
        return

    parsed = _parse_amount_currency(" ".join(parts[1:3]))
    if not parsed:
        await message.answer("❌ Summa formati noto'g'ri. Masalan: <code>50 usd</code>", parse_mode="HTML")
        return

    amount, currency = parsed
    await _ask_portfolio_reason(
        state=state,
        message=message,
        transaction_type=transaction_type,
        amount=amount,
        currency=currency,
    )


def _portfolio_summary_text(summary) -> str:
    status = "🟢 PLUS" if summary.net_usd >= 0 else "🔴 MINUS"
    return (
        f"💼 <b>Portfel</b>\n"
        f"{'─' * 30}\n\n"
        f"<b>💳 Obunalar</b>\n"
        f"  Tasdiqlangan: <b>{summary.approved_payments}</b>\n"
        f"  Brutto tushum: <b>{_usd(summary.gross_revenue_usd)}</b>\n"
        f"  Kurs: <code>1$ = {USD_TO_SOMONI} somoni</code>, <code>1$ = {USD_TO_YUAN} ¥</code>\n\n"
        f"<b>📈 Foyda</b>\n"
        f"  Obunalardan auto 40%: <b>{_usd(summary.subscription_profit_usd)}</b>\n"
        f"  Qo'lda qo'shilgan foyda: <b>{_usd(summary.manual_profit_usd)}</b>\n"
        f"  Jami foyda: <b>{_usd(summary.total_profit_usd)}</b>\n\n"
        f"<b>📉 Rasxod</b>\n"
        f"  Qo'lda qo'shilgan rasxod: <b>{_usd(summary.manual_expense_usd)}</b>\n"
        f"  Jami rasxod: <b>{_usd(summary.total_expense_usd)}</b>\n\n"
        f"<b>📊 Holat</b>\n"
        f"  Net: <b>{_signed_usd(summary.net_usd)}</b>\n"
        f"  Status: <b>{status}</b>\n\n"
        f"<i>OpenAI, Railway, reklama va boshqa tushum/rasxodlar tokenlardan avtomatik olinmaydi. Ularni o'zingiz +/- qilib kiritasiz.</i>"
    )


def _portfolio_history_text(rows) -> str:
    if not rows:
        return "📜 <b>Portfel history</b>\n\nHali transaction yo'q."

    lines = ["📜 <b>Portfel history</b>", ""]
    for row in rows:
        created = row.created_at
        if created and created.tzinfo:
            created = created.astimezone(timezone.utc)
        date_text = created.strftime("%d.%m %H:%M") if created else "-"
        icon = "📈" if row.transaction_type == "profit" else "📉"
        sign = "+" if row.transaction_type == "profit" else "-"
        source = escape(row.source.replace("_", " "))
        note = escape(row.note or "")
        original = ""
        if row.original_amount is not None and row.original_currency:
            original = f" · {row.original_amount:g} {escape(row.original_currency)}"
        lines.append(
            f"{icon} <code>{date_text}</code> {sign}{_usd(row.amount_usd)}"
            f"{original}\n"
            f"  <b>{source}</b>{f' — {note}' if note else ''}"
        )
    return "\n\n".join(lines)


@router.message(Command("admin"))
async def admin_menu_handler(message: Message, session):
    if not _is_admin(message.from_user.id):
        return
    await message.answer(
        "<b>🛠 Admin panel</b>\n\nQuyidagi amallardan birini tanlang:",
        reply_markup=admin_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "adm:menu")
async def admin_menu_callback(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await callback.answer()
    await callback.message.answer(
        "<b>🛠 Admin panel</b>\n\nQuyidagi amallardan birini tanlang:",
        reply_markup=admin_menu_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "adm:portfolio")
async def admin_portfolio_callback(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    summary = await PortfolioService(session).get_summary()
    await session.commit()
    await callback.answer()
    await callback.message.answer(
        _portfolio_summary_text(summary),
        reply_markup=portfolio_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "adm:portfolio_history")
async def admin_portfolio_history_callback(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    rows = await PortfolioService(session).list_history(limit=20)
    await session.commit()
    await callback.answer()
    await callback.message.answer(
        _portfolio_history_text(rows),
        reply_markup=portfolio_history_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "adm:portfolio_expense_info")
async def admin_portfolio_expense_info(callback: CallbackQuery, state: FSMContext, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await callback.answer()
    await _start_portfolio_flow(
        state=state,
        respond=callback.message.answer,
        transaction_type="expense",
    )


@router.callback_query(F.data == "adm:portfolio_profit_info")
async def admin_portfolio_profit_info(callback: CallbackQuery, state: FSMContext, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await callback.answer()
    await _start_portfolio_flow(
        state=state,
        respond=callback.message.answer,
        transaction_type="profit",
    )


@router.message(Command("portfolio_expense"))
async def admin_portfolio_expense_handler(message: Message, state: FSMContext, session):
    if not _is_admin(message.from_user.id):
        return

    await _start_portfolio_command_flow(
        message=message,
        state=state,
        transaction_type="expense",
    )


@router.message(Command("portfolio_profit"))
async def admin_portfolio_profit_handler(message: Message, state: FSMContext, session):
    if not _is_admin(message.from_user.id):
        return

    await _start_portfolio_command_flow(
        message=message,
        state=state,
        transaction_type="profit",
    )


@router.message(StateFilter(AdminPortfolioStates.waiting_amount))
async def admin_portfolio_amount_handler(message: Message, state: FSMContext, session):
    if not _is_admin(message.from_user.id):
        return

    data = await state.get_data()
    transaction_type = data.get("portfolio_transaction_type")
    if transaction_type not in {"profit", "expense"}:
        await state.clear()
        await message.answer("❌ Portfel flow buzildi. Qaytadan boshlang.")
        return

    parsed = _parse_amount_currency(message.text or "")
    if not parsed:
        await message.answer(
            "❌ Summa va currency yuboring. Masalan: <code>50 usd</code>",
            parse_mode="HTML",
        )
        return

    amount, currency = parsed
    await _ask_portfolio_reason(
        state=state,
        message=message,
        transaction_type=transaction_type,
        amount=amount,
        currency=currency,
    )


@router.message(StateFilter(AdminPortfolioStates.waiting_reason))
async def admin_portfolio_reason_handler(message: Message, state: FSMContext, session):
    if not _is_admin(message.from_user.id):
        return

    note = (message.text or "").strip()
    if len(note) < 2:
        await message.answer("❌ Sabab juda qisqa. Sababini yozing.")
        return

    data = await state.get_data()
    transaction_type = data.get("portfolio_transaction_type")
    amount = data.get("portfolio_amount")
    currency = data.get("portfolio_currency")
    if transaction_type not in {"profit", "expense"} or amount is None or not currency:
        await state.clear()
        await message.answer("❌ Portfel flow buzildi. Qaytadan boshlang.")
        return

    transaction = await PortfolioService(session).add_manual_transaction(
        transaction_type=transaction_type,
        admin_telegram_id=message.from_user.id,
        amount=float(amount),
        currency=str(currency),
        note=note,
    )
    if not transaction:
        await state.clear()
        await message.answer("❌ Currency noto'g'ri. Qaytadan boshlang.")
        return

    await session.commit()
    await state.clear()
    label = "Foyda" if transaction_type == "profit" else "Rasxod"
    await message.answer(
        f"✅ {label} qo'shildi: <b>{_usd(transaction.amount_usd)}</b>\n"
        f"📝 Sabab: {escape(note)}",
        parse_mode="HTML",
    )


@router.callback_query(F.data == "adm:stats")
async def admin_stats_callback(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return

    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    # --- Foydalanuvchilar ---
    total = (await session.execute(select(func.count()).select_from(User))).scalar() or 0

    status_counts = {
        r.status: r.cnt
        for r in (await session.execute(
            select(User.status, func.count().label("cnt")).group_by(User.status)
        )).fetchall()
    }
    lang_counts = {
        r.language: r.cnt
        for r in (await session.execute(
            select(User.language, func.count().label("cnt")).group_by(User.language)
        )).fetchall()
    }
    level_counts = {
        r.level: r.cnt
        for r in (await session.execute(
            select(User.level, func.count().label("cnt")).group_by(User.level)
        )).fetchall()
    }
    mode_counts = {
        r.learning_mode: r.cnt
        for r in (await session.execute(
            select(User.learning_mode, func.count().label("cnt")).group_by(User.learning_mode)
        )).fetchall()
    }

    # --- Faollik ---
    new_today = (await session.execute(
        select(func.count()).select_from(User).where(User.created_at >= today_start)
    )).scalar() or 0
    new_week = (await session.execute(
        select(func.count()).select_from(User).where(User.created_at >= week_ago)
    )).scalar() or 0
    new_month = (await session.execute(
        select(func.count()).select_from(User).where(User.created_at >= month_ago)
    )).scalar() or 0
    active_today = (await session.execute(
        select(func.count()).select_from(User).where(User.last_active_at >= today_start)
    )).scalar() or 0
    active_week = (await session.execute(
        select(func.count()).select_from(User).where(User.last_active_at >= week_ago)
    )).scalar() or 0

    # --- To'lovlar ---
    pay_rows = (await session.execute(
        select(
            Payment.payment_status,
            func.count().label("cnt"),
            func.sum(Payment.amount).label("total_sum"),
        ).group_by(Payment.payment_status)
    )).fetchall()
    pay_by_status = {r.payment_status: (r.cnt, int(r.total_sum or 0)) for r in pay_rows}

    pay_plan_rows = (await session.execute(
        select(Payment.plan_type, func.count().label("cnt"))
        .where(Payment.payment_status == "approved")
        .group_by(Payment.plan_type)
    )).fetchall()
    pay_by_plan = {r.plan_type: r.cnt for r in pay_plan_rows}

    # --- Kurs ---
    course_total = (await session.execute(
        select(func.count()).select_from(CourseProgress)
    )).scalar() or 0
    course_with_lessons = (await session.execute(
        select(func.count()).select_from(CourseProgress)
        .where(CourseProgress.completed_lessons_count > 0)
    )).scalar() or 0
    course_lessons_sum = (await session.execute(
        select(func.sum(CourseProgress.completed_lessons_count)).select_from(CourseProgress)
    )).scalar() or 0
    course_reminders = (await session.execute(
        select(func.count()).select_from(CourseProgress)
        .where(CourseProgress.reminder_enabled == True)  # noqa: E712
    )).scalar() or 0

    # --- Referallar ---
    ref_total = (await session.execute(
        select(func.count()).select_from(Referral)
    )).scalar() or 0
    ref_activated = (await session.execute(
        select(func.count()).select_from(Referral).where(Referral.status == "activated")
    )).scalar() or 0
    ref_bonus = (await session.execute(
        select(func.count()).select_from(Referral).where(Referral.bonus_granted == True)  # noqa: E712
    )).scalar() or 0
    discount_eligible = (await session.execute(
        select(func.count()).select_from(User).where(User.discount_eligible == True)  # noqa: E712
    )).scalar() or 0
    discount_used_cnt = (await session.execute(
        select(func.count()).select_from(User).where(User.discount_used == True)  # noqa: E712
    )).scalar() or 0

    # --- Hisob ---
    free_cnt    = status_counts.get("free", 0)
    trial_cnt   = status_counts.get("trial", 0)
    active_cnt  = status_counts.get("active", 0)
    expired_cnt = status_counts.get("expired", 0)
    blocked_cnt = status_counts.get("blocked", 0)

    pending_cnt,  _            = pay_by_status.get("pending",  (0, 0))
    approved_cnt, approved_sum = pay_by_status.get("approved", (0, 0))
    rejected_cnt, _            = pay_by_status.get("rejected", (0, 0))

    conversion  = round(active_cnt / total * 100, 1) if total > 0 else 0
    qa_users    = (await session.execute(
        select(func.count()).select_from(User).where(User.questions_used > 0)
    )).scalar() or 0
    engagement  = round(qa_users / total * 100, 1) if total > 0 else 0
    avg_lessons = round(course_lessons_sum / course_with_lessons, 1) if course_with_lessons > 0 else 0

    level_order = ["beginner", "hsk1", "hsk2", "hsk3", "hsk4"]
    level_str   = "  " + "   ".join(
        f"{l.upper()}: {level_counts.get(l, 0)}" for l in level_order
    )
    lang_str = "  " + " | ".join(f"{k}: {v}" for k, v in sorted(lang_counts.items()))
    now_str  = now.strftime("%d.%m.%Y %H:%M UTC")

    text = (
        f"📊 <b>Statistika</b>  <i>{now_str}</i>\n"
        f"{'─' * 32}\n\n"

        f"<b>👥 FOYDALANUVCHILAR  [{total}]</b>\n"
        f"  Free: <b>{free_cnt}</b>   Trial: <b>{trial_cnt}</b>\n"
        f"  Aktiv: <b>{active_cnt}</b>   Tugagan: <b>{expired_cnt}</b>   Bloklangan: <b>{blocked_cnt}</b>\n\n"

        f"<b>📅 FAOLLIK</b>\n"
        f"  Yangi:  bugun <b>+{new_today}</b>  |  hafta <b>+{new_week}</b>  |  oy <b>+{new_month}</b>\n"
        f"  Aktiv:  bugun <b>{active_today}</b>  |  hafta <b>{active_week}</b>\n\n"

        f"<b>📊 DARAJALAR</b>\n"
        f"{level_str}\n\n"

        f"<b>🌐 TIL</b>\n"
        f"{lang_str}\n\n"

        f"<b>🎯 O'QISH REJIMI</b>\n"
        f"  QA: <b>{mode_counts.get('qa', 0)}</b>   Kurs: <b>{mode_counts.get('course', 0)}</b>\n\n"

        f"<b>💳 TO'LOVLAR</b>\n"
        f"  Kutilmoqda: <b>{pending_cnt}</b>   Tasdiqlangan: <b>{approved_cnt}</b>   Rad: <b>{rejected_cnt}</b>\n"
        f"  10 kun: <b>{pay_by_plan.get('10_days', 0)}</b>   1 oy: <b>{pay_by_plan.get('1_month', 0)}</b>\n"
        f"  Jami daromad: <b>{approved_sum:,}</b> so'm\n\n"

        f"<b>📚 KURS</b>\n"
        f"  Yozilgan: <b>{course_total}</b>   Dars tugatganlar: <b>{course_with_lessons}</b>\n"
        f"  Jami tugatilgan darslar: <b>{course_lessons_sum}</b>   O'rtacha: <b>{avg_lessons}</b>\n"
        f"  Eslatma yoqilgan: <b>{course_reminders}</b>\n\n"

        f"<b>🎁 REFERALLAR</b>\n"
        f"  Jami: <b>{ref_total}</b>   Faollashgan: <b>{ref_activated}</b>   Bonus: <b>{ref_bonus}</b>\n"
        f"  Chegirma eligible: <b>{discount_eligible}</b>   Ishlatilgan: <b>{discount_used_cnt}</b>\n\n"

        f"<b>📈 KONVERSIYA</b>\n"
        f"  Free → Aktiv: <b>{conversion}%</b>\n"
        f"  Savol berganlar: <b>{qa_users}</b> (<b>{engagement}%</b>)"
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
        "Panelni ochish: <code>/broadcast</code>\n\n"
        "Panelda segmentni tanlab, matn/foto/video + caption yuboring.\n\n"
        "⚠️ Filtrsiz hammaga yuborish kerak bo'lsa: <code>/broadcast_all Xabar matni</code>",
        parse_mode="HTML",
    )


@router.message(Command("broadcast_all"))
async def admin_broadcast_handler(message: Message, session):
    if not _is_admin(message.from_user.id):
        return

    text = message.text.strip()[len("/broadcast_all"):].strip()
    if not text:
        await message.answer("Foydalanish: <code>/broadcast_all Xabar matni</code>", parse_mode="HTML")
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


@router.message(Command("audio_list"))
async def admin_audio_list_handler(message: Message, session):
    """Yuklangan audio fayllar ro'yxati: /audio_list hsk1 1"""
    if not _is_admin(message.from_user.id):
        return

    parts = message.text.strip().split()
    if len(parts) < 3:
        await message.answer(
            "Foydalanish: <code>/audio_list hsk1 1</code>\n"
            "(level va lesson_order)",
            parse_mode="HTML",
        )
        return

    level = parts[1].lower()
    try:
        lesson_order = int(parts[2])
    except ValueError:
        await message.answer("❌ lesson_order raqam bo'lishi kerak")
        return

    repo = CourseAudioRepository(session)
    rows = await repo.list_for_lesson(level, lesson_order)

    if not rows:
        await message.answer(f"🔇 {level} / lesson_{lesson_order:02d} uchun audio yo'q")
        return

    lines = [f"🎵 <b>{level} — Dars {lesson_order}</b>\n"]
    for row in rows:
        lines.append(f"  <code>{row.audio_type}</code> → <code>{row.file_id[:30]}…</code>")
    await message.answer("\n".join(lines), parse_mode="HTML")


@router.message(F.voice | F.audio | F.document)
async def admin_upload_audio_handler(message: Message, session):
    """Audio yuklash — voice, audio yoki mp3/ogg fayl sifatida yuboring.

    Caption (podpis) ga yozing:  hsk1 1 dialogue_1
    Format:  {level} {lesson_order} {audio_type}
    audio_type:  vocab | dialogue_1 | dialogue_2 | dialogue_3 | dialogue_4

    Misol caption:
      hsk1 1 vocab
      hsk1 1 dialogue_1
      hsk2 3 dialogue_2
    """
    if not _is_admin(message.from_user.id):
        raise SkipHandler()

    caption = (message.caption or "").strip().lower()
    import re
    m = re.match(r"^(hsk\d+)\s+(\d+)\s+(vocab|dialogue_\d+)$", caption)
    if not m:
        # Caption yo'q yoki noto'g'ri — yordam ko'rsat
        await message.answer(
            "📎 Fayl qabul qilindi, lekin <b>caption (podpis) noto'g'ri</b>.\n\n"
            "Faylni qaytadan yuboring, caption qatoriga quyidagi formatda yozing:\n"
            "<code>hsk1 1 dialogue_1</code>\n\n"
            "Misollар:\n"
            "<code>hsk1 1 vocab</code> — 1-dars so'zlar\n"
            "<code>hsk1 1 dialogue_1</code> — 1-dars 1-dialog\n"
            "<code>hsk1 1 dialogue_2</code> — 1-dars 2-dialog\n"
            "<code>hsk2 3 dialogue_1</code> — HSK2 3-dars 1-dialog",
            parse_mode="HTML",
        )
        return

    level = m.group(1)
    lesson_order = int(m.group(2))
    audio_type = m.group(3)

    # file_id olish — voice, audio yoki document (mp3 fayl)
    if message.voice:
        file_id = message.voice.file_id
    elif message.audio:
        file_id = message.audio.file_id
    elif message.document:
        file_id = message.document.file_id
    else:
        await message.answer("❌ Audio, voice yoki fayl yuboring")
        return

    repo = CourseAudioRepository(session)
    await repo.upsert(level=level, lesson_order=lesson_order, audio_type=audio_type, file_id=file_id)

    await message.answer(
        f"✅ Saqlandi!\n"
        f"📍 <b>{level}</b> · Dars <b>{lesson_order}</b> · <code>{audio_type}</code>\n"
        f"🔑 <code>{file_id[:50]}…</code>",
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
