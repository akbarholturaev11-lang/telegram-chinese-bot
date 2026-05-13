from pathlib import Path
from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile

from app.config import settings
from app.repositories.user_repo import UserRepository
from app.services.discount_service import DiscountService
from app.services.payment_service import PaymentService
from app.bot.utils.discount_formatter import build_admin_discount_block, build_discount_plan_line
from app.bot.utils.i18n import t
from app.bot.keyboards.subscription import (
    subscription_discount_progress_keyboard,
    subscription_discount_ready_keyboard,
    payment_method_keyboard,
)
from app.bot.keyboards.checkout import checkout_keyboard


router = Router()

# subscription.py → bot/handlers/ → bot/ → app/ → project root → app/static/payments/
_STATIC_PAYMENTS = Path(__file__).parent.parent.parent / "static" / "payments"

QR_PHOTO_PATHS = {
    "alipay_10_days":          str(_STATIC_PAYMENTS / "alipay_10_days.jpg"),
    "alipay_10_days_discount": str(_STATIC_PAYMENTS / "alipay_10_days_discount.jpg"),
    "alipay_1_month":          str(_STATIC_PAYMENTS / "alipay_1_month.jpg"),
    "alipay_1_month_discount": str(_STATIC_PAYMENTS / "alipay_1_month_discount.jpg"),
    "wechat_10_days":          str(_STATIC_PAYMENTS / "wechat_10_days.jpg"),
    "wechat_10_days_discount": str(_STATIC_PAYMENTS / "wechat_10_days_discount.jpg"),
    "wechat_1_month":          str(_STATIC_PAYMENTS / "wechat_1_month.jpg"),
    "wechat_1_month_discount": str(_STATIC_PAYMENTS / "wechat_1_month_discount.jpg"),
    "alipay_admin_discount":    str(_STATIC_PAYMENTS / "alipay_admin_discount.jpg"),
    "wechat_admin_discount":    str(_STATIC_PAYMENTS / "wechat_admin_discount.jpg"),
}


def _plan_price(plan_type: str, payment_method: str | None) -> tuple[int, str]:
    if payment_method in ("alipay", "wechat"):
        return (66 if plan_type == "1_month" else 29), "¥"
    return (89 if plan_type == "1_month" else 29), "somoni"


async def _admin_discount_offer(session, user, lang: str) -> str | None:
    service = DiscountService(session)
    plan_choices = {}
    for plan in ("10_days", "1_month"):
        choice = await service.get_best_admin_discount(
            user=user,
            plan_type=plan,
            payment_method=user.payment_method,
        )
        if choice.source == "admin_campaign" and choice.ends_at and choice.starts_at:
            plan_choices[plan] = choice

    if not plan_choices:
        return None

    main_choice = max(plan_choices.values(), key=lambda item: item.percent)
    lines = []
    for plan in ("10_days", "1_month"):
        base, currency = _plan_price(plan, user.payment_method)
        choice = plan_choices.get(plan)
        percent = choice.percent if choice else 0
        lines.append(
            build_discount_plan_line(
                lang=lang,
                plan=plan,
                base=base,
                currency=currency,
                percent=percent,
            )
        )

    return build_admin_discount_block(
        lang=lang,
        discount=main_choice,
        percent=main_choice.percent,
        starts_at=main_choice.starts_at,
        ends_at=main_choice.ends_at,
        quota_total=main_choice.quota_total,
        repeat_interval_days=main_choice.repeat_interval_days,
        plan_lines="\n".join(lines),
        now=datetime.now(timezone.utc),
    )


def build_subscription_main_text_for_user(user, lang: str, admin_discount_block: str | None = None) -> str:
    if admin_discount_block:
        return admin_discount_block

    use_yuan = getattr(user, "payment_method", None) in ("alipay", "wechat")

    plan_10_key = "subscription_plan_10_days_yuan" if use_yuan else "subscription_plan_10_days"
    plan_1m_key = "subscription_plan_1_month_yuan" if use_yuan else "subscription_plan_1_month"

    base = (
        f"{t('subscription_main_title', lang)}\n\n"
        f"{t(plan_10_key, lang)}\n"
        f"{t(plan_1m_key, lang)}"
    )

    # Show discount hint only if user hasn't used it yet
    if not user.discount_used:
        base += f"\n\n{t('subscription_referral_hint', lang)}"

    return base


