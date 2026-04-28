from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# ─── STEP KEYBOARDS (inline) ────────────────────────────────────────────────

def course_intro_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "uz": "📖 So'zlarni o'rganamiz",
        "tj": "📖 Калимаҳоро меомӯзем",
        "ru": "📖 Изучаем слова",
    }
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=labels.get(lang, labels["ru"]), callback_data="course:go_vocab")
    ]])


def course_vocab_keyboard(lang: str) -> InlineKeyboardMarkup:
    audio_label = "🔉"
    next_labels = {
        "uz": "💬 Dialogni o'rganamiz",
        "tj": "💬 Муколамаро меомӯзем",
        "ru": "💬 Изучаем диалог",
    }
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=audio_label, callback_data="course:audio_vocab"),
            InlineKeyboardButton(text=next_labels.get(lang, next_labels["ru"]), callback_data="course:go_dialogue"),
        ]
    ])


def course_dialogue_keyboard(lang: str) -> InlineKeyboardMarkup:
    audio_label = "🔉"
    next_labels = {
        "uz": "📐 Grammatikaga o'tamiz",
        "tj": "📐 Ба грамматика мегузарем",
        "ru": "📐 Переходим к грамматике",
    }
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=audio_label, callback_data="course:audio_dialogue"),
            InlineKeyboardButton(text=next_labels.get(lang, next_labels["ru"]), callback_data="course:go_grammar"),
        ]
    ])


def course_grammar_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "uz": "✏️ Mashqlarga o'tamiz",
        "tj": "✏️ Ба машқҳо мегузарем",
        "ru": "✏️ Переходим к упражнениям",
    }
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=labels.get(lang, labels["ru"]), callback_data="course:go_exercise")
    ]])


def course_exercise_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "uz": "📝 Quizga o‘tamiz",
        "tj": "📝 Ба quiz мегузарем",
        "ru": "📝 Переходим к quiz",
    }
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=labels.get(lang, labels["ru"]), callback_data="course:go_quiz")
    ]])


def course_homework_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "uz": "✅ Dars tugadi — Keyingi darsga",
        "tj": "✅ Дарс тамом шуд — Ба дарси навбатӣ",
        "ru": "✅ Урок завершён — К следующему уроку",
    }
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=labels.get(lang, labels["ru"]), callback_data="course:start_next_lesson")
    ]])


def review_choice_keyboard(lang: str) -> InlineKeyboardMarkup:
    yes_labels = {"uz": "✅ Ha, takrorlaymiz", "tj": "✅ Бале, такрор мекунем", "ru": "✅ Да, повторим"}
    no_labels  = {"uz": "➡️ Yo'q, keyingisiga", "tj": "➡️ Не, ба навбатӣ", "ru": "➡️ Нет, к следующему"}
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=yes_labels.get(lang, yes_labels["ru"]), callback_data="course:review_yes"),
        InlineKeyboardButton(text=no_labels.get(lang, no_labels["ru"]),  callback_data="course:review_no"),
    ]])


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
            nav.append(InlineKeyboardButton(text="⬆️ 上", callback_data=f"course:lessons_page:{page-1}"))
        if end < total:
            nav.append(InlineKeyboardButton(text="⬇️ 下", callback_data=f"course:lessons_page:{page+1}"))
    else:
        prev_labels = {"tj": "⬅️ Қабл", "uz": "⬅️ Oldingi", "ru": "⬅️ Назад"}
        next_labels = {"tj": "Баъд ➡️", "uz": "Keyingi ➡️", "ru": "Далее ➡️"}
        if page > 0:
            nav.append(InlineKeyboardButton(
                text=prev_labels.get(lang, "⬅️"),
                callback_data=f"course:lessons_page:{page-1}",
            ))
        if end < total:
            nav.append(InlineKeyboardButton(
                text=next_labels.get(lang, "➡️"),
                callback_data=f"course:lessons_page:{page+1}",
            ))
    if nav:
        buttons.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=buttons)
