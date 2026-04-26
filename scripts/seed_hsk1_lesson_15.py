import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 15,
    "lesson_code": "HSK1-L15",
    "title": "我是坐飞机来的",
    "goal": "是……的 konstruktsiyasi — vaqt, joy va usulni ta'kidlash",
    "intro_text": (
        "O'n beshinchi — oxirgi darsda siz 是……的 konstruktsiyasi bilan "
        "qachon, qayerda va qanday usulda biror ish qilinganini ta'kidlashni o'rganasiz. "
        "9 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "认识",  "pinyin": "rènshi",   "pos": "v.",   "meaning": "tanishmoq, bilmoq"},
        {"no": 2, "zh": "年",    "pinyin": "nián",     "pos": "n.",   "meaning": "yil"},
        {"no": 3, "zh": "大学",  "pinyin": "dàxué",    "pos": "n.",   "meaning": "universitet, oliy maktab"},
        {"no": 4, "zh": "饭店",  "pinyin": "fàndiàn",  "pos": "n.",   "meaning": "restoran, mehmonxona"},
        {"no": 5, "zh": "出租车","pinyin": "chūzūchē", "pos": "n.",   "meaning": "taksi"},
        {"no": 6, "zh": "一起",  "pinyin": "yīqǐ",     "pos": "adv.", "meaning": "birga, birgalikda"},
        {"no": 7, "zh": "高兴",  "pinyin": "gāoxìng",  "pos": "adj.", "meaning": "xursand, shod"},
        {"no": 8, "zh": "听",    "pinyin": "tīng",     "pos": "v.",   "meaning": "tinglash, eshitmoq"},
        {"no": 9, "zh": "飞机",  "pinyin": "fēijī",    "pos": "n.",   "meaning": "samolyot"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Dasturxon yonida — qachon va qayerda tanishdingiz",
            "dialogue": [
                {"speaker": "A", "zh": "你和李小姐是什么时候认识的？",    "pinyin": "Nǐ hé Lǐ xiǎojiě shì shénme shíhou rènshi de?",    "translation": "Siz Li xonim bilan qachon tanishgansiz?"},
                {"speaker": "B", "zh": "我们是2011年9月认识的。",        "pinyin": "Wǒmen shì èr líng yī yī nián jiǔ yuè rènshi de.",  "translation": "Biz 2011 yil sentabrda tanishganmiz."},
                {"speaker": "A", "zh": "你们在哪儿认识的？",             "pinyin": "Nǐmen zài nǎr rènshi de?",                         "translation": "Qayerda tanishgansizlar?"},
                {"speaker": "B", "zh": "我们是在学校认识的，她是我大学同学。","pinyin": "Wǒmen shì zài xuéxiào rènshi de, tā shì wǒ dàxué tóngxué.", "translation": "Universitetda tanishganmiz, u universitetdagi sinfdoshim."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Mehmonxona oldida — qanday keldingiz",
            "dialogue": [
                {"speaker": "A", "zh": "你们是怎么来饭店的？",          "pinyin": "Nǐmen shì zěnme lái fàndiàn de?",                "translation": "Siz restoraniga qanday keldingiz?"},
                {"speaker": "B", "zh": "我们是坐出租车来的。",          "pinyin": "Wǒmen shì zuò chūzūchē lái de.",               "translation": "Biz taksi bilan keldik."},
                {"speaker": "A", "zh": "李先生呢？",                    "pinyin": "Lǐ xiānsheng ne?",                             "translation": "Li janob-chi?"},
                {"speaker": "B", "zh": "他是和朋友一起开车来的。",      "pinyin": "Tā shì hé péngyou yīqǐ kāi chē lái de.",       "translation": "U do'sti bilan birga mashinada keldi."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Kompaniyada — samolyot bilan kelding",
            "dialogue": [
                {"speaker": "A", "zh": "很高兴认识您！李小姐。",          "pinyin": "Hěn gāoxìng rènshi nín! Lǐ xiǎojiě.",          "translation": "Siz bilan tanishganimdan juda xursandman! Li xonim."},
                {"speaker": "B", "zh": "认识你我也很高兴！",             "pinyin": "Rènshi nǐ wǒ yě hěn gāoxìng!",                "translation": "Men ham siz bilan tanishganimdan xursandman!"},
                {"speaker": "A", "zh": "听张先生说，您是坐飞机来北京的？","pinyin": "Tīng Zhāng xiānsheng shuō, nín shì zuò fēijī lái Běijīng de?", "translation": "Zhang janob aytdilar, siz Pekinga samolyotda keldingizmi?"},
                {"speaker": "B", "zh": "是的。",                        "pinyin": "Shì de.",                                      "translation": "Ha, to'g'ri."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "是……的 — Vaqt, joy va usulni ta'kidlash",
            "explanation": (
                "是……的 konstruktsiyasi allaqachon sodir bo'lgan harakatning "
                "vaqtini, joyini yoki usulini ta'kidlash uchun ishlatiladi.\n\n"
                "Tuzilishi:\n"
                "Ega + 是 + [Vaqt/Joy/Usul] + Fe'l + 的\n\n"
                "Vaqtni ta'kidlash:\n"
                "我们是2011年认识的。— Biz 2011 yilda tanishdik.\n\n"
                "Joyni ta'kidlash:\n"
                "我们是在学校认识的。— Biz universitetda tanishdik.\n\n"
                "Usulni ta'kidlash:\n"
                "我是坐飞机来的。— Men samolyotda keldim.\n\n"
                "Inkor: 不是……的\n"
                "我不是坐出租车来的。— Men taksi bilan kelmadim."
            ),
            "examples": [
                {"zh": "我们是2011年认识的。",   "pinyin": "Wǒmen shì èr líng yī yī nián rènshi de.",   "meaning": "Biz 2011 yilda tanishdik."},
                {"zh": "我是坐飞机来的。",        "pinyin": "Wǒ shì zuò fēijī lái de.",                 "meaning": "Men samolyotda keldim."},
                {"zh": "她是在北京买的。",        "pinyin": "Tā shì zài Běijīng mǎi de.",               "meaning": "U Pekinda sotib oldi."},
                {"zh": "我们不是坐出租车来的。",  "pinyin": "Wǒmen bú shì zuò chūzūchē lái de.",        "meaning": "Biz taksi bilan kelmadik."},
            ]
        },
        {
            "no": 2,
            "title_zh": "日期的表达(2) — To'liq sana ifodalash",
            "explanation": (
                "Xitoy tilida to'liq sana kattadan kichikka:\n"
                "Yil + Oy + Kun + Hafta kuni\n\n"
                "Yilni o'qish: har raqam alohida o'qiladi\n"
                "2011 → 二零一一年 (èr líng yī yī nián)\n"
                "2024 → 二零二四年 (èr líng èr sì nián)\n\n"
                "To'liq misol:\n"
                "2011年9月10号，星期三\n"
                "Ikki ming o'n bir yil, to'qqizinchi oy, o'ninchi kun, chorshanba"
            ),
            "examples": [
                {"zh": "2011年9月认识的",     "pinyin": "èr líng yī yī nián jiǔ yuè rènshi de", "meaning": "2011 yil sentabrda tanishgan"},
                {"zh": "今天是2024年4月26号。","pinyin": "Jīntiān shì èr líng èr sì nián sì yuè èrshíliù hào.", "meaning": "Bugun 2024 yil 26 aprel."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing (是……的 ishlatib):",
            "items": [
                {"prompt": "Biz 2011 yilda tanishdik.",          "answer": "我们是2011年认识的。",       "pinyin": "Wǒmen shì èr líng yī yī nián rènshi de."},
                {"prompt": "Men samolyotda keldim.",              "answer": "我是坐飞机来的。",           "pinyin": "Wǒ shì zuò fēijī lái de."},
                {"prompt": "Siz restoraniga qanday keldingiz?",  "answer": "你是怎么来饭店的？",         "pinyin": "Nǐ shì zěnme lái fàndiàn de?"},
                {"prompt": "Biz taksi bilan keldik.",             "answer": "我们是坐出租车来的。",       "pinyin": "Wǒmen shì zuò chūzūchē lái de."},
                {"prompt": "U do'sti bilan birga keldi.",         "answer": "他是和朋友一起来的。",       "pinyin": "Tā shì hé péngyou yīqǐ lái de."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "你们___什么时候认识的？",    "answer": "是",   "pinyin": "shì"},
                {"prompt": "我是坐飞机来___。",          "answer": "的",   "pinyin": "de"},
                {"prompt": "他们是___学校认识的。",      "answer": "在",   "pinyin": "zài"},
                {"prompt": "我不___坐出租车来的。",      "answer": "是",   "pinyin": "shì"},
            ]
        },
        {
            "no": 3,
            "type": "emphasis",
            "instruction": "是……的 ishlatib ta'kidlang:",
            "items": [
                {"prompt": "我坐飞机来。(usul ta'kidlash)",      "answer": "我是坐飞机来的。",         "pinyin": "Wǒ shì zuò fēijī lái de."},
                {"prompt": "他们在北京认识。(joy ta'kidlash)",   "answer": "他们是在北京认识的。",     "pinyin": "Tāmen shì zài Běijīng rènshi de."},
                {"prompt": "我2011年来中国。(vaqt ta'kidlash)",  "answer": "我是2011年来中国的。",     "pinyin": "Wǒ shì èr líng yī yī nián lái Zhōngguó de."},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["我们是2011年认识的。", "我是坐飞机来的。", "你是怎么来饭店的？", "我们是坐出租车来的。", "他是和朋友一起来的。"]},
        {"no": 2, "answers": ["是", "的", "在", "是"]},
        {"no": 3, "answers": ["我是坐飞机来的。", "他们是在北京认识的。", "我是2011年来中国的。"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "O'zingiz haqida 是……的 ishlatib 4 ta gap yozing:",
            "template": "我是___年___的。我是在___认识___的。我是坐___来___的。",
            "words": ["是", "的", "在", "年", "坐", "飞机", "出租车", "认识"],
        },
        {
            "no": 2,
            "instruction": "Do'stingiz haqida savol bering (是……的 ishlatib):",
            "items": [
                {"prompt": "Qachon tanishgansizlar?",     "example": "你们是什么时候认识的？"},
                {"prompt": "Qayerda tanishgansizlar?",    "example": "你们是在哪儿认识的？"},
                {"prompt": "U qanday keldi?",             "example": "他是怎么来的？"},
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
