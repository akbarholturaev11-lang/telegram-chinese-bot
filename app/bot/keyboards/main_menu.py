from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.bot.utils.i18n import t


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t("menu_start_lesson", lang))],
            [
                KeyboardButton(text=t("menu_profile", lang)),
                KeyboardButton(text=t("menu_subscription", lang)),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="...",
    )
