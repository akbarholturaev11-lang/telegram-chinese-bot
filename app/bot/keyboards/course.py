from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.utils.i18n import t


def course_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "tj": "📚 Дарсро оғоз кунед",
        "uz": "📚 Darsni boshlash",
        "ru": "📚 Начать урок",
    }
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=labels.get(lang, labels["ru"]),
                callback_data="course:continue",
            )
        ]]
    )


def review_choice_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "tj": {"yes": "🔁 Такрор", "no": "▶️ Давом"},
        "uz": {"yes": "🔁 Takror", "no": "▶️ Davom"},
        "ru": {"yes": "🔁 Повторить", "no": "▶️ Продолжить"},
    }
    l = labels.get(lang, labels["ru"])
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=l["yes"], callback_data="course:review_last"),
            InlineKeyboardButton(text=l["no"], callback_data="course:continue"),
        ]]
    )


def lesson_selection_keyboard(
    lessons: list,
    page: int = 0,
    lang: str = "ru",
) -> InlineKeyboardMarkup:
    if not lessons:
        return InlineKeyboardMarkup(inline_keyboard=[])

    level = lessons[0].level if lessons else "hsk1"
    page_size = 10 if level == "hsk4" else 7

    start = page * page_size
    end = start + page_size
    page_lessons = lessons[start:end]
    total = len(lessons)

    buttons = []
    for lesson in page_lessons:
        buttons.append([
            InlineKeyboardButton(
                text=f"{lesson.lesson_order}. {lesson.title}",
                callback_data=f"course:pick_lesson:{lesson.id}",
            )
        ])

    nav = []
    if level == "hsk4":
        if page > 0:
            nav.append(InlineKeyboardButton(
                text="⬆️ 上",
                callback_data=f"course:lessons_page:{page - 1}",
            ))
        if end < total:
            nav.append(InlineKeyboardButton(
                text="⬇️ 下",
                callback_data=f"course:lessons_page:{page + 1}",
            ))
    else:
        prev_labels = {"tj": "⬅️ Қабл", "uz": "⬅️ Oldingi", "ru": "⬅️ Назад"}
        next_labels = {"tj": "Баъд ➡️", "uz": "Keyingi ➡️", "ru": "Далее ➡️"}
        if page > 0:
            nav.append(InlineKeyboardButton(
                text=prev_labels.get(lang, "⬅️"),
                callback_data=f"course:lessons_page:{page - 1}",
            ))
        if end < total:
            nav.append(InlineKeyboardButton(
                text=next_labels.get(lang, "➡️"),
                callback_data=f"course:lessons_page:{page + 1}",
            ))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
