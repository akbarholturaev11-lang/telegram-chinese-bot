import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 15,
    "lesson_code": "HSK3-L15",
    "title": "其他都没什么问题",
    "goal": "istisno, qolgan narsalar va darajani ifodalash",
    "intro_text": "Bu dars istisno, qolgan narsalar va darajani ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 除了……以外，都/还/也…… va 程度的表达：极了 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "留学",
                        "pinyin": "liúxué",
                        "pos": "v.",
                        "meaning": "chet elda o'qimoq"
                },
                {
                        "no": 2,
                        "zh": "水平",
                        "pinyin": "shuǐpíng",
                        "pos": "n.",
                        "meaning": "daraja"
                },
                {
                        "no": 3,
                        "zh": "提高",
                        "pinyin": "tígāo",
                        "pos": "v.",
                        "meaning": "oshirmoq"
                },
                {
                        "no": 4,
                        "zh": "新闻",
                        "pinyin": "xīnwén",
                        "pos": "n.",
                        "meaning": "yangilik"
                },
                {
                        "no": 5,
                        "zh": "文化",
                        "pinyin": "wénhuà",
                        "pos": "n.",
                        "meaning": "madaniyat"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Checking a plan",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "其他都没什么问题。",
                                        "pinyin": "",
                                        "translation": "Qolgani deyarli muammosiz."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "那我们就按计划进行吧。",
                                        "pinyin": "",
                                        "translation": "Unda rejaga ko'ra davom etamiz."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Study abroad",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "除了语言以外，你还担心什么？",
                                        "pinyin": "",
                                        "translation": "Tildan tashqari yana nimadan xavotirdasan?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我最想提高自己的文化水平。",
                                        "pinyin": "",
                                        "translation": "Men eng ko'p o'z madaniy saviyamni oshirmoqchiman."
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
                        "title_zh": "除了……以外，都/还/也……",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "其他都没什么问题。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有留学和水平。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 留学 va 水平 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "程度的表达：极了",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "其他都没什么问题。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有留学和水平。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 留学 va 水平 ishlatilgan."
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
                                        "prompt": "chet elda o'qimoq",
                                        "answer": "留学",
                                        "pinyin": "liúxué"
                                },
                                {
                                        "prompt": "daraja",
                                        "answer": "水平",
                                        "pinyin": "shuǐpíng"
                                },
                                {
                                        "prompt": "oshirmoq",
                                        "answer": "提高",
                                        "pinyin": "tígāo"
                                },
                                {
                                        "prompt": "yangilik",
                                        "answer": "新闻",
                                        "pinyin": "xīnwén"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "留学",
                                        "answer": "chet elda o'qimoq",
                                        "pinyin": "liúxué"
                                },
                                {
                                        "prompt": "水平",
                                        "answer": "daraja",
                                        "pinyin": "shuǐpíng"
                                },
                                {
                                        "prompt": "提高",
                                        "answer": "oshirmoq",
                                        "pinyin": "tígāo"
                                },
                                {
                                        "prompt": "新闻",
                                        "answer": "yangilik",
                                        "pinyin": "xīnwén"
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
                                "留学",
                                "水平",
                                "提高",
                                "新闻"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "chet elda o'qimoq",
                                "daraja",
                                "oshirmoq",
                                "yangilik"
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
                                "留学",
                                "水平",
                                "提高"
                        ],
                        "example": "留学 和 水平 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "其他都没什么问题"
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
