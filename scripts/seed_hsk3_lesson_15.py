import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 15,
    "lesson_code": "HSK3-L15",
    "title": "其他都没什么问题",
    "goal": json.dumps({"uz": "istisnolar, qolgan narsalar va darajani ifodalash", "ru": "выражение исключений, оставшегося и степени", "tj": "ифода кардани истисноҳо, боқимондаҳо ва дараҷа"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda istisnolar, qolgan narsalar va darajani ifodalash o'rgatiladi. 5 ta asosiy so'z va 除了……以外，都/还/也…… hamda 程度的表达：极了 grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению исключений, оставшегося и степени. Вводятся 5 ключевых слов и грамматические конструкции 除了……以外，都/还/也…… и 程度的表达：极了.", "tj": "Ин дарс ба ифода кардани истисноҳо, боқимондаҳо ва дараҷа бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии 除了……以外，都/还/也…… ва 程度的表达：极了 омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "留学",
                        "pinyin": "liúxué",
                        "pos": "v.",
                        "uz": "chet elda o'qimoq",
                        "ru": "учиться за рубежом",
                        "tj": "дар хориҷа таҳсил кардан"
                },
                {
                        "no": 2,
                        "zh": "水平",
                        "pinyin": "shuǐpíng",
                        "pos": "n.",
                        "uz": "daraja; saviya",
                        "ru": "уровень; стандарт",
                        "tj": "сатҳ; дараҷа"
                },
                {
                        "no": 3,
                        "zh": "提高",
                        "pinyin": "tígāo",
                        "pos": "v.",
                        "uz": "yaxshilamoq; oshirmoq",
                        "ru": "улучшать; повышать",
                        "tj": "беҳтар кардан; баланд бардоштан"
                },
                {
                        "no": 4,
                        "zh": "新闻",
                        "pinyin": "xīnwén",
                        "pos": "n.",
                        "uz": "yangilik; xabar",
                        "ru": "новости",
                        "tj": "хабар; ахбор"
                },
                {
                        "no": 5,
                        "zh": "文化",
                        "pinyin": "wénhuà",
                        "pos": "n.",
                        "uz": "madaniyat",
                        "ru": "культура",
                        "tj": "фарҳанг"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Rejani tekshirish",
                        "scene_ru": "Проверка плана",
                        "scene_tj": "Санҷиши нақша",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "其他都没什么问题。",
                                        "pinyin": "Qítā dōu méi shénme wèntí.",
                                        "uz": "Qolgan hamma narsa yaxshi.",
                                        "ru": "В остальном всё нормально.",
                                        "tj": "Дигар ҳама чиз хуб аст."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "那我们就按计划进行吧。",
                                        "pinyin": "Nà wǒmen jiù àn jìhuà jìnxíng ba.",
                                        "uz": "Unda rejaga muvofiq davom etamiz.",
                                        "ru": "Тогда будем действовать по плану.",
                                        "tj": "Пас мувофиқи нақша идома медиҳем."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Chet elda ta'lim",
                        "scene_ru": "Учёба за рубежом",
                        "scene_tj": "Таҳсил дар хориҷа",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "除了语言以外，你还担心什么？",
                                        "pinyin": "Chúle yǔyán yǐwài, nǐ hái dānxīn shénme?",
                                        "uz": "Til tashqari, yana nima haqida xavotirlanasiz?",
                                        "ru": "Помимо языка, о чём ещё беспокоишься?",
                                        "tj": "Ғайр аз забон, боз аз чӣ нигаронед?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我最想提高自己的文化水平。",
                                        "pinyin": "Wǒ zuì xiǎng tígāo zìjǐ de wénhuà shuǐpíng.",
                                        "uz": "Men eng ko'p o'z madaniy saviyamni yaxshilashni xohlayman.",
                                        "ru": "Больше всего я хочу повысить свой культурный уровень.",
                                        "tj": "Ман бештар мехоҳам сатҳи фарҳангии худро баланд бардорам."
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
                        "title_zh": "除了……以外，都/还/也……",
                        "title_uz": "……dan tashqari, hammasi/ham/yana……",
                        "title_ru": "Кроме……, все/тоже/ещё……",
                        "title_tj": "Ғайр аз……, ҳама/ҳам/боз……",
                        "rule_uz": "Bu grammatik shakl istisnoni yoki qo'shimchani ifodalaydi.",
                        "rule_ru": "Эта конструкция выражает исключение или дополнение.",
                        "rule_tj": "Ин намуна истисно ё иловаро ифода мекунад.",
                        "examples": [
                                {
                                        "zh": "除了语言以外，我还担心文化差异。",
                                        "pinyin": "Chúle yǔyán yǐwài, wǒ hái dānxīn wénhuà chāyì.",
                                        "uz": "Tildan tashqari, men madaniy farqlardan ham xavotirlanaman.",
                                        "ru": "Помимо языка, я ещё беспокоюсь о культурных различиях.",
                                        "tj": "Ғайр аз забон, ман аз фарқҳои фарҳангӣ ҳам нигаронам."
                                },
                                {
                                        "zh": "除了他以外，大家都来了。",
                                        "pinyin": "Chúle tā yǐwài, dàjiā dōu lái le.",
                                        "uz": "Undan tashqari, hammasi keldi.",
                                        "ru": "Кроме него, все пришли.",
                                        "tj": "Ғайр аз вай, ҳама омаданд."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "程度的表达：极了",
                        "title_uz": "Darajani ifodalash: 极了 (juda/nihoyatda)",
                        "title_ru": "Выражение степени: 极了 (крайне/очень)",
                        "title_tj": "Ифода кардани дараҷа: 极了 (хеле/бениҳоят)",
                        "rule_uz": "极了 sifat yoki hol so'zidan keyin kelib, o'ta yuqori darajani bildiradi.",
                        "rule_ru": "极了 стоит после прилагательного или наречия и выражает крайнюю степень.",
                        "rule_tj": "极了 пас аз сифат ё зарф меояд ва дараҷаи ниҳоии баландро ифода мекунад.",
                        "examples": [
                                {
                                        "zh": "这里的文化有趣极了。",
                                        "pinyin": "Zhèlǐ de wénhuà yǒuqù jí le.",
                                        "uz": "Bu yerdagi madaniyat nihoyatda qiziq.",
                                        "ru": "Культура здесь крайне интересна.",
                                        "tj": "Фарҳанги ин ҷо бениҳоят ҷолиб аст."
                                },
                                {
                                        "zh": "今天的新闻重要极了。",
                                        "pinyin": "Jīntiān de xīnwén zhòngyào jí le.",
                                        "uz": "Bugungi yangiliklar nihoyatda muhim.",
                                        "ru": "Сегодняшние новости крайне важны.",
                                        "tj": "Хабарҳои имрӯза бениҳоят муҳим аст."
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
                        "instruction_uz": "Quyidagi so'zlarni xitoycha yozing:",
                        "instruction_ru": "Напишите китайский для следующих слов:",
                        "instruction_tj": "Калимаҳои зеринро ба хитоӣ нависед:",
                        "items": [
                                {
                                        "prompt_uz": "chet elda o'qimoq",
                                        "prompt_ru": "учиться за рубежом",
                                        "prompt_tj": "дар хориҷа таҳсил кардан",
                                        "answer": "留学",
                                        "pinyin": "liúxué"
                                },
                                {
                                        "prompt_uz": "daraja; saviya",
                                        "prompt_ru": "уровень; стандарт",
                                        "prompt_tj": "сатҳ; дараҷа",
                                        "answer": "水平",
                                        "pinyin": "shuǐpíng"
                                },
                                {
                                        "prompt_uz": "yaxshilamoq; oshirmoq",
                                        "prompt_ru": "улучшать; повышать",
                                        "prompt_tj": "беҳтар кардан; баланд бардоштан",
                                        "answer": "提高",
                                        "pinyin": "tígāo"
                                },
                                {
                                        "prompt_uz": "yangilik; xabar",
                                        "prompt_ru": "новости",
                                        "prompt_tj": "хабар; ахбор",
                                        "answer": "新闻",
                                        "pinyin": "xīnwén"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction_uz": "Quyidagi xitoycha so'zlarni tarjima qiling:",
                        "instruction_ru": "Переведите следующие китайские слова:",
                        "instruction_tj": "Калимаҳои зерини хитоиро тарҷума кунед:",
                        "items": [
                                {
                                        "prompt_uz": "留学",
                                        "prompt_ru": "留学",
                                        "prompt_tj": "留学",
                                        "answer": "chet elda o'qimoq / учиться за рубежом / дар хориҷа таҳсил кардан",
                                        "pinyin": "liúxué"
                                },
                                {
                                        "prompt_uz": "水平",
                                        "prompt_ru": "水平",
                                        "prompt_tj": "水平",
                                        "answer": "daraja / уровень / сатҳ",
                                        "pinyin": "shuǐpíng"
                                },
                                {
                                        "prompt_uz": "提高",
                                        "prompt_ru": "提高",
                                        "prompt_tj": "提高",
                                        "answer": "yaxshilamoq / улучшать / беҳтар кардан",
                                        "pinyin": "tígāo"
                                },
                                {
                                        "prompt_uz": "新闻",
                                        "prompt_ru": "新闻",
                                        "prompt_tj": "新闻",
                                        "answer": "yangilik / новости / хабар",
                                        "pinyin": "xīnwén"
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
                        "answers": ["留学", "水平", "提高", "新闻"]
                },
                {
                        "no": 2,
                        "answers": [
                                "chet elda o'qimoq / учиться за рубежом / дар хориҷа таҳсил кардан",
                                "daraja / уровень / сатҳ",
                                "yaxshilamoq / улучшать / беҳтар кардан",
                                "yangilik / новости / хабар"
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
                        "instruction_tj": "Бо истифода аз калимаҳои зерин 3 ҷумла созед:",
                        "words": ["留学", "水平", "提高"],
                        "example": "留学可以帮助我提高语言水平。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Qolgan hamma narsa yaxshi",
                        "topic_ru": "В остальном всё нормально",
                        "topic_tj": "Дигар ҳама чиз хуб аст"
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
