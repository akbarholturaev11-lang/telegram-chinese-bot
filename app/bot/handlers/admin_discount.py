from datetime import datetime, timedelta, timezone
from typing import Optional
from zoneinfo import ZoneInfo

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.config import settings
from app.bot.fsm.admin_discount import DiscountStates
from app.bot.keyboards.admin_discount import (
    discount_confirm_keyboard,
    discount_duration_keyboard,
    discount_language_keyboard,
    discount_list_keyboard,
    discount_panel_keyboard,
    discount_payment_method_keyboard,
    discount_plan_keyboard,
    discount_start_keyboard,
    discount_status_keyboard,
    discount_usage_keyboard,
)
from app.repositories.discount_campaign_repo import DiscountCampaignRepository

router = Router()

ADMIN_TZ = ZoneInfo("Asia/Shanghai")


def _is_admin(user_id: int) -> bool:
    admin_ids = [int(x.strip()) for x in settings.ADMIN_IDS.split(",") if x.strip()]
    return user_id in admin_ids


def _none_if_all(value: Optional[str]) -> Optional[str]:
    return None if value in (None, "all") else value


def _fmt_filter(value: Optional[str], default: str = "Hamma") -> str:
    return value or default


def _preview(data: dict) -> str:
    start_at = data["starts_at"]
    ends_at = start_at + timedelta(hours=data["duration_hours"])
    quota = data.get("quota_total") or "limitsiz"
    repeat = data.get("repeat_interval_days")
    usage = f"har {repeat} kunda" if repeat else "bir marta"
    return (
        "🎁 <b>Chegirma tasdiqlash</b>\n\n"
        f"Nomi: <b>{data['title']}</b>\n"
        f"Foiz: <b>{data['percent']}%</b>\n"
        f"Muddat: <b>{start_at.astimezone(ADMIN_TZ):%Y-%m-%d %H:%M}</b> dan "
        f"<b>{ends_at.astimezone(ADMIN_TZ):%Y-%m-%d %H:%M}</b> gacha\n"
        f"Kimlarga: status=<b>{_fmt_filter(data.get('audience_status'))}</b>, "
        f"til=<b>{_fmt_filter(data.get('audience_language'))}</b>\n"
        f"To'lov: <b>{_fmt_filter(data.get('payment_method'))}</b>, "
        f"tarif=<b>{_fmt_filter(data.get('plan_type'))}</b>\n"
        f"Limit: <b>{quota}</b>\n"
        f"Qoida: <b>{usage}</b>\n\n"
        "Tasdiqlaysizmi?"
    )


