from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.utils.i18n import t


LIKED_OPTIONS = ("course", "answers", "photo", "practice", "other")
DISLIKED_OPTIONS = ("price", "limits", "unclear", "pace", "other")


def feedback_like_label(code: str, lang: str) -> str:
    return t(f"feedback_like_{code}", lang)


def feedback_dislike_label(code: str, lang: str) -> str:
    return t(f"feedback_dislike_{code}", lang)


def feedback_like_keyboard(feedback_id: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=feedback_like_label(code, lang),
                    callback_data=f"fb:{feedback_id}:like:{code}",
                )
            ]
            for code in LIKED_OPTIONS
        ]
    )


def feedback_dislike_keyboard(feedback_id: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=feedback_dislike_label(code, lang),
                    callback_data=f"fb:{feedback_id}:dislike:{code}",
                )
            ]
            for code in DISLIKED_OPTIONS
        ]
    )


def feedback_cancel_keyboard(feedback_id: int, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("feedback_cancel_button", lang),
                    callback_data=f"fb:{feedback_id}:cancel_other",
                )
            ]
        ]
    )
