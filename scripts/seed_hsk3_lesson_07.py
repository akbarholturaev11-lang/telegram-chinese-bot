import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 7,
    "lesson_code": "HSK3-L07",
    "title": "我跟她都认识五年了",
    "goal": "expressing duration and acquaintance",
    "intro_text": 'This lesson is dedicated to expressing duration and acquaintance. It uses 5 key vocabulary words and covers core grammar patterns such as 时段的表达 and using "半" "刻" "差" to express time.',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "同事",
                        "pinyin": "tóngshì",
                        "pos": "n.",
                        "meaning": "colleague, coworker"
                },
                {
                        "no": 2,
                        "zh": "银行",
                        "pinyin": "yínháng",
                        "pos": "n.",
                        "meaning": "bank"
                },
                {
                        "no": 3,
                        "zh": "结婚",
                        "pinyin": "jiéhūn",
                        "pos": "v.",
                        "meaning": "to get married"
                },
                {
                        "no": 4,
                        "zh": "迟到",
                        "pinyin": "chídào",
                        "pos": "v.",
                        "meaning": "to be late"
                },
                {
                        "no": 5,
                        "zh": "半",
                        "pinyin": "bàn",
                        "pos": "num.",
                        "meaning": "half"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Old friends",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你跟她认识多久了？",
                                        "pinyin": "",
                                        "translation": "How long have you known her?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我跟她都认识五年了。",
                                        "pinyin": "",
                                        "translation": "I've known her for five years now."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "At the bank",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你们以前是同事吗？",
                                        "pinyin": "",
                                        "translation": "Were you colleagues before?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "对，我们在银行一起工作过。",
                                        "pinyin": "",
                                        "translation": "Yes, we worked together at a bank."
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
                        "title_zh": "时段的表达",
                        "explanation": "This topic teaches how to express time and duration naturally.",
                        "examples": [
                                {
                                        "zh": "我跟她都认识五年了。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有同事和银行。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 同事 and 银行."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": '用"半""刻""差"表示时间',

                        "explanation": "This topic teaches how to express time and duration naturally.",
                        "examples": [
                                {
                                        "zh": "我跟她都认识五年了。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有同事和银行。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 同事 and 银行."
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
                                        "prompt": "colleague, coworker",
                                        "answer": "同事",
                                        "pinyin": "tóngshì"
                                },
                                {
                                        "prompt": "bank",
                                        "answer": "银行",
                                        "pinyin": "yínháng"
                                },
                                {
                                        "prompt": "to get married",
                                        "answer": "结婚",
                                        "pinyin": "jiéhūn"
                                },
                                {
                                        "prompt": "to be late",
                                        "answer": "迟到",
                                        "pinyin": "chídào"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "同事",
                                        "answer": "colleague, coworker",
                                        "pinyin": "tóngshì"
                                },
                                {
                                        "prompt": "银行",
                                        "answer": "bank",
                                        "pinyin": "yínháng"
                                },
                                {
                                        "prompt": "结婚",
                                        "answer": "to get married",
                                        "pinyin": "jiéhūn"
                                },
                                {
                                        "prompt": "迟到",
                                        "answer": "to be late",
                                        "pinyin": "chídào"
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
                                "同事",
                                "银行",
                                "结婚",
                                "迟到"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "colleague, coworker",
                                "bank",
                                "to get married",
                                "to be late"
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
                                "同事",
                                "银行",
                                "结婚"
                        ],
                        "example": "同事 和 银行 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "我跟她都认识五年了"
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
