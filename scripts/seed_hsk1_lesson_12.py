import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 12,
    "lesson_code": "HSK1-L12",
    "title": "明天天气怎么样",
    "goal": "Ob-havo haqida gapirish, 怎么样 so'rog'i va 太...了 konstruktsiyasi",
    "intro_text": (
        "O'n ikkinchi darsda siz ob-havo haqida gapirish, "
        "怎么样 bilan holat so'rash va 太...了 konstruktsiyasini o'rganasiz. "
        "13 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "天气",  "pinyin": "tiānqì",   "pos": "n.",   "meaning": "ob-havo"},
        {"no": 2,  "zh": "怎么样","pinyin": "zěnmeyàng","pos": "pron.","meaning": "qanday, qanaqa"},
        {"no": 3,  "zh": "太",    "pinyin": "tài",      "pos": "adv.", "meaning": "juda, haddan tashqari"},
        {"no": 4,  "zh": "热",    "pinyin": "rè",       "pos": "adj.", "meaning": "issiq"},
        {"no": 5,  "zh": "冷",    "pinyin": "lěng",     "pos": "adj.", "meaning": "sovuq"},
        {"no": 6,  "zh": "下雨",  "pinyin": "xià yǔ",   "pos": "v.",   "meaning": "yomg'ir yog'moq"},
        {"no": 7,  "zh": "小姐",  "pinyin": "xiǎojiě",  "pos": "n.",   "meaning": "xonim, qiz"},
        {"no": 8,  "zh": "来",    "pinyin": "lái",      "pos": "v.",   "meaning": "kelmoq"},
        {"no": 9,  "zh": "身体",  "pinyin": "shēntǐ",   "pos": "n.",   "meaning": "tana, sog'liq"},
        {"no": 10, "zh": "爱",    "pinyin": "ài",       "pos": "v.",   "meaning": "sevmoq, yaxshi ko'rmoq"},
        {"no": 11, "zh": "些",    "pinyin": "xiē",      "pos": "m.",   "meaning": "biroz, bir nechta"},
        {"no": 12, "zh": "水果",  "pinyin": "shuǐguǒ",  "pos": "n.",   "meaning": "meva"},
        {"no": 13, "zh": "水",    "pinyin": "shuǐ",     "pos": "n.",   "meaning": "suv"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Yo'lda — ob-havo muhokamasi",
            "dialogue": [
                {"speaker": "A", "zh": "昨天北京的天气怎么样？",    "pinyin": "Zuótiān Běijīng de tiānqì zěnmeyàng?",   "translation": "Kecha Pekinda ob-havo qanday edi?"},
                {"speaker": "B", "zh": "太热了。",                  "pinyin": "Tài rè le.",                             "translation": "Haddan tashqari issiq edi."},
                {"speaker": "A", "zh": "明天呢？明天天气怎么样？",  "pinyin": "Míngtiān ne? Míngtiān tiānqì zěnmeyàng?","translation": "Ertaga-chi? Ertaga qanday?"},
                {"speaker": "B", "zh": "明天天气很好，不冷不热。",  "pinyin": "Míngtiān tiānqì hěn hǎo, bù lěng bú rè.","translation": "Ertaga yaxshi, sovuq ham emas issiq ham emas."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Sport zalda — yomg'ir va sovuq",
            "dialogue": [
                {"speaker": "A", "zh": "今天会下雨吗？",        "pinyin": "Jīntiān huì xià yǔ ma?",            "translation": "Bugun yomg'ir yog'adimi?"},
                {"speaker": "B", "zh": "今天不会下雨。",        "pinyin": "Jīntiān bú huì xià yǔ.",           "translation": "Bugun yomg'ir yog'maydi."},
                {"speaker": "A", "zh": "王小姐今天会来吗？",    "pinyin": "Wáng xiǎojiě jīntiān huì lái ma?", "translation": "Van xonim bugun keladimi?"},
                {"speaker": "B", "zh": "不会来，天气太冷了。",  "pinyin": "Bú huì lái, tiānqì tài lěng le.",  "translation": "Kelmaydi, ob-havo juda sovuq."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kasalxonada — sog'liq haqida",
            "dialogue": [
                {"speaker": "A", "zh": "你身体怎么样？",                      "pinyin": "Nǐ shēntǐ zěnmeyàng?",                          "translation": "Sog'lig'ingiz qanday?"},
                {"speaker": "B", "zh": "我身体不太好。天气太热了，不爱吃饭。", "pinyin": "Wǒ shēntǐ bú tài hǎo. Tiānqì tài rè le, bú ài chī fàn.", "translation": "Sog'lig'im unchalik yaxshi emas. Ob-havo juda issiq, ishtaham yo'q."},
                {"speaker": "A", "zh": "你多吃些水果，多喝水。",              "pinyin": "Nǐ duō chī xiē shuǐguǒ, duō hē shuǐ.",          "translation": "Ko'proq meva yeng, ko'proq suv iching."},
                {"speaker": "B", "zh": "谢谢你，医生。",                     "pinyin": "Xièxie nǐ, yīshēng.",                           "translation": "Rahmat, doktor."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "怎么样 — Holat so'roq olmoshi",
            "explanation": (
                "怎么样(zěnmeyàng) — holat, sifat, fikrni so'rash uchun.\n"
                "Tuzilishi: Ega + 怎么样?\n\n"
                "天气怎么样？— Ob-havo qanday?\n"
                "你身体怎么样？— Sog'lig'ingiz qanday?\n"
                "你的汉语怎么样？— Xitoy tilingiz qanday?"
            ),
            "examples": [
                {"zh": "明天天气怎么样？", "pinyin": "Míngtiān tiānqì zěnmeyàng?", "meaning": "Ertaga ob-havo qanday?"},
                {"zh": "你身体怎么样？",   "pinyin": "Nǐ shēntǐ zěnmeyàng?",      "meaning": "Sog'lig'ingiz qanday?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "太……了 — Haddan tashqari",
            "explanation": (
                "太(tài) + Sifat + 了 — 'juda, haddan tashqari'\n"
                "Inkorda: 不太 + Sifat (了 yo'q)\n\n"
                "天气太热了。— Ob-havo juda issiq.\n"
                "太冷了！— Juda sovuq!\n"
                "我身体不太好。— Sog'lig'im unchalik yaxshi emas."
            ),
            "examples": [
                {"zh": "太热了！",      "pinyin": "Tài rè le!",       "meaning": "Juda issiq!"},
                {"zh": "天气太冷了。",  "pinyin": "Tiānqì tài lěng le.", "meaning": "Ob-havo juda sovuq."},
                {"zh": "我不太好。",    "pinyin": "Wǒ bú tài hǎo.",   "meaning": "Men unchalik yaxshi emasman."},
            ]
        },
        {
            "no": 3,
            "title_zh": "能愿动词 会 (2) — 会 ehtimollik bildiradi",
            "explanation": (
                "会 — kelajakda bo'lishi mumkin bo'lgan holat.\n\n"
                "今天会下雨吗？— Bugun yomg'ir yog'adimi?\n"
                "她会来吗？— U keladimi?\n"
                "不会 — bo'lmaydi, kelmaydi, yog'maydi"
            ),
            "examples": [
                {"zh": "今天会下雨吗？", "pinyin": "Jīntiān huì xià yǔ ma?", "meaning": "Bugun yomg'ir yog'adimi?"},
                {"zh": "明天会冷吗？",   "pinyin": "Míngtiān huì lěng ma?",  "meaning": "Ertaga sovuq bo'ladimi?"},
                {"zh": "她今天不会来。", "pinyin": "Tā jīntiān bú huì lái.", "meaning": "U bugun kelmaydi."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Ertaga ob-havo qanday?",   "answer": "明天天气怎么样？", "pinyin": "Míngtiān tiānqì zěnmeyàng?"},
                {"prompt": "Ob-havo juda issiq.",       "answer": "天气太热了。",     "pinyin": "Tiānqì tài rè le."},
                {"prompt": "Bugun yomg'ir yog'adimi?", "answer": "今天会下雨吗？",   "pinyin": "Jīntiān huì xià yǔ ma?"},
                {"prompt": "Sog'lig'ingiz qanday?",    "answer": "你身体怎么样？",   "pinyin": "Nǐ shēntǐ zěnmeyàng?"},
                {"prompt": "Ko'proq meva yeng.",        "answer": "多吃些水果。",     "pinyin": "Duō chī xiē shuǐguǒ."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "天气___热了。",    "answer": "太",     "pinyin": "tài"},
                {"prompt": "明天天气___？",    "answer": "怎么样", "pinyin": "zěnmeyàng"},
                {"prompt": "今天会___雨吗？",  "answer": "下",     "pinyin": "xià"},
                {"prompt": "我身体不___好。",  "answer": "太",     "pinyin": "tài"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["明天天气怎么样？", "天气太热了。", "今天会下雨吗？", "你身体怎么样？", "多吃些水果。"]},
        {"no": 2, "answers": ["太", "怎么样", "下", "太"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Bugungi ob-havo haqida 3-4 gap yozing:",
            "template": "今天天气___。天气___了。今天会___吗？",
            "words": ["天气", "太", "了", "热", "冷", "下雨", "怎么样"],
        },
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
