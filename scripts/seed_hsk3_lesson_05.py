import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 5,
    "lesson_code": "HSK3-L05",
    "title": "我最近越来越胖了",
    "goal": "sog'liq va o'zgarishni ifodalash",
    "intro_text": "Bu dars sog'liq va o'zgarishni ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda “了”表示变化 va 越来越 + Adj/Mental V kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "最近",
                        "pinyin": "zuìjìn",
                        "pos": "adv.",
                        "meaning": "so'nggi paytda"
                },
                {
                        "no": 2,
                        "zh": "发烧",
                        "pinyin": "fāshāo",
                        "pos": "v.",
                        "meaning": "isitmalamoq"
                },
                {
                        "no": 3,
                        "zh": "感冒",
                        "pinyin": "gǎnmào",
                        "pos": "v./n.",
                        "meaning": "shamollamoq, shamollash"
                },
                {
                        "no": 4,
                        "zh": "季节",
                        "pinyin": "jìjié",
                        "pos": "n.",
                        "meaning": "fasl"
                },
                {
                        "no": 5,
                        "zh": "夏天",
                        "pinyin": "xiàtiān",
                        "pos": "n.",
                        "meaning": "yoz"
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
                                        "translation": "So'nggi paytda senga nima bo'ldi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我最近越来越胖了，而且还感冒了。",
                                        "pinyin": "",
                                        "translation": "Men so'nggi paytda tobora semiryapman, ustiga-ustak shamolladim."
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
                                        "translation": "Yozda tez-tez isitmalaysanmi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "有时候，因为这个季节太热了。",
                                        "pinyin": "",
                                        "translation": "Ba'zida, chunki bu fasl juda issiq."
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
                        "title_zh": "“了”表示变化",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "我最近越来越胖了。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有最近和发烧。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 最近 va 发烧 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "越来越 + Adj/Mental V",
                        "explanation": "Bu qolip holatning bosqichma-bosqich kuchayib borishini bildiradi.",
                        "examples": [
                                {
                                        "zh": "我最近越来越胖了。",
                                        "pinyin": "",
                                        "meaning": "Men so'nggi paytda tobora semiryapman."
                                },
                                {
                                        "zh": "他的汉语越来越好了。",
                                        "pinyin": "",
                                        "meaning": "Uning xitoy tili tobora yaxshilanmoqda."
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
                        "instruction": "Quyidagi ma'nolarning xitoychasini yozing:",
                        "items": [
                                {
                                        "prompt": "so'nggi paytda",
                                        "answer": "最近",
                                        "pinyin": "zuìjìn"
                                },
                                {
                                        "prompt": "isitmalamoq",
                                        "answer": "发烧",
                                        "pinyin": "fāshāo"
                                },
                                {
                                        "prompt": "shamollamoq, shamollash",
                                        "answer": "感冒",
                                        "pinyin": "gǎnmào"
                                },
                                {
                                        "prompt": "fasl",
                                        "answer": "季节",
                                        "pinyin": "jìjié"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "最近",
                                        "answer": "so'nggi paytda",
                                        "pinyin": "zuìjìn"
                                },
                                {
                                        "prompt": "发烧",
                                        "answer": "isitmalamoq",
                                        "pinyin": "fāshāo"
                                },
                                {
                                        "prompt": "感冒",
                                        "answer": "shamollamoq, shamollash",
                                        "pinyin": "gǎnmào"
                                },
                                {
                                        "prompt": "季节",
                                        "answer": "fasl",
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
                                "so'nggi paytda",
                                "isitmalamoq",
                                "shamollamoq, shamollash",
                                "fasl"
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
                {
                        "no": 1,
                        "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                        "words": [
                                "最近",
                                "发烧",
                                "感冒"
                        ],
                        "example": "最近 和 发烧 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
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
