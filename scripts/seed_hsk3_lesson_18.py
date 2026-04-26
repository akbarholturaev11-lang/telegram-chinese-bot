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
    "goal": "ishonch, shart va mavzu haqida gapirish",
    "intro_text": "Bu dars ishonch, shart va mavzu haqida gapirishga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 只要……就…… va 介词“关于” kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "相信",
                        "pinyin": "xiāngxìn",
                        "pos": "v.",
                        "meaning": "ishonmoq"
                },
                {
                        "no": 2,
                        "zh": "同意",
                        "pinyin": "tóngyì",
                        "pos": "v.",
                        "meaning": "rozi bo'lmoq"
                },
                {
                        "no": 3,
                        "zh": "关于",
                        "pinyin": "guānyú",
                        "pos": "prep.",
                        "meaning": "haqida"
                },
                {
                        "no": 4,
                        "zh": "机会",
                        "pinyin": "jīhuì",
                        "pos": "n.",
                        "meaning": "imkoniyat"
                },
                {
                        "no": 5,
                        "zh": "国家",
                        "pinyin": "guójiā",
                        "pos": "n.",
                        "meaning": "davlat"
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
                                        "translation": "Men ularning rozi bo'lishiga ishonaman."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "只要你说明理由，他们就会考虑。",
                                        "pinyin": "",
                                        "translation": "Sababini tushuntirsang, albatta ko'rib chiqishadi."
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
                                        "translation": "Qaysi davlat haqida maqola yozmoqchisan?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我想写一个我很感兴趣的国家。",
                                        "pinyin": "",
                                        "translation": "Men o'zimni qiziqtiradigan bir davlat haqida yozmoqchiman."
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
                        "explanation": "Bu qolip yetarli shart va kutilgan natijani ko'rsatadi.",
                        "examples": [
                                {
                                        "zh": "只要你努力，就会进步。",
                                        "pinyin": "",
                                        "meaning": "Faqat harakat qilsang, albatta rivojlanasan."
                                },
                                {
                                        "zh": "只要有时间，我就来。",
                                        "pinyin": "",
                                        "meaning": "Vaqtim bo'lsa, albatta kelaman."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "介词“关于”",
                        "explanation": "Bu mavzu gap qismlarini tabiiy bog'lash va ma'no aniqligini oshirishga xizmat qiladi.",
                        "examples": [
                                {
                                        "zh": "我相信他们会同意的。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有相信和同意。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 相信 va 同意 ishlatilgan."
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
                                        "prompt": "ishonmoq",
                                        "answer": "相信",
                                        "pinyin": "xiāngxìn"
                                },
                                {
                                        "prompt": "rozi bo'lmoq",
                                        "answer": "同意",
                                        "pinyin": "tóngyì"
                                },
                                {
                                        "prompt": "haqida",
                                        "answer": "关于",
                                        "pinyin": "guānyú"
                                },
                                {
                                        "prompt": "imkoniyat",
                                        "answer": "机会",
                                        "pinyin": "jīhuì"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "相信",
                                        "answer": "ishonmoq",
                                        "pinyin": "xiāngxìn"
                                },
                                {
                                        "prompt": "同意",
                                        "answer": "rozi bo'lmoq",
                                        "pinyin": "tóngyì"
                                },
                                {
                                        "prompt": "关于",
                                        "answer": "haqida",
                                        "pinyin": "guānyú"
                                },
                                {
                                        "prompt": "机会",
                                        "answer": "imkoniyat",
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
                                "ishonmoq",
                                "rozi bo'lmoq",
                                "haqida",
                                "imkoniyat"
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
                                "相信",
                                "同意",
                                "关于"
                        ],
                        "example": "相信 和 同意 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
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
