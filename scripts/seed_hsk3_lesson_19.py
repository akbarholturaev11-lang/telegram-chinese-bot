import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 19,
    "lesson_code": "HSK3-L19",
    "title": "你没看出来吗",
    "goal": "natijaviy yo'nalish va sababchini ifodalash",
    "intro_text": "Bu dars natijaviy yo'nalish va sababchini ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 趋向补语的引申义 va “使”“叫”“让” kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "认出来",
                        "pinyin": "rènchūlai",
                        "pos": "v.",
                        "meaning": "tanib olmoq"
                },
                {
                        "no": 2,
                        "zh": "耳朵",
                        "pinyin": "ěrduo",
                        "pos": "n.",
                        "meaning": "quloq"
                },
                {
                        "no": 3,
                        "zh": "船",
                        "pinyin": "chuán",
                        "pos": "n.",
                        "meaning": "qayiq, kema"
                },
                {
                        "no": 4,
                        "zh": "黄河",
                        "pinyin": "Huánghé",
                        "pos": "n.",
                        "meaning": "Sariq daryo"
                },
                {
                        "no": 5,
                        "zh": "经过",
                        "pinyin": "jīngguò",
                        "pos": "v.",
                        "meaning": "yonidan o'tmoq"
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
                                        "translation": "Sen uni tanimadingmi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "没有，他戴了帽子，我一下没认出来。",
                                        "pinyin": "",
                                        "translation": "Yo'q, u bosh kiyim kiygan ekan, birdan tanimadim."
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
                                        "translation": "Bu qayiq Sariq daryodan o'tayotganda juda sekin yurdi."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "风太大了，让大家都很紧张。",
                                        "pinyin": "",
                                        "translation": "Shamol juda kuchli edi, hammaga taranglik berdi."
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
                        "explanation": "Bu mavzu harakatning qaysi tomonga yo'nalganini yoki natijada qayerga kelganini ko'rsatadi.",
                        "examples": [
                                {
                                        "zh": "你没看出来吗。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有认出来和耳朵。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 认出来 va 耳朵 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "“使”“叫”“让”",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "你没看出来吗。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有认出来和耳朵。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 认出来 va 耳朵 ishlatilgan."
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
                                        "prompt": "tanib olmoq",
                                        "answer": "认出来",
                                        "pinyin": "rènchūlai"
                                },
                                {
                                        "prompt": "quloq",
                                        "answer": "耳朵",
                                        "pinyin": "ěrduo"
                                },
                                {
                                        "prompt": "qayiq, kema",
                                        "answer": "船",
                                        "pinyin": "chuán"
                                },
                                {
                                        "prompt": "Sariq daryo",
                                        "answer": "黄河",
                                        "pinyin": "Huánghé"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "认出来",
                                        "answer": "tanib olmoq",
                                        "pinyin": "rènchūlai"
                                },
                                {
                                        "prompt": "耳朵",
                                        "answer": "quloq",
                                        "pinyin": "ěrduo"
                                },
                                {
                                        "prompt": "船",
                                        "answer": "qayiq, kema",
                                        "pinyin": "chuán"
                                },
                                {
                                        "prompt": "黄河",
                                        "answer": "Sariq daryo",
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
                                "tanib olmoq",
                                "quloq",
                                "qayiq, kema",
                                "Sariq daryo"
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
                                "认出来",
                                "耳朵",
                                "船"
                        ],
                        "example": "认出来 和 耳朵 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
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
