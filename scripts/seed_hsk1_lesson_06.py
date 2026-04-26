import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 6,
    "lesson_code": "HSK1-L06",
    "title": "我会说汉语",
    "goal": "Qobiliyat va ko'nikmalar haqida gapirish, 会 modal fe'li",
    "intro_text": (
        "Oltinchi darsda siz 会 modal fe'li bilan qobiliyatlarni ifodalashni, "
        "sifat kesimli gaplar va 怎么 so'roq olmoshini o'rganasiz. "
        "12 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "会",   "pinyin": "huì",    "pos": "mod.", "meaning": "bila olmoq, qodir bo'lmoq (o'rganib)"},
        {"no": 2,  "zh": "说",   "pinyin": "shuō",   "pos": "v.",   "meaning": "gapirmoq, aytmoq"},
        {"no": 3,  "zh": "妈妈", "pinyin": "māma",   "pos": "n.",   "meaning": "ona, mama"},
        {"no": 4,  "zh": "菜",   "pinyin": "cài",    "pos": "n.",   "meaning": "taom, ovqat, sabzavot"},
        {"no": 5,  "zh": "很",   "pinyin": "hěn",    "pos": "adv.", "meaning": "juda, ancha"},
        {"no": 6,  "zh": "好吃", "pinyin": "hǎochī", "pos": "adj.", "meaning": "mazali, yaxshi ta'm"},
        {"no": 7,  "zh": "做",   "pinyin": "zuò",    "pos": "v.",   "meaning": "qilmoq, tayyorlamoq"},
        {"no": 8,  "zh": "写",   "pinyin": "xiě",    "pos": "v.",   "meaning": "yozmoq"},
        {"no": 9,  "zh": "汉字", "pinyin": "Hànzì",  "pos": "n.",   "meaning": "xitoy yozuvi (ierogliflar)"},
        {"no": 10, "zh": "字",   "pinyin": "zì",     "pos": "n.",   "meaning": "belgi, harf, ieroglifA"},
        {"no": 11, "zh": "怎么", "pinyin": "zěnme",  "pos": "pron.","meaning": "qanday, qanday qilib"},
        {"no": 12, "zh": "读",   "pinyin": "dú",     "pos": "v.",   "meaning": "o'qimoq (ovoz chiqarib)"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Maktabda — xitoy tilida gapirish",
            "dialogue": [
                {"speaker": "A", "zh": "你会说汉语吗？",    "pinyin": "Nǐ huì shuō Hànyǔ ma?",     "translation": "Siz xitoycha gapira olasizmi?"},
                {"speaker": "B", "zh": "我会说汉语。",      "pinyin": "Wǒ huì shuō Hànyǔ.",        "translation": "Men xitoycha gapira olaman."},
                {"speaker": "A", "zh": "你妈妈会说汉语吗？", "pinyin": "Nǐ māma huì shuō Hànyǔ ma?", "translation": "Onangiz xitoycha gapira oladimi?"},
                {"speaker": "B", "zh": "她不会说。",        "pinyin": "Tā bú huì shuō.",            "translation": "U gapira olmaydi."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Oshxonada — xitoy taomi",
            "dialogue": [
                {"speaker": "A", "zh": "中国菜好吃吗？",    "pinyin": "Zhōngguó cài hǎochī ma?",    "translation": "Xitoy taomi mazalimi?"},
                {"speaker": "B", "zh": "中国菜很好吃。",    "pinyin": "Zhōngguó cài hěn hǎochī.",   "translation": "Xitoy taomi juda mazali."},
                {"speaker": "A", "zh": "你会做中国菜吗？",  "pinyin": "Nǐ huì zuò Zhōngguó cài ma?", "translation": "Siz xitoy taomi tayyorlay olasizmi?"},
                {"speaker": "B", "zh": "我不会做。",        "pinyin": "Wǒ bú huì zuò.",             "translation": "Men tayyorlay olmayman."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kutubxonada — xitoy yozuvi",
            "dialogue": [
                {"speaker": "A", "zh": "你会写汉字吗？",              "pinyin": "Nǐ huì xiě Hànzì ma?",                    "translation": "Siz xitoy ierogliflarini yoza olasizmi?"},
                {"speaker": "B", "zh": "我会写。",                    "pinyin": "Wǒ huì xiě.",                             "translation": "Men yoza olaman."},
                {"speaker": "A", "zh": "这个字怎么写？",              "pinyin": "Zhège zì zěnme xiě?",                     "translation": "Bu ieroglifni qanday yoziladi?"},
                {"speaker": "B", "zh": "对不起，这个字我会读，不会写。", "pinyin": "Duìbuqǐ, zhège zì wǒ huì dú, bú huì xiě.", "translation": "Kechirasiz, bu ieroglifni o'qiy olaman, lekin yoza olmayman."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "能愿动词 会 — Modal fe'l 会",
            "explanation": (
                "会(huì) — o'rganish orqali qodir bo'lmoq ma'nosini bildiradi.\n"
                "Tuzilishi: Ega + (不)会 + Fe'l\n\n"
                "Ijobiy: 我会说汉语。— Men xitoycha gapira olaman.\n"
                "Inkor: 我不会做中国菜。— Men xitoy taomi tayyorlay olmayman.\n"
                "So'roq: 你会写汉字吗？— Siz ierogliflarini yoza olasizmi?\n\n"
                "Eslatma: 会 bilan 不会, so'roqda 吗 ishlatiladi."
            ),
            "examples": [
                {"zh": "我会说汉语。",     "pinyin": "Wǒ huì shuō Hànyǔ.",          "meaning": "Men xitoycha gapira olaman."},
                {"zh": "她不会做中国菜。", "pinyin": "Tā bú huì zuò Zhōngguó cài.", "meaning": "U xitoy taomi tayyorlay olmaydi."},
                {"zh": "你会写汉字吗？",   "pinyin": "Nǐ huì xiě Hànzì ma?",        "meaning": "Siz ierogliflarini yoza olasizmi?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "形容词谓语句 — Sifat kesimli gap",
            "explanation": (
                "Sifat kesim: Ega + 很/不 + Sifat\n\n"
                "Xitoy tilida sifat gap kesimi bo'la oladi.\n"
                "Tasdiqda odatda 很(hěn) ishlatiladi:\n"
                "中国菜很好吃。— Xitoy taomi juda mazali.\n\n"
                "Inkorda 不 ishlatiladi (很 shart emas):\n"
                "我妈妈的汉语不好。— Onamning xitoy tili yaxshi emas.\n\n"
                "Diqqat: 很 ko'pincha ma'nosiz bo'lib, grammatik talabdan kelib chiqadi."
            ),
            "examples": [
                {"zh": "中国菜很好吃。",     "pinyin": "Zhōngguó cài hěn hǎochī.", "meaning": "Xitoy taomi juda mazali."},
                {"zh": "她的汉语很好。",     "pinyin": "Tā de Hànyǔ hěn hǎo.",    "meaning": "Uning xitoy tili yaxshi."},
                {"zh": "我妈妈的汉语不好。", "pinyin": "Wǒ māma de Hànyǔ bù hǎo.", "meaning": "Onamning xitoy tili yaxshi emas."},
            ]
        },
        {
            "no": 3,
            "title_zh": "怎么 — Qanday so'roq olmoshi",
            "explanation": (
                "怎么(zěnme) — fe'l oldida kelib, harakat usulini so'raydi.\n"
                "Tuzilishi: Ega + 怎么 + Fe'l?\n\n"
                "Misol:\n"
                "这个字怎么写？— Bu ieroglifni qanday yoziladi?\n"
                "这个字怎么读？— Bu ieroglifni qanday o'qiladi?\n"
                "中国菜怎么做？— Xitoy taomi qanday tayyorlanadi?"
            ),
            "examples": [
                {"zh": "这个字怎么写？", "pinyin": "Zhège zì zěnme xiě?", "meaning": "Bu ieroglifni qanday yoziladi?"},
                {"zh": "这个字怎么读？", "pinyin": "Zhège zì zěnme dú?",  "meaning": "Bu ieroglifni qanday o'qiladi?"},
                {"zh": "汉语怎么说？",   "pinyin": "Hànyǔ zěnme shuō?",  "meaning": "Xitoycha qanday aytiladi?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Siz xitoycha gapira olasizmi?",       "answer": "你会说汉语吗？",   "pinyin": "Nǐ huì shuō Hànyǔ ma?"},
                {"prompt": "Men xitoycha gapira olaman.",          "answer": "我会说汉语。",     "pinyin": "Wǒ huì shuō Hànyǔ."},
                {"prompt": "Xitoy taomi juda mazali.",             "answer": "中国菜很好吃。",   "pinyin": "Zhōngguó cài hěn hǎochī."},
                {"prompt": "Men xitoy taomi tayyorlay olmayman.",  "answer": "我不会做中国菜。", "pinyin": "Wǒ bú huì zuò Zhōngguó cài."},
                {"prompt": "Bu ieroglifni qanday yoziladi?",       "answer": "这个字怎么写？",   "pinyin": "Zhège zì zěnme xiě?"},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "你___说汉语吗？",     "answer": "会",   "pinyin": "huì"},
                {"prompt": "中国菜___好吃。",     "answer": "很",   "pinyin": "hěn"},
                {"prompt": "这个字___写？",       "answer": "怎么", "pinyin": "zěnme"},
                {"prompt": "我会___，不会___。",  "answer": "读/写", "pinyin": "dú/xiě"},
            ]
        },
        {
            "no": 3,
            "type": "make_negative",
            "instruction": "Inkor gapga aylantiring:",
            "items": [
                {"prompt": "我会说汉语。",   "answer": "我不会说汉语。",   "pinyin": "Wǒ bú huì shuō Hànyǔ."},
                {"prompt": "中国菜很好吃。", "answer": "中国菜不好吃。",   "pinyin": "Zhōngguó cài bù hǎochī."},
                {"prompt": "她会写汉字。",   "answer": "她不会写汉字。",   "pinyin": "Tā bú huì xiě Hànzì."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你会说汉语吗？", "我会说汉语。", "中国菜很好吃。", "我不会做中国菜。", "这个字怎么写？"]},
        {"no": 2, "answers": ["会", "很", "怎么", "读/写"]},
        {"no": 3, "answers": ["我不会说汉语。", "中国菜不好吃。", "她不会写汉字。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "O'zingiz haqida 4 ta gap yozing (nima qila olasiz/olmaysiz):",
            "template": "我会___。我不会___。我___会___吗？",
            "words": ["会", "不会", "说", "写", "做", "读", "汉语", "汉字", "中国菜"],
        },
        {
            "no": 2,
            "instruction": "Savollarga javob bering:",
            "items": [
                {"prompt": "你会说汉语吗？",      "hint": "Ha yoki yo'q, to'liq gap bilan"},
                {"prompt": "中国菜好吃吗？",      "hint": "O'z fikringizni ayting"},
                {"prompt": "这个字怎么写？ (好)", "hint": "Hǎo — yaxshi ieroglifini tasvirlab bering"},
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
