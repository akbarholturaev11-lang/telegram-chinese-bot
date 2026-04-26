import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 8,
    "lesson_code": "HSK1-L08",
    "title": "我想喝茶",
    "goal": "Xohish bildirish, narx so'rash va o'lchov so'zlarini o'rganish",
    "intro_text": (
        "Sakkizinchi darsda siz 想 modal fe'li bilan xohish bildirish, "
        "narx so'rash (多少钱?) va 个/口 o'lchov so'zlarini o'rganasiz. "
        "15 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "想",   "pinyin": "xiǎng",    "pos": "mod.", "meaning": "xohlamoq, istamoq"},
        {"no": 2,  "zh": "喝",   "pinyin": "hē",       "pos": "v.",   "meaning": "ichmoq"},
        {"no": 3,  "zh": "茶",   "pinyin": "chá",      "pos": "n.",   "meaning": "choy"},
        {"no": 4,  "zh": "吃",   "pinyin": "chī",      "pos": "v.",   "meaning": "yemoq"},
        {"no": 5,  "zh": "米饭", "pinyin": "mǐfàn",    "pos": "n.",   "meaning": "guruch oshi, pishirilgan guruch"},
        {"no": 6,  "zh": "下午", "pinyin": "xiàwǔ",    "pos": "n.",   "meaning": "tushdan keyin, peshin"},
        {"no": 7,  "zh": "商店", "pinyin": "shāngdiàn","pos": "n.",   "meaning": "do'kon, magazin"},
        {"no": 8,  "zh": "买",   "pinyin": "mǎi",      "pos": "v.",   "meaning": "sotib olmoq"},
        {"no": 9,  "zh": "个",   "pinyin": "gè",       "pos": "m.",   "meaning": "umumiy o'lchov so'z (dona)"},
        {"no": 10, "zh": "杯子", "pinyin": "bēizi",    "pos": "n.",   "meaning": "piyola, stakan"},
        {"no": 11, "zh": "这",   "pinyin": "zhè",      "pos": "pron.","meaning": "bu (ko'rsatish olmoshi)"},
        {"no": 12, "zh": "多少", "pinyin": "duōshao",  "pos": "pron.","meaning": "qancha, necha (10+)"},
        {"no": 13, "zh": "钱",   "pinyin": "qián",     "pos": "n.",   "meaning": "pul"},
        {"no": 14, "zh": "块",   "pinyin": "kuài",     "pos": "m.",   "meaning": "yuan (og'zaki)"},
        {"no": 15, "zh": "那",   "pinyin": "nà",       "pos": "pron.","meaning": "u, o'sha (ko'rsatish olmoshi)"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Restoranда — nima ichish/yeyish",
            "dialogue": [
                {"speaker": "A", "zh": "你想喝什么？",  "pinyin": "Nǐ xiǎng hē shénme?",  "translation": "Siz nima ichmoqchisiz?"},
                {"speaker": "B", "zh": "我想喝茶。",    "pinyin": "Wǒ xiǎng hē chá.",     "translation": "Men choy ichmoqchiman."},
                {"speaker": "A", "zh": "你想吃什么？",  "pinyin": "Nǐ xiǎng chī shénme?", "translation": "Siz nima yemoqchisiz?"},
                {"speaker": "B", "zh": "我想吃米饭。",  "pinyin": "Wǒ xiǎng chī mǐfàn.",  "translation": "Men guruch oshi yemoqchiman."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Mehmonxonada — tushdan keyingi reja",
            "dialogue": [
                {"speaker": "A", "zh": "下午你想做什么？",   "pinyin": "Xiàwǔ nǐ xiǎng zuò shénme?",   "translation": "Tushdan keyin nima qilmoqchisiz?"},
                {"speaker": "B", "zh": "下午我想去商店。",   "pinyin": "Xiàwǔ wǒ xiǎng qù shāngdiàn.", "translation": "Tushdan keyin do'konga bormoqchiman."},
                {"speaker": "A", "zh": "你想买什么？",       "pinyin": "Nǐ xiǎng mǎi shénme?",         "translation": "Nima sotib olmoqchisiz?"},
                {"speaker": "B", "zh": "我想买一个杯子。",   "pinyin": "Wǒ xiǎng mǎi yī gè bēizi.",    "translation": "Bitta piyola sotib olmoqchiman."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Do'konda — narx so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "你好！这个杯子多少钱？",  "pinyin": "Nǐ hǎo! Zhège bēizi duōshao qián?", "translation": "Salom! Bu piyola qancha turadi?"},
                {"speaker": "B", "zh": "28块。",                  "pinyin": "Èrshíbā kuài.",                     "translation": "28 yuan."},
                {"speaker": "A", "zh": "那个杯子多少钱？",        "pinyin": "Nàge bēizi duōshao qián?",          "translation": "U piyola qancha?"},
                {"speaker": "B", "zh": "那个杯子18块钱。",        "pinyin": "Nàge bēizi shíbā kuài qián.",       "translation": "U piyola 18 yuan."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "能愿动词 想 — Modal fe'l 想",
            "explanation": (
                "想(xiǎng) — xohish yoki reja bildiradi.\n"
                "Tuzilishi: Ega + 想 + Fe'l + Narsa\n\n"
                "Ijobiy: 我想喝茶。— Men choy ichmoqchiman.\n"
                "So'roq: 你想做什么？— Nima qilmoqchisiz?\n\n"
                "想 vs 会:\n"
                "我想说汉语。— Men xitoycha gapirmoqchiman (xohish).\n"
                "我会说汉语。— Men xitoycha gapira olaman (qobiliyat)."
            ),
            "examples": [
                {"zh": "我想喝茶。",         "pinyin": "Wǒ xiǎng hē chá.",           "meaning": "Men choy ichmoqchiman."},
                {"zh": "她想去学校看书。",   "pinyin": "Tā xiǎng qù xuéxiào kàn shū.", "meaning": "U maktabda kitob o'qimoqchi."},
                {"zh": "你想买什么？",       "pinyin": "Nǐ xiǎng mǎi shénme?",       "meaning": "Nima sotib olmoqchisiz?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "多少 — Qancha so'rog'i (10+)",
            "explanation": (
                "多少(duōshao) — 10 dan katta sonlar uchun so'roq olmoshi.\n"
                "Eslatma: 几(jǐ) — 10 gacha, 多少(duōshao) — 10 dan katta.\n\n"
                "Narx so'rash: ……多少钱？\n"
                "这个杯子多少钱？— Bu piyola qancha?\n\n"
                "Son so'rash:\n"
                "你们学校有多少学生？— Maktabingizda nechta o'quvchi bor?\n"
                "你有多少钱？— Sizda qancha pul bor?"
            ),
            "examples": [
                {"zh": "这个杯子多少钱？",   "pinyin": "Zhège bēizi duōshao qián?",    "meaning": "Bu piyola qancha turadi?"},
                {"zh": "你家有多少口人？",   "pinyin": "Nǐ jiā yǒu duōshao kǒu rén?", "meaning": "Oilangizda necha kishi bor?"},
                {"zh": "一个苹果多少钱？",   "pinyin": "Yī gè píngguǒ duōshao qián?", "meaning": "Bitta olma qancha?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "量词 个/口 — O'lchov so'zlar",
            "explanation": (
                "Xitoy tilida son + ot orasida o'lchov so'z kerak.\n\n"
                "个(gè) — eng umumiy o'lchov so'z:\n"
                "一个杯子 — bitta piyola\n"
                "三个学生 — uchta o'quvchi\n"
                "两个老师 — ikkita o'qituvchi\n\n"
                "口(kǒu) — oila a'zolari uchun:\n"
                "三口人 — uch kishilik oila\n"
                "六口人 — olti kishilik oila"
            ),
            "examples": [
                {"zh": "一个杯子",   "pinyin": "yī gè bēizi",    "meaning": "bitta piyola"},
                {"zh": "五个学生",   "pinyin": "wǔ gè xuésheng", "meaning": "beshta o'quvchi"},
                {"zh": "三口人",     "pinyin": "sān kǒu rén",    "meaning": "uch kishilik oila"},
            ]
        },
        {
            "no": 4,
            "title_zh": "钱数的表达 — Pul miqdori",
            "explanation": (
                "Xitoy milliy valyutasi: 人民币 (Renminbi, RMB)\n"
                "Rasmiy: 元(yuán)\n"
                "Og'zaki: 块(kuài)\n\n"
                "Misol:\n"
                "28块 = 28元 — 28 yuan\n"
                "18块钱 — 18 yuan (so'zlashuvda)\n\n"
                "这个杯子多少钱？— Bu qancha?\n"
                "28块。— 28 yuan."
            ),
            "examples": [
                {"zh": "这个多少钱？",  "pinyin": "Zhège duōshao qián?", "meaning": "Bu qancha turadi?"},
                {"zh": "28块钱。",     "pinyin": "Èrshíbā kuài qián.",  "meaning": "28 yuan."},
                {"zh": "一百块。",     "pinyin": "Yìbǎi kuài.",         "meaning": "100 yuan."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Siz nima ichmoqchisiz?",                  "answer": "你想喝什么？",      "pinyin": "Nǐ xiǎng hē shénme?"},
                {"prompt": "Men choy ichmoqchiman.",                   "answer": "我想喝茶。",        "pinyin": "Wǒ xiǎng hē chá."},
                {"prompt": "Bu piyola qancha turadi?",                 "answer": "这个杯子多少钱？",  "pinyin": "Zhège bēizi duōshao qián?"},
                {"prompt": "28 yuan.",                                 "answer": "28块钱。",          "pinyin": "Èrshíbā kuài qián."},
                {"prompt": "Men tushdan keyin do'konga bormoqchiman.", "answer": "下午我想去商店。",  "pinyin": "Xiàwǔ wǒ xiǎng qù shāngdiàn."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "你___喝什么？",              "answer": "想",    "pinyin": "xiǎng"},
                {"prompt": "这___杯子多少钱？",          "answer": "个",    "pinyin": "gè"},
                {"prompt": "___个杯子18块___。",         "answer": "那/钱", "pinyin": "nà/qián"},
                {"prompt": "我想买___个杯子。",          "answer": "一",    "pinyin": "yī"},
            ]
        },
        {
            "no": 3,
            "type": "price_dialogue",
            "instruction": "Narx so'rab-javob bering:",
            "items": [
                {"prompt": "苹果(apple) — 5块/个",  "question": "这个苹果多少钱？", "answer": "五块钱。"},
                {"prompt": "书(book) — 35块",       "question": "这本书多少钱？",   "answer": "三十五块钱。"},
                {"prompt": "茶(tea) — 18块",        "question": "这个茶多少钱？",   "answer": "十八块钱。"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你想喝什么？", "我想喝茶。", "这个杯子多少钱？", "28块钱。", "下午我想去商店。"]},
        {"no": 2, "answers": ["想", "个", "那/钱", "一"]},
        {"no": 3, "answers": ["五块钱。", "三十五块钱。", "十八块钱。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Bugungi rejangizni yozing (想 ishlatib, 3-4 gap):",
            "template": "今天下午我想___。我想___。我想买___。",
            "words": ["想", "喝", "吃", "去", "买", "茶", "米饭", "杯子"],
        },
        {
            "no": 2,
            "instruction": "Do'konda narx so'rash dialogini tuzing (4 qator):",
            "example": "A: 你好！___多少钱？\nB: ___块。\nA: ___多少钱？\nB: ___块钱。",
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
