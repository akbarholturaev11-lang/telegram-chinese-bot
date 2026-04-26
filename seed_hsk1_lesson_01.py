import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 1,
    "lesson_code": "HSK1-L01",
    "title": "你好",
    "goal": "Salomlashish va kechirim so'rashni o'rganish",
    "intro_text": (
        "Birinchi darsda siz xitoycha salomlashishni o'rganasiz. "
        "Ushbu dars 6 ta yangi so'z, 3 ta dialog va asosiy talaffuz qoidalarini o'z ichiga oladi."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "你",    "pinyin": "nǐ",        "pos": "pron.", "meaning": "sen (yagona)"},
        {"no": 2, "zh": "好",    "pinyin": "hǎo",       "pos": "adj.",  "meaning": "yaxshi, zo'r"},
        {"no": 3, "zh": "您",    "pinyin": "nín",       "pos": "pron.", "meaning": "Siz (hurmat bilan)"},
        {"no": 4, "zh": "你们",  "pinyin": "nǐmen",     "pos": "pron.", "meaning": "sizlar (ko'plik)"},
        {"no": 5, "zh": "对不起","pinyin": "duìbuqǐ",   "pos": "v.",    "meaning": "kechirasiz, uzr"},
        {"no": 6, "zh": "没关系","pinyin": "méi guānxi","pos": "expr.", "meaning": "arzimaydi, xavotir olmang"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Tanishlar uchrashadi",
            "dialogue": [
                {"speaker": "A", "zh": "你好！",  "pinyin": "Nǐ hǎo!",   "translation": "Salom!"},
                {"speaker": "B", "zh": "你好！",  "pinyin": "Nǐ hǎo!",   "translation": "Salom!"},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Hurmatli salomlashuv",
            "dialogue": [
                {"speaker": "A", "zh": "您好！",   "pinyin": "Nín hǎo!",    "translation": "Salom (hurmat bilan)!"},
                {"speaker": "B", "zh": "你们好！", "pinyin": "Nǐmen hǎo!",  "translation": "Hammangizga salom!"},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kechirim so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "对不起！", "pinyin": "Duìbuqǐ!",      "translation": "Kechirasiz!"},
                {"speaker": "B", "zh": "没关系！", "pinyin": "Méi guānxi!",   "translation": "Arzimaydi!"},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "四声 — To'rt ton",
            "explanation": (
                "Xitoy tilida har bir bo'g'inning 4 ta toni bor:\n"
                "1-ton (—): tekis va baland — mā (ona)\n"
                "2-ton (ˊ): ko'tariluvchi — má (kanop o'simlik)\n"
                "3-ton (ˇ): tushib ko'tariluvchi — mǎ (ot)\n"
                "4-ton (ˋ): tushuvchi — mà (so'kmoq)\n\n"
                "Ton ma'noni o'zgartiradi!"
            ),
            "examples": [
                {"zh": "妈", "pinyin": "mā", "meaning": "ona (1-ton)"},
                {"zh": "马", "pinyin": "mǎ", "meaning": "ot (3-ton)"},
                {"zh": "骂", "pinyin": "mà", "meaning": "so'kmoq (4-ton)"},
            ]
        },
        {
            "no": 2,
            "title_zh": "变调 — Ton o'zgarishi (3+3)",
            "explanation": (
                "Ikkita 3-ton ketma-ket kelganda, birinchisi 2-tonga o'zgaradi.\n"
                "3+3 → 2+3\n"
                "Masalan: 你(nǐ) + 好(hǎo) → nī hǎo (lekin yozuvda: nǐ hǎo)"
            ),
            "examples": [
                {"zh": "你好", "pinyin": "nī hǎo → nǐ hǎo", "meaning": "salom (yozuvda nǐ hǎo)"},
                {"zh": "可以", "pinyin": "ké yǐ → kě yǐ",   "meaning": "mumkin"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Salom! (oddiy)",          "answer": "你好！",   "pinyin": "Nǐ hǎo!"},
                {"prompt": "Salom! (hurmat bilan)",   "answer": "您好！",   "pinyin": "Nín hǎo!"},
                {"prompt": "Kechirasiz!",              "answer": "对不起！", "pinyin": "Duìbuqǐ!"},
                {"prompt": "Arzimaydi!",               "answer": "没关系！", "pinyin": "Méi guānxi!"},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "A: 你___！  B: 你好！",     "answer": "好", "pinyin": "hǎo"},
                {"prompt": "A: 对不起！  B: ___！",     "answer": "没关系", "pinyin": "méi guānxi"},
                {"prompt": "一个老师对很多学生说: ___好！", "answer": "你们", "pinyin": "nǐmen"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你好！", "您好！", "对不起！", "没关系！"]},
        {"no": 2, "answers": ["好", "没关系", "你们"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Quyidagi so'zlardan foydalanib 2 ta dialog tuzing (yozma):",
            "words": ["你好", "您好", "对不起", "没关系"],
            "example": "A: 对不起！B: 没关系！",
        },
        {
            "no": 2,
            "instruction": "Tonlarni o'rganing va aytib ko'ring:",
            "words": [
                {"zh": "妈", "pinyin": "mā", "meaning": "ona"},
                {"zh": "马", "pinyin": "mǎ", "meaning": "ot"},
                {"zh": "骂", "pinyin": "mà", "meaning": "so'kmoq"},
            ]
        }
    ], ensure_ascii=False),

    "is_active": True,
}


async def seed():
    async with SessionLocal() as session:
        existing = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])
        )
        if existing.scalar_one_or_none():
            print(f"Lesson {LESSON['lesson_code']} already exists, skipping.")
            return

        lesson = CourseLesson(**LESSON)
        session.add(lesson)
        await session.commit()
        print(f"✅ Lesson {LESSON['lesson_code']} — {LESSON['title']} created.")


if __name__ == "__main__":
    asyncio.run(seed())
