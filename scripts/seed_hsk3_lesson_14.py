import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 14,
    "lesson_code": "HSK3-L14",
    "title": "你把水果拿过来",
    "goal": "expressing commands, sequence, and direction",
    "intro_text": 'This lesson is dedicated to expressing commands, sequence, and direction. It uses 5 key vocabulary words and covers core grammar patterns such as "把"字句 3：A 把 B + V + 结果补语/趋向补语 and 先……，再/又……，然后……',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "水果",
                        "pinyin": "shuǐguǒ",
                        "pos": "n.",
                        "meaning": "fruit"
                },
                {
                        "no": 2,
                        "zh": "打扫",
                        "pinyin": "dǎsǎo",
                        "pos": "v.",
                        "meaning": "to clean, to sweep"
                },
                {
                        "no": 3,
                        "zh": "冰箱",
                        "pinyin": "bīngxiāng",
                        "pos": "n.",
                        "meaning": "refrigerator"
                },
                {
                        "no": 4,
                        "zh": "香蕉",
                        "pinyin": "xiāngjiāo",
                        "pos": "n.",
                        "meaning": "banana"
                },
                {
                        "no": 5,
                        "zh": "月亮",
                        "pinyin": "yuèliang",
                        "pos": "n.",
                        "meaning": "moon"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "In the kitchen",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你把水果拿过来。",
                                        "pinyin": "",
                                        "translation": "Bring the fruit over here."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我先从冰箱里拿出来。",
                                        "pinyin": "",
                                        "translation": "Sure, I'll take it out of the fridge first."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Housework order",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你先打扫桌子，然后洗水果。",
                                        "pinyin": "",
                                        "translation": "Clean the table first, then wash the fruit."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "洗好了以后，我再拿香蕉过来。",
                                        "pinyin": "",
                                        "translation": "After washing them, I'll bring the bananas over."
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
                        "title_zh": '"把"字句 3：A 把 B + V + 结果补语/趋向补语',

                        "explanation": "This pattern indicates that an action has been completed successfully or satisfactorily.",
                        "examples": [
                                {
                                        "zh": "我准备好了。",
                                        "pinyin": "",
                                        "meaning": "I'm ready."
                                },
                                {
                                        "zh": "电影票买好了。",
                                        "pinyin": "",
                                        "meaning": "The movie tickets have been bought."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "先……，再/又……，然后……",
                        "explanation": "This grammar topic helps to practise the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "你把水果拿过来。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有水果和打扫。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 水果 and 打扫."
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
                                        "prompt": "fruit",
                                        "answer": "水果",
                                        "pinyin": "shuǐguǒ"
                                },
                                {
                                        "prompt": "to clean, to sweep",
                                        "answer": "打扫",
                                        "pinyin": "dǎsǎo"
                                },
                                {
                                        "prompt": "refrigerator",
                                        "answer": "冰箱",
                                        "pinyin": "bīngxiāng"
                                },
                                {
                                        "prompt": "banana",
                                        "answer": "香蕉",
                                        "pinyin": "xiāngjiāo"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "水果",
                                        "answer": "fruit",
                                        "pinyin": "shuǐguǒ"
                                },
                                {
                                        "prompt": "打扫",
                                        "answer": "to clean, to sweep",
                                        "pinyin": "dǎsǎo"
                                },
                                {
                                        "prompt": "冰箱",
                                        "answer": "refrigerator",
                                        "pinyin": "bīngxiāng"
                                },
                                {
                                        "prompt": "香蕉",
                                        "answer": "banana",
                                        "pinyin": "xiāngjiāo"
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
                                "水果",
                                "打扫",
                                "冰箱",
                                "香蕉"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "fruit",
                                "to clean, to sweep",
                                "refrigerator",
                                "banana"
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
                                "水果",
                                "打扫",
                                "冰箱"
                        ],
                        "example": "水果 和 打扫 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "你把水果拿过来"
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
