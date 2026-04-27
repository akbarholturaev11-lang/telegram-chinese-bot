import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 8,
    "lesson_code": "HSK3-L08",
    "title": "你去哪儿我就去哪儿",
    "goal": "freely using interrogative pronouns and expressing direction",
    "intro_text": 'This lesson is dedicated to freely using interrogative pronouns and expressing direction. It introduces 5 key vocabulary words and covers core grammar patterns such as "又"和"再" and 疑问代词活用 1.',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "熊猫",
                        "pinyin": "xióngmāo",
                        "pos": "n.",
                        "meaning": "panda"
                },
                {
                        "no": 2,
                        "zh": "电梯",
                        "pinyin": "diàntī",
                        "pos": "n.",
                        "meaning": "elevator / lift"
                },
                {
                        "no": 3,
                        "zh": "洗手间",
                        "pinyin": "xǐshǒujiān",
                        "pos": "n.",
                        "meaning": "restroom / bathroom"
                },
                {
                        "no": 4,
                        "zh": "马上",
                        "pinyin": "mǎshàng",
                        "pos": "adv.",
                        "meaning": "immediately / right away"
                },
                {
                        "no": 5,
                        "zh": "健康",
                        "pinyin": "jiànkāng",
                        "pos": "adj./n.",
                        "meaning": "healthy; health"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Going together",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你去哪儿我就去哪儿。",
                                        "pinyin": "",
                                        "translation": "Wherever you go, I'll go too."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "那我们先去看熊猫吧。",
                                        "pinyin": "",
                                        "translation": "Then let's go see the pandas first."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "In a building",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你害怕坐电梯吗？",
                                        "pinyin": "",
                                        "translation": "Are you afraid of taking the elevator?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "不害怕，我马上就上去。",
                                        "pinyin": "",
                                        "translation": "No, I'll go up right away."
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
                        "title_zh": '"又"和"再"',

                        "explanation": "This grammar topic helps practice the core sentence patterns used in the lesson.",
                        "examples": [
                                {
                                        "zh": "你去哪儿我就去哪儿。",
                                        "pinyin": "",
                                        "meaning": "The key pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有熊猫和电梯。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 熊猫 and 电梯."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "疑问代词活用 1",
                        "explanation": "This topic shows how interrogative pronouns can be used in a general or open-ended sense.",
                        "examples": [
                                {
                                        "zh": "你去哪儿我就去哪儿。",
                                        "pinyin": "",
                                        "meaning": "Wherever you go, I'll go too."
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
                                        "prompt": "panda",
                                        "answer": "熊猫",
                                        "pinyin": "xióngmāo"
                                },
                                {
                                        "prompt": "elevator / lift",
                                        "answer": "电梯",
                                        "pinyin": "diàntī"
                                },
                                {
                                        "prompt": "restroom / bathroom",
                                        "answer": "洗手间",
                                        "pinyin": "xǐshǒujiān"
                                },
                                {
                                        "prompt": "immediately / right away",
                                        "answer": "马上",
                                        "pinyin": "mǎshàng"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "熊猫",
                                        "answer": "panda",
                                        "pinyin": "xióngmāo"
                                },
                                {
                                        "prompt": "电梯",
                                        "answer": "elevator / lift",
                                        "pinyin": "diàntī"
                                },
                                {
                                        "prompt": "洗手间",
                                        "answer": "restroom / bathroom",
                                        "pinyin": "xǐshǒujiān"
                                },
                                {
                                        "prompt": "马上",
                                        "answer": "immediately / right away",
                                        "pinyin": "mǎshàng"
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
                                "熊猫",
                                "电梯",
                                "洗手间",
                                "马上"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "panda",
                                "elevator / lift",
                                "restroom / bathroom",
                                "immediately / right away"
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
                {
                        "no": 1,
                        "instruction": "Write 3 sentences using the following words:",
                        "words": [
                                "熊猫",
                                "电梯",
                                "洗手间"
                        ],
                        "example": "熊猫 和 电梯 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short passage of 4–5 sentences about the lesson topic:",
                        "topic": "你去哪儿我就去哪儿"
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
