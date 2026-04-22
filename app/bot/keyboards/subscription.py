from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.utils.i18n import t


def subscription_main_keyboard(lang: str, show_discount: bool = True) -> InlineKeyboardMarkup:
    rows = []

    # Invite button shown FIRST — only if user hasn't used discount yet
    if show_discount:
        rows.append([
            InlineKeyboardButton(
                text=t("subscription_referral_discount_button", lang),
                callback_data="subscription:referral_discount",
            )
        ])

    rows.append([
        InlineKeyboardButton(
            text=t("subscription_button_10_days", lang),
            callback_data="subscription:plan:10_days",
        ),
        InlineKeyboardButton(
            text=t("subscription_button_1_month", lang),
            callback_data="subscription:plan:1_month",
        ),
    ])
    rows.append([
        InlineKeyboardButton(
            text=t("payment_back", lang),
            callback_data="subscription:change_payment_method",
        ),
    ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def subscription_discount_progress_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Shown while waiting for 3 referrals — only back button."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("subscription_back_to_main", lang),
                    callback_data="subscription:back_to_main",
                )
            ]
        ]
    )


def subscription_discount_ready_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Shown when 3/3 referrals reached — plan buttons + back."""
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
            [
                InlineKeyboardButton(
                    text=t("subscription_back_to_main", lang),
                    callback_data="subscription:back_to_main",
                ),
            ],
        ]
    )


def payment_method_keyboard(lang: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="VISA", callback_data="payment:visa"),
        ],
        [
            InlineKeyboardButton(text="Alipay", callback_data="payment:alipay"),
        ],
        [
            InlineKeyboardButton(text="WeChat Pay", callback_data="payment:wechat"),
        ],
        [
            InlineKeyboardButton(text=t("payment_back", lang), callback_data="payment:back"),
        ]
    ])
