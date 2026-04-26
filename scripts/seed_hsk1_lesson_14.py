import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 14,
    "lesson_code": "HSK1-L14",
    "title": "她买了不少衣服",
    "goal": "了 yuklamasi — harakat tugallangani, 后 vaqt belgisi va 都 ravishi",
    "intro_text": (
        "O'n to'rtinchi darsda siz 了 yuklamasi bilan harakatning tugallanganini, "
        "后 bilan kelajak vaqtini va 都 ravishini o'rganasiz. "
        "16 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "东西",  "pinyin": "dōngxi",    "pos": "n.",   "meaning": "narsa, buyum"},
        {"no": 2,  "zh": "一点儿","pinyin": "yīdiǎnr",   "pos": "num.", "meaning": "biroz, bir oz"},
        {"no": 3,  "zh": "苹果",  "pinyin": "píngguǒ",   "pos": "n.",   "meaning": "olma"},
        {"no": 4,  "zh": "看见",  "pinyin": "kànjiàn",   "pos": "v.",   "meaning": "ko'rmoq (ko'rib qolmoq)"},
        {"no": 5,  "zh": "先生",  "pinyin": "xiānsheng", "pos": "n.",   "meaning": "janob, janob (hurmat)"},
        {"no": 6,  "zh": "开",    "pinyin": "kāi",       "pos": "v.",   "meaning": "ochmoq, haydamoq (mashina)"},
        {"no": 7,  "zh": "车",    "pinyin": "chē",       "pos": "n.",   "meaning": "mashina, transport"},
        {"no": 8,  "zh": "回来",  "pinyin": "huílai",    "pos": "v.",   "meaning": "qaytib kelmoq"},
        {"no": 9,  "zh": "分钟",  "pinyin": "fēnzhōng",  "pos": "n.",   "meaning": "daqiqa (vaqt o'lchovi)"},
        {"no": 10, "zh": "后",    "pinyin": "hòu",       "pos": "n.",   "meaning": "keyin, -dan keyin"},
        {"no": 11, "zh": "衣服",  "pinyin": "yīfu",      "pos": "n.",   "meaning": "kiyim"},
        {"no": 12, "zh": "漂亮",  "pinyin": "piàoliang", "pos": "adj.", "meaning": "chiroyli, go'zal"},
        {"no": 13, "zh": "啊",    "pinyin": "a",         "pos": "part.","meaning": "ha, albatta (his yuklamasi)"},
        {"no": 14, "zh": "少",    "pinyin": "shǎo",      "pos": "adj.", "meaning": "kam, oz"},
        {"no": 15, "zh": "这些",  "pinyin": "zhèxiē",    "pos": "pron.","meaning": "bular, bu narsalar"},
        {"no": 16, "zh": "都",    "pinyin": "dōu",       "pos": "adv.", "meaning": "hammasi, barchasi"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Yotoqxonada — kecha nima qilding",
            "dialogue": [
                {"speaker": "A", "zh": "昨天上午你去哪儿了？",   "pinyin": "Zuótiān shàngwǔ nǐ qù nǎr le?",     "translation": "Kecha ertalab qayerga ketdingiz?"},
                {"speaker": "B", "zh": "我去商店买东西了。",     "pinyin": "Wǒ qù shāngdiàn mǎi dōngxi le.",    "translation": "Do'konga narsa sotib olishga ketdim."},
                {"speaker": "A", "zh": "你买什么了？",           "pinyin": "Nǐ mǎi shénme le?",                 "translation": "Nima sotib oldingiz?"},
                {"speaker": "B", "zh": "我买了一点儿苹果。",     "pinyin": "Wǒ mǎile yīdiǎnr píngguǒ.",        "translation": "Biroz olma sotib oldim."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Kompaniyada — Zhang janobni ko'rdingizmi",
            "dialogue": [
                {"speaker": "A", "zh": "你看见张先生了吗？",        "pinyin": "Nǐ kànjiàn Zhāng xiānsheng le ma?",      "translation": "Zhang janobni ko'rdingizmi?"},
                {"speaker": "B", "zh": "看见了，他去学开车了。",    "pinyin": "Kànjiàn le, tā qù xué kāi chē le.",      "translation": "Ko'rdim, u mashina haydashni o'rganishga ketdi."},
                {"speaker": "A", "zh": "他什么时候能回来？",        "pinyin": "Tā shénme shíhou néng huílai?",           "translation": "U qachon qaytib kelishi mumkin?"},
                {"speaker": "B", "zh": "40分钟后回来。",           "pinyin": "Sìshí fēnzhōng hòu huílai.",             "translation": "40 daqiqadan keyin qaytadi."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Do'kon oldida — kiyimlar",
            "dialogue": [
                {"speaker": "A", "zh": "王方的衣服太漂亮了！",     "pinyin": "Wáng Fāng de yīfu tài piàoliang le!",    "translation": "Van Fanning kiyimlari juda chiroyli!"},
                {"speaker": "B", "zh": "是啊，她买了不少衣服。",   "pinyin": "Shì a, tā mǎile bùshǎo yīfu.",          "translation": "Ha albatta, u ko'p kiyim sotib oldi."},
                {"speaker": "A", "zh": "你买什么了？",             "pinyin": "Nǐ mǎi shénme le?",                     "translation": "Siz nima sotib oldingiz?"},
                {"speaker": "B", "zh": "我没买，这些都是王方的东西。","pinyin": "Wǒ méi mǎi, zhèxiē dōu shì Wáng Fāng de dōngxi.", "translation": "Men hech narsa olmadim, bular hammasi Van Fangning narsalari."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "了 — Harakat tugallangani",
            "explanation": (
                "了(le) gap oxirida — harakat sodir bo'lgani yoki tugallanganini bildiradi.\n\n"
                "Tuzilishi:\n"
                "Ega + Fe'l + 了 (gap oxiri)\n"
                "Ega + Fe'l + 了 + Son/Sifat + Ot\n\n"
                "Misol:\n"
                "我去商店了。— Men do'konga bordim.\n"
                "她买了不少衣服。— U ko'p kiyim sotib oldi.\n"
                "我买了一点儿苹果。— Men biroz olma sotib oldim.\n\n"
                "Inkor: 没 + Fe'l (了 o'chiriladi)\n"
                "我没买。— Men sotib olmadim.\n"
                "她没去商店。— U do'konga bormadi."
            ),
            "examples": [
                {"zh": "我去商店了。",       "pinyin": "Wǒ qù shāngdiàn le.",    "meaning": "Men do'konga bordim."},
                {"zh": "她买了不少衣服。",   "pinyin": "Tā mǎile bùshǎo yīfu.", "meaning": "U ko'p kiyim sotib oldi."},
                {"zh": "我没买。",           "pinyin": "Wǒ méi mǎi.",            "meaning": "Men sotib olmadim."},
            ]
        },
        {
            "no": 2,
            "title_zh": "名词 后 — 后 vaqt belgisi",
            "explanation": (
                "后(hòu) — biror vaqtdan keyingi paytni bildiradi.\n\n"
                "40分钟后 — 40 daqiqadan keyin\n"
                "三天后 — uch kundan keyin\n"
                "一个星期后 — bir haftadan keyin\n"
                "五点后 — soat beshdan keyin\n\n"
                "Misol:\n"
                "40分钟后回来。— 40 daqiqadan keyin qaytadi.\n"
                "三天后我去北京。— Uch kundan keyin Pekinga boraman."
            ),
            "examples": [
                {"zh": "40分钟后回来。",   "pinyin": "Sìshí fēnzhōng hòu huílai.", "meaning": "40 daqiqadan keyin qaytadi."},
                {"zh": "三天后见。",       "pinyin": "Sān tiān hòu jiàn.",         "meaning": "Uch kundan keyin ko'rishamiz."},
                {"zh": "八点后能来吗？",   "pinyin": "Bā diǎn hòu néng lái ma?",   "meaning": "Soat sakkizdan keyin kela olasizmi?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "副词 都 — Ravish 都 (hammasi)",
            "explanation": (
                "都(dōu) — 'hammasi, barchasi' ma'nosini bildiradi.\n"
                "Muhim: Sanab o'tilgan narsalar 都 DAN OLDIN keladi.\n\n"
                "Misol:\n"
                "这些都是王方的东西。— Bular hammasi Van Fangning narsalari.\n"
                "我们都是中国人。— Biz hammamiz xitoyliklar.\n"
                "他们都喜欢喝茶。— Ular hammasi choy ichishni yaxshi ko'radi."
            ),
            "examples": [
                {"zh": "这些都是王方的东西。", "pinyin": "Zhèxiē dōu shì Wáng Fāng de dōngxi.", "meaning": "Bular hammasi Van Fangning narsalari."},
                {"zh": "我们都是中国人。",     "pinyin": "Wǒmen dōu shì Zhōngguó rén.",         "meaning": "Biz hammamiz xitoyliklar."},
                {"zh": "他们都喜欢喝茶。",     "pinyin": "Tāmen dōu xǐhuan hē chá.",           "meaning": "Ular hammasi choy ichishni yaxshi ko'radi."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Kecha ertalab qayerga ketdingiz?",     "answer": "昨天上午你去哪儿了？",  "pinyin": "Zuótiān shàngwǔ nǐ qù nǎr le?"},
                {"prompt": "Men do'konga narsalar sotib olishga ketdim.", "answer": "我去商店买东西了。","pinyin": "Wǒ qù shāngdiàn mǎi dōngxi le."},
                {"prompt": "U ko'p kiyim sotib oldi.",             "answer": "她买了不少衣服。",      "pinyin": "Tā mǎile bùshǎo yīfu."},
                {"prompt": "40 daqiqadan keyin qaytadi.",          "answer": "40分钟后回来。",        "pinyin": "Sìshí fēnzhōng hòu huílai."},
                {"prompt": "Bular hammasi uning narsalari.",       "answer": "这些都是他的东西。",    "pinyin": "Zhèxiē dōu shì tā de dōngxi."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "我去商店买东西___。",       "answer": "了",  "pinyin": "le"},
                {"prompt": "40分钟___回来。",           "answer": "后",  "pinyin": "hòu"},
                {"prompt": "这些___是王方的东西。",     "answer": "都",  "pinyin": "dōu"},
                {"prompt": "我___买，这些不是我的。",   "answer": "没",  "pinyin": "méi"},
            ]
        },
        {
            "no": 3,
            "type": "negative",
            "instruction": "Inkor gapga aylantiring (没):",
            "items": [
                {"prompt": "她买了不少衣服。",   "answer": "她没买衣服。",     "pinyin": "Tā méi mǎi yīfu."},
                {"prompt": "我去商店了。",       "answer": "我没去商店。",     "pinyin": "Wǒ méi qù shāngdiàn."},
                {"prompt": "他看见张先生了。",   "answer": "他没看见张先生。", "pinyin": "Tā méi kànjiàn Zhāng xiānsheng."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["昨天上午你去哪儿了？", "我去商店买东西了。", "她买了不少衣服。", "40分钟后回来。", "这些都是他的东西。"]},
        {"no": 2, "answers": ["了", "后", "都", "没"]},
        {"no": 3, "answers": ["她没买衣服。", "我没去商店。", "他没看见张先生。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Kechagi kuniyingizni yozing (了 ishlatib, 4 ta gap):",
            "template": "昨天我___了。我买了___。我没___。___后我回家了。",
            "words": ["了", "没", "去", "买", "后", "分钟"],
        },
        {
            "no": 2,
            "instruction": "都 ishlatib javob bering:",
            "items": [
                {"prompt": "你的朋友都是中国人吗？", "hint": "Ha/yo'q, 都 ishlatib"},
                {"prompt": "桌子上的东西都是谁的？", "hint": "Egalikni ayting"},
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
