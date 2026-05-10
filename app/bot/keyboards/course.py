from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


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


def course_next_step_keyboard(lang: str) -> InlineKeyboardMarkup:
    """V2 darslar uchun universal 'Davom etamiz' tugmasi (audiosiz)."""
    labels = {
        "uz": "▶️ Davom etamiz",
        "tj": "▶️ Идома медиҳем",
        "ru": "▶️ Продолжаем",
    }
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=labels.get(lang, labels["ru"]), callback_data="course:go_next_step")
    ]])


def course_vocab_v2_keyboard(lang: str) -> InlineKeyboardMarkup:
    """V2 vocab_1 / vocab_2 step: [🔉]  [▶️ Davom etamiz]."""
    next_labels = {
        "uz": "▶️ Davom etamiz",
        "tj": "▶️ Идома медиҳем",
        "ru": "▶️ Продолжаем",
    }
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔉", callback_data="course:audio_vocab"),
        InlineKeyboardButton(
            text=next_labels.get(lang, next_labels["ru"]),
            callback_data="course:go_next_step",
        ),
    ]])


def course_dialogue_n_keyboard(lang: str, n: int) -> InlineKeyboardMarkup:
    """V2 dialogue_N step: [🔉]  [▶️ Davom etamiz]."""
    next_labels = {
        "uz": "▶️ Davom etamiz",
        "tj": "▶️ Идома медиҳем",
        "ru": "▶️ Продолжаем",
    }
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔉", callback_data=f"course:audio_dialogue:{n}"),
        InlineKeyboardButton(
            text=next_labels.get(lang, next_labels["ru"]),
            callback_data="course:go_next_step",
        ),
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


def course_reminder_timezone_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="UTC+3 🇷🇺 Москва",   callback_data="course:set_tz:3")
    builder.button(text="UTC+5 🇺🇿 Тошкент",  callback_data="course:set_tz:5")
    builder.button(text="UTC+5 🇹🇯 Душанбе",  callback_data="course:set_tz:5")
    builder.button(text="UTC+8 🇨🇳 Пекин",    callback_data="course:set_tz:8")
    builder.adjust(2)
    return builder.as_markup()


def course_reminder_notification_keyboard(lang: str) -> InlineKeyboardMarkup:
    labels = {
        "uz": "📖 Darsni davom ettirish",
        "ru": "📖 Продолжить урок",
        "tj": "📖 Идома додани дарс",
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=labels.get(lang, labels["ru"]), callback_data="course:continue")
    return builder.as_markup()


def next_study_time_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    """Keyingi o'qish vaqtini tanlash — inline tugmalar (ReplyKeyboard o'rniga)."""
    skip_labels = {
        "uz": "⏩ O'tkazib yuborish",
        "ru": "⏩ Пропустить",
        "tj": "⏩ Гузаронидан",
    }
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="09:00", callback_data="course:study_time:09:00"),
            InlineKeyboardButton(text="14:00", callback_data="course:study_time:14:00"),
        ],
        [
            InlineKeyboardButton(text="19:00", callback_data="course:study_time:19:00"),
            InlineKeyboardButton(text="21:00", callback_data="course:study_time:21:00"),
        ],
        [
            InlineKeyboardButton(
                text=skip_labels.get(lang, skip_labels["ru"]),
                callback_data="course:skip_next_study_time",
            ),
        ],
    ])


def reminder_time_keyboard(lang: str) -> ReplyKeyboardMarkup:
    cancel_map = {
        "uz": "❌ Bekor qilish",
        "ru": "❌ Отмена",
        "tj": "❌ Бекор кардан",
    }
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="08:00"), KeyboardButton(text="14:00"), KeyboardButton(text="20:00")],
            [KeyboardButton(text=cancel_map.get(lang, "❌ Отмена"))],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
