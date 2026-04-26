import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 10,
    "lesson_code": "HSK1-L10",
    "title": "我能坐这儿吗",
    "goal": "Joylashuv bildirish, 有-gaplar, 能 modal fe'li va 和 bog'lovchisi",
    "intro_text": (
        "O'ninchi darsda siz narsalar qayerda ekanini aytishni, "
        "有 bilan mavjudlikni bildirish, 能 modal fe'li va 和 bog'lovchisini o'rganasiz. "
        "12 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "桌子", "pinyin": "zhuōzi",   "pos": "n.",   "meaning": "stol, parta"},
        {"no": 2,  "zh": "上",   "pinyin": "shàng",    "pos": "n.",   "meaning": "ustida, yuqorida"},
        {"no": 3,  "zh": "电脑", "pinyin": "diànnǎo",  "pos": "n.",   "meaning": "kompyuter"},
        {"no": 4,  "zh": "和",   "pinyin": "hé",       "pos": "conj.","meaning": "va, bilan"},
        {"no": 5,  "zh": "本",   "pinyin": "běn",      "pos": "m.",   "meaning": "kitob uchun o'lchov so'z"},
        {"no": 6,  "zh": "里",   "pinyin": "lǐ",       "pos": "n.",   "meaning": "ichida, -ning ichida"},
        {"no": 7,  "zh": "前面", "pinyin": "qiánmiàn", "pos": "n.",   "meaning": "old tomon, oldida"},
        {"no": 8,  "zh": "后面", "pinyin": "hòumiàn",  "pos": "n.",   "meaning": "orqa tomon, orqasida"},
        {"no": 9,  "zh": "这儿", "pinyin": "zhèr",     "pos": "pron.","meaning": "bu yerda, shu yerda"},
        {"no": 10, "zh": "没有", "pinyin": "méiyǒu",   "pos": "adv.", "meaning": "yo'q, mavjud emas"},
        {"no": 11, "zh": "能",   "pinyin": "néng",     "pos": "mod.", "meaning": "mumkin, qodir (imkoniyat)"},
        {"no": 12, "zh": "坐",   "pinyin": "zuò",      "pos": "v.",   "meaning": "o'tirmoq"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Ofisda — stol ustida nima bor",
            "dialogue": [
                {"speaker": "A", "zh": "桌子上有什么？",           "pinyin": "Zhuōzi shàng yǒu shénme?",          "translation": "Stol ustida nima bor?"},
                {"speaker": "B", "zh": "桌子上有一个电脑和一本书。", "pinyin": "Zhuōzi shàng yǒu yī gè diànnǎo hé yī běn shū.", "translation": "Stol ustida bitta kompyuter va bitta kitob bor."},
                {"speaker": "A", "zh": "杯子在哪儿？",             "pinyin": "Bēizi zài nǎr?",                    "translation": "Piyola qayerda?"},
                {"speaker": "B", "zh": "杯子在桌子里。",           "pinyin": "Bēizi zài zhuōzi lǐ.",             "translation": "Piyola stol ichida."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Sport zalda — oldida va orqasida kim",
            "dialogue": [
                {"speaker": "A", "zh": "前面那个人叫什么名字？",         "pinyin": "Qiánmiàn nàge rén jiào shénme míngzi?",     "translation": "Oldidagi odam ismi nima?"},
                {"speaker": "B", "zh": "她叫王方，在医院工作。",         "pinyin": "Tā jiào Wáng Fāng, zài yīyuàn gōngzuò.",   "translation": "Uning ismi Van Fan, shifoxonada ishlaydi."},
                {"speaker": "A", "zh": "后面那个人呢？他叫什么名字？",   "pinyin": "Hòumiàn nàge rén ne? Tā jiào shénme míngzi?", "translation": "Orqasidagi odam-chi? Ismi nima?"},
                {"speaker": "B", "zh": "他叫谢朋，在商店工作。",         "pinyin": "Tā jiào Xiè Péng, zài shāngdiàn gōngzuò.", "translation": "Uning ismi Xie Pen, do'konda ishlaydi."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kutubxonada — o'tirish so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "这儿有人吗？",   "pinyin": "Zhèr yǒu rén ma?",   "translation": "Bu yerda odam bormi?"},
                {"speaker": "B", "zh": "没有。",         "pinyin": "Méiyǒu.",             "translation": "Yo'q."},
                {"speaker": "A", "zh": "我能坐这儿吗？", "pinyin": "Wǒ néng zuò zhèr ma?","translation": "Bu yerga o'tirsam bo'ladimi?"},
                {"speaker": "B", "zh": "请坐。",         "pinyin": "Qǐng zuò.",           "translation": "Marhamat, o'tiring."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "有字句 — 有 gapi (mavjudlik)",
            "explanation": (
                "有(yǒu) — biror joyda narsa/odam borligini bildiradi.\n"
                "Tuzilishi: Joy + 有 + Narsa/Odam\n\n"
                "Misol:\n"
                "桌子上有一个电脑。— Stol ustida bitta kompyuter bor.\n"
                "学校里有一个商店。— Maktabda bitta do'kon bor.\n\n"
                "Inkor: 没有 (méiyǒu)\n"
                "椅子下面没有小狗。— Stul tagida kuchuk yo'q.\n"
                "这儿有人吗？ — 没有。— Bu yerda odam bormi? — Yo'q."
            ),
            "examples": [
                {"zh": "桌子上有一个电脑。",   "pinyin": "Zhuōzi shàng yǒu yī gè diànnǎo.",  "meaning": "Stol ustida bitta kompyuter bor."},
                {"zh": "学校里没有商店。",     "pinyin": "Xuéxiào lǐ méiyǒu shāngdiàn.",     "meaning": "Maktabda do'kon yo'q."},
                {"zh": "这儿有人吗？",         "pinyin": "Zhèr yǒu rén ma?",                 "meaning": "Bu yerda odam bormi?"},
            ]
        },
        {
            "no": 2,
            "title_zh": "连词 和 — Bog'lovchi 和",
            "explanation": (
                "和(hé) — ikkita ot yoki olmoshni bog'laydi ('va', 'bilan').\n"
                "Tuzilishi: Ot1 + 和 + Ot2\n\n"
                "Misol:\n"
                "一个电脑和一本书 — bitta kompyuter va bitta kitob\n"
                "爸爸和妈妈 — ota va ona\n"
                "我有一个中国朋友和一个美国朋友。\n\n"
                "Eslatma: 和 faqat ot va olmoshlarni bog'laydi,\n"
                "fe'l va gaplarni bog'lamaydi."
            ),
            "examples": [
                {"zh": "电脑和书",               "pinyin": "diànnǎo hé shū",          "meaning": "kompyuter va kitob"},
                {"zh": "爸爸和妈妈",             "pinyin": "bàba hé māma",             "meaning": "ota va ona"},
                {"zh": "我有一个中国朋友和一个美国朋友。", "pinyin": "Wǒ yǒu yī gè Zhōngguó péngyou hé yī gè Měiguó péngyou.", "meaning": "Mening bitta xitoylik va bitta amerikalik do'stim bor."},
            ]
        },
        {
            "no": 3,
            "title_zh": "能愿动词 能 — Modal fe'l 能",
            "explanation": (
                "能(néng) — imkoniyat yoki ruxsat bildiradi.\n"
                "Tuzilishi: Ega + 能 + Fe'l\n\n"
                "Misol:\n"
                "我能坐这儿吗？— Bu yerga o'tirsam bo'ladimi?\n"
                "你能在这儿写名字吗？— Bu yerga ismingizni yozsa bo'ladimi?\n\n"
                "能 vs 会:\n"
                "会 — o'rganib qodir bo'lmoq (skill)\n"
                "能 — imkoniyat/ruxsat (can/may)"
            ),
            "examples": [
                {"zh": "我能坐这儿吗？",       "pinyin": "Wǒ néng zuò zhèr ma?",       "meaning": "Bu yerga o'tirsam bo'ladimi?"},
                {"zh": "你能在这儿工作吗？",   "pinyin": "Nǐ néng zài zhèr gōngzuò ma?","meaning": "Bu yerda ishlay olasizmi?"},
                {"zh": "明天你能去商店吗？",   "pinyin": "Míngtiān nǐ néng qù shāngdiàn ma?","meaning": "Ertaga do'konga bora olasizmi?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Stol ustida nima bor?",                "answer": "桌子上有什么？",             "pinyin": "Zhuōzi shàng yǒu shénme?"},
                {"prompt": "Stol ustida kitob va kompyuter bor.",  "answer": "桌子上有一本书和一个电脑。", "pinyin": "Zhuōzi shàng yǒu yī běn shū hé yī gè diànnǎo."},
                {"prompt": "Bu yerda odam bormi?",                 "answer": "这儿有人吗？",               "pinyin": "Zhèr yǒu rén ma?"},
                {"prompt": "Bu yerga o'tirsam bo'ladimi?",         "answer": "我能坐这儿吗？",             "pinyin": "Wǒ néng zuò zhèr ma?"},
                {"prompt": "Marhamat, o'tiring.",                  "answer": "请坐。",                     "pinyin": "Qǐng zuò."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "桌子上___一个电脑和一本书。", "answer": "有",   "pinyin": "yǒu"},
                {"prompt": "这儿有人吗？___。",          "answer": "没有", "pinyin": "méiyǒu"},
                {"prompt": "我___坐这儿吗？",             "answer": "能",   "pinyin": "néng"},
                {"prompt": "桌子上有电脑___书。",         "answer": "和",   "pinyin": "hé"},
            ]
        },
        {
            "no": 3,
            "type": "location",
            "instruction": "Qayerda ekanini ayting (上/里/下面/前面/后面):",
            "items": [
                {"prompt": "Kitob — stol ustida",       "answer": "书在桌子上。",     "pinyin": "Shū zài zhuōzi shàng."},
                {"prompt": "Kuchuk — stul tagida",      "answer": "狗在椅子下面。",  "pinyin": "Gǒu zài yǐzi xiàmian."},
                {"prompt": "Kompyuter — stol ichida",   "answer": "电脑在桌子里。",  "pinyin": "Diànnǎo zài zhuōzi lǐ."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["桌子上有什么？", "桌子上有一本书和一个电脑。", "这儿有人吗？", "我能坐这儿吗？", "请坐。"]},
        {"no": 2, "answers": ["有", "没有", "能", "和"]},
        {"no": 3, "answers": ["书在桌子上。", "狗在椅子下面。", "电脑在桌子里。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "O'z xonangiz haqida 4 ta gap yozing (有 ishlatib):",
            "template": "我的桌子上有___。桌子里有___。椅子___有___。",
            "words": ["有", "没有", "上", "里", "下面", "电脑", "书", "杯子"],
        },
        {
            "no": 2,
            "instruction": "能 bilan 3 ta so'roq tuzing va javob bering:",
            "example": "A: 我能坐这儿吗？ B: 请坐。/ 对不起，不能。",
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