def build_subscription_discount_progress_text(
    lang: str,
    referral_link: str,
    count: int,
    discount_eligible: bool = False,
    discount_used: bool = False,
    payment_method: str = None,
) -> str:
    base = (
        f"{t('subscription_discount_title', lang)}\n\n"
        f"{t('subscription_discount_link_label', lang)}\n"
        f"{referral_link}\n\n"
        f"{t('subscription_discount_progress', lang, count=count)}"
    )

    if discount_eligible and not discount_used:
        # Show correct currency prices based on payment method
        is_yuan = payment_method in ("alipay", "wechat")
        plan_10_key = "subscription_discount_plan_10_days_yuan" if is_yuan else "subscription_discount_plan_10_days"
        plan_1m_key = "subscription_discount_plan_1_month_yuan" if is_yuan else "subscription_discount_plan_1_month"

        base += (
            f"\n\n{t('subscription_discount_ready', lang)}\n\n"
            f"{t(plan_10_key, lang)}\n"
            f"{t(plan_1m_key, lang)}"
        )

    return base


def build_subscription_main_keyboard_for_user(user, lang: str, show_referral: bool = True) -> InlineKeyboardMarkup:
    rows = [
        [
            InlineKeyboardButton(
                text=t("subscription_button_10_days", lang),
                callback_data="subscription:plan:10_days",
            ),
            InlineKeyboardButton(
                text=t("subscription_button_1_month", lang),
                callback_data="subscription:plan:1_month",
            ),
        ],
    ]
    if show_referral and not user.discount_used:
        rows.append([
            InlineKeyboardButton(
                text=t("subscription_referral_discount_button", lang),
                callback_data="subscription:referral_discount",
            )
        ])
    rows.append([
        InlineKeyboardButton(
            text=t("payment_back", lang),
            callback_data="subscription:change_payment_method",
        ),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def build_subscription_main_view(session, user, lang: str) -> tuple[str, InlineKeyboardMarkup]:
    admin_discount_block = await _admin_discount_offer(session, user, lang)
    return (
        build_subscription_main_text_for_user(user, lang, admin_discount_block),
        build_subscription_main_keyboard_for_user(user, lang, show_referral=not bool(admin_discount_block)),
    )


def build_checkout_text(lang: str, checkout_info: dict) -> str:
    plan_type = checkout_info["plan_type"]
    base_amount = checkout_info["base_amount"]
    final_amount = checkout_info["final_amount"]
    discount_applied = checkout_info["discount_applied"]
    currency = checkout_info["currency"]
    is_qr = (currency == "¥")

    if lang == "tj":
        plan_label = "10 рӯз" if plan_type == "10_days" else "1 моҳ"
        plan_line = f"Тариф: {plan_label}"
    elif lang == "uz":
        plan_label = "10 kunlik" if plan_type == "10_days" else "1 oylik"
        plan_line = f"Tarif: {plan_label}"
    else:
        plan_label = "10 дней" if plan_type == "10_days" else "1 месяц"
        plan_line = f"Тариф: {plan_label}"

    title_key = "checkout_title_qr" if is_qr else "checkout_title_visa"

    lines = [
        t(title_key, lang),
        plan_line,
        "",
    ]

    if discount_applied:
        lines.append(f"{t('subscription_original_price_label', lang)}: {base_amount} {currency}")
        percent = checkout_info.get("discount_percent", 20)
        lines.append(f"💎 {t('subscription_discounted_price_label', lang)}: {final_amount} {currency} (-{percent}%)")
    else:
        lines.append(f"{t('subscription_price_label', lang)}: {final_amount} {currency}")

    lines.append("")

    if is_qr:
        lines.append(t("checkout_qr_scan", lang))
    else:
        lines.append(f"{t('payment_details_label', lang)}: {settings.PAYMENT_DETAILS}")

    lines.extend([
        "",
        t("payment_send_screenshot", lang),
    ])

    return "\n".join(lines)


@router.callback_query(F.data == "subscription:open")
async def subscription_open_handler(callback: CallbackQuery, session):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"

    await callback.answer()
    await callback.message.edit_text(
        t("payment_method_choose", lang),
        reply_markup=payment_method_keyboard(lang),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "subscription:referral_discount")
async def subscription_referral_discount_handler(callback: CallbackQuery, session):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    if not user:
        await callback.answer()
        return

    # Guard: if user already used discount — ignore silently
    if user.discount_used:
        await callback.answer()
        return

    await user_repo.ensure_referral_code(user)

    # Only start the offer once — do NOT reset count on repeated clicks
    if not user.discount_offer_started_at:
        await user_repo.start_discount_offer(user)

    await session.flush()

    lang = user.language if user.language else "ru"
    referral_link = f"https://t.me/{settings.BOT_USERNAME}?start={user.referral_code}"
    count = user.discount_referral_count

    text = build_subscription_discount_progress_text(
        lang,
        referral_link,
        count,
        discount_eligible=user.discount_eligible,
        discount_used=user.discount_used,
        payment_method=user.payment_method,
    )
    keyboard = (
        subscription_discount_ready_keyboard(lang)
        if user.discount_eligible and not user.discount_used
        else subscription_discount_progress_keyboard(lang)
    )

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )

    await user_repo.set_discount_progress_message(
        user=user,
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
    )
    await session.commit()
    await callback.answer()


@router.callback_query(F.data == "subscription:back_to_main")
async def subscription_back_to_main_handler(callback: CallbackQuery, session):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"
    text, keyboard = await build_subscription_main_view(session, user, lang)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    await user_repo.clear_discount_progress_message(user)
    await session.commit()


@router.callback_query(F.data == "payment:visa")
async def payment_visa_handler(callback: CallbackQuery, session):

    await callback.answer()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        return

    user.payment_method = "visa"
    await session.commit()

    lang = user.language if user.language else "ru"
    text, keyboard = await build_subscription_main_view(session, user, lang)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "payment:alipay")
