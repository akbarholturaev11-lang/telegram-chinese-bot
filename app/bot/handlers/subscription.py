from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile

from app.config import settings
from app.repositories.user_repo import UserRepository
from app.services.payment_service import PaymentService
from app.bot.utils.i18n import t
from app.bot.keyboards.subscription import (
    subscription_main_keyboard,
    subscription_discount_progress_keyboard,
    subscription_discount_ready_keyboard,
    payment_method_keyboard,
)
from app.bot.keyboards.checkout import checkout_keyboard


router = Router()


def build_subscription_main_text_for_user(user, lang: str) -> str:
    base = (
        f"{t('subscription_main_title', lang)}\n\n"
        f"{t('subscription_plan_10_days', lang)}\n"
        f"{t('subscription_plan_1_month', lang)}"
    )

    if not user.discount_used:
        base += f"\n\n{t('subscription_referral_hint', lang)}"

    return base


def build_subscription_discount_progress_text(
    lang: str,
    referral_link: str,
    count: int,
    discount_eligible: bool = False,
    discount_used: bool = False,
) -> str:
    base = (
        f"{t('subscription_discount_title', lang)}\n\n"
        f"{t('subscription_discount_link_label', lang)}\n"
        f"{referral_link}\n\n"
        f"{t('subscription_discount_progress', lang, count=count)}"
    )

    if discount_eligible and not discount_used:
        base += (
            f"\n\n{t('subscription_discount_ready', lang)}\n\n"
            f"{t('subscription_discount_plan_10_days', lang)}\n"
            f"{t('subscription_discount_plan_1_month', lang)}"
        )

    return base



def build_subscription_main_keyboard_for_user(user, lang: str) -> InlineKeyboardMarkup:
    if user.discount_used:
        return InlineKeyboardMarkup(
            inline_keyboard=[
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
        )

    return subscription_main_keyboard(lang)


def build_checkout_text(lang: str, checkout_info: dict) -> str:
    plan_type = checkout_info["plan_type"]
    base_amount = checkout_info["base_amount"]
    final_amount = checkout_info["final_amount"]
    discount_applied = checkout_info["discount_applied"]
    currency = checkout_info["currency"]

    if lang == "tj":
        plan_label = "10 рӯз" if plan_type == "10_days" else "1 моҳ"
        plan_line = f"Тариф: {plan_label}"
    elif lang == "uz":
        plan_label = "10 kunlik" if plan_type == "10_days" else "1 oylik"
        plan_line = f"Tarif: {plan_label}"
    else:
        plan_label = "10 дней" if plan_type == "10_days" else "1 месяц"
        plan_line = f"Тариф: {plan_label}"

    lines = [
        t("subscription_checkout_title", lang),
        plan_line,
        "",
    ]

    if discount_applied:
        lines.append(f"{t('subscription_original_price_label', lang)}: {base_amount} {currency}")
        lines.append(f"{t('subscription_discounted_price_label', lang)}: {final_amount} {currency}")
    else:
        lines.append(f"{t('subscription_price_label', lang)}: {final_amount} {currency}")

    lines.extend([
        "",
        f"{t('payment_details_label', lang)}: {settings.PAYMENT_DETAILS}",
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

    await user_repo.ensure_referral_code(user)
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

    await callback.message.edit_text(
        build_subscription_main_text_for_user(user, lang),
        reply_markup=build_subscription_main_keyboard_for_user(user, lang),
        disable_web_page_preview=True,
    )

    await user_repo.clear_discount_progress_message(user)
    await session.commit()
    await callback.answer()


@router.callback_query(F.data == "payment:visa")
async def payment_visa_handler(callback: CallbackQuery, session):

    await callback.answer()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"

    await callback.message.edit_text(
        build_subscription_main_text_for_user(user, lang),
        reply_markup=build_subscription_main_keyboard_for_user(user, lang),
    )

    await callback.answer()


@router.callback_query(F.data == "payment:alipay")
async def payment_alipay_handler(callback: CallbackQuery, session):

    await callback.answer()

    user_repo = UserRepo(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    user.payment_method = "alipay"
    await session.commit()

    lang = user.language

    await callback.message.edit_text(
        t("subscription_main_title", lang),
        reply_markup=subscription_plan_keyboard(lang)
    )


@router.callback_query(F.data == "payment:wechat")
async def payment_wechat_handler(callback: CallbackQuery, session):

    await callback.answer()

    user_repo = UserRepo(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    user.payment_method = "wechat"
    await session.commit()

    lang = user.language

    await callback.message.edit_text(
        t("subscription_main_title", lang),
        reply_markup=subscription_plan_keyboard(lang)
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

    await callback.message.edit_text(
        build_subscription_main_text_for_user(user, lang),
        reply_markup=build_subscription_main_keyboard_for_user(user, lang),
        disable_web_page_preview=True,
    )


@router.callback_query(F.data.startswith("subscription:plan:"))
async def subscription_plan_handler(callback: CallbackQuery, session):
    user_repo = UserRepository(session)
    payment_service = PaymentService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"
    plan_type = callback.data.split(":")[2]

    await user_repo.set_selected_plan_type(user, plan_type)
    await session.commit()

    checkout_info, error_key = await payment_service.get_checkout_info(
        telegram_id=callback.from_user.id,
        plan_type=plan_type,
    )
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    await callback.answer()

    method = user.payment_method

    text = t(
        "subscription_checkout_block",
        lang,
        plan=checkout_info["plan_name"],
        price=checkout_info["final_amount"]
    )

    if method == "visa":
        await callback.message.edit_text(
            text,
            reply_markup=checkout_keyboard(lang),
            parse_mode="HTML"
        )

    elif method == "alipay":
        photo = FSInputFile("app/static/payments/alipay.jpg")

        await callback.message.delete()

        await callback.message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=checkout_keyboard(lang),
            parse_mode="HTML"
        )

    elif method == "wechat":
        photo = FSInputFile("app/static/payments/wechat.jpg")

        await callback.message.delete()

        await callback.message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=checkout_keyboard(lang),
            parse_mode="HTML"
        )
