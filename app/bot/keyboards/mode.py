from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.utils.i18n import t


def mode_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("qa_mode_title", lang),
                    callback_data="mode:qa",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("course_mode_title", lang),
                    callback_data="mode:course",
                )
            ],
        ]
    )
