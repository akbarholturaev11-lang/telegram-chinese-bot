import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 3,
    "lesson_code": "HSK3-L03",
    "title": "桌子上放着很多饮料",
    "goal": json.dumps({"uz": "narsalarning joylashuvini va mavjudligini tasvirlash", "ru": "описание местонахождения и наличия предметов", "tj": "тавсифи ҷойгиршавӣ ва мавҷудияти ашё"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu dars narsalarning joylashuvini va mavjudligini tasvirlashga bag'ishlangan. Unda 5 ta asosiy so'z o'rganiladi va 还是 va 或者 hamda mavjudlik ifodalash kabi grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён описанию местонахождения и наличия предметов. В нём изучаются 5 ключевых слов и рассматриваются грамматические темы: 还是 и 或者, а также конструкции существования.", "tj": "Ин дарс ба тавсифи ҷойгиршавӣ ва мавҷудияти ашё бахшида шудааст. Дар он 5 калимаи асосӣ омӯхта мешавад ва мавзӯҳои грамматикии 还是 ва 或者 ва инчунин конструксияҳои мавҷудият баррасӣ мегарданд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "饮料",
                        "pinyin": "yǐnliào",
                        "pos": "n.",
                        "uz": "ichimlik, sharbat",
                        "ru": "напиток",
                        "tj": "нӯшокӣ"
                },
                {
                        "no": 2,
                        "zh": "放",
                        "pinyin": "fàng",
                        "pos": "v.",
                        "uz": "qo'ymoq, joylashmoq",
                        "ru": "класть, ставить",
                        "tj": "гузоштан, мондан"
                },
                {
                        "no": 3,
                        "zh": "花",
                        "pinyin": "huā",
                        "pos": "n.",
                        "uz": "gul",
                        "ru": "цветок",
                        "tj": "гул"
                },
                {
                        "no": 4,
                        "zh": "新鲜",
                        "pinyin": "xīnxiān",
                        "pos": "adj.",
                        "uz": "yangi, toza",
                        "ru": "свежий",
                        "tj": "тоза, нав"
                },
                {
                        "no": 5,
                        "zh": "或者",
                        "pinyin": "huòzhě",
                        "pos": "conj.",
                        "uz": "yoki (da'voda emas)",
                        "ru": "или (в повествовании)",
                        "tj": "ё (дар баёни оддӣ)"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Stol ustida",
                        "scene_ru": "На столе",
                        "scene_tj": "Рӯи миз",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "uz": "Stol ustida ko'p ichimlik bor.",
                                        "ru": "На столе стоит много напитков.",
                                        "tj": "Рӯи миз нӯшокиҳои зиёде мавҷуданд."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "那边也有花，看起来很新鲜。",
                                        "pinyin": "",
                                        "uz": "U tomonda ham gul bor, juda yangi ko'rinadi.",
                                        "ru": "Там тоже есть цветы, они выглядят очень свежими.",
                                        "tj": "Он тараф ҳам гул дорад, хеле тоза менамояд."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Ichimlik tanlash",
                        "scene_ru": "Выбор напитка",
                        "scene_tj": "Интихоби нӯшокӣ",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你想喝茶还是果汁？",
                                        "pinyin": "",
                                        "uz": "Choy ichmoqchimisiz yoki sharbat?",
                                        "ru": "Ты хочешь чай или сок?",
                                        "tj": "Чой мехоҳӣ ё шарбат?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "果汁或者水都可以。",
                                        "pinyin": "",
                                        "uz": "Sharbat yoki suv ham bo'ladi.",
                                        "ru": "Сок или вода — подойдёт любое.",
                                        "tj": "Шарбат ё об ҳам мешавад."
                                }
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
                {
                        "no": 1,
                        "title_zh": '"还是"和"或者"',
                        "title_uz": "\"还是\" va \"或者\"",
                        "title_ru": "«还是» и «或者»",
                        "title_tj": "«还是» ва «或者»",
                        "rule_uz": "还是 savolda, 或者 esa da'vo gapda 'yoki' ma'nosini beradi.",
                        "rule_ru": "还是 используется в вопросах, а 或者 — в повествовательных предложениях для значения 'или'.",
                        "rule_tj": "还是 дар суолҳо ва 或者 дар ҷумлаҳои хабарӣ барои маънои 'ё' истифода мешавад.",
                        "examples": [
                                {
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "uz": "Darsning asosiy qolipi.",
                                        "ru": "Основная конструкция урока.",
                                        "tj": "Қолаби асосии дарс."
                                },
                                {
                                        "zh": "这个句子里有饮料和放。",
                                        "pinyin": "",
                                        "uz": "Bu gapda 饮料 va 放 so'zlari bor.",
                                        "ru": "В этом предложении используются слова 饮料 и 放.",
                                        "tj": "Дар ин ҷумла калимаҳои 饮料 ва 放 истифода шудаанд."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "存在的表达",
                        "title_uz": "Mavjudlikni ifodalash",
                        "title_ru": "Выражение существования",
                        "title_tj": "Ифодаи мавҷудият",
                        "rule_uz": "Bu qolip biror narsa ma'lum joyda joylashganligini yoki turganligini tasvirlash uchun ishlatiladi.",
                        "rule_ru": "Этот шаблон используется для описания того, что что-то находится или расположено в определённом месте.",
                        "rule_tj": "Ин қолаб барои тавсифи он ки чизе дар ягон ҷой ҷойгир аст ё меистад, истифода мешавад.",
                        "examples": [
                                {
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "uz": "Stol ustida ko'p ichimlik bor.",
                                        "ru": "На столе стоит много напитков.",
                                        "tj": "Рӯи миз нӯшокиҳои зиёде мавҷуданд."
                                },
                                {
                                        "zh": "门口站着一个客人。",
                                        "pinyin": "",
                                        "uz": "Eshik oldida bir mehmon turmoqda.",
                                        "ru": "У двери стоит гость.",
                                        "tj": "Дар дари вуруд як меҳмон истодааст."
                                }
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "exercise_json": json.dumps(
        [
                {
                        "no": 1,
                        "type": "translate_to_chinese",
                        "instruction_uz": "Quyidagi so'zlarning xitoychasini yozing:",
                        "instruction_ru": "Запишите по-китайски следующие слова:",
                        "instruction_tj": "Калимаҳои зеринро бо хитоӣ нависед:",
                        "items": [
                                {
                                        "prompt_uz": "ichimlik, sharbat",
                                        "prompt_ru": "напиток",
                                        "prompt_tj": "нӯшокӣ",
                                        "answer": "饮料",
                                        "pinyin": "yǐnliào"
                                },
                                {
                                        "prompt_uz": "qo'ymoq, joylashmoq",
                                        "prompt_ru": "класть, ставить",
                                        "prompt_tj": "гузоштан",
                                        "answer": "放",
                                        "pinyin": "fàng"
                                },
                                {
                                        "prompt_uz": "gul",
                                        "prompt_ru": "цветок",
                                        "prompt_tj": "гул",
                                        "answer": "花",
                                        "pinyin": "huā"
                                },
                                {
                                        "prompt_uz": "yangi, toza",
                                        "prompt_ru": "свежий",
                                        "prompt_tj": "тоза, нав",
                                        "answer": "新鲜",
                                        "pinyin": "xīnxiān"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction_uz": "Quyidagi so'zlarning ma'nosini yozing:",
                        "instruction_ru": "Запишите значение следующих слов:",
                        "instruction_tj": "Маънои калимаҳои зеринро нависед:",
                        "items": [
                                {
                                        "prompt_uz": "饮料",
                                        "prompt_ru": "饮料",
                                        "prompt_tj": "饮料",
                                        "answer": "饮料",
                                        "pinyin": "yǐnliào"
                                },
                                {
                                        "prompt_uz": "放",
                                        "prompt_ru": "放",
                                        "prompt_tj": "放",
                                        "answer": "放",
                                        "pinyin": "fàng"
                                },
                                {
                                        "prompt_uz": "花",
                                        "prompt_ru": "花",
                                        "prompt_tj": "花",
                                        "answer": "花",
                                        "pinyin": "huā"
                                },
                                {
                                        "prompt_uz": "新鲜",
                                        "prompt_ru": "新鲜",
                                        "prompt_tj": "新鲜",
                                        "answer": "新鲜",
                                        "pinyin": "xīnxiān"
                                }
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
                {
                        "no": 1,
                        "answers": [
                                "饮料",
                                "放",
                                "花",
                                "新鲜"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "饮料",
                                "放",
                                "花",
                                "新鲜"
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
                {
                        "no": 1,
                        "instruction_uz": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                        "instruction_ru": "Составьте 3 предложения, используя следующие слова:",
                        "instruction_tj": "Бо истифода аз калимаҳои зерин 3 ҷумла тартиб диҳед:",
                        "words": [
                                "饮料",
                                "放",
                                "花"
                        ],
                        "topic_uz": "饮料 va 放 so'zlarini bir gapda ishlatish mumkin.",
                        "topic_ru": "Слова 饮料 и 放 можно использовать в одном предложении.",
                        "topic_tj": "Калимаҳои 饮料 ва 放 метавонанд дар як ҷумла истифода шаванд."
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий абзац из 4-5 предложений по теме урока:",
                        "instruction_tj": "Дар мавзӯи дарс матни кӯтоҳи 4-5 ҷумлагӣ нависед:",
                        "topic_uz": "桌子上放着很多饮料",
                        "topic_ru": "桌子上放着很多饮料",
                        "topic_tj": "桌子上放着很多饮料"
                }
        ],
        ensure_ascii=False,
    ),
    "review_json": "[]",
    "is_active": True
}


async def upsert_lesson():
    async with SessionLocal() as session:
        result = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            for key, value in LESSON.items():
                setattr(existing, key, value)
            print(f"updated: {LESSON['lesson_code']}")
        else:
            session.add(CourseLesson(**LESSON))
            print(f"inserted: {LESSON['lesson_code']}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(upsert_lesson())
