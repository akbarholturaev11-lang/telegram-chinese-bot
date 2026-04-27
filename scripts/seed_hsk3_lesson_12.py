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
    "goal": "expressing leaving something in a place and handing things over",
    "intro_text": 'This lesson is dedicated to expressing leaving something in a place and handing things over. It uses 5 key vocabulary words and covers core grammar patterns such as "才"和"就" and "把"字句 2：A 把 B + V + 在/到/给……',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "行李箱",
                        "pinyin": "xínglixiāng",
                        "pos": "n.",
                        "meaning": "suitcase"
                },
                {
                        "no": 2,
                        "zh": "护照",
                        "pinyin": "hùzhào",
                        "pos": "n.",
                        "meaning": "passport"
                },
                {
                        "no": 3,
                        "zh": "起飞",
                        "pinyin": "qǐfēi",
                        "pos": "v.",
                        "meaning": "to take off (plane)"
                },
                {
                        "no": 4,
                        "zh": "司机",
                        "pinyin": "sījī",
                        "pos": "n.",
                        "meaning": "driver"
                },
                {
                        "no": 5,
                        "zh": "黑板",
                        "pinyin": "hēibǎn",
                        "pos": "n.",
                        "meaning": "blackboard"
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
                                        "translation": "Leave the important things here with me."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，护照和票我先给你。",
                                        "pinyin": "",
                                        "translation": "Sure, I'll give you the passport and tickets first."
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
                                        "translation": "When will the driver arrive?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "他到了以后，我们就出发。",
                                        "pinyin": "",
                                        "translation": "We'll set off once he arrives."
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
                        "title_zh": '"才"和"就"',

                        "explanation": "This grammar topic helps to practise the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "把重要的东西放在我这儿吧。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有行李箱和护照。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 行李箱 and 护照."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": '"把"字句 2：A 把 B + V + 在/到/给……',

                        "explanation": "This structure moves the affected object to the front to emphasise the result or direction.",
                        "examples": [
                                {
                                        "zh": "把重要的东西放在我这儿吧。",
                                        "pinyin": "",
                                        "meaning": "A sample pattern from the lesson title."
                                },
                                {
                                        "zh": "请把行李箱放这儿。",
                                        "pinyin": "",
                                        "meaning": "Please put the 行李箱 here."
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
                                        "prompt": "suitcase",
                                        "answer": "行李箱",
                                        "pinyin": "xínglixiāng"
                                },
                                {
                                        "prompt": "passport",
                                        "answer": "护照",
                                        "pinyin": "hùzhào"
                                },
                                {
                                        "prompt": "to take off (plane)",
                                        "answer": "起飞",
                                        "pinyin": "qǐfēi"
                                },
                                {
                                        "prompt": "driver",
                                        "answer": "司机",
                                        "pinyin": "sījī"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "行李箱",
                                        "answer": "suitcase",
                                        "pinyin": "xínglixiāng"
                                },
                                {
                                        "prompt": "护照",
                                        "answer": "passport",
                                        "pinyin": "hùzhào"
                                },
                                {
                                        "prompt": "起飞",
                                        "answer": "to take off (plane)",
                                        "pinyin": "qǐfēi"
                                },
                                {
                                        "prompt": "司机",
                                        "answer": "driver",
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
                                "suitcase",
                                "passport",
                                "to take off (plane)",
                                "driver"
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
                                "行李箱",
                                "护照",
                                "起飞"
                        ],
                        "example": "行李箱 和 护照 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
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