async def payment_alipay_handler(callback: CallbackQuery, session):

    await callback.answer()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        return

    user.payment_method = "alipay"
    await session.commit()

    lang = user.language if user.language else "ru"
    text, keyboard = await build_subscription_main_view(session, user, lang)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "payment:wechat")
async def payment_wechat_handler(callback: CallbackQuery, session):

    await callback.answer()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        return

    user.payment_method = "wechat"
    await session.commit()

    lang = user.language if user.language else "ru"
    text, keyboard = await build_subscription_main_view(session, user, lang)

    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "checkout:change_plan")
async def checkout_change_plan_handler(callback: CallbackQuery, session):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"

    await user_repo.set_selected_plan_type(user, None)
    await session.commit()

    text, keyboard = await build_subscription_main_view(session, user, lang)

    try:
        await callback.message.edit_text(
            text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    except Exception:
        # message is a photo (QR checkout) — delete and send new text message
        await callback.message.delete()
        await callback.message.answer(
            text,
            reply_markup=keyboard,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    await callback.answer()


@router.callback_query(F.data.startswith("subscription:plan:"))
async def subscription_plan_handler(callback: CallbackQuery, session):
    await callback.answer()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    if not user:
        return

    lang = user.language or "ru"

    if not user.payment_method:
        await callback.message.edit_text(
            t("payment_method_choose", lang),
            reply_markup=payment_method_keyboard(lang),
            parse_mode="HTML",
        )
        return

    plan = callback.data.split(":")[-1]

    payment_service = PaymentService(session)
    payment, checkout_info, error_key = await payment_service.create_checkout_draft(
        telegram_id=callback.from_user.id,
        plan_type=plan,
    )

    if not payment or not checkout_info:
        if error_key:
            await callback.message.answer(t(error_key, lang))
        return

    await user_repo.set_selected_plan_type(user, plan)
    await session.commit()

    text = build_checkout_text(lang, checkout_info)
    keyboard = checkout_keyboard(lang)

    checkout_msg_id: int | None = None

    if checkout_info["currency"] == "¥":
        # Send QR photo for Alipay / WeChat — pick correct image by method + plan + discount
        if checkout_info.get("discount_source") == "admin_campaign":
            qr_key = f"{user.payment_method}_admin_discount"
        else:
            qr_key = f"{user.payment_method}_{plan}"
            if checkout_info.get("discount_applied"):
                qr_key += "_discount"
        photo_path = QR_PHOTO_PATHS.get(qr_key)
        if photo_path:
            photo = FSInputFile(photo_path)
            try:
                await callback.message.delete()
            except Exception:
                pass
            sent = await callback.message.answer_photo(
                photo,
                caption=text,
                reply_markup=keyboard,
            )
            checkout_msg_id = sent.message_id
        else:
            sent = await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
            checkout_msg_id = callback.message.message_id
    else:
        # VISA — text message
        try:
            await callback.message.edit_text(
                text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
            checkout_msg_id = callback.message.message_id
        except Exception:
            await callback.message.delete()
            sent = await callback.message.answer(
                text,
                reply_markup=keyboard,
                disable_web_page_preview=True,
            )
            checkout_msg_id = sent.message_id

    await user_repo.set_pending_checkout_msg_id(user, checkout_msg_id)
    await session.commit()


@router.callback_query(F.data == "payment:back")
async def payment_back_handler(callback: CallbackQuery, session):
    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass


@router.callback_query(F.data == "payment:retry")
async def payment_retry_handler(callback: CallbackQuery, session):
    from app.repositories.user_repo import UserRepository

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"
    text, keyboard = await build_subscription_main_view(session, user, lang)
    await callback.answer()
    await callback.message.answer(
        text,
        reply_markup=keyboard,
        parse_mode="HTML",
    )


@router.callback_query(F.data == "subscription:change_payment_method")
async def subscription_change_payment_method_handler(callback: CallbackQuery, session):
    await callback.answer()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    if not user:
        return

    lang = user.language if user.language else "ru"

    await callback.message.edit_text(
        t("payment_method_choose", lang),
        reply_markup=payment_method_keyboard(lang),
        parse_mode="HTML",
    )
