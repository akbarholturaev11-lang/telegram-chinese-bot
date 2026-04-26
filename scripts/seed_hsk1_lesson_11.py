import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 11,
    "lesson_code": "HSK1-L11",
    "title": "现在几点",
    "goal": "Vaqtni aytish va so'rash, vaqt ravishi va 前 so'zi",
    "intro_text": (
        "O'n birinchi darsda siz soatni aytishni, "
        "vaqt ravishlarini ishlatishni va 前 so'zi bilan vaqtni ifodalashni o'rganasiz. "
        "11 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "现在", "pinyin": "xiànzài",  "pos": "n.",   "meaning": "hozir, hozirgi vaqtda"},
        {"no": 2,  "zh": "点",   "pinyin": "diǎn",     "pos": "m.",   "meaning": "soat (o'lchov so'z)"},
        {"no": 3,  "zh": "分",   "pinyin": "fēn",      "pos": "m.",   "meaning": "daqiqa"},
        {"no": 4,  "zh": "中午", "pinyin": "zhōngwǔ",  "pos": "n.",   "meaning": "tush vaqti, peshin"},
        {"no": 5,  "zh": "吃饭", "pinyin": "chī fàn",  "pos": "v.",   "meaning": "ovqat yemoq"},
        {"no": 6,  "zh": "时候", "pinyin": "shíhou",   "pos": "n.",   "meaning": "vaqt, payt"},
        {"no": 7,  "zh": "回",   "pinyin": "huí",      "pos": "v.",   "meaning": "qaytmoq, qaytib kelmoq"},
        {"no": 8,  "zh": "我们", "pinyin": "wǒmen",    "pos": "pron.","meaning": "biz"},
        {"no": 9,  "zh": "电影", "pinyin": "diànyǐng", "pos": "n.",   "meaning": "kino, film"},
        {"no": 10, "zh": "住",   "pinyin": "zhù",      "pos": "v.",   "meaning": "yashaymoq, turmoq"},
        {"no": 11, "zh": "前",   "pinyin": "qián",     "pos": "n.",   "meaning": "oldin, -dan avval"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Kutubxonada — soat so'rash",
            "dialogue": [
                {"speaker": "A", "zh": "现在几点？",    "pinyin": "Xiànzài jǐ diǎn?",     "translation": "Hozir soat necha?"},
                {"speaker": "B", "zh": "现在十点十分。", "pinyin": "Xiànzài shí diǎn shí fēn.", "translation": "Hozir soat o'n o'n daqiqa."},
                {"speaker": "A", "zh": "中午几点吃饭？", "pinyin": "Zhōngwǔ jǐ diǎn chī fàn?",  "translation": "Tushda soat nechada ovqatlanasiz?"},
                {"speaker": "B", "zh": "十二点吃饭。",  "pinyin": "Shí'èr diǎn chī fàn.",  "translation": "Soat o'n ikkida ovqatlanamiz."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Uyda — otani kutish",
            "dialogue": [
                {"speaker": "A", "zh": "爸爸什么时候回家？",   "pinyin": "Bàba shénme shíhou huí jiā?",        "translation": "Ota qachon uyga qaytadi?"},
                {"speaker": "B", "zh": "下午五点。",           "pinyin": "Xiàwǔ wǔ diǎn.",                    "translation": "Tushdan keyin soat beshda."},
                {"speaker": "A", "zh": "我们什么时候去看电影？","pinyin": "Wǒmen shénme shíhou qù kàn diànyǐng?","translation": "Biz qachon kino ko'rgani boramiz?"},
                {"speaker": "B", "zh": "六点三十分。",         "pinyin": "Liù diǎn sānshí fēn.",              "translation": "Soat olti o'ttizda."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Uyda — Pekin safari rejasi",
            "dialogue": [
                {"speaker": "A", "zh": "我星期一去北京。",          "pinyin": "Wǒ xīngqī yī qù Běijīng.",              "translation": "Men dushanbada Pekinga boraman."},
                {"speaker": "B", "zh": "你想在北京住几天？",        "pinyin": "Nǐ xiǎng zài Běijīng zhù jǐ tiān?",     "translation": "Pekinda necha kun yashay deb o'ylayapsiz?"},
                {"speaker": "A", "zh": "住三天。",                  "pinyin": "Zhù sān tiān.",                         "translation": "Uch kun."},
                {"speaker": "B", "zh": "星期五前能回家吗？",        "pinyin": "Xīngqī wǔ qián néng huí jiā ma?",       "translation": "Jumadan oldin uyga qayta olasizmi?"},
                {"speaker": "A", "zh": "能。",                      "pinyin": "Néng.",                                 "translation": "Ha, olaman."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "时间的表达 — Vaqtni ifodalash",
            "explanation": (
                "Soat: 点(diǎn)\n"
                "Daqiqa: 分(fēn)\n"
                "Tuzilishi: N点 yoki N点M分\n\n"
                "9:00 → 九点\n"
                "10:10 → 十点十分\n"
                "5:30 → 五点三十分\n"
                "2:05 → 两点零五分\n\n"
                "Kun qismlari:\n"
                "上午 shàngwǔ — ertalab (AM)\n"
                "中午 zhōngwǔ — tush\n"
                "下午 xiàwǔ — tushdan keyin (PM)\n\n"
                "2:00 → 两点 (liǎng diǎn), 二点 emas!"
            ),
            "examples": [
                {"zh": "现在九点。",       "pinyin": "Xiànzài jiǔ diǎn.",          "meaning": "Hozir soat to'qqiz."},
                {"zh": "下午三点十分。",   "pinyin": "Xiàwǔ sān diǎn shí fēn.",   "meaning": "Tushdan keyin soat uch o'n daqiqa."},
                {"zh": "上午两点半。",     "pinyin": "Shàngwǔ liǎng diǎn bàn.",   "meaning": "Ertalab soat ikki yarim."},
            ]
        },
        {
            "no": 2,
            "title_zh": "时间词做状语 — Vaqt ravishi",
            "explanation": (
                "Vaqt so'zi gap ichida ravish bo'la oladi.\n"
                "Odatda ega dan keyin yoki ega dan oldin keladi.\n\n"
                "Tuzilishi 1: Ega + Vaqt + Fe'l\n"
                "妈妈六点做饭。— Ona soat oltida ovqat tayyorlaydi.\n\n"
                "Tuzilishi 2: Vaqt + Ega + Fe'l\n"
                "中午十二点我们吃饭。— Tush soat o'n ikkida ovqatlanamiz.\n\n"
                "So'roq: 什么时候 — qachon?"
            ),
            "examples": [
                {"zh": "他们六点吃饭。",       "pinyin": "Tāmen liù diǎn chī fàn.",     "meaning": "Ular soat oltida ovqatlanadi."},
                {"zh": "我星期一去北京。",     "pinyin": "Wǒ xīngqī yī qù Běijīng.",   "meaning": "Men dushanbada Pekinga boraman."},
                {"zh": "你什么时候回家？",     "pinyin": "Nǐ shénme shíhou huí jiā?",  "meaning": "Qachon uyga qaytasiz?"},
            ]
        },
        {
            "no": 3,
            "title_zh": "名词 前 — 前 vaqt belgisi",
            "explanation": (
                "前(qián) — biror vaqtdan oldingi paytni bildiradi.\n\n"
                "三天前 — uch kun oldin\n"
                "一个星期前 — bir hafta oldin\n"
                "四点前 — soat to'rtdan oldin\n"
                "星期五前 — jumadan oldin\n\n"
                "Misol:\n"
                "星期五前能回家吗？— Jumadan oldin uyga qayta olasizmi?\n"
                "八点前去学校。— Soat sakkizdan oldin maktabga bor."
            ),
            "examples": [
                {"zh": "星期五前能回家吗？", "pinyin": "Xīngqī wǔ qián néng huí jiā ma?", "meaning": "Jumadan oldin uyga qayta olasizmi?"},
                {"zh": "三天前我在北京。",   "pinyin": "Sān tiān qián wǒ zài Běijīng.",   "meaning": "Uch kun oldin men Pekinda edim."},
                {"zh": "八点前来。",         "pinyin": "Bā diǎn qián lái.",               "meaning": "Soat sakkizdan oldin kel."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "time_writing",
            "instruction": "Vaqtni xitoycha yozing:",
            "items": [
                {"prompt": "9:00",          "answer": "九点",         "pinyin": "jiǔ diǎn"},
                {"prompt": "2:00",          "answer": "两点",         "pinyin": "liǎng diǎn"},
                {"prompt": "10:10",         "answer": "十点十分",     "pinyin": "shí diǎn shí fēn"},
                {"prompt": "6:30",          "answer": "六点三十分",   "pinyin": "liù diǎn sānshí fēn"},
                {"prompt": "PM 3:15",       "answer": "下午三点十五分","pinyin": "xiàwǔ sān diǎn shíwǔ fēn"},
            ]
        },
        {
            "no": 2,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Hozir soat necha?",              "answer": "现在几点？",           "pinyin": "Xiànzài jǐ diǎn?"},
                {"prompt": "Biz qachon kino ko'rgani boramiz?","answer": "我们什么时候去看电影？","pinyin": "Wǒmen shénme shíhou qù kàn diànyǐng?"},
                {"prompt": "Jumadan oldin uyga qayta olasizmi?","answer": "星期五前能回家吗？", "pinyin": "Xīngqī wǔ qián néng huí jiā ma?"},
                {"prompt": "Men Pekinda uch kun yashayman.",  "answer": "我在北京住三天。",     "pinyin": "Wǒ zài Běijīng zhù sān tiān."},
            ]
        },
        {
            "no": 3,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "现在___点___分？",           "answer": "几/几",    "pinyin": "jǐ/jǐ"},
                {"prompt": "爸爸什么___回家？",          "answer": "时候",     "pinyin": "shíhou"},
                {"prompt": "星期五___能回家吗？",        "answer": "前",       "pinyin": "qián"},
                {"prompt": "我___一去北京。",            "answer": "星期",     "pinyin": "xīngqī"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["九点", "两点", "十点十分", "六点三十分", "下午三点十五分"]},
        {"no": 2, "answers": ["现在几点？", "我们什么时候去看电影？", "星期五前能回家吗？", "我在北京住三天。"]},
        {"no": 3, "answers": ["几/几", "时候", "前", "星期"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Bugungi kun jadvalingizni yozing (vaqt + harakat):",
            "template": "上午___点我___。中午___点我___。下午___点我___。",
            "words": ["点", "分", "吃饭", "去", "回家", "看书", "工作"],
        },
        {
            "no": 2,
            "instruction": "Savollarga javob bering:",
            "items": [
                {"prompt": "现在几点？",           "hint": "Hozirgi vaqtni ayting"},
                {"prompt": "你几点吃饭？",         "hint": "Qaysi soatda ovqatlanasiz?"},
                {"prompt": "你什么时候回家？",     "hint": "Qachon uyga qaytasiz?"},
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
