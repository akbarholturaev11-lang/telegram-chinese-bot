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
    "goal": "describing the location and existence of objects",
    "intro_text": "This lesson is dedicated to describing the location and existence of objects. It uses 5 key vocabulary words and covers core grammar patterns such as 还是 and 或者, and existential expressions.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "饮料",
                        "pinyin": "yǐnliào",
                        "pos": "n.",
                        "meaning": "drink, beverage"
                },
                {
                        "no": 2,
                        "zh": "放",
                        "pinyin": "fàng",
                        "pos": "v.",
                        "meaning": "to put, to place"
                },
                {
                        "no": 3,
                        "zh": "花",
                        "pinyin": "huā",
                        "pos": "n.",
                        "meaning": "flower"
                },
                {
                        "no": 4,
                        "zh": "新鲜",
                        "pinyin": "xīnxiān",
                        "pos": "adj.",
                        "meaning": "fresh"
                },
                {
                        "no": 5,
                        "zh": "或者",
                        "pinyin": "huòzhě",
                        "pos": "conj.",
                        "meaning": "or"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "On the table",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "translation": "There are lots of drinks on the table."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "那边也有花，看起来很新鲜。",
                                        "pinyin": "",
                                        "translation": "There are flowers over there too, they look very fresh."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Choosing drinks",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你想喝茶还是果汁？",
                                        "pinyin": "",
                                        "translation": "Would you like tea or juice?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "果汁或者水都可以。",
                                        "pinyin": "",
                                        "translation": "Either juice or water is fine."
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
                        "explanation": "This grammar topic helps to practice the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有饮料和放。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 饮料 and 放."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "存在的表达",
                        "explanation": "This pattern is used to describe something existing at a location or being positioned somewhere.",
                        "examples": [
                                {
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "meaning": "There are lots of drinks on the table."
                                },
                                {
                                        "zh": "门口站着一个客人。",
                                        "pinyin": "",
                                        "meaning": "There is a guest standing at the door."
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
                        "instruction": "Write the Chinese for the following meanings:",
                        "items": [
                                {
                                        "prompt": "drink, beverage",
                                        "answer": "饮料",
                                        "pinyin": "yǐnliào"
                                },
                                {
                                        "prompt": "to put, to place",
                                        "answer": "放",
                                        "pinyin": "fàng"
                                },
                                {
                                        "prompt": "flower",
                                        "answer": "花",
                                        "pinyin": "huā"
                                },
                                {
                                        "prompt": "fresh",
                                        "answer": "新鲜",
                                        "pinyin": "xīnxiān"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "饮料",
                                        "answer": "drink, beverage",
                                        "pinyin": "yǐnliào"
                                },
                                {
                                        "prompt": "放",
                                        "answer": "to put, to place",
                                        "pinyin": "fàng"
                                },
                                {
                                        "prompt": "花",
                                        "answer": "flower",
                                        "pinyin": "huā"
                                },
                                {
                                        "prompt": "新鲜",
                                        "answer": "fresh",
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
                                "drink, beverage",
                                "to put, to place",
                                "flower",
                                "fresh"
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
                {
                        "no": 1,
                        "instruction": "Make 3 sentences using the following words:",
                        "words": [
                                "饮料",
                                "放",
                                "花"
                        ],
                        "example": "饮料 和 放 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "桌子上放着很多饮料"
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
