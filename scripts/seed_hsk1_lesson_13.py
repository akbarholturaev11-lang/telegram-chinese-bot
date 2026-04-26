import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 13,
    "lesson_code": "HSK1-L13",
    "title": "他在学做中国菜呢",
    "goal": "Hozir bajariladigan harakatni ifodalash (在...呢), telefon raqamlari",
    "intro_text": (
        "O'n uchinchi darsda siz hozirgi vaqtda bajariladigan harakatni, "
        "在...呢 konstruktsiyasini va 吧 yuklamasini o'rganasiz. "
        "10 ta yangi so'z, 3 ta dialog."
    ),
    "vocabulary_json": json.dumps([
        {"no": 1,  "zh": "喂",   "pinyin": "wèi",      "pos": "int.", "meaning": "allo (telefonda)"},
        {"no": 2,  "zh": "也",   "pinyin": "yě",       "pos": "adv.", "meaning": "ham, shuningdek"},
        {"no": 3,  "zh": "学习", "pinyin": "xuéxí",    "pos": "v.",   "meaning": "o'rganmoq, o'qimoq"},
        {"no": 4,  "zh": "上午", "pinyin": "shàngwǔ",  "pos": "n.",   "meaning": "ertalab (tushdan oldin)"},
        {"no": 5,  "zh": "睡觉", "pinyin": "shuì jiào","pos": "v.",   "meaning": "uxlamoq"},
        {"no": 6,  "zh": "电视", "pinyin": "diànshì",  "pos": "n.",   "meaning": "televizor"},
        {"no": 7,  "zh": "喜欢", "pinyin": "xǐhuan",   "pos": "v.",   "meaning": "yoqtirmoq, yaxshi ko'rmoq"},
        {"no": 8,  "zh": "给",   "pinyin": "gěi",      "pos": "prep.","meaning": "-ga, uchun (kimgadir)"},
        {"no": 9,  "zh": "打电话","pinyin": "dǎ diànhuà","pos": "v.",  "meaning": "telefon qilmoq"},
        {"no": 10, "zh": "吧",   "pinyin": "ba",       "pos": "part.","meaning": "taklif/buyruq yumshatuvchi yukla"},
    ], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "Telefonda — hozir nima qilyapsan",
            "dialogue": [
                {"speaker": "A", "zh": "喂，你在做什么呢？",              "pinyin": "Wèi, nǐ zài zuò shénme ne?",                    "translation": "Allo, hozir nima qilyapsan?"},
                {"speaker": "B", "zh": "我在看书呢。",                    "pinyin": "Wǒ zài kàn shū ne.",                            "translation": "Hozir kitob o'qiyapman."},
                {"speaker": "A", "zh": "大卫也在看书吗？",                "pinyin": "Dàwèi yě zài kàn shū ma?",                     "translation": "David ham kitob o'qiyaptimi?"},
                {"speaker": "B", "zh": "他没看书，他在学做中国菜呢。",    "pinyin": "Tā méi kàn shū, tā zài xué zuò Zhōngguó cài ne.", "translation": "U kitob o'qiyapti emas, u xitoy taomi tayyorlashni o'rganayapti."},
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_label_zh": "Qahvaxonada — kecha nima qilding",
            "dialogue": [
                {"speaker": "A", "zh": "昨天上午你在做什么呢？",          "pinyin": "Zuótiān shàngwǔ nǐ zài zuò shénme ne?",         "translation": "Kecha ertalab nima qilyapding?"},
                {"speaker": "B", "zh": "我在睡觉呢。你呢？",              "pinyin": "Wǒ zài shuì jiào ne. Nǐ ne?",                  "translation": "Uxlayapman edi. Siz-chi?"},
                {"speaker": "A", "zh": "我在家看电视呢。你喜欢看电视吗？","pinyin": "Wǒ zài jiā kàn diànshì ne. Nǐ xǐhuan kàn diànshì ma?", "translation": "Men uyda televizor ko'rayapman edi. Siz televizor ko'rishni yoqtirasizmi?"},
                {"speaker": "B", "zh": "我不喜欢看电视，我喜欢看电影。",  "pinyin": "Wǒ bù xǐhuan kàn diànshì, wǒ xǐhuan kàn diànyǐng.", "translation": "Men televizor ko'rishni yoqtirmayman, kino ko'rishni yoqtiraman."},
            ]
        },
        {
            "block_no": 3,
            "section_label": "课文 3",
            "scene_label_zh": "Maktab ofisida — telefon raqami",
            "dialogue": [
                {"speaker": "A", "zh": "82304155，这是李老师的电话吗？",     "pinyin": "Bā èr sān líng sì yāo wǔ wǔ, zhè shì Lǐ lǎoshī de diànhuà ma?", "translation": "82304155, bu Li o'qituvchining telefoni?"},
                {"speaker": "B", "zh": "不是。她的电话是82304156。",         "pinyin": "Bú shì. Tā de diànhuà shì bā èr sān líng sì yāo wǔ liù.",      "translation": "Yo'q. Uning telefoni 82304156."},
                {"speaker": "A", "zh": "好，我现在给她打电话。",             "pinyin": "Hǎo, wǒ xiànzài gěi tā dǎ diànhuà.",                           "translation": "Yaxshi, hozir unga telefon qilaman."},
                {"speaker": "B", "zh": "她在工作呢，你下午打吧。",           "pinyin": "Tā zài gōngzuò ne, nǐ xiàwǔ dǎ ba.",                          "translation": "U ishlayapti, tushdan keyin qil."},
            ]
        },
    ], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "在……呢 — Hozirgi davom harakat",
            "explanation": (
                "Hozir bajarilayotgan harakat uchun:\n"
                "Tuzilishi 1: 在 + Fe'l (+ Narsa)\n"
                "Tuzilishi 2: Fe'l + Narsa + 呢\n"
                "Tuzilishi 3: 在 + Fe'l + 呢 (kuchaytirish)\n\n"
                "Misol:\n"
                "我在看书呢。— Men hozir kitob o'qiyapman.\n"
                "他在学做中国菜呢。— U xitoy taomi o'rganayapti.\n\n"
                "Inkor: 没(在) + Fe'l, 呢 yo'q\n"
                "他没看书。— U kitob o'qiyapti emas.\n"
                "他们没在工作。— Ular ishlamayapti."
            ),
            "examples": [
                {"zh": "我在看书呢。",         "pinyin": "Wǒ zài kàn shū ne.",           "meaning": "Men hozir kitob o'qiyapman."},
                {"zh": "他在学做中国菜呢。",   "pinyin": "Tā zài xué zuò Zhōngguó cài ne.", "meaning": "U xitoy taomi o'rganayapti."},
                {"zh": "她没在工作。",         "pinyin": "Tā méi zài gōngzuò.",          "meaning": "U ishlamayapti."},
            ]
        },
        {
            "no": 2,
            "title_zh": "也 — Ham ravishi",
            "explanation": (
                "也(yě) — 'ham, shuningdek' ma'nosida.\n"
                "Doim fe'l yoki modal fe'ldan oldin keladi.\n\n"
                "Misol:\n"
                "大卫也在看书吗？— David ham kitob o'qiyaptimi?\n"
                "我也喜欢看电影。— Men ham kino ko'rishni yoqtiraman.\n"
                "她也是老师。— U ham o'qituvchi."
            ),
            "examples": [
                {"zh": "大卫也在看书吗？",   "pinyin": "Dàwèi yě zài kàn shū ma?",   "meaning": "David ham kitob o'qiyaptimi?"},
                {"zh": "我也喜欢中国菜。",   "pinyin": "Wǒ yě xǐhuan Zhōngguó cài.", "meaning": "Men ham xitoy taomini yoqtiraman."},
                {"zh": "她也是学生。",       "pinyin": "Tā yě shì xuésheng.",         "meaning": "U ham o'quvchi."},
            ]
        },
        {
            "no": 3,
            "title_zh": "吧 — Yumshatuvchi yukla",
            "explanation": (
                "吧(ba) — taklif, maslahat yoki yumshoq buyruq bildiradi.\n"
                "Gap oxirida keladi.\n\n"
                "Misol:\n"
                "你下午打吧。— Tushdan keyin qil.\n"
                "今天我们在家吃饭吧。— Bugun uyda ovqatlansak.\n"
                "请坐吧。— O'tiring."
            ),
            "examples": [
                {"zh": "你下午打吧。",           "pinyin": "Nǐ xiàwǔ dǎ ba.",           "meaning": "Tushdan keyin qil."},
                {"zh": "我们一起去吧。",         "pinyin": "Wǒmen yīqǐ qù ba.",         "meaning": "Birga boraylik."},
                {"zh": "请坐吧。",               "pinyin": "Qǐng zuò ba.",               "meaning": "Marhamat, o'tiring."},
            ]
        },
    ], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction": "Xitoycha yozing:",
            "items": [
                {"prompt": "Hozir nima qilyapsan?",               "answer": "你在做什么呢？",          "pinyin": "Nǐ zài zuò shénme ne?"},
                {"prompt": "Men hozir kitob o'qiyapman.",          "answer": "我在看书呢。",             "pinyin": "Wǒ zài kàn shū ne."},
                {"prompt": "U ishlayapti emas.",                   "answer": "他没在工作。",             "pinyin": "Tā méi zài gōngzuò."},
                {"prompt": "Men ham kino ko'rishni yoqtiraman.",   "answer": "我也喜欢看电影。",         "pinyin": "Wǒ yě xǐhuan kàn diànyǐng."},
                {"prompt": "Hozir unga telefon qilaman.",          "answer": "我现在给她打电话。",       "pinyin": "Wǒ xiànzài gěi tā dǎ diànhuà."},
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction": "Bo'sh joyni to'ldiring:",
            "items": [
                {"prompt": "我___看书呢。",               "answer": "在",   "pinyin": "zài"},
                {"prompt": "大卫___在看书吗？",           "answer": "也",   "pinyin": "yě"},
                {"prompt": "他没___书，他在学做菜呢。",   "answer": "看",   "pinyin": "kàn"},
                {"prompt": "你下午打___。",               "answer": "吧",   "pinyin": "ba"},
            ]
        },
        {
            "no": 3,
            "type": "phone_numbers",
            "instruction": "Telefon raqamlarini xitoycha o'qing:",
            "items": [
                {"prompt": "8069478",    "answer": "bā líng liù jiǔ sì qī bā"},
                {"prompt": "13851897623","answer": "yāo sān bā wǔ yāo bā jiǔ liù èr sān"},
                {"prompt": "82304156",   "answer": "bā èr sān líng sì yāo wǔ liù"},
            ]
        },
    ], ensure_ascii=False),

    "answers_json": json.dumps([
        {"no": 1, "answers": ["你在做什么呢？", "我在看书呢。", "他没在工作。", "我也喜欢看电影。", "我现在给她打电话。"]},
        {"no": 2, "answers": ["在", "也", "看", "吧"]},
        {"no": 3, "answers": ["bā líng liù jiǔ sì qī bā", "yāo sān bā wǔ yāo bā jiǔ liù èr sān", "bā èr sān líng sì yāo wǔ liù"]},
    ], ensure_ascii=False),

    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction": "Kecha ertalab nima qilyapding? 3-4 gap yoz:",
            "template": "昨天上午我在___呢。我___喜欢___。",
            "words": ["在", "呢", "也", "喜欢", "看书", "看电视", "睡觉", "学习"],
        },
        {
            "no": 2,
            "instruction": "Do'stingga qo'ng'iroq qilish dialogini yoz (4 qator 喂 bilan boshla):",
            "example": "A: 喂，你在做什么呢？\nB: 我在___呢。\nA: ___也在___吗？\nB: 她___，她在___呢。",
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
