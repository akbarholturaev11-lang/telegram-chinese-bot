import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 5,
    "lesson_code": "HSK3-L05",
    "title": "我最近越来越胖了",
    "goal": "expressing health changes and progressive states",
    "intro_text": 'This lesson is dedicated to expressing health changes and progressive states. It uses 5 key vocabulary words and covers core grammar patterns such as "了" expressing change and 越来越 + Adj/Mental V.',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "最近",
                        "pinyin": "zuìjìn",
                        "pos": "adv.",
                        "meaning": "recently, lately"
                },
                {
                        "no": 2,
                        "zh": "发烧",
                        "pinyin": "fāshāo",
                        "pos": "v.",
                        "meaning": "to have a fever"
                },
                {
                        "no": 3,
                        "zh": "感冒",
                        "pinyin": "gǎnmào",
                        "pos": "v./n.",
                        "meaning": "to catch a cold, cold"
                },
                {
                        "no": 4,
                        "zh": "季节",
                        "pinyin": "jìjié",
                        "pos": "n.",
                        "meaning": "season"
                },
                {
                        "no": 5,
                        "zh": "夏天",
                        "pinyin": "xiàtiān",
                        "pos": "n.",
                        "meaning": "summer"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Talking about health",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你最近怎么了？",
                                        "pinyin": "",
                                        "translation": "What's been going on with you lately?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我最近越来越胖了，而且还感冒了。",
                                        "pinyin": "",
                                        "translation": "I've been getting more and more chubby lately, and on top of that I caught a cold."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "About seasons",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "夏天你容易发烧吗？",
                                        "pinyin": "",
                                        "translation": "Do you often get a fever in summer?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "有时候，因为这个季节太热了。",
                                        "pinyin": "",
                                        "translation": "Sometimes, because this season is very hot."
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
                        "title_zh": '"了"表示变化',

                        "explanation": "This grammar topic helps to practise the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "我最近越来越胖了。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有最近和发烧。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 最近 and 发烧."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "越来越 + Adj/Mental V",
                        "explanation": "This pattern indicates a gradual increase or intensification of a state.",
                        "examples": [
                                {
                                        "zh": "我最近越来越胖了。",
                                        "pinyin": "",
                                        "meaning": "I've been getting more and more chubby lately."
                                },
                                {
                                        "zh": "他的汉语越来越好了。",
                                        "pinyin": "",
                                        "meaning": "His Chinese keeps getting better and better."
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
                                        "prompt": "recently, lately",
                                        "answer": "最近",
                                        "pinyin": "zuìjìn"
                                },
                                {
                                        "prompt": "to have a fever",
                                        "answer": "发烧",
                                        "pinyin": "fāshāo"
                                },
                                {
                                        "prompt": "to catch a cold, cold",
                                        "answer": "感冒",
                                        "pinyin": "gǎnmào"
                                },
                                {
                                        "prompt": "season",
                                        "answer": "季节",
                                        "pinyin": "jìjié"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "最近",
                                        "answer": "recently, lately",
                                        "pinyin": "zuìjìn"
                                },
                                {
                                        "prompt": "发烧",
                                        "answer": "to have a fever",
                                        "pinyin": "fāshāo"
                                },
                                {
                                        "prompt": "感冒",
                                        "answer": "to catch a cold, cold",
                                        "pinyin": "gǎnmào"
                                },
                                {
                                        "prompt": "季节",
                                        "answer": "season",
                                        "pinyin": "jìjié"
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
                                "最近",
                                "发烧",
                                "感冒",
                                "季节"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "recently, lately",
                                "to have a fever",
                                "to catch a cold, cold",
                                "season"
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
                                "最近",
                                "发烧",
                                "感冒"
                        ],
                        "example": "最近 和 发烧 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "我最近越来越胖了"
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
