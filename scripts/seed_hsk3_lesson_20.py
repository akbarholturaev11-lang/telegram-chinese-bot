import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 20,
    "lesson_code": "HSK3-L20",
    "title": "我被他影响了",
    "goal": "using passive voice and restrictive conditions",
    "intro_text": 'This lesson is dedicated to using passive voice and restrictive conditions. It uses 5 key vocabulary words and covers core grammar patterns such as "被"字句 and 只有……才……',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "被",
                        "pinyin": "bèi",
                        "pos": "prep.",
                        "meaning": "by (passive marker)"
                },
                {
                        "no": 2,
                        "zh": "影响",
                        "pinyin": "yǐngxiǎng",
                        "pos": "v./n.",
                        "meaning": "to influence, influence"
                },
                {
                        "no": 3,
                        "zh": "解决",
                        "pinyin": "jiějué",
                        "pos": "v.",
                        "meaning": "to solve, to resolve"
                },
                {
                        "no": 4,
                        "zh": "关心",
                        "pinyin": "guānxīn",
                        "pos": "v.",
                        "meaning": "to care about, to show concern"
                },
                {
                        "no": 5,
                        "zh": "照相机",
                        "pinyin": "zhàoxiàngjī",
                        "pos": "n.",
                        "meaning": "camera"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Talking about influence",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你怎么开始认真学习了？",
                                        "pinyin": "",
                                        "translation": "Why did you start studying seriously?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我被他影响了。",
                                        "pinyin": "",
                                        "translation": "I was influenced by him."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Solving a problem",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "这个问题怎么解决？",
                                        "pinyin": "",
                                        "translation": "How do we solve this problem?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "只有大家一起努力，才会解决。",
                                        "pinyin": "",
                                        "translation": "Only if everyone works together will it be solved."
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
                        "title_zh": '"被"字句',

                        "explanation": "This structure expresses a passive meaning and shows who or what is affected by the action.",
                        "examples": [
                                {
                                        "zh": "我被他影响了。",
                                        "pinyin": "",
                                        "meaning": "I was influenced by him."
                                },
                                {
                                        "zh": "他被老师表扬了。",
                                        "pinyin": "",
                                        "meaning": "He was praised by the teacher."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "只有……才……",
                        "explanation": "This pattern emphasises the one and only necessary condition.",
                        "examples": [
                                {
                                        "zh": "只有认真学习，才会成功。",
                                        "pinyin": "",
                                        "meaning": "Only by studying seriously will you succeed."
                                },
                                {
                                        "zh": "只有解决问题，大家才放心。",
                                        "pinyin": "",
                                        "meaning": "Only when the problem is solved will everyone be at ease."
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
                                        "prompt": "by (passive marker)",
                                        "answer": "被",
                                        "pinyin": "bèi"
                                },
                                {
                                        "prompt": "to influence, influence",
                                        "answer": "影响",
                                        "pinyin": "yǐngxiǎng"
                                },
                                {
                                        "prompt": "to solve, to resolve",
                                        "answer": "解决",
                                        "pinyin": "jiějué"
                                },
                                {
                                        "prompt": "to care about, to show concern",
                                        "answer": "关心",
                                        "pinyin": "guānxīn"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "被",
                                        "answer": "by (passive marker)",
                                        "pinyin": "bèi"
                                },
                                {
                                        "prompt": "影响",
                                        "answer": "to influence, influence",
                                        "pinyin": "yǐngxiǎng"
                                },
                                {
                                        "prompt": "解决",
                                        "answer": "to solve, to resolve",
                                        "pinyin": "jiějué"
                                },
                                {
                                        "prompt": "关心",
                                        "answer": "to care about, to show concern",
                                        "pinyin": "guānxīn"
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
                                "被",
                                "影响",
                                "解决",
                                "关心"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "by (passive marker)",
                                "to influence, influence",
                                "to solve, to resolve",
                                "to care about, to show concern"
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
                                "被",
                                "影响",
                                "解决"
                        ],
                        "example": "被 和 影响 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "我被他影响了"
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
