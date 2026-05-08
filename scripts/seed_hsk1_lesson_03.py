import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 3,
    "lesson_code": "HSK1-L03",
    "title": "你叫什么名字",
    "goal": json.dumps({
        "uz": "Xitoy tilida ismingizni, millatingizni va kasbingizni aytishni o'rganing",
        "tj": "Ба забони чинӣ ном, миллат ва шуғли худро омӯзед",
        "ru": "Научитесь произносить свое имя, национальность и род занятий на китайском языке."
}, ensure_ascii=False),
    "intro_text": json.dumps({
        "uz": "Uchinchi darsda siz xitoy tilida ismingizni, millatingizni va kasbingizni qanday aytishni o'rganasiz. 9 ta yangi soʻz, 3 ta dialog va hí-jumlalar uchun grammatika.",
        "tj": "Дар дарси сеюм шумо мефаҳмед, ки чӣ гуна ном, миллат ва шуғли худро бо забони чинӣ гуфтан мумкин аст. 9 калимаи нав, 3 муколама ва грамматика барои 是-ҷумла.",
        "ru": "На третьем уроке вы научитесь произносить свое имя, национальность и род занятий на китайском языке. 9 новых слов, 3 диалога и грамматика 是-предложений."
}, ensure_ascii=False),

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "叫",
                "pinyin": "jiào",
                "pos": "v.",
                "meaning": {
                        "uz": "chaqirilmoq, chaqirmoq",
                        "tj": "даъват шудан, даъват кардан",
                        "ru": "быть вызванным, позвонить"
                }
        },
        {
                "no": 2,
                "zh": "什么",
                "pinyin": "shénme",
                "pos": "pron.",
                "meaning": {
                        "uz": "nima, qaysi",
                        "tj": "чи, ки",
                        "ru": "что, какой"
                }
        },
        {
                "no": 3,
                "zh": "名字",
                "pinyin": "míngzi",
                "pos": "n.",
                "meaning": {
                        "uz": "nomi",
                        "tj": "ном",
                        "ru": "имя"
                }
        },
        {
                "no": 4,
                "zh": "我",
                "pinyin": "wǒ",
                "pos": "pron.",
                "meaning": {
                        "uz": "Men, men",
                        "tj": "ман, ман",
                        "ru": "я, я"
                }
        },
        {
                "no": 5,
                "zh": "是",
                "pinyin": "shì",
                "pos": "v.",
                "meaning": {
                        "uz": "bo'lish (=)",
                        "tj": "будан (=)",
                        "ru": "быть (=)"
                }
        },
        {
                "no": 6,
                "zh": "老师",
                "pinyin": "lǎoshī",
                "pos": "n.",
                "meaning": {
                        "uz": "o'qituvchi",
                        "tj": "муаллим",
                        "ru": "учитель"
                }
        },
        {
                "no": 7,
                "zh": "吗",
                "pinyin": "ma",
                "pos": "part.",
                "meaning": {
                        "uz": "savol zarrasi",
                        "tj": "заррачаи савол",
                        "ru": "вопросительная частица"
                }
        },
        {
                "no": 8,
                "zh": "学生",
                "pinyin": "xuésheng",
                "pos": "n.",
                "meaning": {
                        "uz": "talaba",
                        "tj": "донишҷӯ",
                        "ru": "студент"
                }
        },
        {
                "no": 9,
                "zh": "人",
                "pinyin": "rén",
                "pos": "n.",
                "meaning": {
                        "uz": "odam, odamlar",
                        "tj": "одам, одамон",
                        "ru": "человек, люди"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Maktabda — ism so'rash",
                        "tj": "Дар мактаб - пурсидани номҳо",
                        "ru": "В школе - спрашиваю имена"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你叫什么名字？",
                                "pinyin": "Nǐ jiào shénme míngzi?",
                                "translation": {
                                        "uz": "Ismingiz nima?",
                                        "tj": "Номи шумо чӣ?",
                                        "ru": "Как вас зовут?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我叫李月。",
                                "pinyin": "Wǒ jiào Lǐ Yuè.",
                                "translation": {
                                        "uz": "Mening ismim Li Yue.",
                                        "tj": "Номи ман Ли Юэ аст.",
                                        "ru": "Меня зовут Ли Юэ."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Sinfda — kasb so'rash",
                        "tj": "Дар синф — касбу хунарро талаб кунед",
                        "ru": "В классе – спроси про профессию"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你是老师吗？",
                                "pinyin": "Nǐ shì lǎoshī ma?",
                                "translation": {
                                        "uz": "Siz o'qituvchimisiz?",
                                        "tj": "Шумо муаллим ҳастед?",
                                        "ru": "Вы учитель?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我不是老师，我是学生。",
                                "pinyin": "Wǒ bú shì lǎoshī, wǒ shì xuésheng.",
                                "translation": {
                                        "uz": "Men o'qituvchi emasman, men talabaman.",
                                        "tj": "Ман муаллим нестам, ман донишҷӯ ҳастам.",
                                        "ru": "Я не учитель, я ученик."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Maktabda — millat so'rash",
                        "tj": "Дар мактаб - миллатро пурсед",
                        "ru": "В школе - спроси национальность"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你是中国人吗？",
                                "pinyin": "Nǐ shì Zhōngguó rén ma?",
                                "translation": {
                                        "uz": "Siz Xitoymisiz?",
                                        "tj": "Шумо чинӣ ҳастед?",
                                        "ru": "Вы китаец?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我不是中国人，我是美国人。",
                                "pinyin": "Wǒ bú shì Zhōngguó rén, wǒ shì Měiguó rén.",
                                "translation": {
                                        "uz": "Men xitoylik emasman, men amerikalikman.",
                                        "tj": "Ман чинӣ нестам, ман амрикоӣ ҳастам.",
                                        "ru": "Я не китаец, я американец."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "是字句 — 是 gapi",
                "explanation": {
                        "rule_uz": "shì(shì) — tenglikni ifodalaydi (= boʻlmoq).\nTuzilishi: Mavzu + mí + Ot/Ot so'z birikmasi\nInkor: Mavzu + shēngí + Ot/Ot so'z birikmasi\n\nMisol:\nmàngāngāngī- Men o'qituvchiman.\nmíngìnìnhì- Men oʻqituvchi emasman.\nlíngyǎngyǎngyīng。— Li Yue xitoylik.",
                        "rule_tj": "是(shì) — баробариро ифода мекунад (= будан).\nСохтор: Мавзӯъ + 是 + Ибораи исм/Исм\nИнкор: Мавзӯъ + 不是 + Ибораи исм/Исм\n\nМисол:\n我是老师。— Ман муаллим ҳастам.\n我不是老师。— Ман муаллим нестам.\n李月是中国人。— Ли Юэ чинӣ аст.",
                        "rule_ru": "是(ши) — выражает равенство (= быть).\nСтруктура: Тема + 是 + существительное/именная группа.\nОтрицание: Подлежащее + 不是 + существительное/существительная фраза.\n\nПример:\n我是老师。 — Я учитель.\n我不是老师。 — Я не учитель.\n李月是中国人。 — Ли Юэ китаец."
                },
                "examples": [
                        {
                                "zh": "我是学生。",
                                "pinyin": "Wǒ shì xuésheng.",
                                "meaning": {
                                        "uz": "Men talabaman.",
                                        "tj": "Ман донишҷӯй ҳастам.",
                                        "ru": "Я студент."
                                }
                        },
                        {
                                "zh": "我不是老师。",
                                "pinyin": "Wǒ bú shì lǎoshī.",
                                "meaning": {
                                        "uz": "Men o'qituvchi emasman.",
                                        "tj": "Ман муаллим нестам.",
                                        "ru": "Я не учитель."
                                }
                        },
                        {
                                "zh": "她是中国人。",
                                "pinyin": "Tā shì Zhōngguó rén.",
                                "meaning": {
                                        "uz": "U xitoylik.",
                                        "tj": "Вай чинӣ аст.",
                                        "ru": "Она китаянка."
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "吗 — So'roq gapi",
                "explanation": {
                        "rule_uz": "mí(ma) — gap oxirida qoʻyilgan boʻlsa, uni ha/yoʻq savoliga aylantiradi.\nTuzilishi: bayonot + ?\n\nMisol:\nmēngīngīkīkī → shīngīngīngī?\nSiz o'qituvchisiz. → Siz o'qituvchimisiz?\n\nJavob: hí (ha) yoki díči (yo'q)",
                        "rule_tj": "吗(ma) — дар охири ҷумла гузошта шуда, онро ба саволи ҳа/не табдил медиҳад.\nСохтор: Изҳорот + 吗？\n\nМисол:\n你是老师。→ 你是老师吗？\nШумо муаллим ҳастед. → Шумо муаллим ҳастед?\n\nҶавоб: 是 (ҳа) ё 不是 (не)",
                        "rule_ru": "吗(ма) — помещенный в конце предложения, превращает его в вопрос типа «да/нет».\nСтруктура: Оператор + 吗？\n\nПример:\n你是老师。→ 你是老师吗？\nВы учитель. → Вы учитель?\n\nОтвет: 是 (да) или 不是 (нет)."
                },
                "examples": [
                        {
                                "zh": "你是学生吗？",
                                "pinyin": "Nǐ shì xuésheng ma?",
                                "meaning": {
                                        "uz": "Siz talabasizmi?",
                                        "tj": "Ту донишомӯзӣ?",
                                        "ru": "Вы студент?"
                                }
                        },
                        {
                                "zh": "你是美国人吗？",
                                "pinyin": "Nǐ shì Měiguó rén ma?",
                                "meaning": {
                                        "uz": "Siz amerikalikmisiz?",
                                        "tj": "Шумо амрикоӣ ҳастед?",
                                        "ru": "Вы американец?"
                                }
                        },
                        {
                                "zh": "你叫李月吗？",
                                "pinyin": "Nǐ jiào Lǐ Yuè ma?",
                                "meaning": {
                                        "uz": "Sizning ismingiz Li Yuemi?",
                                        "tj": "Номи шумо Ли Юэ?",
                                        "ru": "Вас зовут Ли Юэ?"
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "什么 — So'roq olmoshi",
                "explanation": {
                        "rule_uz": "shénme (shénme) - \"nima\", \"qaysi\" degan ma'noni anglatadi.\nOxirida chàn qo‘shmang — mínning o‘zi gapni savolga aylantiradi.\n\nMisol:\nchàngāngāngāngīn？— Ismingiz nima?\nlìnìnìnì？— Bu nima?\nmíngīnīnīn？— Siz kimsiz?",
                        "rule_tj": "什么(shénme) — маънои 'чӣ', 'кадом'.\nДар охир 吗 илова накунед — 什么 худ ҷумларо савол мекунад.\n\nМисол:\n你叫什么名字？— Номи шумо чист?\n这是什么？— Ин чист?\n你是什么人？— Шумо кистед?",
                        "rule_ru": "什么(сэнмэ) — означает «что», «который».\nНе добавляйте 吗 в конце — 什么 само по себе делает предложение вопросительным.\n\nПример:\n你叫什么名字？ — Как тебя зовут?\n这是什么？— Что это?\n你是什么人？ — Кто ты?"
                },
                "examples": [
                        {
                                "zh": "你叫什么名字？",
                                "pinyin": "Nǐ jiào shénme míngzi?",
                                "meaning": {
                                        "uz": "Ismingiz nima?",
                                        "tj": "Номи шумо чӣ?",
                                        "ru": "Как вас зовут?"
                                }
                        },
                        {
                                "zh": "这是什么？",
                                "pinyin": "Zhè shì shénme?",
                                "meaning": {
                                        "uz": "Bu nima?",
                                        "tj": "Ин чи аст?",
                                        "ru": "Что это?"
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
                "no": 1,
                "type": "translate_to_chinese",
                "instruction": {
                        "uz": "Xitoy tilida yozing:",
                        "tj": "Ба забони чинӣ нависед:",
                        "ru": "Напишите по-китайски:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "Ismingiz nima?",
                                        "tj": "Номи шумо чӣ?",
                                        "ru": "Как вас зовут?"
                                },
                                "answer": "你叫什么名字？",
                                "pinyin": "Nǐ jiào shénme míngzi?"
                        },
                        {
                                "prompt": {
                                        "uz": "Mening ismim Vang Fang.",
                                        "tj": "Номи ман Ван Фанг аст.",
                                        "ru": "Меня зовут Ван Фан."
                                },
                                "answer": "我叫王芳。",
                                "pinyin": "Wǒ jiào Wáng Fāng."
                        },
                        {
                                "prompt": {
                                        "uz": "Siz o'qituvchimisiz?",
                                        "tj": "Шумо муаллим ҳастед?",
                                        "ru": "Вы учитель?"
                                },
                                "answer": "你是老师吗？",
                                "pinyin": "Nǐ shì lǎoshī ma?"
                        },
                        {
                                "prompt": {
                                        "uz": "Men talabaman.",
                                        "tj": "Ман донишҷӯй ҳастам.",
                                        "ru": "Я студент."
                                },
                                "answer": "我是学生。",
                                "pinyin": "Wǒ shì xuésheng."
                        },
                        {
                                "prompt": {
                                        "uz": "Men xitoylik emasman, men amerikalikman.",
                                        "tj": "Ман чинӣ нестам, ман амрикоӣ ҳастам.",
                                        "ru": "Я не китаец, я американец."
                                },
                                "answer": "我不是中国人，我是美国人。",
                                "pinyin": "Wǒ bú shì Zhōngguó rén, wǒ shì Měiguó rén."
                        }
                ]
        },
        {
                "no": 2,
                "type": "fill_blank",
                "instruction": {
                        "uz": "Bo'sh joyni to'ldiring:",
                        "tj": "Холиро пур кунед:",
                        "ru": "Заполните пробел:"
                },
                "items": [
                        {
                                "prompt": "A: 你叫___名字？  B: 我叫李月。",
                                "answer": "什么",
                                "pinyin": "shénme"
                        },
                        {
                                "prompt": "A: 你___老师吗？  B: 是，我是老师。",
                                "answer": "是",
                                "pinyin": "shì"
                        },
                        {
                                "prompt": "A: 你是中国人___？ B: 不是，我是美国人。",
                                "answer": "吗",
                                "pinyin": "ma"
                        },
                        {
                                "prompt": "我不___老师，我是学生。",
                                "answer": "是",
                                "pinyin": "shì"
                        }
                ]
        },
        {
                "no": 3,
                "type": "make_question",
                "instruction": {
                        "uz": "吗 yordamida savolga aylantiring:",
                        "tj": "Бо истифода аз 吗 ба савол табдил диҳед:",
                        "ru": "Превратите вопрос в вопрос, используя 吗:"
                },
                "items": [
                        {
                                "prompt": "你是学生。",
                                "answer": "你是学生吗？",
                                "pinyin": "Nǐ shì xuésheng ma?"
                        },
                        {
                                "prompt": "他是中国人。",
                                "answer": "他是中国人吗？",
                                "pinyin": "Tā shì Zhōngguó rén ma?"
                        },
                        {
                                "prompt": "她叫李月。",
                                "answer": "她叫李月吗？",
                                "pinyin": "Tā jiào Lǐ Yuè ma?"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "你叫什么名字？",
                        "我叫王芳。",
                        "你是老师吗？",
                        "我是学生。",
                        "我不是中国人，我是美国人。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "什么",
                        "是",
                        "吗",
                        "是"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "你是学生吗？",
                        "他是中国人吗？",
                        "她叫李月吗？"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "O'zingiz haqingizda 3 ta jumla yozing (ismi, millati, kasbi):",
                        "tj": "Дар бораи худ 3 ҷумла нависед (ном, миллат, шуғл):",
                        "ru": "Напишите 3 предложения о себе (имя, национальность, род занятий):"
                },
                "example": "我叫___。我是___人。我是___。",
                "words": [
                        "叫",
                        "是",
                        "不是",
                        "老师",
                        "学生",
                        "中国人",
                        "美国人"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Quyidagi jumlalarni h dan foydalanib savolga aylantiring:",
                        "tj": "Ҷумлаҳои зеринро бо истифода аз 吗 ба саволҳо табдил диҳед:",
                        "ru": "Превратите следующие предложения в вопросы, используя 吗:"
                },
                "items": [
                        {
                                "prompt": "你是老师。",
                                "answer": "你是老师吗？"
                        },
                        {
                                "prompt": "他叫大卫。",
                                "answer": "他叫大卫吗？"
                        },
                        {
                                "prompt": "她是美国人。",
                                "answer": "她是美国人吗？"
                        }
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
        print(f"\u2705 Lesson {LESSON['lesson_code']} \u2014 {LESSON['title']} created.")


if __name__ == "__main__":
    asyncio.run(seed())
