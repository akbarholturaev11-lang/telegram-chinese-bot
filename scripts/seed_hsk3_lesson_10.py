import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 10,
    "lesson_code": "HSK3-L10",
    "title": "数学比历史难多了",
    "goal": "qiyoslash va daraja farqini ko'rsatish",
    "intro_text": "Bu dars qiyoslash va daraja farqini ko'rsatishga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 比较句 2：A 比 B + Adj + 一点儿/一些/得多/多了 va 概数的表达 1 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "数学",
                        "pinyin": "shùxué",
                        "pos": "n.",
                        "meaning": "matematika"
                },
                {
                        "no": 2,
                        "zh": "历史",
                        "pinyin": "lìshǐ",
                        "pos": "n.",
                        "meaning": "tarix"
                },
                {
                        "no": 3,
                        "zh": "体育",
                        "pinyin": "tǐyù",
                        "pos": "n.",
                        "meaning": "jismoniy tarbiya"
                },
                {
                        "no": 4,
                        "zh": "自行车",
                        "pinyin": "zìxíngchē",
                        "pos": "n.",
                        "meaning": "velosiped"
                },
                {
                        "no": 5,
                        "zh": "附近",
                        "pinyin": "fùjìn",
                        "pos": "n.",
                        "meaning": "yaqin atrof"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "About subjects",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "数学比历史难多了。",
                                        "pinyin": "",
                                        "translation": "Matematika tarixdan ancha qiyin."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我觉得体育比数学轻松一些。",
                                        "pinyin": "",
                                        "translation": "Menga ko'ra jismoniy tarbiya matematikadan osonroq."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "On the way",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "学校离你家远吗？",
                                        "pinyin": "",
                                        "translation": "Maktab uyingdan uzoqmi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "不太远，骑自行车二十分钟左右。",
                                        "pinyin": "",
                                        "translation": "Unchalik emas, velosipedda taxminan yigirma daqiqa."
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
                        "explanation": "Bu qolip ikki narsa yoki odamni daraja jihatidan qiyoslash uchun ishlatiladi.",
                        "examples": [
                                {
                                        "zh": "数学比历史难多了。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi qiyoslash namunasi."
                                },
                                {
                                        "zh": "数学比历史更重要。",
                                        "pinyin": "",
                                        "meaning": "数学 历史dan ham muhimroq."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "概数的表达 1",
                        "explanation": "Bu mavzu taxminiy son yoki vaqtni yumshoq usulda ifodalashga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "数学比历史难多了。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有数学和历史。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 数学 va 历史 ishlatilgan."
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
                        "instruction": "Quyidagi ma'nolarning xitoychasini yozing:",
                        "items": [
                                {
                                        "prompt": "matematika",
                                        "answer": "数学",
                                        "pinyin": "shùxué"
                                },
                                {
                                        "prompt": "tarix",
                                        "answer": "历史",
                                        "pinyin": "lìshǐ"
                                },
                                {
                                        "prompt": "jismoniy tarbiya",
                                        "answer": "体育",
                                        "pinyin": "tǐyù"
                                },
                                {
                                        "prompt": "velosiped",
                                        "answer": "自行车",
                                        "pinyin": "zìxíngchē"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "数学",
                                        "answer": "matematika",
                                        "pinyin": "shùxué"
                                },
                                {
                                        "prompt": "历史",
                                        "answer": "tarix",
                                        "pinyin": "lìshǐ"
                                },
                                {
                                        "prompt": "体育",
                                        "answer": "jismoniy tarbiya",
                                        "pinyin": "tǐyù"
                                },
                                {
                                        "prompt": "自行车",
                                        "answer": "velosiped",
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
                        "answers": [
                                "数学",
                                "历史",
                                "体育",
                                "自行车"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "matematika",
                                "tarix",
                                "jismoniy tarbiya",
                                "velosiped"
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
                {
                        "no": 1,
                        "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                        "words": [
                                "数学",
                                "历史",
                                "体育"
                        ],
                        "example": "数学 和 历史 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "数学比历史难多了"
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
            existing.level = LESSON["level"]
            existing.lesson_order = LESSON["lesson_order"]
            existing.title = LESSON["title"]
            existing.goal = LESSON["goal"]
            existing.intro_text = LESSON["intro_text"]
            existing.vocabulary_json = LESSON["vocabulary_json"]
            existing.dialogue_json = LESSON["dialogue_json"]
            existing.grammar_json = LESSON["grammar_json"]
            existing.exercise_json = LESSON["exercise_json"]
            existing.answers_json = LESSON["answers_json"]
            existing.homework_json = LESSON["homework_json"]
            existing.review_json = LESSON["review_json"]
            existing.is_active = LESSON["is_active"]
            print(f"updated: {LESSON['lesson_code']}")
        else:
            session.add(CourseLesson(**LESSON))
            print(f"inserted: {LESSON['lesson_code']}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(upsert_lesson())
