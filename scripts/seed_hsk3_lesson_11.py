import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 11,
    "lesson_code": "HSK3-L11",
    "title": "别忘了把空调关了",
    "goal": "eslatma berish va “把” gapini ishlatish",
    "intro_text": "Bu dars eslatma berish va “把” gapini ishlatishga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda “把”字句 1：A 把 B + V + …… va 概数的表达 2：左右 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "空调",
                        "pinyin": "kōngtiáo",
                        "pos": "n.",
                        "meaning": "konditsioner"
                },
                {
                        "no": 2,
                        "zh": "图书馆",
                        "pinyin": "túshūguǎn",
                        "pos": "n.",
                        "meaning": "kutubxona"
                },
                {
                        "no": 3,
                        "zh": "词典",
                        "pinyin": "cídiǎn",
                        "pos": "n.",
                        "meaning": "lug'at"
                },
                {
                        "no": 4,
                        "zh": "地铁",
                        "pinyin": "dìtiě",
                        "pos": "n.",
                        "meaning": "metro"
                },
                {
                        "no": 5,
                        "zh": "关",
                        "pinyin": "guān",
                        "pos": "v.",
                        "meaning": "yopmoq, o'chirmoq"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Before leaving",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "别忘了把空调关了。",
                                        "pinyin": "",
                                        "translation": "Konditsionerni o'chirishni unutma."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我把门也关上。",
                                        "pinyin": "",
                                        "translation": "Xo'p, eshikni ham yopaman."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "At the library",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你要借这本词典吗？",
                                        "pinyin": "",
                                        "translation": "Sen bu lug'atni olmoqchimisan?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "要，坐地铁过去大概二十分钟左右。",
                                        "pinyin": "",
                                        "translation": "Ha, metro bilan taxminan yigirma daqiqada yetaman."
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
                        "title_zh": "“把”字句 1：A 把 B + V + ……",
                        "explanation": "Bu tuzilma ta'sir qilinayotgan ob'ektni oldinga chiqarib, natijani yoki yo'nalishni ta'kidlaydi.",
                        "examples": [
                                {
                                        "zh": "别忘了把空调关了。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi qolip namunasi."
                                },
                                {
                                        "zh": "请把空调放这儿。",
                                        "pinyin": "",
                                        "meaning": "Iltimos, 空调ni bu yerga qo'ying."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "概数的表达 2：左右",
                        "explanation": "Bu mavzu taxminiy son yoki vaqtni yumshoq usulda ifodalashga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "别忘了把空调关了。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有空调和图书馆。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 空调 va 图书馆 ishlatilgan."
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
                                        "prompt": "konditsioner",
                                        "answer": "空调",
                                        "pinyin": "kōngtiáo"
                                },
                                {
                                        "prompt": "kutubxona",
                                        "answer": "图书馆",
                                        "pinyin": "túshūguǎn"
                                },
                                {
                                        "prompt": "lug'at",
                                        "answer": "词典",
                                        "pinyin": "cídiǎn"
                                },
                                {
                                        "prompt": "metro",
                                        "answer": "地铁",
                                        "pinyin": "dìtiě"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "空调",
                                        "answer": "konditsioner",
                                        "pinyin": "kōngtiáo"
                                },
                                {
                                        "prompt": "图书馆",
                                        "answer": "kutubxona",
                                        "pinyin": "túshūguǎn"
                                },
                                {
                                        "prompt": "词典",
                                        "answer": "lug'at",
                                        "pinyin": "cídiǎn"
                                },
                                {
                                        "prompt": "地铁",
                                        "answer": "metro",
                                        "pinyin": "dìtiě"
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
                                "空调",
                                "图书馆",
                                "词典",
                                "地铁"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "konditsioner",
                                "kutubxona",
                                "lug'at",
                                "metro"
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
                                "空调",
                                "图书馆",
                                "词典"
                        ],
                        "example": "空调 和 图书馆 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "别忘了把空调关了"
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
