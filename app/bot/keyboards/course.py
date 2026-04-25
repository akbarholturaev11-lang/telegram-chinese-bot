from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def course_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "tj": "📚 Дарсро оғоз кунед",
        "uz": "📚 Darsni boshlash",
        "ru": "📚 Начать урок",
    }
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text=labels.get(lang, labels["ru"]), callback_data="course:continue")
        ]]
    )


def lesson_selection_keyboard(lessons: list, page: int = 0, lang: str = "ru") -> InlineKeyboardMarkup:
    """
    Shows lessons in pages of 7.
    HSK1: 15 lessons → page 0: lessons 1-7, page 1: lessons 8-15
    HSK2: 15 lessons → same
    HSK3: 20 lessons → page 0: 1-7, page 1: 8-14, page 2: 15-20
    HSK4: uses 上/下 (上=page 0, 下=page 1), 10 per page
    """
    if not lessons:
        return InlineKeyboardMarkup(inline_keyboard=[])

    level = lessons[0].level if lessons else "hsk1"
    page_size = 10 if level == "hsk4" else 7

    start = page * page_size
    end = start + page_size
    page_lessons = lessons[start:end]

    buttons = []
    row = []
    for i, lesson in enumerate(page_lessons):
        btn = InlineKeyboardButton(
            text=f"{lesson.lesson_order}. {lesson.title}",
            callback_data=f"course:pick_lesson:{lesson.id}",
        )
        row.append(btn)
        if len(row) == 1:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    nav = []
    total = len(lessons)

    if level == "hsk4":
        if page > 0:
            nav.append(InlineKeyboardButton(text="⬆️ 上", callback_data=f"course:lessons_page:{page-1}"))
        if end < total:
            nav.append(InlineKeyboardButton(text="⬇️ 下", callback_data=f"course:lessons_page:{page+1}"))
    else:
        prev_labels = {"tj": "⬅️ Қабл", "uz": "⬅️ Oldingi", "ru": "⬅️ Назад"}
        next_labels = {"tj": "Баъд ➡️", "uz": "Keyingi ➡️", "ru": "Далее ➡️"}
        if page > 0:
            nav.append(InlineKeyboardButton(text=prev_labels.get(lang, "⬅️"), callback_data=f"course:lessons_page:{page-1}"))
        if end < total:
            nav.append(InlineKeyboardButton(text=next_labels.get(lang, "➡️"), callback_data=f"course:lessons_page:{page+1}"))

    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


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
