import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 18,
    "lesson_code": "HSK3-L18",
    "title": "我相信他们会同意的",
    "goal": "talking about belief, conditions, and topics",
    "intro_text": 'This lesson is dedicated to talking about belief, conditions, and topics. It uses 5 key vocabulary words and covers core grammar patterns such as 只要……就…… and the preposition "关于".',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "相信",
                        "pinyin": "xiāngxìn",
                        "pos": "v.",
                        "meaning": "to believe, to trust"
                },
                {
                        "no": 2,
                        "zh": "同意",
                        "pinyin": "tóngyì",
                        "pos": "v.",
                        "meaning": "to agree"
                },
                {
                        "no": 3,
                        "zh": "关于",
                        "pinyin": "guānyú",
                        "pos": "prep.",
                        "meaning": "about, regarding"
                },
                {
                        "no": 4,
                        "zh": "机会",
                        "pinyin": "jīhuì",
                        "pos": "n.",
                        "meaning": "opportunity, chance"
                },
                {
                        "no": 5,
                        "zh": "国家",
                        "pinyin": "guójiā",
                        "pos": "n.",
                        "meaning": "country, nation"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "On a proposal",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "我相信他们会同意的。",
                                        "pinyin": "",
                                        "translation": "I believe they will agree."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "只要你说明理由，他们就会考虑。",
                                        "pinyin": "",
                                        "translation": "As long as you explain your reasons, they will consider it."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "About a country",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你想写关于哪个国家的文章？",
                                        "pinyin": "",
                                        "translation": "Which country do you want to write an article about?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我想写一个我很感兴趣的国家。",
                                        "pinyin": "",
                                        "translation": "I want to write about a country that interests me."
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
                        "title_zh": "只要……就……",
                        "explanation": "This pattern expresses a sufficient condition and an expected result.",
                        "examples": [
                                {
                                        "zh": "只要你努力，就会进步。",
                                        "pinyin": "",
                                        "meaning": "As long as you make an effort, you will improve."
                                },
                                {
                                        "zh": "只要有时间，我就来。",
                                        "pinyin": "",
                                        "meaning": "As long as I have time, I'll come."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": '介词"关于"',

                        "explanation": "This topic helps to naturally connect parts of a sentence and enhance clarity of meaning.",
                        "examples": [
                                {
                                        "zh": "我相信他们会同意的。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有相信和同意。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 相信 and 同意."
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
                                        "prompt": "to believe, to trust",
                                        "answer": "相信",
                                        "pinyin": "xiāngxìn"
                                },
                                {
                                        "prompt": "to agree",
                                        "answer": "同意",
                                        "pinyin": "tóngyì"
                                },
                                {
                                        "prompt": "about, regarding",
                                        "answer": "关于",
                                        "pinyin": "guānyú"
                                },
                                {
                                        "prompt": "opportunity, chance",
                                        "answer": "机会",
                                        "pinyin": "jīhuì"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "相信",
                                        "answer": "to believe, to trust",
                                        "pinyin": "xiāngxìn"
                                },
                                {
                                        "prompt": "同意",
                                        "answer": "to agree",
                                        "pinyin": "tóngyì"
                                },
                                {
                                        "prompt": "关于",
                                        "answer": "about, regarding",
                                        "pinyin": "guānyú"
                                },
                                {
                                        "prompt": "机会",
                                        "answer": "opportunity, chance",
                                        "pinyin": "jīhuì"
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
                                "相信",
                                "同意",
                                "关于",
                                "机会"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "to believe, to trust",
                                "to agree",
                                "about, regarding",
                                "opportunity, chance"
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
                                "相信",
                                "同意",
                                "关于"
                        ],
                        "example": "相信 和 同意 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "我相信他们会同意的"
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
