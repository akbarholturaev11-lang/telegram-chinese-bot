import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 3,
    "lesson_code": "HSK3-L03",
    "title": "桌子上放着很多饮料",
    "goal": "joylashuv va mavjud narsalarni tasvirlash",
    "intro_text": "Bu dars joylashuv va mavjud narsalarni tasvirlashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda “还是”和“或者” va 存在的表达 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "饮料",
                        "pinyin": "yǐnliào",
                        "pos": "n.",
                        "meaning": "ichimlik"
                },
                {
                        "no": 2,
                        "zh": "放",
                        "pinyin": "fàng",
                        "pos": "v.",
                        "meaning": "qo'ymoq"
                },
                {
                        "no": 3,
                        "zh": "花",
                        "pinyin": "huā",
                        "pos": "n.",
                        "meaning": "gul"
                },
                {
                        "no": 4,
                        "zh": "新鲜",
                        "pinyin": "xīnxiān",
                        "pos": "adj.",
                        "meaning": "yangi, toza"
                },
                {
                        "no": 5,
                        "zh": "或者",
                        "pinyin": "huòzhě",
                        "pos": "conj.",
                        "meaning": "yoki"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "On the table",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "translation": "Stol ustida juda ko'p ichimliklar turibdi."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "那边也有花，看起来很新鲜。",
                                        "pinyin": "",
                                        "translation": "U yerda gullar ham bor, juda yangi ko'rinyapti."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Choosing drinks",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你想喝茶还是果汁？",
                                        "pinyin": "",
                                        "translation": "Sen choy ichasanmi yoki sharbatmi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "果汁或者水都可以。",
                                        "pinyin": "",
                                        "translation": "Sharbat yoki suv, ikkalasi ham bo'ladi."
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
                        "title_zh": "“还是”和“或者”",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有饮料和放。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 饮料 va 放 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "存在的表达",
                        "explanation": "Bu qolip joyda narsa borligini yoki joylashib turganini tasvirlash uchun ishlatiladi.",
                        "examples": [
                                {
                                        "zh": "桌子上放着很多饮料。",
                                        "pinyin": "",
                                        "meaning": "Stol ustida juda ko'p ichimliklar turibdi."
                                },
                                {
                                        "zh": "门口站着一个客人。",
                                        "pinyin": "",
                                        "meaning": "Eshik oldida bitta mehmon turibdi."
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
                                        "prompt": "ichimlik",
                                        "answer": "饮料",
                                        "pinyin": "yǐnliào"
                                },
                                {
                                        "prompt": "qo'ymoq",
                                        "answer": "放",
                                        "pinyin": "fàng"
                                },
                                {
                                        "prompt": "gul",
                                        "answer": "花",
                                        "pinyin": "huā"
                                },
                                {
                                        "prompt": "yangi, toza",
                                        "answer": "新鲜",
                                        "pinyin": "xīnxiān"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "饮料",
                                        "answer": "ichimlik",
                                        "pinyin": "yǐnliào"
                                },
                                {
                                        "prompt": "放",
                                        "answer": "qo'ymoq",
                                        "pinyin": "fàng"
                                },
                                {
                                        "prompt": "花",
                                        "answer": "gul",
                                        "pinyin": "huā"
                                },
                                {
                                        "prompt": "新鲜",
                                        "answer": "yangi, toza",
                                        "pinyin": "xīnxiān"
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
                                "饮料",
                                "放",
                                "花",
                                "新鲜"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "ichimlik",
                                "qo'ymoq",
                                "gul",
                                "yangi, toza"
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
                                "饮料",
                                "放",
                                "花"
                        ],
                        "example": "饮料 和 放 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "桌子上放着很多饮料"
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
