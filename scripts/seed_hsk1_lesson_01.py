import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 1,
    "lesson_code": "HSK1-L01",
    "title": "你好",
    "goal": {
        "uz": "Xitoy tilida salomlashish va kechirim so‘rashni o‘rganing",
        "tj": "Омӯзед, ки чӣ тавр ба одамон салом додан ва узр пурсиданро бо забони чинӣ",
        "ru": "Научитесь приветствовать людей и извиняться на китайском языке."
    },
    "intro_text": {
        "uz": "Birinchi darsda siz xitoycha salomlashishni o'rganasiz. Ushbu dars 6 ta yangi so'z, 3 ta dialog va asosiy talaffuz qoidalarini o'z ichiga oladi.",
        "tj": "Дар дарси аввал шумо саломҳои чиниро меомӯзед. Ин дарс 6 калимаи нав, 3 муколама ва қоидаҳои асосии талаффузро дар бар мегирад.",
        "ru": "На первом уроке вы выучите китайские приветствия. Этот урок включает в себя 6 новых слов, 3 диалога и основные правила произношения."
    },

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "你",
                "pinyin": "nǐ",
                "pos": "pron.",
                "meaning": {
                        "uz": "you (singular)",
                        "tj": "шумо (якгона)",
                        "ru": "ты (единственное число)"
                }
        },
        {
                "no": 2,
                "zh": "好",
                "pinyin": "hǎo",
                "pos": "adj.",
                "meaning": {
                        "uz": "yaxshi, ajoyib",
                        "tj": "хуб, бузург",
                        "ru": "хорошо, отлично"
                }
        },
        {
                "no": 3,
                "zh": "您",
                "pinyin": "nín",
                "pos": "pron.",
                "meaning": {
                        "uz": "siz (rasmiy/odobli)",
                        "tj": "шумо (расмӣ/одоб)",
                        "ru": "ты (официально/вежливо)"
                }
        },
        {
                "no": 4,
                "zh": "你们",
                "pinyin": "nǐmen",
                "pos": "pron.",
                "meaning": {
                        "uz": "siz (ko'plik)",
                        "tj": "шумо (ҷамъ)",
                        "ru": "ты (множественное число)"
                }
        },
        {
                "no": 5,
                "zh": "对不起",
                "pinyin": "duìbuqǐ",
                "pos": "v.",
                "meaning": {
                        "uz": "kechirasiz, kechirasiz",
                        "tj": "бубахшед, бубахшед",
                        "ru": "извини, извини"
                }
        },
        {
                "no": 6,
                "zh": "没关系",
                "pinyin": "méi guānxi",
                "pos": "expr.",
                "meaning": {
                        "uz": "muammo yo'q, tashvishlanmang",
                        "tj": "мушкил нест, хавотир нашав",
                        "ru": "нет проблем, не волнуйся"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Tanishlar uchrashadi",
                        "tj": "Шиносхо вомехуранд",
                        "ru": "Знакомые встречаются"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你好！",
                                "pinyin": "Nǐ hǎo!",
                                "translation": {
                                        "uz": "Salom!",
                                        "tj": "Салом!",
                                        "ru": "Привет!"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "你好！",
                                "pinyin": "Nǐ hǎo!",
                                "translation": {
                                        "uz": "Salom!",
                                        "tj": "Салом!",
                                        "ru": "Привет!"
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Hurmatli salomlashuv",
                        "tj": "Бо эҳтиром",
                        "ru": "С наилучшими пожеланиями"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "您好！",
                                "pinyin": "Nín hǎo!",
                                "translation": {
                                        "uz": "Salom (rasmiy)!",
                                        "tj": "Салом (расмӣ)!",
                                        "ru": "Здравствуйте (официально)!"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "你们好！",
                                "pinyin": "Nǐmen hǎo!",
                                "translation": {
                                        "uz": "Hammaga salom!",
                                        "tj": "Салом ба ҳама!",
                                        "ru": "Всем привет!"
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Kechirim so'rash",
                        "tj": "Узр",
                        "ru": "Извиняться"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "对不起！",
                                "pinyin": "Duìbuqǐ!",
                                "translation": {
                                        "uz": "Kechirasiz!",
                                        "tj": "Бубахшед!",
                                        "ru": "Извини!"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "没关系！",
                                "pinyin": "Méi guānxi!",
                                "translation": {
                                        "uz": "Hammasi joyida!",
                                        "tj": "Масъалае нест!",
                                        "ru": "Без проблем!"
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "四声 — To'rt ton",
                "explanation": {
                        "rule_uz": "Xitoy tilida har bir bo'g'in 4 ohangga ega:\nOhang 1 (—): tekis va baland - ma (ona)\n2-ohang (ˊ): ko'tarilish - má (kenevir o'simligi)\n3-ohang (ˇ): pastga tushadi, keyin ko'tariladi - mǎ (ot)\n4-ohang (ˋ): yiqilish — mà (tanashish)\n\nOhang ma'noni o'zgartiradi!",
                        "rule_tj": "Дар забони чинӣ ҳар як ҳиҷо 4 оҳанг дорад:\nОҳанги 1 (—): ҳамвор ва баланд - mā (модар)\nОҳанги 2 (ˊ): болоравӣ — má (растании бангдона)\nОҳанги 3 (ˇ): афтодан ва баъд баланд шудан — mǎ (асп)\nОҳанги 4 (ˋ): афтидан — mà (сарзаниш кардан)\n\nОҳанг маънои онро тағйир медиҳад!",
                        "rule_ru": "В китайском языке каждый слог имеет 4 тона:\nТон 1 (—): ровный и высокий — ма (мать).\nТон 2 (ˊ): восходящий — má (растение конопли)\nТон 3 (ˇ): падение, затем повышение — m (лошадь)\nТон 4 (ˋ): падение — mà (ругать)\n\nТон меняет смысл!"
                },
                "examples": [
                        {
                                "zh": "妈",
                                "pinyin": "mā",
                                "meaning": {
                                        "uz": "ona (1-ohang)",
                                        "tj": "модар (оханги 1)",
                                        "ru": "мать (тон 1)"
                                }
                        },
                        {
                                "zh": "马",
                                "pinyin": "mǎ",
                                "meaning": {
                                        "uz": "ot (3-ohang)",
                                        "tj": "асп (оханги 3)",
                                        "ru": "лошадь (тон 3)"
                                }
                        },
                        {
                                "zh": "骂",
                                "pinyin": "mà",
                                "meaning": {
                                        "uz": "so'kmoq (4-ohang)",
                                        "tj": "сарзаниш кардан (оханги 4)",
                                        "ru": "ругать (тон 4)"
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "变调 — Ton o'zgarishi (3+3)",
                "explanation": {
                        "rule_uz": "Ikki ohang-3 bo'g'in ketma-ket kelganda, birinchisi 2-tonga o'zgaradi.\n3+3 → 2+3\nMisol: nǐ(nǐ) + nǐ(hǎo) → nī hǎo (lekin yozilgan: nǐ hǎo)",
                        "rule_tj": "Вақте ки ду тон-3 ҳиҷо дар як саф пайдо мешаванд, аввал ба оҳанги 2 табдил меёбад.\n3+3 → 2+3\nМисол: 你(nǐ) + 好(hǎo) → nī hǎo (вале навишта шудааст: nǐ hǎo)",
                        "rule_ru": "Когда два слога тона 3 появляются подряд, первый меняется на тон 2.\n3+3 → 2+3\nПример: 你(nǐ) + 好(hǎo) → nī hǎo (но пишется: nǐ hǎo)"
                },
                "examples": [
                        {
                                "zh": "你好",
                                "pinyin": "nī hǎo → nǐ hǎo",
                                "meaning": {
                                        "uz": "salom (yozma nǐ hǎo)",
                                        "tj": "салом (навишта nǐ hǎo)",
                                        "ru": "здравствуйте (пишется nϐ hώo)"
                                }
                        },
                        {
                                "zh": "可以",
                                "pinyin": "ké yǐ → kě yǐ",
                                "meaning": {
                                        "uz": "mumkin, mumkin",
                                        "tj": "мумкин, мумкин",
                                        "ru": "может, может"
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
                                        "uz": "Salom! (tasodifiy)",
                                        "tj": "Салом! (тасодуфӣ)",
                                        "ru": "Привет! (повседневный)"
                                },
                                "answer": "你好！",
                                "pinyin": "Nǐ hǎo!"
                        },
                        {
                                "prompt": {
                                        "uz": "Salom! (rasmiy)",
                                        "tj": "Салом! (расмӣ)",
                                        "ru": "Привет! (официальный)"
                                },
                                "answer": "您好！",
                                "pinyin": "Nín hǎo!"
                        },
                        {
                                "prompt": {
                                        "uz": "Kechirasiz!",
                                        "tj": "Бубахшед!",
                                        "ru": "Извини!"
                                },
                                "answer": "对不起！",
                                "pinyin": "Duìbuqǐ!"
                        },
                        {
                                "prompt": {
                                        "uz": "Hammasi joyida!",
                                        "tj": "Масъалае нест!",
                                        "ru": "Без проблем!"
                                },
                                "answer": "没关系！",
                                "pinyin": "Méi guānxi!"
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
                                "prompt": "A: 你___！  B: 你好！",
                                "answer": "好",
                                "pinyin": "hǎo"
                        },
                        {
                                "prompt": "A: 对不起！  B: ___！",
                                "answer": "没关系",
                                "pinyin": "méi guānxi"
                        },
                        {
                                "prompt": "一个老师对很多学生说: ___好！",
                                "answer": "你们",
                                "pinyin": "nǐmen"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "你好！",
                        "您好！",
                        "对不起！",
                        "没关系！"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "好",
                        "没关系",
                        "你们"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Quyidagi so‘zlardan foydalangan holda 2 ta dialog yozing (yozma):",
                        "tj": "Бо истифода аз калимаҳои зерин 2 муколама нависед (хаттӣ):",
                        "ru": "Напишите 2 диалога, используя следующие слова (письменно):"
                },
                "words": [
                        "你好",
                        "您好",
                        "对不起",
                        "没关系"
                ],
                "example": "A: 对不起！B: 没关系！"
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Ohanglarni mashq qiling va ularni baland ovozda ayting:",
                        "tj": "Оҳангҳоро машқ кунед ва онҳоро бо овози баланд бигӯед:",
                        "ru": "Потренируйтесь произносить интонации и произносите их вслух:"
                },
                "words": [
                        {
                                "zh": "妈",
                                "pinyin": "mā",
                                "meaning": "mother"
                        },
                        {
                                "zh": "马",
                                "pinyin": "mǎ",
                                "meaning": "horse"
                        },
                        {
                                "zh": "骂",
                                "pinyin": "mà",
                                "meaning": "to scold"
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
