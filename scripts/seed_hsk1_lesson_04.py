import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 4,
    "lesson_code": "HSK1-L04",
    "title": "她是我的汉语老师",
    "goal": json.dumps({
        "uz": "Uchinchi shaxslar haqida gapiring, ii bilan egalik qiling va so'roq so'zlaridan foydalaning.",
        "tj": "Дар бораи шахсони сеюм сӯҳбат кунед, бо 的 соҳибӣ кунед ва калимаҳои 谁/哪 саволро истифода баред",
        "ru": "Говорите о третьих лицах, выражайте владение с помощью 的 и используйте вопросительные слова 谁/哪."
}, ensure_ascii=False),
    "intro_text": json.dumps({
        "uz": "To'rtinchi darsda siz uchinchi shaxslar (u/u) haqida gapirishni, zán zarrachasi yordamida egalikni ifodalashni va so'roq so'zlaridan foydalanishni o'rganasiz. 10 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси чорум шумо мефаҳмед, ки чӣ тавр дар бораи шахсони сеюм (ӯ) сӯҳбат кардан, соҳибиятро бо истифода аз заррачаи 的 ифода кардан ва калимаҳои саволии 谁/哪 истифода бурданро меомӯзед. 10 калимаи нав, 3 муколама.",
        "ru": "На четвертом уроке вы научитесь говорить о третьем лице (он/она), выражать принадлежность с помощью частицы 的 и использовать вопросительные слова 谁/哪. 10 новых слов, 3 диалога."
}, ensure_ascii=False),

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "她",
                "pinyin": "tā",
                "pos": "pron.",
                "meaning": {
                        "uz": "u, uni",
                        "tj": "вай, вай",
                        "ru": "она, ее"
                }
        },
        {
                "no": 2,
                "zh": "谁",
                "pinyin": "shéi",
                "pos": "pron.",
                "meaning": {
                        "uz": "JSSV",
                        "tj": "Ташкили Тандурустии Ҷаҳон",
                        "ru": "ВОЗ"
                }
        },
        {
                "no": 3,
                "zh": "的",
                "pinyin": "de",
                "pos": "part.",
                "meaning": {
                        "uz": "ning (ega zarrasi)",
                        "tj": "'s (заррачаи соҳибӣ)",
                        "ru": "'s (притяжательная частица)"
                }
        },
        {
                "no": 4,
                "zh": "汉语",
                "pinyin": "Hànyǔ",
                "pos": "n.",
                "meaning": {
                        "uz": "Xitoy tili",
                        "tj": "забони чинӣ",
                        "ru": "китайский язык"
                }
        },
        {
                "no": 5,
                "zh": "哪",
                "pinyin": "nǎ",
                "pos": "pron.",
                "meaning": {
                        "uz": "qaysi, qayerdan",
                        "tj": "ки, аз кучо",
                        "ru": "который, откуда"
                }
        },
        {
                "no": 6,
                "zh": "国",
                "pinyin": "guó",
                "pos": "n.",
                "meaning": {
                        "uz": "mamlakat, millat",
                        "tj": "кишвар, миллат",
                        "ru": "страна, нация"
                }
        },
        {
                "no": 7,
                "zh": "呢",
                "pinyin": "ne",
                "pos": "part.",
                "meaning": {
                        "uz": "nima haqida? (keyingi savol)",
                        "tj": "дар бораи? (саволи минбаъда)",
                        "ru": "что насчет? (дополнительный вопрос)"
                }
        },
        {
                "no": 8,
                "zh": "他",
                "pinyin": "tā",
                "pos": "pron.",
                "meaning": {
                        "uz": "u, u",
                        "tj": "ӯ, ӯ",
                        "ru": "он, он"
                }
        },
        {
                "no": 9,
                "zh": "同学",
                "pinyin": "tóngxué",
                "pos": "n.",
                "meaning": {
                        "uz": "sinfdosh",
                        "tj": "ҳамсинф",
                        "ru": "одноклассник"
                }
        },
        {
                "no": 10,
                "zh": "朋友",
                "pinyin": "péngyou",
                "pos": "n.",
                "meaning": {
                        "uz": "do'st",
                        "tj": "дуст",
                        "ru": "друг"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Sinfda — o'qituvchi haqida",
                        "tj": "Дар синф — дар бораи муаллим",
                        "ru": "На уроке – об учителе"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "她是谁？",
                                "pinyin": "Tā shì shéi?",
                                "translation": {
                                        "uz": "Kim u?",
                                        "tj": "Ӯ кист?",
                                        "ru": "Кто она?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "她是我的汉语老师，她叫李月。",
                                "pinyin": "Tā shì wǒ de Hànyǔ lǎoshī, tā jiào Lǐ Yuè.",
                                "translation": {
                                        "uz": "U mening xitoycha o‘qituvchim, uning ismi Li Yue.",
                                        "tj": "Вай муаллими чинии ман аст, номаш Ли Юэ аст.",
                                        "ru": "Она моя учительница китайского языка, ее зовут Ли Юэ."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Kutubxonada — millat so'rash",
                        "tj": "Дар китобхона — миллатро пурсед",
                        "ru": "В библиотеке - спроси национальность"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你是哪国人？",
                                "pinyin": "Nǐ shì nǎ guó rén?",
                                "translation": {
                                        "uz": "Siz qaysi davlatdansiz?",
                                        "tj": "Шумо аз кадом кишваред?",
                                        "ru": "Из какой ты страны?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我是美国人。你呢？",
                                "pinyin": "Wǒ shì Měiguó rén. Nǐ ne?",
                                "translation": {
                                        "uz": "Men amerikalikman. Sizchi?",
                                        "tj": "Ман амрикоӣ ҳастам. Шумо чӣ?",
                                        "ru": "Я американец. А вы?"
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "我是中国人。",
                                "pinyin": "Wǒ shì Zhōngguó rén.",
                                "translation": {
                                        "uz": "Men xitoylikman.",
                                        "tj": "Ман чиноиям.",
                                        "ru": "Я китаец."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Fotoda — do'st va sinfdosh",
                        "tj": "Дар сурат рафик ва хамсинф",
                        "ru": "На фото друг и одноклассник"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "他是谁？",
                                "pinyin": "Tā shì shéi?",
                                "translation": {
                                        "uz": "U kim?",
                                        "tj": "Ӯ кист?",
                                        "ru": "Кто он?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "他是我同学。",
                                "pinyin": "Tā shì wǒ tóngxué.",
                                "translation": {
                                        "uz": "U mening sinfdoshim.",
                                        "tj": "Ӯ ҳамсинфи ман аст.",
                                        "ru": "Он мой одноклассник."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "她呢？她是你同学吗？",
                                "pinyin": "Tā ne? Tā shì nǐ tóngxué ma?",
                                "translation": {
                                        "uz": "Unga-chi? U ham sizning sinfdoshingizmi?",
                                        "tj": "Дар бораи вай чӣ? Оё вай ҳамсинфи шумост?",
                                        "ru": "Что насчет нее? Она тоже твоя одноклассница?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "她不是我同学，她是我朋友。",
                                "pinyin": "Tā bú shì wǒ tóngxué, tā shì wǒ péngyou.",
                                "translation": {
                                        "uz": "U mening sinfdoshim emas, u mening do'stim.",
                                        "tj": "Вай ҳамсинфи ман нест, вай дӯсти ман аст.",
                                        "ru": "Она не моя одноклассница, она мой друг."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "结构助词 的 — Egalik yuklamasi",
                "explanation": {
                        "rule_uz": "y(de) — egalik yoki birlashmani ifodalaydi.\nTuzilishi: Ism/Olmosh + lín + Ism\n\nMisol:\nlíngín - mening ustozim\nlíngjíng - uning do'sti\n\nEslatma: qarindoshlik atamalari va shaxs ismlaridan oldin yán tushirilishi mumkin:\nlín(yīng) ✓ — mening ustozim\nlín(yán)mēng ✓ — do'stim",
                        "rule_tj": "的(de) — моликият ё иттиҳодияро ифода мекунад.\nСохтор: Исм / Ҷонишин + 的 + Исм\n\nМисол:\n我的老师 — муаллими ман\n她的朋友 - дӯсти вай\n\nЭзоҳ: 的 метавонад пеш аз истилоҳҳои хешовандӣ ва исмҳои шахсӣ гузошта шавад:\n我(的)老师 ✓ — муаллими ман\n我(的)朋友 ✓ — дустам",
                        "rule_ru": "的(де) — выражает обладание или ассоциацию.\nСтруктура: Существительное/Местоимение + 的 + Существительное\n\nПример:\n我的老师 — мой учитель\n她的朋友 — ее друг\n\nПримечание. 的 можно опустить перед терминами родства и личными существительными:\n我(的)老师 ✓ — мой учитель\n我(的)朋友 ✓ — мой друг"
                },
                "examples": [
                        {
                                "zh": "我的汉语老师",
                                "pinyin": "wǒ de Hànyǔ lǎoshī",
                                "meaning": {
                                        "uz": "mening xitoy o'qituvchim",
                                        "tj": "муаллими хитоии ман",
                                        "ru": "мой учитель китайского языка"
                                }
                        },
                        {
                                "zh": "他的同学",
                                "pinyin": "tā de tóngxué",
                                "meaning": {
                                        "uz": "uning sinfdoshi",
                                        "tj": "хамсинфаш",
                                        "ru": "его одноклассник"
                                }
                        },
                        {
                                "zh": "你的朋友",
                                "pinyin": "nǐ de péngyou",
                                "meaning": {
                                        "uz": "do'stingiz",
                                        "tj": "дӯсти шумо",
                                        "ru": "твой друг"
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "谁 — Kim so'roq olmoshi",
                "explanation": {
                        "rule_uz": "shéi (shéi) - \"kim?\" degan ma'noni anglatadi.\nU gapda sub'ekt yoki ob'ekt vazifasini bajarishi mumkin.\n\nMisol:\nchàngāng?- U kim?\nlíngāngān？— O‘qituvchi kim?\nchàngāngāngīng？— U kimning do‘sti?",
                        "rule_tj": "谁(shéi) - маънои \"кӣ?\".\nОн метавонад ҳамчун субъект ё объект дар ҷумла амал кунад.\n\nМисол:\n她是谁？— Вай кист?\n谁是老师？— Муаллим кист?\n他是谁的朋友？— Ӯ дӯсти кист?",
                        "rule_ru": "谁(shéi) — означает «кто?».\nОн может выступать в роли субъекта или объекта в предложении.\n\nПример:\n她是谁？— Кто она?\n谁是老师？ — Кто учитель?\n他是谁的朋友？ — Чей он друг?"
                },
                "examples": [
                        {
                                "zh": "她是谁？",
                                "pinyin": "Tā shì shéi?",
                                "meaning": {
                                        "uz": "Kim u?",
                                        "tj": "Ӯ кист?",
                                        "ru": "Кто она?"
                                }
                        },
                        {
                                "zh": "谁是你的老师？",
                                "pinyin": "Shéi shì nǐ de lǎoshī?",
                                "meaning": {
                                        "uz": "Sizning o'qituvchingiz kim?",
                                        "tj": "Устоди шумо кист?",
                                        "ru": "Кто твой учитель?"
                                }
                        },
                        {
                                "zh": "他是谁的同学？",
                                "pinyin": "Tā shì shéi de tóngxué?",
                                "meaning": {
                                        "uz": "U kimning sinfdoshi?",
                                        "tj": "Ӯ ҳамсинфи кист?",
                                        "ru": "Чей он одноклассник?"
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "呢 — Qaytarma so'roq yuklamasi",
                "explanation": {
                        "rule_uz": "y(ne) - oldingi gapda aytilgan bir xil mavzu haqida so'rash uchun ishlatiladi.\nTuzilishi: A bayonoti... Bjđ？ (B haqida nima deyish mumkin?)\n\nMisol:\nmíngjínzínzဂdínjín?\nMen amerikalikman. Sizchi?\n\nchàngìnìmìnìnìnì?\nUning ismi Li Yue. U haqida-chi?",
                        "rule_tj": "呢(ne) - барои пурсидан дар бораи ҳамон мавзӯи дар ҷумлаи қаблӣ зикршуда истифода мешавад.\nСохтор: Изҳороти A... B呢？ (Дар бораи B чӣ гуфтан мумкин аст?)\n\nМисол:\n我是美国人。你呢？\nМан амрикоӣ ҳастам. Шумо чӣ?\n\n她叫李月。他呢？\nНоми вай Ли Юэ аст. Дар бораи ӯ чӣ гуфтан мумкин аст?",
                        "rule_ru": "呢(нэ) — используется для вопроса о той же теме, что и в предыдущем предложении.\nСтруктура: Утверждение A... B呢？ (А как насчет B?)\n\nПример:\n我是美国人。你呢？\nЯ американец. А вы?\n\n她叫李月。他呢？\nЕе зовут Ли Юэ. А что насчет него?"
                },
                "examples": [
                        {
                                "zh": "我是学生。你呢？",
                                "pinyin": "Wǒ shì xuésheng. Nǐ ne?",
                                "meaning": {
                                        "uz": "Men talabaman. Sizchi?",
                                        "tj": "Ман донишҷӯй ҳастам. Шумо чӣ?",
                                        "ru": "Я студент. А вы?"
                                }
                        },
                        {
                                "zh": "她是中国人。他呢？",
                                "pinyin": "Tā shì Zhōngguó rén. Tā ne?",
                                "meaning": {
                                        "uz": "U xitoylik. U haqida-chi?",
                                        "tj": "Вай чинӣ аст. Дар бораи ӯ чӣ гуфтан мумкин аст?",
                                        "ru": "Она китаянка. А что насчет него?"
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
                                        "uz": "Kim u?",
                                        "tj": "Ӯ кист?",
                                        "ru": "Кто она?"
                                },
                                "answer": "她是谁？",
                                "pinyin": "Tā shì shéi?"
                        },
                        {
                                "prompt": {
                                        "uz": "U mening xitoycha o'qituvchim.",
                                        "tj": "Вай муаллими чинии ман аст.",
                                        "ru": "Она моя учительница китайского языка."
                                },
                                "answer": "她是我的汉语老师。",
                                "pinyin": "Tā shì wǒ de Hànyǔ lǎoshī."
                        },
                        {
                                "prompt": {
                                        "uz": "Siz qaysi davlatdansiz?",
                                        "tj": "Шумо аз кадом кишваред?",
                                        "ru": "Из какой ты страны?"
                                },
                                "answer": "你是哪国人？",
                                "pinyin": "Nǐ shì nǎ guó rén?"
                        },
                        {
                                "prompt": {
                                        "uz": "Men amerikalikman. Sizchi?",
                                        "tj": "Ман амрикоӣ ҳастам. Шумо чӣ?",
                                        "ru": "Я американец. А вы?"
                                },
                                "answer": "我是美国人。你呢？",
                                "pinyin": "Wǒ shì Měiguó rén. Nǐ ne?"
                        },
                        {
                                "prompt": {
                                        "uz": "U mening sinfdoshim emas, u mening do'stim.",
                                        "tj": "Ӯ ҳамсинфи ман нест, ӯ дӯсти ман аст.",
                                        "ru": "Он не мой одноклассник, он мой друг."
                                },
                                "answer": "他不是我同学，他是我朋友。",
                                "pinyin": "Tā bú shì wǒ tóngxué, tā shì wǒ péngyou."
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
                                "prompt": "她是我___汉语老师。",
                                "answer": "的",
                                "pinyin": "de"
                        },
                        {
                                "prompt": "A: 他是___？  B: 他是我同学。",
                                "answer": "谁",
                                "pinyin": "shéi"
                        },
                        {
                                "prompt": "我是中国人。你___？",
                                "answer": "呢",
                                "pinyin": "ne"
                        },
                        {
                                "prompt": "你是___国人？",
                                "answer": "哪",
                                "pinyin": "nǎ"
                        }
                ]
        },
        {
                "no": 3,
                "type": "make_sentence",
                "instruction": {
                        "uz": "Berilgan so‘zlardan gap tuzing:",
                        "tj": "Аз калимаҳои додашуда ҷумла созед:",
                        "ru": "Составьте предложение из данных слов:"
                },
                "items": [
                        {
                                "words": [
                                        "她",
                                        "是",
                                        "我",
                                        "的",
                                        "朋友"
                                ],
                                "answer": "她是我的朋友。",
                                "pinyin": "Tā shì wǒ de péngyou."
                        },
                        {
                                "words": [
                                        "他",
                                        "哪",
                                        "是",
                                        "国",
                                        "人"
                                ],
                                "answer": "他是哪国人？",
                                "pinyin": "Tā shì nǎ guó rén?"
                        },
                        {
                                "words": [
                                        "谁",
                                        "你",
                                        "老师",
                                        "是",
                                        "的"
                                ],
                                "answer": "谁是你的老师？",
                                "pinyin": "Shéi shì nǐ de lǎoshī?"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "她是谁？",
                        "她是我的汉语老师。",
                        "你是哪国人？",
                        "我是美国人。你呢？",
                        "他不是我同学，他是我朋友。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "的",
                        "谁",
                        "呢",
                        "哪"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "她是我的朋友。",
                        "他是哪国人？",
                        "谁是你的老师？"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Do'stingiz haqida 4 ta jumla yozing:",
                        "tj": "Дар бораи дӯст 4 ҷумла нависед:",
                        "ru": "Напишите 4 предложения о друге:"
                },
                "template": "他/她叫___。他/她是___人。他/她是我的___。他/她是不是___？",
                "words": [
                        "的",
                        "同学",
                        "朋友",
                        "老师",
                        "汉语老师"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Quyidagi savollarga javob bering:",
                        "tj": "Ба саволҳои зерин ҷавоб диҳед:",
                        "ru": "Ответьте на следующие вопросы:"
                },
                "items": [
                        {
                                "prompt": "你的汉语老师是哪国人？",
                                "hint": "What country is your Chinese teacher from?"
                        },
                        {
                                "prompt": "你的朋友叫什么名字？",
                                "hint": "What is your friend's name?"
                        },
                        {
                                "prompt": "他/她是你的同学吗？",
                                "hint": "Is he/she your classmate?"
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
