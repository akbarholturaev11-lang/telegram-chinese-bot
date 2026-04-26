import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 2,
    "lesson_code": "HSK1-L02",
    "title": "谢谢你",
    "goal": "Minnatdorchilik bildirish va xayrlashishni o'rganish",
    "intro_text": (
        "Ikkinchi darsda siz xitoycha minnatdorchilik va xayrlashishni o'rganasiz. "
        "4 ta yangi so'z, 3 ta dialog va neytral ton qoidalari."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "谢谢",   "pinyin": "xièxie",  "pos": "v.",   "meaning": "rahmat aytmoq"},
        {"no": 2, "zh": "不",     "pinyin": "bù",       "pos": "adv.", "meaning": "yo'q, emas"},
        {"no": 3, "zh": "不客气", "pinyin": "bú kèqi",  "pos": "expr.", "meaning": "arzimaydi, marhamat"},
        {"no": 4, "zh": "再见",   "pinyin": "zàijiàn",  "pos": "v.",   "meaning": "xayr, ko'rishguncha"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Yordam uchun rahmat",
            "dialogue": [
                {"speaker": "A", "zh": "谢谢！", "pinyin": "Xièxie!", "translation": "Rahmat!"},
                {"speaker": "B", "zh": "不谢！", "pinyin": "Bú xiè!", "translation": "Arzimaydi!"},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Rasmiy rahmat",
            "dialogue": [
                {"speaker": "A", "zh": "谢谢你！", "pinyin": "Xièxie nǐ!", "translation": "Sizga rahmat!"},
                {"speaker": "B", "zh": "不客气！", "pinyin": "Bú kèqi!",   "translation": "Arzimaydi (marhamat)!"},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Xayrlashuv",
            "dialogue": [
                {"speaker": "A", "zh": "再见！", "pinyin": "Zàijiàn!", "translation": "Xayr!"},
                {"speaker": "B", "zh": "再见！", "pinyin": "Zàijiàn!", "translation": "Xayr!"},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "不 — Inkor yuklamasi",
            "explanation": (
                "不(bù) — inkor ma'nosini beradi (yo'q, emas).\n"
                "Lekin: 不 4-tonda, lekin 4-ton oldida 2-tonga o'zgaradi.\n"
                "bù + 4-ton → bú + 4-ton\n"
                "Masalan: 不客气 → bú kèqi\n"
                "不谢 → bú xiè"
            ),
            "examples": [
                {"zh": "不谢",   "pinyin": "bú xiè",  "meaning": "arzimaydi"},
                {"zh": "不客气", "pinyin": "bú kèqi", "meaning": "marhamat"},
                {"zh": "不好",   "pinyin": "bù hǎo",  "meaning": "yaxshi emas"},
            ]
        },
        {
            "no": 2,
            "title_zh": "轻声 — Neytral ton",
            "explanation": (
                "Xitoy tilida 5-ton ham bor — neytral ton (轻声).\n"
                "U qisqa va engil o'qiladi, ton belgisi yo'q.\n"
                "Ko'pincha oila a'zolari nomlarida uchraydi.\n"
                "Masalan: 妈妈(māma), 爸爸(bàba), 爷爷(yéye), 奶奶(nǎinai)"
            ),
            "examples": [
                {"zh": "妈妈", "pinyin": "māma",   "meaning": "ona"},
                {"zh": "爸爸", "pinyin": "bàba",   "meaning": "ota"},
                {"zh": "爷爷", "pinyin": "yéye",   "meaning": "buva"},
                {"zh": "奶奶", "pinyin": "nǎinai", "meaning": "buvi"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Rahmat!",               "answer": "谢谢！",   "pinyin": "Xièxie!"},
                {"prompt": "Sizga rahmat!",          "answer": "谢谢你！", "pinyin": "Xièxie nǐ!"},
                {"prompt": "Arzimaydi (marhamat)!",  "answer": "不客气！", "pinyin": "Bú kèqi!"},
                {"prompt": "Xayr!",                  "answer": "再见！",   "pinyin": "Zàijiàn!"},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "A: 谢谢你！  B: ___！", "answer": "不客气", "pinyin": "bú kèqi"},
                {"prompt": "A: ___！     B: 再见！", "answer": "再见",   "pinyin": "zàijiàn"},
                {"prompt": "A: 谢谢！    B: ___！",  "answer": "不谢",   "pinyin": "bú xiè"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["谢谢！", "谢谢你！", "不客气！", "再见！"]},
        {"no": 2, "answers": ["不客气", "再见", "不谢"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Quyidagi so'zlardan foydalanib 2 ta to'liq dialog tuzing:",
            "words": ["谢谢", "不客气", "再见", "你好"],
            "example": "A: 你好！... A: 谢谢！B: 不客气！再见！B: 再见！",
        },
        {
            "no": 2,
            "instruction": "不 ning to'g'ri talaffuzini yozing (bù yoki bú):",
            "items": [
                {"prompt": "不好",   "answer": "bù hǎo"},
                {"prompt": "不谢",   "answer": "bú xiè"},
                {"prompt": "不客气", "answer": "bú kèqi"},
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
