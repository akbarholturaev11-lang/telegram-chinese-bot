import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 12,
    "lesson_code": "HSK3-L12",
    "title": "把重要的东西放在我这儿吧",
    "goal": "narsani bir joyda qoldirish va berishni ifodalash",
    "intro_text": "Bu dars narsani bir joyda qoldirish va berishni ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda “才”和“就” va “把”字句 2：A 把 B + V + 在/到/给…… kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "行李箱",
                        "pinyin": "xínglixiāng",
                        "pos": "n.",
                        "meaning": "chamadon"
                },
                {
                        "no": 2,
                        "zh": "护照",
                        "pinyin": "hùzhào",
                        "pos": "n.",
                        "meaning": "pasport"
                },
                {
                        "no": 3,
                        "zh": "起飞",
                        "pinyin": "qǐfēi",
                        "pos": "v.",
                        "meaning": "uchib ketmoq"
                },
                {
                        "no": 4,
                        "zh": "司机",
                        "pinyin": "sījī",
                        "pos": "n.",
                        "meaning": "haydovchi"
                },
                {
                        "no": 5,
                        "zh": "黑板",
                        "pinyin": "hēibǎn",
                        "pos": "n.",
                        "meaning": "doska"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "At the airport",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "把重要的东西放在我这儿吧。",
                                        "pinyin": "",
                                        "translation": "Muhim narsalarni mening yonimda qoldir."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，护照和票我先给你。",
                                        "pinyin": "",
                                        "translation": "Xo'p, pasport bilan biletni avval senga beraman."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Before class",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "司机什么时候到？",
                                        "pinyin": "",
                                        "translation": "Haydovchi qachon keladi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "他到了以后，我们就出发。",
                                        "pinyin": "",
                                        "translation": "U kelganidan keyin yo'lga chiqamiz."
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
                        "title_zh": "“才”和“就”",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "把重要的东西放在我这儿吧。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有行李箱和护照。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 行李箱 va 护照 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "“把”字句 2：A 把 B + V + 在/到/给……",
                        "explanation": "Bu tuzilma ta'sir qilinayotgan ob'ektni oldinga chiqarib, natijani yoki yo'nalishni ta'kidlaydi.",
                        "examples": [
                                {
                                        "zh": "把重要的东西放在我这儿吧。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi qolip namunasi."
                                },
                                {
                                        "zh": "请把行李箱放这儿。",
                                        "pinyin": "",
                                        "meaning": "Iltimos, 行李箱ni bu yerga qo'ying."
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
                                        "prompt": "chamadon",
                                        "answer": "行李箱",
                                        "pinyin": "xínglixiāng"
                                },
                                {
                                        "prompt": "pasport",
                                        "answer": "护照",
                                        "pinyin": "hùzhào"
                                },
                                {
                                        "prompt": "uchib ketmoq",
                                        "answer": "起飞",
                                        "pinyin": "qǐfēi"
                                },
                                {
                                        "prompt": "haydovchi",
                                        "answer": "司机",
                                        "pinyin": "sījī"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "行李箱",
                                        "answer": "chamadon",
                                        "pinyin": "xínglixiāng"
                                },
                                {
                                        "prompt": "护照",
                                        "answer": "pasport",
                                        "pinyin": "hùzhào"
                                },
                                {
                                        "prompt": "起飞",
                                        "answer": "uchib ketmoq",
                                        "pinyin": "qǐfēi"
                                },
                                {
                                        "prompt": "司机",
                                        "answer": "haydovchi",
                                        "pinyin": "sījī"
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
                                "行李箱",
                                "护照",
                                "起飞",
                                "司机"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "chamadon",
                                "pasport",
                                "uchib ketmoq",
                                "haydovchi"
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
                                "行李箱",
                                "护照",
                                "起飞"
                        ],
                        "example": "行李箱 和 护照 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "把重要的东西放在我这儿吧"
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
