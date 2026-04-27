import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 6,
    "lesson_code": "HSK3-L06",
    "title": "怎么突然找不到了",
    "goal": "searching for lost items and asking about location",
    "intro_text": 'This lesson is dedicated to searching for lost items and asking about location. It uses 5 key vocabulary words and covers core grammar patterns such as 可能补语：V得/不 + Complements and "呢" asking about location.',

    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "眼镜",
                        "pinyin": "yǎnjìng",
                        "pos": "n.",
                        "meaning": "glasses, spectacles"
                },
                {
                        "no": 2,
                        "zh": "突然",
                        "pinyin": "tūrán",
                        "pos": "adv.",
                        "meaning": "suddenly"
                },
                {
                        "no": 3,
                        "zh": "离开",
                        "pinyin": "líkāi",
                        "pos": "v.",
                        "meaning": "to leave"
                },
                {
                        "no": 4,
                        "zh": "公园",
                        "pinyin": "gōngyuán",
                        "pos": "n.",
                        "meaning": "park"
                },
                {
                        "no": 5,
                        "zh": "明白",
                        "pinyin": "míngbai",
                        "pos": "v./adj.",
                        "meaning": "to understand, clear"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Looking for glasses",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "我的眼镜怎么突然找不到了？",
                                        "pinyin": "",
                                        "translation": "Why can't I suddenly find my glasses?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "你刚才是不是离开教室了？",
                                        "pinyin": "",
                                        "translation": "Didn't you just leave the classroom?"
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Asking location",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "小王呢？",
                                        "pinyin": "",
                                        "translation": "Where is Xiao Wang?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "他在公园那边，等会儿回来。",
                                        "pinyin": "",
                                        "translation": "He's over by the park, he'll be back soon."
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
                        "title_zh": "可能补语：V得/不 + Complements",
                        "explanation": "This grammar topic helps to practise the core sentence patterns of the lesson in context.",
                        "examples": [
                                {
                                        "zh": "怎么突然找不到了。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有眼镜和突然。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 眼镜 and 突然."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": '"呢"问处所',

                        "explanation": "This usage is used to softly ask about location, state, or an ongoing situation.",
                        "examples": [
                                {
                                        "zh": "怎么突然找不到了。",
                                        "pinyin": "",
                                        "meaning": "The main pattern from the lesson title."
                                },
                                {
                                        "zh": "这个句子里有眼镜和突然。",
                                        "pinyin": "",
                                        "meaning": "This sentence uses 眼镜 and 突然."
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
                                        "prompt": "glasses, spectacles",
                                        "answer": "眼镜",
                                        "pinyin": "yǎnjìng"
                                },
                                {
                                        "prompt": "suddenly",
                                        "answer": "突然",
                                        "pinyin": "tūrán"
                                },
                                {
                                        "prompt": "to leave",
                                        "answer": "离开",
                                        "pinyin": "líkāi"
                                },
                                {
                                        "prompt": "park",
                                        "answer": "公园",
                                        "pinyin": "gōngyuán"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Write the English for the following words:",
                        "items": [
                                {
                                        "prompt": "眼镜",
                                        "answer": "glasses, spectacles",
                                        "pinyin": "yǎnjìng"
                                },
                                {
                                        "prompt": "突然",
                                        "answer": "suddenly",
                                        "pinyin": "tūrán"
                                },
                                {
                                        "prompt": "离开",
                                        "answer": "to leave",
                                        "pinyin": "líkāi"
                                },
                                {
                                        "prompt": "公园",
                                        "answer": "park",
                                        "pinyin": "gōngyuán"
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
                                "眼镜",
                                "突然",
                                "离开",
                                "公园"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "glasses, spectacles",
                                "suddenly",
                                "to leave",
                                "park"
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
                                "眼镜",
                                "突然",
                                "离开"
                        ],
                        "example": "眼镜 和 突然 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Write a short paragraph of 4-5 sentences about the lesson topic:",
                        "topic": "怎么突然找不到了"
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
