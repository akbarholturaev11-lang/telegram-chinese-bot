import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 14,
    "lesson_code": "HSK3-L14",
    "title": "你把水果拿过来",
    "goal": "buyruq, tartib va yo'nalishni ifodalash",
    "intro_text": "Bu dars buyruq, tartib va yo'nalishni ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda “把”字句 3：A 把 B + V + 结果补语/趋向补语 va 先……，再/又……，然后…… kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "水果",
                        "pinyin": "shuǐguǒ",
                        "pos": "n.",
                        "meaning": "meva"
                },
                {
                        "no": 2,
                        "zh": "打扫",
                        "pinyin": "dǎsǎo",
                        "pos": "v.",
                        "meaning": "tozalamoq"
                },
                {
                        "no": 3,
                        "zh": "冰箱",
                        "pinyin": "bīngxiāng",
                        "pos": "n.",
                        "meaning": "muzlatkich"
                },
                {
                        "no": 4,
                        "zh": "香蕉",
                        "pinyin": "xiāngjiāo",
                        "pos": "n.",
                        "meaning": "banan"
                },
                {
                        "no": 5,
                        "zh": "月亮",
                        "pinyin": "yuèliang",
                        "pos": "n.",
                        "meaning": "oy"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "In the kitchen",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你把水果拿过来。",
                                        "pinyin": "",
                                        "translation": "Mevalarni bu yerga olib kel."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我先从冰箱里拿出来。",
                                        "pinyin": "",
                                        "translation": "Xo'p, avval muzlatkichdan olaman."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Housework order",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你先打扫桌子，然后洗水果。",
                                        "pinyin": "",
                                        "translation": "Avval stolni tozala, keyin mevalarni yuv."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "洗好了以后，我再拿香蕉过来。",
                                        "pinyin": "",
                                        "translation": "Yuvib bo'lgach, keyin bananlarni olib kelaman."
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
                        "title_zh": "“把”字句 3：A 把 B + V + 结果补语/趋向补语",
                        "explanation": "Bu qolip harakatning muvaffaqiyatli yoki qoniqarli tugaganini bildiradi.",
                        "examples": [
                                {
                                        "zh": "我准备好了。",
                                        "pinyin": "",
                                        "meaning": "Men tayyor bo'ldim."
                                },
                                {
                                        "zh": "电影票买好了。",
                                        "pinyin": "",
                                        "meaning": "Kinoga bilet sotib olinib bo'ldi."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "先……，再/又……，然后……",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "你把水果拿过来。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有水果和打扫。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 水果 va 打扫 ishlatilgan."
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
                                        "prompt": "meva",
                                        "answer": "水果",
                                        "pinyin": "shuǐguǒ"
                                },
                                {
                                        "prompt": "tozalamoq",
                                        "answer": "打扫",
                                        "pinyin": "dǎsǎo"
                                },
                                {
                                        "prompt": "muzlatkich",
                                        "answer": "冰箱",
                                        "pinyin": "bīngxiāng"
                                },
                                {
                                        "prompt": "banan",
                                        "answer": "香蕉",
                                        "pinyin": "xiāngjiāo"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "水果",
                                        "answer": "meva",
                                        "pinyin": "shuǐguǒ"
                                },
                                {
                                        "prompt": "打扫",
                                        "answer": "tozalamoq",
                                        "pinyin": "dǎsǎo"
                                },
                                {
                                        "prompt": "冰箱",
                                        "answer": "muzlatkich",
                                        "pinyin": "bīngxiāng"
                                },
                                {
                                        "prompt": "香蕉",
                                        "answer": "banan",
                                        "pinyin": "xiāngjiāo"
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
                                "水果",
                                "打扫",
                                "冰箱",
                                "香蕉"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "meva",
                                "tozalamoq",
                                "muzlatkich",
                                "banan"
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
                                "水果",
                                "打扫",
                                "冰箱"
                        ],
                        "example": "水果 和 打扫 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "你把水果拿过来"
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
