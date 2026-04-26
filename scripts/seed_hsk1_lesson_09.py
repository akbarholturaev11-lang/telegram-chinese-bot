import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 9,
    "lesson_code": "HSK1-L09",
    "title": "你儿子在哪儿工作",
    "goal": "Joylashuv va ish joyini so'rash, 在 fe'li va predlogi",
    "intro_text": (
        "To'qqizinchi darsda siz kimdir qayerda ekanini, "
        "qayerda ishlaymiz va 在 so'zining ikki xil ishlatilishini o'rganasiz. "
        "14 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "小",   "pinyin": "xiǎo",     "pos": "adj.", "meaning": "kichik, kichkina"},
        {"no": 2,  "zh": "猫",   "pinyin": "māo",      "pos": "n.",   "meaning": "mushuk"},
        {"no": 3,  "zh": "在",   "pinyin": "zài",      "pos": "v./prep.", "meaning": "bor, joylashgan / -da, -da"},
        {"no": 4,  "zh": "哪儿", "pinyin": "nǎr",      "pos": "pron.", "meaning": "qayerda, qayerga"},
        {"no": 5,  "zh": "狗",   "pinyin": "gǒu",      "pos": "n.",   "meaning": "it, kuchuk"},
        {"no": 6,  "zh": "椅子", "pinyin": "yǐzi",     "pos": "n.",   "meaning": "stul"},
        {"no": 7,  "zh": "下面", "pinyin": "xiàmian",  "pos": "n.",   "meaning": "pastda, tagida"},
        {"no": 8,  "zh": "工作", "pinyin": "gōngzuò",  "pos": "v./n.","meaning": "ishlash / ish, kasb"},
        {"no": 9,  "zh": "儿子", "pinyin": "érzi",     "pos": "n.",   "meaning": "o'g'il (farzand)"},
        {"no": 10, "zh": "医院", "pinyin": "yīyuàn",   "pos": "n.",   "meaning": "shifoxona, kasalxona"},
        {"no": 11, "zh": "医生", "pinyin": "yīshēng",  "pos": "n.",   "meaning": "shifokor, doktor"},
        {"no": 12, "zh": "爸爸", "pinyin": "bàba",     "pos": "n.",   "meaning": "ota, dada"},
        {"no": 13, "zh": "家",   "pinyin": "jiā",      "pos": "n.",   "meaning": "uy, oila"},
        {"no": 14, "zh": "那儿", "pinyin": "nàr",      "pos": "pron.", "meaning": "u yerda, o'sha yerda"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Uyda — mushuk va it qayerda",
            "dialogue": [
                {"speaker": "A", "zh": "小猫在哪儿？",          "pinyin": "Xiǎo māo zài nǎr?",           "translation": "Mushukcha qayerda?"},
                {"speaker": "B", "zh": "小猫在那儿。",          "pinyin": "Xiǎo māo zài nàr.",           "translation": "Mushukcha u yerda."},
                {"speaker": "A", "zh": "小狗在哪儿？",          "pinyin": "Xiǎo gǒu zài nǎr?",           "translation": "Kuchukcha qayerda?"},
                {"speaker": "B", "zh": "小狗在椅子下面。",      "pinyin": "Xiǎo gǒu zài yǐzi xiàmian.",  "translation": "Kuchukcha stul tagida."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Temir yo'l stansiyasida — ish joyi",
            "dialogue": [
                {"speaker": "A", "zh": "你在哪儿工作？",              "pinyin": "Nǐ zài nǎr gōngzuò?",                      "translation": "Siz qayerda ishlaysiz?"},
                {"speaker": "B", "zh": "我在学校工作。",              "pinyin": "Wǒ zài xuéxiào gōngzuò.",                  "translation": "Men maktabda ishlayman."},
                {"speaker": "A", "zh": "你儿子在哪儿工作？",          "pinyin": "Nǐ érzi zài nǎr gōngzuò?",                 "translation": "O'g'lingiz qayerda ishlaydi?"},
                {"speaker": "B", "zh": "我儿子在医院工作，他是医生。", "pinyin": "Wǒ érzi zài yīyuàn gōngzuò, tā shì yīshēng.", "translation": "O'g'lim shifoxonada ishlaydi, u shifokor."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Telefonda — ota qayerda",
            "dialogue": [
                {"speaker": "A", "zh": "你爸爸在家吗？",    "pinyin": "Nǐ bàba zài jiā ma?",  "translation": "Otangiz uyda bormi?"},
                {"speaker": "B", "zh": "不在家。",          "pinyin": "Bú zài jiā.",           "translation": "Uyda yo'q."},
                {"speaker": "A", "zh": "他在哪儿呢？",      "pinyin": "Tā zài nǎr ne?",        "translation": "U qayerda?"},
                {"speaker": "B", "zh": "他在医院。",        "pinyin": "Tā zài yīyuàn.",        "translation": "U shifoxonada."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "动词 在 — Fe'l 在 (joylashuv)",
            "explanation": (
                "在(zài) — fe'l sifatida biror narsa qayerda ekanini bildiradi.\n"
                "Tuzilishi: Ega + 在 + Joy\n\n"
                "Misol:\n"
                "小猫在那儿。— Mushukcha u yerda.\n"
                "我朋友在学校。— Do'stim maktabda.\n"
                "我妈妈在家。— Onam uyda.\n\n"
                "Inkor: Ega + 不在 + Joy\n"
                "爸爸不在家。— Ota uyda yo'q."
            ),
            "examples": [
                {"zh": "小猫在那儿。",   "pinyin": "Xiǎo māo zài nàr.",     "meaning": "Mushukcha u yerda."},
                {"zh": "我朋友在学校。", "pinyin": "Wǒ péngyou zài xuéxiào.","meaning": "Do'stim maktabda."},
                {"zh": "爸爸不在家。",   "pinyin": "Bàba bú zài jiā.",      "meaning": "Ota uyda yo'q."},
            ]
        },
        {
            "no": 2,
            "title_zh": "哪儿 — Qayerda so'roq olmoshi",
            "explanation": (
                "哪儿(nǎr) — joy so'rash olmoshi.\n"
                "Tuzilishi: Ega + 在 + 哪儿?\n\n"
                "Misol:\n"
                "小猫在哪儿？— Mushukcha qayerda?\n"
                "你在哪儿工作？— Siz qayerda ishlaysiz?\n"
                "他在哪儿呢？— U qayerda?"
            ),
            "examples": [
                {"zh": "你在哪儿工作？",  "pinyin": "Nǐ zài nǎr gōngzuò?",  "meaning": "Siz qayerda ishlaysiz?"},
                {"zh": "小狗在哪儿？",    "pinyin": "Xiǎo gǒu zài nǎr?",    "meaning": "Kuchukcha qayerda?"},
                {"zh": "他爸爸在哪儿呢？","pinyin": "Tā bàba zài nǎr ne?",   "meaning": "Uning otasi qayerda?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "介词 在 — Predlog 在 (joy bildiradi)",
            "explanation": (
                "在(zài) — predlog sifatida fe'l oldida kelib, harakatning joyi.\n"
                "Tuzilishi: Ega + 在 + Joy + Fe'l\n\n"
                "Misol:\n"
                "我儿子在医院工作。— O'g'lim shifoxonada ishlaydi.\n"
                "他们在学校看书。— Ular maktabda kitob o'qiydi.\n"
                "我在朋友家喝茶。— Men do'stimnikida choy ichyapman.\n\n"
                "Farq:\n"
                "她在医院。(Fe'l 在) — U shifoxonada.\n"
                "她在医院工作。(Predlog 在) — U shifoxonada ishlaydi."
            ),
            "examples": [
                {"zh": "我儿子在医院工作。", "pinyin": "Wǒ érzi zài yīyuàn gōngzuò.",  "meaning": "O'g'lim shifoxonada ishlaydi."},
                {"zh": "他们在学校看书。",   "pinyin": "Tāmen zài xuéxiào kàn shū.",   "meaning": "Ular maktabda kitob o'qiydi."},
                {"zh": "我在家喝茶。",       "pinyin": "Wǒ zài jiā hē chá.",           "meaning": "Men uyda choy ichyapman."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Mushukcha qayerda?",                       "answer": "小猫在哪儿？",               "pinyin": "Xiǎo māo zài nǎr?"},
                {"prompt": "Kuchukcha stul tagida.",                    "answer": "小狗在椅子下面。",           "pinyin": "Xiǎo gǒu zài yǐzi xiàmian."},
                {"prompt": "Siz qayerda ishlaysiz?",                   "answer": "你在哪儿工作？",             "pinyin": "Nǐ zài nǎr gōngzuò?"},
                {"prompt": "O'g'lim shifoxonada ishlaydi.",            "answer": "我儿子在医院工作。",         "pinyin": "Wǒ érzi zài yīyuàn gōngzuò."},
                {"prompt": "Otangiz uyda bormi?",                      "answer": "你爸爸在家吗？",             "pinyin": "Nǐ bàba zài jiā ma?"},
                {"prompt": "Uyda yo'q, u shifoxonada.",                "answer": "不在家，他在医院。",         "pinyin": "Bú zài jiā, tā zài yīyuàn."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "小猫___那儿。",              "answer": "在",   "pinyin": "zài"},
                {"prompt": "你___哪儿工作？",            "answer": "在",   "pinyin": "zài"},
                {"prompt": "小狗在椅子___面。",          "answer": "下",   "pinyin": "xià"},
                {"prompt": "我儿子在医院___，他是医生。", "answer": "工作", "pinyin": "gōngzuò"},
            ]
        },
        {
            "no": 3,
            "type": "make_sentence",
            "instruction": "Berilgan so'zlardan gap tuzing:",
            "items": [
                {"words": ["在", "医院", "工作", "我妈妈"],        "answer": "我妈妈在医院工作。",  "pinyin": "Wǒ māma zài yīyuàn gōngzuò."},
                {"words": ["哪儿", "在", "小猫", "？"],            "answer": "小猫在哪儿？",        "pinyin": "Xiǎo māo zài nǎr?"},
                {"words": ["在", "家", "不", "爸爸"],              "answer": "爸爸不在家。",        "pinyin": "Bàba bú zài jiā."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["小猫在哪儿？", "小狗在椅子下面。", "你在哪儿工作？", "我儿子在医院工作。", "你爸爸在家吗？", "不在家，他在医院。"]},
        {"no": 2, "answers": ["在", "在", "下", "工作"]},
        {"no": 3, "answers": ["我妈妈在医院工作。", "小猫在哪儿？", "爸爸不在家。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Oila a'zolaringiz haqida 4 ta gap yozing (qayerda ishlaydi/bor):",
            "template": "我___在___工作/在___。",
            "words": ["在", "工作", "医院", "学校", "家", "商店"],
        },
        {
            "no": 2,
            "instruction": "Savollarga javob bering:",
            "items": [
                {"prompt": "你在哪儿工作/学习？",  "hint": "Siz qayerda ishlaysiz/o'qiysiz?"},
                {"prompt": "你爸爸在哪儿工作？",   "hint": "Otangiz qayerda ishlaydi?"},
                {"prompt": "你现在在哪儿？",        "hint": "Hozir qayerdasiz?"},
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
