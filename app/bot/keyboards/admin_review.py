from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.utils.i18n import t


def admin_payment_review_keyboard(payment_id: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("admin_approve_button", lang),
                    callback_data=f"admin_payment:approve:{payment_id}",
                ),
                InlineKeyboardButton(
                    text=t("admin_reject_button", lang),
                    callback_data=f"admin_payment:reject:{payment_id}",
                ),
            ]
        ]
    )
