import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 8,
    "lesson_code": "HSK3-L08",
    "title": "你去哪儿我就去哪儿",
    "goal": "savol olmoshlari va yo'nalishni erkin ishlatish",
    "intro_text": "Bu dars savol olmoshlari va yo'nalishni erkin ishlatishga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda “又”和“再” va 疑问代词活用 1 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "熊猫",
                        "pinyin": "xióngmāo",
                        "pos": "n.",
                        "meaning": "panda"
                },
                {
                        "no": 2,
                        "zh": "电梯",
                        "pinyin": "diàntī",
                        "pos": "n.",
                        "meaning": "lift"
                },
                {
                        "no": 3,
                        "zh": "洗手间",
                        "pinyin": "xǐshǒujiān",
                        "pos": "n.",
                        "meaning": "hojatxona"
                },
                {
                        "no": 4,
                        "zh": "马上",
                        "pinyin": "mǎshàng",
                        "pos": "adv.",
                        "meaning": "darhol"
                },
                {
                        "no": 5,
                        "zh": "健康",
                        "pinyin": "jiànkāng",
                        "pos": "adj./n.",
                        "meaning": "sog'lom, salomatlik"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Going together",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你去哪儿我就去哪儿。",
                                        "pinyin": "",
                                        "translation": "Sen qayerga borsang, men ham o'sha yerga boraman."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "那我们先去看熊猫吧。",
                                        "pinyin": "",
                                        "translation": "Unda avval pandalarni ko'rgani boraylik."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "In a building",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你害怕坐电梯吗？",
                                        "pinyin": "",
                                        "translation": "Liftga chiqishdan qo'rqasanmi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "不害怕，我马上就上去。",
                                        "pinyin": "",
                                        "translation": "Yo'q, men hozir chiqaman."
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
                        "title_zh": "“又”和“再”",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "你去哪儿我就去哪儿。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有熊猫和电梯。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 熊猫 va 电梯 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "疑问代词活用 1",
                        "explanation": "Bu mavzu so'roq olmoshlarining umumiy yoki erkin ma'noda ishlatilishini ko'rsatadi.",
                        "examples": [
                                {
                                        "zh": "你去哪儿我就去哪儿。",
                                        "pinyin": "",
                                        "meaning": "Sen qayerga borsang, men ham o'sha yerga boraman."
                                },
                                {
                                        "zh": "谁都可以参加。",
                                        "pinyin": "",
                                        "meaning": "Hamma qatnasha oladi."
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
                                        "prompt": "panda",
                                        "answer": "熊猫",
                                        "pinyin": "xióngmāo"
                                },
                                {
                                        "prompt": "lift",
                                        "answer": "电梯",
                                        "pinyin": "diàntī"
                                },
                                {
                                        "prompt": "hojatxona",
                                        "answer": "洗手间",
                                        "pinyin": "xǐshǒujiān"
                                },
                                {
                                        "prompt": "darhol",
                                        "answer": "马上",
                                        "pinyin": "mǎshàng"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "熊猫",
                                        "answer": "panda",
                                        "pinyin": "xióngmāo"
                                },
                                {
                                        "prompt": "电梯",
                                        "answer": "lift",
                                        "pinyin": "diàntī"
                                },
                                {
                                        "prompt": "洗手间",
                                        "answer": "hojatxona",
                                        "pinyin": "xǐshǒujiān"
                                },
                                {
                                        "prompt": "马上",
                                        "answer": "darhol",
                                        "pinyin": "mǎshàng"
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
                                "熊猫",
                                "电梯",
                                "洗手间",
                                "马上"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "panda",
                                "lift",
                                "hojatxona",
                                "darhol"
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
                                "熊猫",
                                "电梯",
                                "洗手间"
                        ],
                        "example": "熊猫 和 电梯 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "你去哪儿我就去哪儿"
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
