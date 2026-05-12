from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import select, func
from datetime import datetime, timezone, timedelta

from app.config import settings
from app.repositories.user_repo import UserRepository
from app.repositories.course_audio_repo import CourseAudioRepository
from app.db.models.user import User
from app.db.models.payment import Payment
from app.db.models.course_progress import CourseProgress
from app.db.models.referral import Referral

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
        [InlineKeyboardButton(text="🎵 Audio boshqaruv", callback_data="adm:audio_panel")],
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
        return

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
