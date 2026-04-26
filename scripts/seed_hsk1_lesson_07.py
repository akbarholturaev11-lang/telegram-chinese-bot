import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 7,
    "lesson_code": "HSK1-L07",
    "title": "今天几号",
    "goal": "Sana, hafta kunlari va ketma-ket fe'lli gaplarni o'rganish",
    "intro_text": (
        "Yettinchi darsda siz bugungi sanani, hafta kunlarini aytishni "
        "va 去+joy+nima qilish konstruktsiyasini o'rganasiz. "
        "12 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "请",   "pinyin": "qǐng",    "pos": "v.",   "meaning": "iltimos, marhamat qiling"},
        {"no": 2,  "zh": "问",   "pinyin": "wèn",     "pos": "v.",   "meaning": "so'ramoq"},
        {"no": 3,  "zh": "今天", "pinyin": "jīntiān", "pos": "n.",   "meaning": "bugun"},
        {"no": 4,  "zh": "号",   "pinyin": "hào",     "pos": "n.",   "meaning": "sana (oy kuni)"},
        {"no": 5,  "zh": "月",   "pinyin": "yuè",     "pos": "n.",   "meaning": "oy (yanvar, fevral...)"},
        {"no": 6,  "zh": "星期", "pinyin": "xīngqī",  "pos": "n.",   "meaning": "hafta, hafta kuni"},
        {"no": 7,  "zh": "昨天", "pinyin": "zuótiān", "pos": "n.",   "meaning": "kecha"},
        {"no": 8,  "zh": "明天", "pinyin": "míngtiān","pos": "n.",   "meaning": "ertaga"},
        {"no": 9,  "zh": "去",   "pinyin": "qù",      "pos": "v.",   "meaning": "bormoq"},
        {"no": 10, "zh": "学校", "pinyin": "xuéxiào", "pos": "n.",   "meaning": "maktab, o'quv yurti"},
        {"no": 11, "zh": "看",   "pinyin": "kàn",     "pos": "v.",   "meaning": "qaramo, ko'rmoq, o'qimoq"},
        {"no": 12, "zh": "书",   "pinyin": "shū",     "pos": "n.",   "meaning": "kitob"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Bankda — bugungi sana",
            "dialogue": [
                {"speaker": "A", "zh": "请问，今天几号？",  "pinyin": "Qǐngwèn, jīntiān jǐ hào?",  "translation": "Kechirasiz, bugun nechanchi?"},
                {"speaker": "B", "zh": "今天9月1号。",     "pinyin": "Jīntiān jiǔ yuè yī hào.",   "translation": "Bugun 1-sentabr."},
                {"speaker": "A", "zh": "今天星期几？",      "pinyin": "Jīntiān xīngqī jǐ?",        "translation": "Bugun haftaning nechanchi kuni?"},
                {"speaker": "B", "zh": "星期三。",          "pinyin": "Xīngqī sān.",                "translation": "Chorshanba."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Taqvimga qarab — kecha va ertaga",
            "dialogue": [
                {"speaker": "A", "zh": "昨天是几月几号？",         "pinyin": "Zuótiān shì jǐ yuè jǐ hào?",          "translation": "Kecha nechanchi oy, nechanchi kun edi?"},
                {"speaker": "B", "zh": "昨天是8月31号，星期二。",  "pinyin": "Zuótiān shì bā yuè sānshíyī hào, xīngqī èr.", "translation": "Kecha 31-avgust, seshanba edi."},
                {"speaker": "A", "zh": "明天呢？",                 "pinyin": "Míngtiān ne?",                         "translation": "Ertaga-chi?"},
                {"speaker": "B", "zh": "明天是9月2号，星期四。",   "pinyin": "Míngtiān shì jiǔ yuè èr hào, xīngqī sì.", "translation": "Ertaga 2-sentabr, payshanba."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Qahvaxonada — ertangi reja",
            "dialogue": [
                {"speaker": "A", "zh": "明天星期六，你去学校吗？",  "pinyin": "Míngtiān xīngqī liù, nǐ qù xuéxiào ma?", "translation": "Ertaga shanba, maktabga borasizmi?"},
                {"speaker": "B", "zh": "我去学校。",               "pinyin": "Wǒ qù xuéxiào.",                        "translation": "Men maktabga boraman."},
                {"speaker": "A", "zh": "你去学校做什么？",          "pinyin": "Nǐ qù xuéxiào zuò shénme?",            "translation": "Maktabga nima qilgani borasiz?"},
                {"speaker": "B", "zh": "我去学校看书。",            "pinyin": "Wǒ qù xuéxiào kàn shū.",               "translation": "Kitob o'qigani boraman."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "日期的表达 — Sana ifodalash",
            "explanation": (
                "Xitoy tilida sana kattadan kichikka qarab aytiladi:\n"
                "Yil → Oy → Kun → Hafta kuni\n\n"
                "Oy: 一月(yanvar) ~ 十二月(dekabr)\n"
                "Kun: 1号(1-sana) ~ 31号(31-sana)\n\n"
                "Hafta kunlari:\n"
                "星期一 Dushanba\n"
                "星期二 Seshanba\n"
                "星期三 Chorshanba\n"
                "星期四 Payshanba\n"
                "星期五 Juma\n"
                "星期六 Shanba\n"
                "星期日/星期天 Yakshanba\n\n"
                "Misol: 9月1号，星期三 — 1-sentabr, chorshanba"
            ),
            "examples": [
                {"zh": "今天9月1号，星期三。",  "pinyin": "Jīntiān jiǔ yuè yī hào, xīngqī sān.", "meaning": "Bugun 1-sentabr, chorshanba."},
                {"zh": "明天星期六。",          "pinyin": "Míngtiān xīngqī liù.",                "meaning": "Ertaga shanba."},
                {"zh": "昨天8月31号。",         "pinyin": "Zuótiān bā yuè sānshíyī hào.",        "meaning": "Kecha 31-avgust edi."},
            ]
        },
        {
            "no": 2,
            "title_zh": "名词谓语句 — Ot kesimli gap",
            "explanation": (
                "Ot yoki son kesim bo'la oladi (是 shart emas).\n"
                "Ko'pincha yosh, sana, vaqt ifodalashda ishlatiladi.\n\n"
                "Misol:\n"
                "今天9月1号。— Bugun 1-sentabr. (9月1号 — ot kesim)\n"
                "明天星期三。— Ertaga chorshanba.\n"
                "我的汉语老师33岁。— Mening xitoy tili o'qituvchim 33 yoshda."
            ),
            "examples": [
                {"zh": "今天9月1号。",   "pinyin": "Jīntiān jiǔ yuè yī hào.",  "meaning": "Bugun 1-sentabr."},
                {"zh": "明天星期三。",   "pinyin": "Míngtiān xīngqī sān.",     "meaning": "Ertaga chorshanba."},
                {"zh": "她今年二十岁。", "pinyin": "Tā jīnnián èrshí suì.",    "meaning": "U bu yil yigirma yoshda."},
            ]
        },
        {
            "no": 3,
            "title_zh": "连动句 — 去+joy+nima qilish",
            "explanation": (
                "Ketma-ket fe'lli gap: birinchi harakat ikkinchisining maqsadi.\n"
                "Tuzilishi: Ega + 去 + Joy + Fe'l + Narsa\n\n"
                "Misol:\n"
                "我去学校看书。— Kitob o'qigani maktabga boraman.\n"
                "我去中国学习汉语。— Xitoy tilini o'rganishga Xitoyga boraman.\n\n"
                "So'roq: 你去哪儿做什么？— Qayerga nima qilgani borasiz?"
            ),
            "examples": [
                {"zh": "我去学校看书。",     "pinyin": "Wǒ qù xuéxiào kàn shū.",        "meaning": "Kitob o'qigani maktabga boraman."},
                {"zh": "她去学校学汉语。",   "pinyin": "Tā qù xuéxiào xué Hànyǔ.",     "meaning": "Xitoy tilini o'rganishga maktabga boradi."},
                {"zh": "你去哪儿做什么？",   "pinyin": "Nǐ qù nǎr zuò shénme?",        "meaning": "Qayerga nima qilgani borasiz?"},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "date_writing",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "3-mart, dushanba",          "answer": "3月3号，星期一",    "pinyin": "sān yuè sān hào, xīngqī yī"},
                {"prompt": "15-may, juma",              "answer": "5月15号，星期五",   "pinyin": "wǔ yuè shíwǔ hào, xīngqī wǔ"},
                {"prompt": "31-dekabr, yakshanba",      "answer": "12月31号，星期日",  "pinyin": "shí'èr yuè sānshíyī hào, xīngqīrì"},
                {"prompt": "bugun nechanchi?",           "answer": "今天几号？",        "pinyin": "Jīntiān jǐ hào?"},
                {"prompt": "Bugun haftaning nechanchi kuni?", "answer": "今天星期几？", "pinyin": "Jīntiān xīngqī jǐ?"},
            ]
        },
        {
            "no": 2,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Kechirasiz, bugun nechanchi?",         "answer": "请问，今天几号？",   "pinyin": "Qǐngwèn, jīntiān jǐ hào?"},
                {"prompt": "Ertaga shanba, maktabga borasizmi?",   "answer": "明天星期六，你去学校吗？", "pinyin": "Míngtiān xīngqī liù, nǐ qù xuéxiào ma?"},
                {"prompt": "Men kitob o'qigani maktabga boraman.", "answer": "我去学校看书。",      "pinyin": "Wǒ qù xuéxiào kàn shū."},
            ]
        },
        {
            "no": 3,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "今天___月___号，___期___。",        "answer": "sana kiritish kerak", "pinyin": "bugungi sanangizni yozing"},
                {"prompt": "我___学校___书。",                  "answer": "去/看",               "pinyin": "qù/kàn"},
                {"prompt": "___天是9月2号，星期四。",           "answer": "明",                  "pinyin": "míng"},
                {"prompt": "请___，今天星期几？",               "answer": "问",                  "pinyin": "wèn"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["3月3号，星期一", "5月15号，星期五", "12月31号，星期日", "今天几号？", "今天星期几？"]},
        {"no": 2, "answers": ["请问，今天几号？", "明天星期六，你去学校吗？", "我去学校看书。"]},
        {"no": 3, "answers": ["bugungi sana", "去/看", "明", "问"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Bugun, kecha va ertaga sanani yozing:",
            "template": "昨天是___月___号，星期___。今天是___月___号，星期___。明天是___月___号，星期___。",
        },
        {
            "no": 2,
            "instruction": "Ertangi rejangizni yozing (去+joy+nima qilish):",
            "example": "明天我去___。",
            "words": ["去", "学校", "看书", "说汉语", "做中国菜"],
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
