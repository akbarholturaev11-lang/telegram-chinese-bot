import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 10,
    "lesson_code": "HSK3-L10",
    "title": "数学比历史难多了",
    "goal": json.dumps({"uz": "taqqoslash va darajadagi farqni ifodalash", "ru": "выражение сравнения и различия по степени", "tj": "ифода кардани муқоиса ва фарқ дар дараҷа"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda taqqoslash va darajadagi farqni ifodalash o'rgatiladi. 5 ta asosiy so'z va 比较句 2：A 比 B + Adj + 一点儿/一些/得多/多了 hamda 概数的表达 1 grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению сравнения и различия по степени. Вводятся 5 ключевых слов и грамматические конструкции 比较句 2：A 比 B + Adj + 一点儿/一些/得多/多了 и 概数的表达 1.", "tj": "Ин дарс ба ифода кардани муқоиса ва фарқ дар дараҷа бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии 比较句 2：A 比 B + Adj + 一点儿/一些/得多/多了 ва 概数的表达 1 омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "数学",
                        "pinyin": "shùxué",
                        "pos": "n.",
                        "uz": "matematika",
                        "ru": "математика",
                        "tj": "математика"
                },
                {
                        "no": 2,
                        "zh": "历史",
                        "pinyin": "lìshǐ",
                        "pos": "n.",
                        "uz": "tarix",
                        "ru": "история",
                        "tj": "таърих"
                },
                {
                        "no": 3,
                        "zh": "体育",
                        "pinyin": "tǐyù",
                        "pos": "n.",
                        "uz": "jismoniy tarbiya; sport",
                        "ru": "физкультура; спорт",
                        "tj": "тарбияи ҷисмонӣ; варзиш"
                },
                {
                        "no": 4,
                        "zh": "自行车",
                        "pinyin": "zìxíngchē",
                        "pos": "n.",
                        "uz": "velosiped",
                        "ru": "велосипед",
                        "tj": "велосипед"
                },
                {
                        "no": 5,
                        "zh": "附近",
                        "pinyin": "fùjìn",
                        "pos": "n.",
                        "uz": "yaqin atrofda; yaqinida",
                        "ru": "рядом; поблизости",
                        "tj": "дар наздикӣ; дар атроф"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Fanlar haqida",
                        "scene_ru": "О предметах",
                        "scene_tj": "Дар бораи фанҳо",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "数学比历史难多了。",
                                        "pinyin": "Shùxué bǐ lìshǐ nán duō le.",
                                        "uz": "Matematika tarixdan ancha qiyin.",
                                        "ru": "Математика намного сложнее истории.",
                                        "tj": "Математика нисбат ба таърих хеле душвортар аст."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我觉得体育比数学轻松一些。",
                                        "pinyin": "Wǒ juéde tǐyù bǐ shùxué qīngsōng yīxiē.",
                                        "uz": "Menimcha, jismoniy tarbiya matematikadan biroz osonroq.",
                                        "ru": "Мне кажется, физкультура немного легче математики.",
                                        "tj": "Ба назарам тарбияи ҷисмонӣ аз математика каме осонтар аст."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Yo'lda",
                        "scene_ru": "В дороге",
                        "scene_tj": "Дар роҳ",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "学校离你家远吗？",
                                        "pinyin": "Xuéxiào lí nǐ jiā yuǎn ma?",
                                        "uz": "Maktab uyingizdan uzoqmi?",
                                        "ru": "Школа далеко от твоего дома?",
                                        "tj": "Мактаб аз хонаи шумо дур аст?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "不太远，骑自行车二十分钟左右。",
                                        "pinyin": "Bú tài yuǎn, qí zìxíngchē èrshí fēnzhōng zuǒyòu.",
                                        "uz": "Unchalik emas, velosipedda taxminan yigirma daqiqa.",
                                        "ru": "Не очень — примерно двадцать минут на велосипеде.",
                                        "tj": "Не он қадар дур, тақрибан бист дақиқа бо велосипед."
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
                        "title_zh": "比较句 2：A 比 B + Adj + 一点儿/一些/得多/多了",
                        "title_uz": "Taqqoslash 2: A, B dan + sifat + biroz/ancha",
                        "title_ru": "Сравнение 2: A + Прил + немного/намного + чем B",
                        "title_tj": "Муқоиса 2: A аз B + сифат + каме/хеле",
                        "rule_uz": "Bu shakl ikki narsa yoki shaxsni darajasi bo'yicha taqqoslashda, farqini ifodalashda ishlatiladi.",
                        "rule_ru": "Эта конструкция используется для сравнения двух предметов или людей по степени признака с указанием разницы.",
                        "rule_tj": "Ин намуна барои муқоисаи ду чиз ё шахс аз рӯи дараҷа ва нишон додани фарқ истифода мешавад.",
                        "examples": [
                                {
                                        "zh": "数学比历史难多了。",
                                        "pinyin": "Shùxué bǐ lìshǐ nán duō le.",
                                        "uz": "Matematika tarixdan ancha qiyin.",
                                        "ru": "Математика намного сложнее истории.",
                                        "tj": "Математика нисбат ба таърих хеле душвортар аст."
                                },
                                {
                                        "zh": "今天比昨天冷一点儿。",
                                        "pinyin": "Jīntiān bǐ zuótiān lěng yīdiǎnr.",
                                        "uz": "Bugun kechagidan biroz sovuqroq.",
                                        "ru": "Сегодня немного холоднее, чем вчера.",
                                        "tj": "Имрӯз аз дирӯз каме сардтар аст."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "概数的表达 1",
                        "title_uz": "Taxminiy sonlar ifodalash 1",
                        "title_ru": "Выражение приблизительных чисел 1",
                        "title_tj": "Ифода кардани рақамҳои тахминӣ 1",
                        "rule_uz": "Bu mavzu taxminiy raqam yoki vaqtni ifodalashda ishlatiladi.",
                        "rule_ru": "Эта тема помогает выражать приблизительные числа или время.",
                        "rule_tj": "Ин мавзӯ барои ифода кардани рақамҳо ё вақти тахминӣ кӯмак мекунад.",
                        "examples": [
                                {
                                        "zh": "骑自行车二十分钟左右。",
                                        "pinyin": "Qí zìxíngchē èrshí fēnzhōng zuǒyòu.",
                                        "uz": "Velosipedda taxminan yigirma daqiqa.",
                                        "ru": "Примерно двадцать минут на велосипеде.",
                                        "tj": "Тақрибан бист дақиқа бо велосипед."
                                },
                                {
                                        "zh": "他有三四个朋友。",
                                        "pinyin": "Tā yǒu sān sì gè péngyou.",
                                        "uz": "Uning uch-to'rtta do'sti bor.",
                                        "ru": "У него три-четыре друга.",
                                        "tj": "Вай се-чор дӯст дорад."
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
                                        "prompt_uz": "matematika",
                                        "prompt_ru": "математика",
                                        "prompt_tj": "математика",
                                        "answer": "数学",
                                        "pinyin": "shùxué"
                                },
                                {
                                        "prompt_uz": "tarix",
                                        "prompt_ru": "история",
                                        "prompt_tj": "таърих",
                                        "answer": "历史",
                                        "pinyin": "lìshǐ"
                                },
                                {
                                        "prompt_uz": "jismoniy tarbiya; sport",
                                        "prompt_ru": "физкультура; спорт",
                                        "prompt_tj": "тарбияи ҷисмонӣ; варзиш",
                                        "answer": "体育",
                                        "pinyin": "tǐyù"
                                },
                                {
                                        "prompt_uz": "velosiped",
                                        "prompt_ru": "велосипед",
                                        "prompt_tj": "велосипед",
                                        "answer": "自行车",
                                        "pinyin": "zìxíngchē"
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
                                        "prompt_uz": "数学",
                                        "prompt_ru": "数学",
                                        "prompt_tj": "数学",
                                        "answer": "matematika / математика / математика",
                                        "pinyin": "shùxué"
                                },
                                {
                                        "prompt_uz": "历史",
                                        "prompt_ru": "历史",
                                        "prompt_tj": "历史",
                                        "answer": "tarix / история / таърих",
                                        "pinyin": "lìshǐ"
                                },
                                {
                                        "prompt_uz": "体育",
                                        "prompt_ru": "体育",
                                        "prompt_tj": "体育",
                                        "answer": "jismoniy tarbiya / физкультура / тарбияи ҷисмонӣ",
                                        "pinyin": "tǐyù"
                                },
                                {
                                        "prompt_uz": "自行车",
                                        "prompt_ru": "自行车",
                                        "prompt_tj": "自行车",
                                        "answer": "velosiped / велосипед / велосипед",
                                        "pinyin": "zìxíngchē"
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
                        "answers": ["数学", "历史", "体育", "自行车"]
                },
                {
                        "no": 2,
                        "answers": [
                                "matematika / математика / математика",
                                "tarix / история / таърих",
                                "jismoniy tarbiya / физкультура / тарбияи ҷисмонӣ",
                                "velosiped / велосипед / велосипед"
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
                        "words": ["数学", "历史", "体育"],
                        "example": "数学比历史难多了，但体育很轻松。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Matematika tarixdan ancha qiyin",
                        "topic_ru": "Математика намного сложнее истории",
                        "topic_tj": "Математика нисбат ба таърих хеле душвортар аст"
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
