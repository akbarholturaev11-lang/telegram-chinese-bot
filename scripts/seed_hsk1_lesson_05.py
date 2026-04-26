import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 5,
    "lesson_code": "HSK1-L05",
    "title": "她女儿今年二十岁",
    "goal": "Yosh va oila a'zolari haqida gapirish, 100 gacha raqamlar",
    "intro_text": (
        "Beshinchi darsda siz yosh so'rash va aytishni, "
        "oila a'zolari sonini va 100 gacha raqamlarni o'rganasiz. "
        "10 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "家",   "pinyin": "jiā",     "pos": "n.",    "meaning": "oila, uy"},
        {"no": 2,  "zh": "有",   "pinyin": "yǒu",     "pos": "v.",    "meaning": "bor, ega bo'lmoq"},
        {"no": 3,  "zh": "口",   "pinyin": "kǒu",     "pos": "m.",    "meaning": "oila a'zolari uchun o'lchov so'z"},
        {"no": 4,  "zh": "女儿", "pinyin": "nǚ'ér",   "pos": "n.",    "meaning": "qiz (farzand)"},
        {"no": 5,  "zh": "几",   "pinyin": "jǐ",      "pos": "pron.", "meaning": "necha, qancha (10 gacha)"},
        {"no": 6,  "zh": "岁",   "pinyin": "suì",     "pos": "m.",    "meaning": "yosh (o'lchov so'z)"},
        {"no": 7,  "zh": "了",   "pinyin": "le",      "pos": "part.", "meaning": "o'zgarish bildiruvchi yukla"},
        {"no": 8,  "zh": "今年", "pinyin": "jīnnián", "pos": "n.",    "meaning": "bu yil"},
        {"no": 9,  "zh": "多",   "pinyin": "duō",     "pos": "adv.",  "meaning": "ko'p, qancha (daraja)"},
        {"no": 10, "zh": "大",   "pinyin": "dà",      "pos": "adj.",  "meaning": "katta (yoshda)"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Maktabda — oila a'zolari",
            "dialogue": [
                {"speaker": "A", "zh": "你家有几口人？",  "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?",  "translation": "Oilangizda necha kishi bor?"},
                {"speaker": "B", "zh": "我家有三口人。",  "pinyin": "Wǒ jiā yǒu sān kǒu rén.", "translation": "Bizning oilamizda uch kishi bor."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Ofisda — yosh so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你女儿几岁了？",   "pinyin": "Nǐ nǚ'ér jǐ suì le?",    "translation": "Qizingiz necha yoshda?"},
                {"speaker": "B", "zh": "她今年四岁了。",   "pinyin": "Tā jīnnián sì suì le.",   "translation": "U bu yil to'rt yoshda."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Ofisda — kattalar yoshi",
            "dialogue": [
                {"speaker": "A", "zh": "李老师多大了？",       "pinyin": "Lǐ lǎoshī duō dà le?",              "translation": "Li o'qituvchi necha yoshda?"},
                {"speaker": "B", "zh": "她今年五十岁了。",     "pinyin": "Tā jīnnián wǔshí suì le.",          "translation": "U bu yil ellik yoshda."},
                {"speaker": "A", "zh": "她女儿呢？",           "pinyin": "Tā nǚ'ér ne?",                      "translation": "Uning qizi-chi?"},
                {"speaker": "B", "zh": "她女儿今年二十岁。",   "pinyin": "Tā nǚ'ér jīnnián èrshí suì.",       "translation": "Uning qizi bu yil yigirma yoshda."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "几 — Necha? (10 gacha)",
            "explanation": (
                "几(jǐ) — 10 dan kam sonlar uchun so'roq olmoshi.\n"
                "Tuzilishi: Ega + 有 + 几 + O'lchov so'z + Ot?\n\n"
                "Misol:\n"
                "你家有几口人？— Oilangizda necha kishi?\n"
                "你有几个汉语老师？— Nechta xitoy tili o'qituvchingiz bor?\n"
                "你女儿几岁了？— Qizingiz necha yoshda?"
            ),
            "examples": [
                {"zh": "你家有几口人？",   "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?",  "meaning": "Oilangizda necha kishi?"},
                {"zh": "你有几个朋友？",   "pinyin": "Nǐ yǒu jǐ ge péngyou?",   "meaning": "Nechta do'stingiz bor?"},
                {"zh": "她有几岁了？",     "pinyin": "Tā yǒu jǐ suì le?",        "meaning": "U necha yoshda?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "100 gacha raqamlar",
            "explanation": (
                "1-10: 一yī 二èr 三sān 四sì 五wǔ 六liù 七qī 八bā 九jiǔ 十shí\n\n"
                "O'nliklar:\n"
                "20 = 二十 (èrshí)\n"
                "30 = 三十 (sānshí)\n"
                "50 = 五十 (wǔshí)\n"
                "99 = 九十九 (jiǔshíjiǔ)\n\n"
                "Aralash sonlar:\n"
                "23 = 二十三 (èrshísān)\n"
                "56 = 五十六 (wǔshíliù)\n"
                "88 = 八十八 (bāshíbā)"
            ),
            "examples": [
                {"zh": "二十",   "pinyin": "èrshí",    "meaning": "20"},
                {"zh": "五十",   "pinyin": "wǔshí",    "meaning": "50"},
                {"zh": "二十三", "pinyin": "èrshísān", "meaning": "23"},
                {"zh": "九十九", "pinyin": "jiǔshíjiǔ","meaning": "99"},
            ]
        },
        {
            "no": 3,
            "title_zh": "了 — O'zgarish yuklamasi",
            "explanation": (
                "了(le) — gap oxirida yangi holat yoki o'zgarishni bildiradi.\n\n"
                "Misol:\n"
                "她今年五十岁了。— U bu yil ellik yoshga to'ldi (yangi holat).\n"
                "我女儿四岁了。— Qizim to'rt yoshga to'ldi.\n\n"
                "多大了？— Necha yoshga to'ldi? (yosh so'rash)"
            ),
            "examples": [
                {"zh": "她今年二十岁了。", "pinyin": "Tā jīnnián èrshí suì le.", "meaning": "U bu yil yigirma yoshga to'ldi."},
                {"zh": "他五十岁了。",     "pinyin": "Tā wǔshí suì le.",         "meaning": "U ellik yoshga to'ldi."},
                {"zh": "你多大了？",       "pinyin": "Nǐ duō dà le?",            "meaning": "Necha yoshga to'lding?"},
            ]
        },
        {
            "no": 4,
            "title_zh": "多大 — Yosh so'rash",
            "explanation": (
                "多大(duō dà) — kattalar yoshini so'rashda ishlatiladi.\n"
                "几岁(jǐ suì) — bolalar yoshini so'rashda ishlatiladi (10 gacha).\n\n"
                "Kattalar: 你多大了？— Necha yoshdasiz?\n"
                "Bolalar:  你女儿几岁了？— Qizingiz necha yoshda?"
            ),
            "examples": [
                {"zh": "你多大了？",     "pinyin": "Nǐ duō dà le?",       "meaning": "Necha yoshdasiz? (kattalar)"},
                {"zh": "她女儿几岁了？", "pinyin": "Tā nǚ'ér jǐ suì le?", "meaning": "Qizi necha yoshda? (bola)"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "numbers",
            "instruction": "Raqamlarni xitoycha yozing:",
            "items": [
                {"prompt": "25",  "answer": "二十五",   "pinyin": "èrshíwǔ"},
                {"prompt": "38",  "answer": "三十八",   "pinyin": "sānshíbā"},
                {"prompt": "50",  "answer": "五十",     "pinyin": "wǔshí"},
                {"prompt": "99",  "answer": "九十九",   "pinyin": "jiǔshíjiǔ"},
                {"prompt": "100", "answer": "一百",     "pinyin": "yìbǎi"},
            ]
        },
        {
            "no": 2,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Oilangizda necha kishi bor?",        "answer": "你家有几口人？",   "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?"},
                {"prompt": "Bizning oilamizda besh kishi bor.",  "answer": "我家有五口人。",   "pinyin": "Wǒ jiā yǒu wǔ kǒu rén."},
                {"prompt": "Necha yoshdasiz?",                    "answer": "你多大了？",       "pinyin": "Nǐ duō dà le?"},
                {"prompt": "U bu yil yigirma yoshda.",            "answer": "她今年二十岁了。", "pinyin": "Tā jīnnián èrshí suì le."},
            ]
        },
        {
            "no": 3,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "你家___几口人？",          "answer": "有", "pinyin": "yǒu"},
                {"prompt": "李老师今年五十___了。",     "answer": "岁", "pinyin": "suì"},
                {"prompt": "你女儿___岁了？",           "answer": "几", "pinyin": "jǐ"},
                {"prompt": "李老师___大了？",            "answer": "多", "pinyin": "duō"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["二十五", "三十八", "五十", "九十九", "一百"]},
        {"no": 2, "answers": ["你家有几口人？", "我家有五口人。", "你多大了？", "她今年二十岁了。"]},
        {"no": 3, "answers": ["有", "岁", "几", "多"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "O'z oilangiz haqida 3-4 gap yozing:",
            "template": "我家有___口人。我今年___岁了。我___有女儿/儿子。",
            "words": ["家", "有", "口", "岁", "今年", "了"],
        },
        {
            "no": 2,
            "instruction": "Raqamlarni xitoycha yozing:",
            "items": [
                {"prompt": "17",  "answer": "十七"},
                {"prompt": "43",  "answer": "四十三"},
                {"prompt": "68",  "answer": "六十八"},
                {"prompt": "100", "answer": "一百"},
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
