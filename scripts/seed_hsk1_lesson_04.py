import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 4,
    "lesson_code": "HSK1-L04",
    "title": "她是我的汉语老师",
    "goal": "Uchinchi shaxs haqida gapirish, qarindoshlik va egalik bildirish",
    "intro_text": (
        "To'rtinchi darsda siz uchinchi shaxs (u/o'sha) haqida gapirish, "
        "的 yuklamasi bilan egalik bildirish va 谁/哪 so'roq olmoshlarini o'rganasiz. "
        "10 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "她",   "pinyin": "tā",      "pos": "pron.", "meaning": "u (ayol)"},
        {"no": 2,  "zh": "谁",   "pinyin": "shéi",    "pos": "pron.", "meaning": "kim, kim?"},
        {"no": 3,  "zh": "的",   "pinyin": "de",      "pos": "part.", "meaning": "ning (egalik yuklamasi)"},
        {"no": 4,  "zh": "汉语", "pinyin": "Hànyǔ",   "pos": "n.",    "meaning": "xitoy tili"},
        {"no": 5,  "zh": "哪",   "pinyin": "nǎ",      "pos": "pron.", "meaning": "qaysi, qayerlik"},
        {"no": 6,  "zh": "国",   "pinyin": "guó",     "pos": "n.",    "meaning": "mamlakat, davlat"},
        {"no": 7,  "zh": "呢",   "pinyin": "ne",      "pos": "part.", "meaning": "nima, bo'lsa? (so'roq)"},
        {"no": 8,  "zh": "他",   "pinyin": "tā",      "pos": "pron.", "meaning": "u (erkak)"},
        {"no": 9,  "zh": "同学", "pinyin": "tóngxué", "pos": "n.",    "meaning": "sinfdosh, kursdosh"},
        {"no": 10, "zh": "朋友", "pinyin": "péngyou", "pos": "n.",    "meaning": "do'st"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Sinfda — o'qituvchi haqida",
            "dialogue": [
                {"speaker": "A", "zh": "她是谁？",              "pinyin": "Tā shì shéi?",                       "translation": "U kim?"},
                {"speaker": "B", "zh": "她是我的汉语老师，她叫李月。", "pinyin": "Tā shì wǒ de Hànyǔ lǎoshī, tā jiào Lǐ Yuè.", "translation": "U mening xitoy tili o'qituvchim, uning ismi Li Yue."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Kutubxonada — millat so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你是哪国人？",    "pinyin": "Nǐ shì nǎ guó rén?",       "translation": "Siz qaysi mamlakatdansiz?"},
                {"speaker": "B", "zh": "我是美国人。你呢？","pinyin": "Wǒ shì Měiguó rén. Nǐ ne?", "translation": "Men amerikalikman. Siz-chi?"},
                {"speaker": "A", "zh": "我是中国人。",    "pinyin": "Wǒ shì Zhōngguó rén.",     "translation": "Men xitoylikman."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Fotoda — do'st va sinfdosh",
            "dialogue": [
                {"speaker": "A", "zh": "他是谁？",                "pinyin": "Tā shì shéi?",                           "translation": "U kim?"},
                {"speaker": "B", "zh": "他是我同学。",             "pinyin": "Tā shì wǒ tóngxué.",                    "translation": "U mening sinfdoshim."},
                {"speaker": "A", "zh": "她呢？她是你同学吗？",     "pinyin": "Tā ne? Tā shì nǐ tóngxué ma?",          "translation": "U-chi? U ham sinfdoshingizmi?"},
                {"speaker": "B", "zh": "她不是我同学，她是我朋友。","pinyin": "Tā bú shì wǒ tóngxué, tā shì wǒ péngyou.", "translation": "U sinfdoshim emas, u mening do'stim."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "结构助词 的 — Egalik yuklamasi",
            "explanation": (
                "的(de) — egalik yoki tegishlilik bildiradi.\n"
                "Tuzilishi: Ot/Olmosh + 的 + Ot\n\n"
                "Misol:\n"
                "我的老师 — mening o'qituvchim\n"
                "她的朋友 — uning do'sti\n\n"
                "Muhim: Qarindoshlik va shaxs nomlari oldidan 的 tushib qolishi mumkin:\n"
                "我(的)老师 ✓ — mening o'qituvchim\n"
                "我(的)朋友 ✓ — mening do'stim"
            ),
            "examples": [
                {"zh": "我的汉语老师",   "pinyin": "wǒ de Hànyǔ lǎoshī", "meaning": "mening xitoy tili o'qituvchim"},
                {"zh": "他的同学",       "pinyin": "tā de tóngxué",       "meaning": "uning sinfdoshi"},
                {"zh": "你的朋友",       "pinyin": "nǐ de péngyou",       "meaning": "sening do'sting"},
            ]
        },
        {
            "no": 2,
            "title_zh": "谁 — Kim so'roq olmoshi",
            "explanation": (
                "谁(shéi) — 'kim?' ma'nosida ishlatiladi.\n"
                "Gapda ega yoki to'ldiruvchi o'rnida keladi.\n\n"
                "Misol:\n"
                "她是谁？— U kim?\n"
                "谁是老师？— Kim o'qituvchi?\n"
                "他是谁的朋友？— U kimning do'sti?"
            ),
            "examples": [
                {"zh": "她是谁？",       "pinyin": "Tā shì shéi?",        "meaning": "U kim?"},
                {"zh": "谁是你的老师？", "pinyin": "Shéi shì nǐ de lǎoshī?", "meaning": "Kimingiz o'qituvchi?"},
                {"zh": "他是谁的同学？", "pinyin": "Tā shì shéi de tóngxué?", "meaning": "U kimning sinfdoshi?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "呢 — Qaytarma so'roq yuklamasi",
            "explanation": (
                "呢(ne) — oldingi gapda aytilgan narsani so'rash uchun.\n"
                "Tuzilishi: A gap... B呢？ (B nima bo'lsa?)\n\n"
                "Misol:\n"
                "我是美国人。你呢？\n"
                "Men amerikalikman. Siz-chi?\n\n"
                "她叫李月。他呢？\n"
                "Uning ismi Li Yue. U-chi?"
            ),
            "examples": [
                {"zh": "我是学生。你呢？",  "pinyin": "Wǒ shì xuésheng. Nǐ ne?", "meaning": "Men o'quvchiman. Siz-chi?"},
                {"zh": "她是中国人。他呢？","pinyin": "Tā shì Zhōngguó rén. Tā ne?","meaning": "U xitoylik. U-chi (erkak)?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "U (ayol) kim?",                        "answer": "她是谁？",                  "pinyin": "Tā shì shéi?"},
                {"prompt": "U mening xitoy tili o'qituvchim.",     "answer": "她是我的汉语老师。",         "pinyin": "Tā shì wǒ de Hànyǔ lǎoshī."},
                {"prompt": "Siz qaysi mamlakatdansiz?",            "answer": "你是哪国人？",               "pinyin": "Nǐ shì nǎ guó rén?"},
                {"prompt": "Men amerikalikman. Siz-chi?",          "answer": "我是美国人。你呢？",         "pinyin": "Wǒ shì Měiguó rén. Nǐ ne?"},
                {"prompt": "U sinfdoshim emas, u mening do'stim.", "answer": "他不是我同学，他是我朋友。", "pinyin": "Tā bú shì wǒ tóngxué, tā shì wǒ péngyou."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "她是我___汉语老师。",            "answer": "的",   "pinyin": "de"},
                {"prompt": "A: 他是___？  B: 他是我同学。", "answer": "谁",   "pinyin": "shéi"},
                {"prompt": "我是中国人。你___？",             "answer": "呢",   "pinyin": "ne"},
                {"prompt": "你是___国人？",                   "answer": "哪",   "pinyin": "nǎ"},
            ]
        },
        {
            "no": 3,
            "type": "make_sentence",
            "instruction": "Berilgan so'zlardan gap tuzing:",
            "items": [
                {"words": ["她", "是", "我", "的", "朋友"], "answer": "她是我的朋友。",       "pinyin": "Tā shì wǒ de péngyou."},
                {"words": ["他", "哪", "是", "国", "人"],   "answer": "他是哪国人？",         "pinyin": "Tā shì nǎ guó rén?"},
                {"words": ["谁", "你", "老师", "是", "的"], "answer": "谁是你的老师？",       "pinyin": "Shéi shì nǐ de lǎoshī?"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["她是谁？", "她是我的汉语老师。", "你是哪国人？", "我是美国人。你呢？", "他不是我同学，他是我朋友。"]},
        {"no": 2, "answers": ["的", "谁", "呢", "哪"]},
        {"no": 3, "answers": ["她是我的朋友。", "他是哪国人？", "谁是你的老师？"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Do'stingiz haqida 4 ta gap yozing:",
            "template": "他/她叫___。他/她是___人。他/她是我的___。他/她是不是___？",
            "words": ["的", "同学", "朋友", "老师", "汉语老师"],
        },
        {
            "no": 2,
            "instruction": "Savollarga javob bering:",
            "items": [
                {"prompt": "你的汉语老师是哪国人？",    "hint": "Xitoy tili o'qituvchingiz qaysi mamlakatdan?"},
                {"prompt": "你的朋友叫什么名字？",       "hint": "Do'stingizning ismi nima?"},
                {"prompt": "他/她是你的同学吗？",        "hint": "U sizning sinfdoshingizmi?"},
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