@router.callback_query(F.data == "adm:discount_panel")
async def admin_discount_panel(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.clear()
    await callback.answer()
    await callback.message.answer(
        "🎁 <b>Chegirma boshqaruvi</b>\n\n"
        "Admin kampaniya ochadi, checkoutda avtomatik narx tushadi va payment review'da manbasi ko'rinadi.",
        reply_markup=discount_panel_keyboard(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "disc:new")
async def discount_new(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.clear()
    await state.set_state(DiscountStates.waiting_title)
    await callback.answer()
    await callback.message.answer("Chegirma nomini yozing. Masalan: <b>May 20%</b>", parse_mode="HTML")


@router.message(StateFilter(DiscountStates.waiting_title))
async def discount_title(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return
    title = (message.text or "").strip()
    if len(title) < 2:
        await message.answer("Nomi juda qisqa. Qayta yozing.")
        return
    await state.update_data(title=title[:120])
    await state.set_state(DiscountStates.waiting_percent)
    await message.answer("Chegirma foizini yozing. Masalan: <b>20</b>", parse_mode="HTML")


@router.message(StateFilter(DiscountStates.waiting_percent))
async def discount_percent(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return
    try:
        percent = int((message.text or "").strip())
    except ValueError:
        await message.answer("Foiz raqam bo'lishi kerak. Masalan: 20")
        return
    if percent < 1 or percent > 90:
        await message.answer("Foiz 1 dan 90 gacha bo'lsin.")
        return
    await state.update_data(percent=percent)
    await state.set_state(None)
    await message.answer("Chegirma qancha davom etadi?", reply_markup=discount_duration_keyboard())


@router.callback_query(F.data.startswith("disc:duration:"))
async def discount_duration(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    value = callback.data.split(":")[2]
    await callback.answer()
    if value == "custom":
        await state.set_state(DiscountStates.waiting_custom_duration)
        await callback.message.answer("Davomiylikni soatda yozing. Masalan: <b>48</b>", parse_mode="HTML")
        return
    await state.update_data(duration_hours=int(value))
    await callback.message.answer("Kimlarga beriladi? Status tanlang:", reply_markup=discount_status_keyboard())


@router.message(StateFilter(DiscountStates.waiting_custom_duration))
async def discount_custom_duration(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return
    try:
        hours = int((message.text or "").strip())
    except ValueError:
        await message.answer("Soat raqam bo'lishi kerak. Masalan: 48")
        return
    if hours < 1 or hours > 24 * 365:
        await message.answer("Muddat 1 soatdan 365 kungacha bo'lsin.")
        return
    await state.update_data(duration_hours=hours)
    await state.set_state(None)
    await message.answer("Kimlarga beriladi? Status tanlang:", reply_markup=discount_status_keyboard())


@router.callback_query(F.data.startswith("disc:status:"))
async def discount_status(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.update_data(audience_status=_none_if_all(callback.data.split(":")[2]))
    await callback.answer()
    await callback.message.answer("Qaysi til segmentiga?", reply_markup=discount_language_keyboard())


@router.callback_query(F.data.startswith("disc:lang:"))
async def discount_language(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.update_data(audience_language=_none_if_all(callback.data.split(":")[2]))
    await callback.answer()
    await callback.message.answer("Qaysi to'lov turiga?", reply_markup=discount_payment_method_keyboard())


@router.callback_query(F.data.startswith("disc:method:"))
async def discount_payment_method(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.update_data(payment_method=_none_if_all(callback.data.split(":")[2]))
    await callback.answer()
    await callback.message.answer("Qaysi tarifga?", reply_markup=discount_plan_keyboard())


@router.callback_query(F.data.startswith("disc:plan:"))
async def discount_plan(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.update_data(plan_type=_none_if_all(callback.data.split(":")[2]))
    await callback.answer()
    await callback.message.answer("Qachon ishga tushsin?", reply_markup=discount_start_keyboard())


@router.callback_query(F.data.startswith("disc:start:"))
async def discount_start(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    mode = callback.data.split(":")[2]
    await callback.answer()
    if mode == "scheduled":
        await state.set_state(DiscountStates.waiting_start_at)
        await callback.message.answer(
            "Boshlanish vaqtini yozing: <code>YYYY-MM-DD HH:MM</code>\n"
            "Vaqt zonasi: Asia/Shanghai",
            parse_mode="HTML",
        )
        return
    await state.update_data(starts_at=datetime.now(timezone.utc))
    await callback.message.answer("Bir martami yoki takrorlanadimi?", reply_markup=discount_usage_keyboard())


@router.message(StateFilter(DiscountStates.waiting_start_at))
async def discount_start_at(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return
    raw = (message.text or "").strip()
    try:
        local_dt = datetime.strptime(raw, "%Y-%m-%d %H:%M").replace(tzinfo=ADMIN_TZ)
    except ValueError:
        await message.answer("Format noto'g'ri. Masalan: <code>2026-05-13 21:30</code>", parse_mode="HTML")
        return
    await state.update_data(starts_at=local_dt.astimezone(timezone.utc))
    await state.set_state(None)
    await message.answer("Bir martami yoki takrorlanadimi?", reply_markup=discount_usage_keyboard())


@router.callback_query(F.data.startswith("disc:usage:"))
async def discount_usage(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    value = callback.data.split(":")[2]
    await callback.answer()
    if value == "repeat":
        await state.set_state(DiscountStates.waiting_repeat_days)
        await callback.message.answer("Necha kunda qayta olish mumkin? Masalan: <b>7</b>", parse_mode="HTML")
        return
    await state.update_data(repeat_interval_days=None)
    await state.set_state(DiscountStates.waiting_quota)
    await callback.message.answer("Limit nechta user? 0 yozsangiz limitsiz. Masalan: <b>20</b>", parse_mode="HTML")


@router.message(StateFilter(DiscountStates.waiting_repeat_days))
async def discount_repeat_days(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return
    try:
        days = int((message.text or "").strip())
    except ValueError:
        await message.answer("Kun raqam bo'lishi kerak. Masalan: 7")
        return
    if days < 1 or days > 365:
        await message.answer("Takror oralig'i 1-365 kun bo'lsin.")
        return
    await state.update_data(repeat_interval_days=days)
    await state.set_state(DiscountStates.waiting_quota)
    await message.answer("Limit nechta user? 0 yozsangiz limitsiz. Masalan: <b>20</b>", parse_mode="HTML")


@router.message(StateFilter(DiscountStates.waiting_quota))
async def discount_quota(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return
    try:
        quota = int((message.text or "").strip())
    except ValueError:
        await message.answer("Limit raqam bo'lishi kerak. Masalan: 20 yoki 0")
        return
    if quota < 0:
        await message.answer("Limit manfiy bo'lmaydi.")
        return
    await state.update_data(quota_total=quota or None)
    data = await state.get_data()
    await state.set_state(None)
    await message.answer(_preview(data), reply_markup=discount_confirm_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "disc:confirm")
async def discount_confirm(callback: CallbackQuery, state: FSMContext, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    data = await state.get_data()
    required = ["title", "percent", "duration_hours", "starts_at"]
    if any(key not in data for key in required):
        await callback.answer("Ma'lumot yetishmayapti", show_alert=True)
        return

    starts_at = data["starts_at"]
    ends_at = starts_at + timedelta(hours=data["duration_hours"])
    repo = DiscountCampaignRepository(session)
    campaign = await repo.create(
        title=data["title"],
        percent=data["percent"],
        starts_at=starts_at,
        ends_at=ends_at,
        audience_status=data.get("audience_status"),
        audience_language=data.get("audience_language"),
        payment_method=data.get("payment_method"),
        plan_type=data.get("plan_type"),
        quota_total=data.get("quota_total"),
        repeat_interval_days=data.get("repeat_interval_days"),
        created_by_telegram_id=callback.from_user.id,
    )
    await session.commit()
    await state.clear()
    await callback.answer("Chegirma saqlandi", show_alert=True)
    await callback.message.edit_text(
        f"✅ Chegirma #{campaign.id} saqlandi.\n"
        f"Ishga tushish: {starts_at.astimezone(ADMIN_TZ):%Y-%m-%d %H:%M}",
        reply_markup=None,
    )


@router.callback_query(F.data == "disc:list")
async def discount_list(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    repo = DiscountCampaignRepository(session)
    campaigns = await repo.list_recent(10)
    if not campaigns:
        await callback.answer()
        await callback.message.answer("Hozircha chegirma kampaniyasi yo'q.", reply_markup=discount_panel_keyboard())
        return

    lines = ["📋 <b>Oxirgi chegirmalar</b>\n"]
    now = datetime.now(timezone.utc)
    for item in campaigns:
        status = "aktiv" if item.is_active and item.starts_at <= now < item.ends_at else "passiv"
        used = await repo.count_used(item.id)
        quota = item.quota_total or "∞"
        lines.append(
            f"#{item.id} {item.title} — {item.percent}% | {status} | {used}/{quota}"
        )
    await callback.answer()
    await callback.message.answer(
        "\n".join(lines),
        reply_markup=discount_list_keyboard(campaigns),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("disc:disable:"))
async def discount_disable(callback: CallbackQuery, session):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    campaign_id = int(callback.data.split(":")[2])
    repo = DiscountCampaignRepository(session)
    campaign = await repo.get_by_id(campaign_id)
    if not campaign:
        await callback.answer("Topilmadi", show_alert=True)
        return
    await repo.deactivate(campaign)
    await session.commit()
    await callback.answer("O'chirildi", show_alert=True)
    await callback.message.answer(f"⛔ Chegirma #{campaign_id} o'chirildi.")


@router.callback_query(F.data == "disc:cancel")
async def discount_cancel(callback: CallbackQuery, state: FSMContext):
    if not _is_admin(callback.from_user.id):
        await callback.answer()
        return
    await state.clear()
    await callback.answer()
    await callback.message.answer("❌ Chegirma yaratish bekor qilindi.", reply_markup=discount_panel_keyboard())
