import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 19,
    "lesson_code": "HSK3-L19",
    "title": "你没看出来吗",
    "goal": "expressing resultative direction and causation",
    "intro_text": 'This lesson is dedicated to expressing resultative direction and causation. It uses 5 key vocabulary words and covers core grammar patterns such as 趋向补语的引申义 and "使""叫""让".',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "认出来",
                        "pinyin": "rènchūlai",
                        "pos": "v.",
                        "meaning": "to recognise, to identify"
                },
                {
                        "no": 2,
                        "zh": "耳朵",
                        "pinyin": "ěrduo",
                        "pos": "n.",
                        "meaning": "ear"
                },
                {
                        "no": 3,
                        "zh": "船",
                        "pinyin": "chuán",
                        "pos": "n.",
                        "meaning": "boat, ship"
                },
                {
                        "no": 4,
                        "zh": "黄河",
                        "pinyin": "Huánghé",
                        "pos": "n.",
                        "meaning": "Yellow River"
                },
                {
                        "no": 5,
                        "zh": "经过",
                        "pinyin": "jīngguò",
                        "pos": "v.",
                        "meaning": "to pass by, to go past"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Recognising someone",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你没看出来吗？",
                                        "pinyin": "",
                                        "translation": "Couldn't you recognise him?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "没有，他戴了帽子，我一下没认出来。",
                                        "pinyin": "",
                                        "translation": "No, he was wearing a hat so I didn't recognise him at first."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "On the river",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "这条船经过黄河的时候很慢。",
                                        "pinyin": "",
                                        "translation": "This boat moved very slowly as it passed through the Yellow River."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "风太大了，让大家都很紧张。",
                                        "pinyin": "",
                                        "translation": "The wind was very strong, making everyone nervous."
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
                        "title_zh": "趋向补语的引申义",
                        "explanation": "This topic shows the extended meaning of a directional complement — indicating a perceptible result rather than literal movement.",
                        "examples": [
                                {
                                        "zh": "你没看出来吗。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有认出来和耳朵。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 认出来 and 耳朵."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": '"使""叫""让"',

                        "explanation": "This grammar topic helps to practise the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "你没看出来吗。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有认出来和耳朵。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 认出来 and 耳朵."
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
                                        "prompt": "to recognise, to identify",
                                        "answer": "认出来",
                                        "pinyin": "rènchūlai"
                                },
                                {
                                        "prompt": "ear",
                                        "answer": "耳朵",
                                        "pinyin": "ěrduo"
                                },
                                {
                                        "prompt": "boat, ship",
                                        "answer": "船",
                                        "pinyin": "chuán"
                                },
                                {
                                        "prompt": "Yellow River",
                                        "answer": "黄河",
                                        "pinyin": "Huánghé"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "认出来",
                                        "answer": "to recognise, to identify",
                                        "pinyin": "rènchūlai"
                                },
                                {
                                        "prompt": "耳朵",
                                        "answer": "ear",
                                        "pinyin": "ěrduo"
                                },
                                {
                                        "prompt": "船",
                                        "answer": "boat, ship",
                                        "pinyin": "chuán"
                                },
                                {
                                        "prompt": "黄河",
                                        "answer": "Yellow River",
                                        "pinyin": "Huánghé"
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
                                "认出来",
                                "耳朵",
                                "船",
                                "黄河"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "to recognise, to identify",
                                "ear",
                                "boat, ship",
                                "Yellow River"
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
                                "认出来",
                                "耳朵",
                                "船"
                        ],
                        "example": "认出来 和 耳朵 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "你没看出来吗"
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
