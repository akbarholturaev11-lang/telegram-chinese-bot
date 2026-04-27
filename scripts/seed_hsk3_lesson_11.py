import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 11,
    "lesson_code": "HSK3-L11",
    "title": "别忘了把空调关了",
    "goal": "giving reminders and using the 把 sentence structure",
    "intro_text": 'This lesson is dedicated to giving reminders and using the 把 sentence structure. It uses 5 key vocabulary words and covers core grammar patterns such as "把"字句 1：A 把 B + V + …… and 概数的表达 2：左右.',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "空调",
                        "pinyin": "kōngtiáo",
                        "pos": "n.",
                        "meaning": "air conditioner"
                },
                {
                        "no": 2,
                        "zh": "图书馆",
                        "pinyin": "túshūguǎn",
                        "pos": "n.",
                        "meaning": "library"
                },
                {
                        "no": 3,
                        "zh": "词典",
                        "pinyin": "cídiǎn",
                        "pos": "n.",
                        "meaning": "dictionary"
                },
                {
                        "no": 4,
                        "zh": "地铁",
                        "pinyin": "dìtiě",
                        "pos": "n.",
                        "meaning": "subway, metro"
                },
                {
                        "no": 5,
                        "zh": "关",
                        "pinyin": "guān",
                        "pos": "v.",
                        "meaning": "to close, to turn off"
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
                                        "translation": "Don't forget to turn off the air conditioner."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我把门也关上。",
                                        "pinyin": "",
                                        "translation": "Sure, I'll close the door too."
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
                                        "translation": "Do you want to borrow this dictionary?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "要，坐地铁过去大概二十分钟左右。",
                                        "pinyin": "",
                                        "translation": "Yes, it's about twenty minutes by subway."
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
                        "title_zh": '"把"字句 1：A 把 B + V + ……',

                        "explanation": "This structure moves the affected object to the front to emphasise the result or direction.",
                        "examples": [
                                {
                                        "zh": "别忘了把空调关了。",
                                        "pinyin": "",
                                        "meaning": "A sample pattern from the lesson title."
                                },
                                {
                                        "zh": "请把空调放这儿。",
                                        "pinyin": "",
                                        "meaning": "Please put the 空调 here."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "概数的表达 2：左右",
                        "explanation": "This topic helps to express approximate numbers or time in a natural way.",
                        "examples": [
                                {
                                        "zh": "别忘了把空调关了。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有空调和图书馆。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 空调 and 图书馆."
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
                                        "prompt": "air conditioner",
                                        "answer": "空调",
                                        "pinyin": "kōngtiáo"
                                },
                                {
                                        "prompt": "library",
                                        "answer": "图书馆",
                                        "pinyin": "túshūguǎn"
                                },
                                {
                                        "prompt": "dictionary",
                                        "answer": "词典",
                                        "pinyin": "cídiǎn"
                                },
                                {
                                        "prompt": "subway, metro",
                                        "answer": "地铁",
                                        "pinyin": "dìtiě"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "空调",
                                        "answer": "air conditioner",
                                        "pinyin": "kōngtiáo"
                                },
                                {
                                        "prompt": "图书馆",
                                        "answer": "library",
                                        "pinyin": "túshūguǎn"
                                },
                                {
                                        "prompt": "词典",
                                        "answer": "dictionary",
                                        "pinyin": "cídiǎn"
                                },
                                {
                                        "prompt": "地铁",
                                        "answer": "subway, metro",
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
                                "air conditioner",
                                "library",
                                "dictionary",
                                "subway, metro"
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
                                "空调",
                                "图书馆",
                                "词典"
                        ],
                        "example": "空调 和 图书馆 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
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
