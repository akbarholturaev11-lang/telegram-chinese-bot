import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 17,
    "lesson_code": "HSK3-L17",
    "title": '谁都有办法看好你的"病"',

    "goal": "using suggestions, methods, and indefinite pronouns",
    "intro_text": "This lesson focuses on using suggestions, methods, and indefinite pronouns. It uses 5 key vocabulary words and covers the main grammar patterns 双音节动词重叠 and 疑问代词活用 3.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "请假",
                        "pinyin": "qǐngjià",
                        "pos": "v.",
                        "meaning": "to ask for time off"
                },
                {
                        "no": 2,
                        "zh": "邻居",
                        "pinyin": "línjū",
                        "pos": "n.",
                        "meaning": "neighbor"
                },
                {
                        "no": 3,
                        "zh": "办法",
                        "pinyin": "bànfǎ",
                        "pos": "n.",
                        "meaning": "method, way"
                },
                {
                        "no": 4,
                        "zh": "决定",
                        "pinyin": "juédìng",
                        "pos": "v.",
                        "meaning": "to decide"
                },
                {
                        "no": 5,
                        "zh": "根据",
                        "pinyin": "gēnjù",
                        "pos": "prep./n.",
                        "meaning": "based on, according to"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Talking about a problem",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": '谁都有办法看好你的"病"。',

                                        "pinyin": "",
                                        "translation": 'Anyone can find a way to cure your \"illness\".'

                                },
                                {
                                        "speaker": "B",
                                        "zh": "真的吗？那我该怎么办？",
                                        "pinyin": "",
                                        "translation": "Really? So what should I do?"
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Making a decision",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你可以根据医生的话决定。",
                                        "pinyin": "",
                                        "translation": "You can decide based on what the doctor says."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我先请假休息两天。",
                                        "pinyin": "",
                                        "translation": "Okay, I'll ask for two days off to rest first."
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
                        "title_zh": "双音节动词重叠",
                        "explanation": "This topic shows how repeating a verb can soften the tone or make the meaning more natural.",
                        "examples": [
                                {
                                        "zh": '谁都有办法看好你的"病"。',

                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有请假和邻居。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 请假 and 邻居."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "疑问代词活用 3",
                        "explanation": "This topic shows how question pronouns can be used with a general or indefinite meaning.",
                        "examples": [
                                {
                                        "zh": "你去哪儿我就去哪儿。",
                                        "pinyin": "",
                                        "meaning": "Wherever you go, I'll go there too."
                                },
                                {
                                        "zh": "谁都可以参加。",
                                        "pinyin": "",
                                        "meaning": "Anyone can participate."
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
                                        "prompt": "to ask for time off",
                                        "answer": "请假",
                                        "pinyin": "qǐngjià"
                                },
                                {
                                        "prompt": "neighbor",
                                        "answer": "邻居",
                                        "pinyin": "línjū"
                                },
                                {
                                        "prompt": "method, way",
                                        "answer": "办法",
                                        "pinyin": "bànfǎ"
                                },
                                {
                                        "prompt": "to decide",
                                        "answer": "决定",
                                        "pinyin": "juédìng"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "请假",
                                        "answer": "to ask for time off",
                                        "pinyin": "qǐngjià"
                                },
                                {
                                        "prompt": "邻居",
                                        "answer": "neighbor",
                                        "pinyin": "línjū"
                                },
                                {
                                        "prompt": "办法",
                                        "answer": "method, way",
                                        "pinyin": "bànfǎ"
                                },
                                {
                                        "prompt": "决定",
                                        "answer": "to decide",
                                        "pinyin": "juédìng"
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
                                "请假",
                                "邻居",
                                "办法",
                                "决定"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "to ask for time off",
                                "neighbor",
                                "method, way",
                                "to decide"
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
                                "请假",
                                "邻居",
                                "办法"
                        ],
                        "example": "请假 和 邻居 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short text of 4-5 sentences about the lesson topic:",
                        "topic": '谁都有办法看好你的"病"'

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
