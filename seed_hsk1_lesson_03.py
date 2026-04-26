import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 3,
    "lesson_code": "HSK1-L03",
    "title": "你叫什么名字",
    "goal": "O'z ismini aytish, millati va kasbi haqida gapirish",
    "intro_text": (
        "Uchinchi darsda siz o'z ismingizni aytishni, "
        "millatingizni va kasbingizni xitoycha ifodalashni o'rganasiz. "
        "9 ta yangi so'z, 3 ta dialog va 是-gaplar grammatikasi."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "叫",   "pinyin": "jiào",     "pos": "v.",    "meaning": "chaqirmoq, ism bo'lmoq"},
        {"no": 2, "zh": "什么", "pinyin": "shénme",   "pos": "pron.", "meaning": "nima, qanday"},
        {"no": 3, "zh": "名字", "pinyin": "míngzi",   "pos": "n.",    "meaning": "ism, familiya"},
        {"no": 4, "zh": "我",   "pinyin": "wǒ",       "pos": "pron.", "meaning": "men"},
        {"no": 5, "zh": "是",   "pinyin": "shì",      "pos": "v.",    "meaning": "bo'lmoq (=)"},
        {"no": 6, "zh": "老师", "pinyin": "lǎoshī",   "pos": "n.",    "meaning": "o'qituvchi"},
        {"no": 7, "zh": "吗",   "pinyin": "ma",       "pos": "part.", "meaning": "so'roq yuklamasi"},
        {"no": 8, "zh": "学生", "pinyin": "xuésheng", "pos": "n.",    "meaning": "o'quvchi, talaba"},
        {"no": 9, "zh": "人",   "pinyin": "rén",      "pos": "n.",    "meaning": "odam, kishi"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Maktabda — ism so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你叫什么名字？",  "pinyin": "Nǐ jiào shénme míngzi?", "translation": "Ismingiz nima?"},
                {"speaker": "B", "zh": "我叫李月。",      "pinyin": "Wǒ jiào Lǐ Yuè.",        "translation": "Mening ismim Li Yue."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Sinfda — kasb so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你是老师吗？",          "pinyin": "Nǐ shì lǎoshī ma?",             "translation": "Siz o'qituvchimisiz?"},
                {"speaker": "B", "zh": "我不是老师，我是学生。", "pinyin": "Wǒ bú shì lǎoshī, wǒ shì xuésheng.", "translation": "Men o'qituvchi emasman, men o'quvchiman."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Maktabda — millat so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你是中国人吗？",           "pinyin": "Nǐ shì Zhōngguó rén ma?",               "translation": "Siz xitoylikmisin?"},
                {"speaker": "B", "zh": "我不是中国人，我是美国人。", "pinyin": "Wǒ bú shì Zhōngguó rén, wǒ shì Měiguó rén.", "translation": "Men xitoylik emasman, men amerikalikman."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "是字句 — 是 gapi",
            "explanation": (
                "是(shì) — tenglik bildiradi (= bo'lmoq).\n"
                "Tuzilishi: Ega + 是 + Ot/Ot birikmasi\n"
                "Inkor: Ega + 不是 + Ot/Ot birikmasi\n\n"
                "Misol:\n"
                "我是老师。— Men o'qituvchiman.\n"
                "我不是老师。— Men o'qituvchi emasman.\n"
                "李月是中国人。— Li Yue xitoylik."
            ),
            "examples": [
                {"zh": "我是学生。",     "pinyin": "Wǒ shì xuésheng.",     "meaning": "Men o'quvchiman."},
                {"zh": "我不是老师。",   "pinyin": "Wǒ bú shì lǎoshī.",    "meaning": "Men o'qituvchi emasman."},
                {"zh": "她是中国人。",   "pinyin": "Tā shì Zhōngguó rén.", "meaning": "U xitoylik."},
            ]
        },
        {
            "no": 2,
            "title_zh": "吗 — So'roq gapi",
            "explanation": (
                "吗(ma) — gapning oxiriga qo'yilsa, so'roq gap hosil bo'ladi.\n"
                "Tuzilishi: Darak gap + 吗？\n\n"
                "Misol:\n"
                "你是老师。→ 你是老师吗？\n"
                "Sen o'qituvchisan. → Sen o'qituvchimisan?\n\n"
                "Javob: 是 (ha) yoki 不是 (yo'q)"
            ),
            "examples": [
                {"zh": "你是学生吗？",   "pinyin": "Nǐ shì xuésheng ma?",   "meaning": "Sen o'quvchimisan?"},
                {"zh": "你是美国人吗？", "pinyin": "Nǐ shì Měiguó rén ma?", "meaning": "Sen amerikalikmisin?"},
                {"zh": "你叫李月吗？",   "pinyin": "Nǐ jiào Lǐ Yuè ma?",   "meaning": "Sening isming Li Yuemi?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "什么 — So'roq olmoshi",
            "explanation": (
                "什么(shénme) — 'nima', 'qanday' ma'nosini beradi.\n"
                "Gap oxiriga 吗 qo'yilmaydi — 什么 o'zi so'roq bildiradi.\n\n"
                "Misol:\n"
                "你叫什么名字？— Ismingiz nima?\n"
                "这是什么？— Bu nima?\n"
                "你是什么人？— Siz kimsin?"
            ),
            "examples": [
                {"zh": "你叫什么名字？", "pinyin": "Nǐ jiào shénme míngzi?", "meaning": "Ismingiz nima?"},
                {"zh": "这是什么？",     "pinyin": "Zhè shì shénme?",        "meaning": "Bu nima?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Ismingiz nima?",                       "answer": "你叫什么名字？",          "pinyin": "Nǐ jiào shénme míngzi?"},
                {"prompt": "Mening ismim Wang Fang.",              "answer": "我叫王芳。",               "pinyin": "Wǒ jiào Wáng Fāng."},
                {"prompt": "Siz o'qituvchimisiz?",                 "answer": "你是老师吗？",             "pinyin": "Nǐ shì lǎoshī ma?"},
                {"prompt": "Men o'quvchiman.",                      "answer": "我是学生。",               "pinyin": "Wǒ shì xuésheng."},
                {"prompt": "Men xitoylik emasman, amerikalikman.", "answer": "我不是中国人，我是美国人。","pinyin": "Wǒ bú shì Zhōngguó rén, wǒ shì Měiguó rén."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "A: 你叫___名字？  B: 我叫李月。",         "answer": "什么",  "pinyin": "shénme"},
                {"prompt": "A: 你___老师吗？  B: 是，我是老师。",     "answer": "是",    "pinyin": "shì"},
                {"prompt": "A: 你是中国人___？ B: 不是，我是美国人。", "answer": "吗",    "pinyin": "ma"},
                {"prompt": "我不___老师，我是学生。",                   "answer": "是",    "pinyin": "shì"},
            ]
        },
        {
            "no": 3,
            "type": "make_question",
            "instruction": "吗 ishlatib so'roq gap tuzing:",
            "items": [
                {"prompt": "你是学生。",     "answer": "你是学生吗？",   "pinyin": "Nǐ shì xuésheng ma?"},
                {"prompt": "他是中国人。",   "answer": "他是中国人吗？", "pinyin": "Tā shì Zhōngguó rén ma?"},
                {"prompt": "她叫李月。",     "answer": "她叫李月吗？",   "pinyin": "Tā jiào Lǐ Yuè ma?"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你叫什么名字？", "我叫王芳。", "你是老师吗？", "我是学生。", "我不是中国人，我是美国人。"]},
        {"no": 2, "answers": ["什么", "是", "吗", "是"]},
        {"no": 3, "answers": ["你是学生吗？", "他是中国人吗？", "她叫李月吗？"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "O'zingiz haqingizda 3 ta gap yozing (ism, millat, kasb):",
            "example": "我叫___。我是___人。我是___。",
            "words": ["叫", "是", "不是", "老师", "学生", "中国人", "美国人"],
        },
        {
            "no": 2,
            "instruction": "Quyidagi gaplarni so'roq gapga aylantiring (吗 ishlatib):",
            "items": [
                {"prompt": "你是老师。",   "answer": "你是老师吗？"},
                {"prompt": "他叫大卫。",   "answer": "他叫大卫吗？"},
                {"prompt": "她是美国人。", "answer": "她是美国人吗？"},
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
