from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.utils.i18n import t


def course_resume_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("course_resume_lesson", lang),
                    callback_data="course:continue",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("course_back_to_qa", lang),
                    callback_data="course:back_to_qa",
                )
            ],
        ]
    )


def course_review_offer_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("course_review_yesterday", lang),
                    callback_data="course:review_last",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("course_skip_review", lang),
                    callback_data="course:continue",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("course_back_to_qa", lang),
                    callback_data="course:back_to_qa",
                )
            ],
        ]
    )


def course_satisfaction_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("course_lesson_satisfied_yes", lang),
                    callback_data="course:satisfied_yes",
                ),
                InlineKeyboardButton(
                    text=t("course_lesson_satisfied_no", lang),
                    callback_data="course:satisfied_no",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=t("course_back_to_qa", lang),
                    callback_data="course:back_to_qa",
                )
            ],
        ]
    )


def course_homework_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("course_start_homework", lang),
                    callback_data="course:show_homework",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("course_back_to_qa", lang),
                    callback_data="course:back_to_qa",
                )
            ],
        ]
    )


def course_next_lesson_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("course_start_next_lesson", lang),
                    callback_data="course:start_next_lesson",
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("course_back_to_qa", lang),
                    callback_data="course:back_to_qa",
                )
            ],
        ]
    )
