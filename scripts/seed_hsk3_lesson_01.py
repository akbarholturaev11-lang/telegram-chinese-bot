import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 1,
    "lesson_code": "HSK3-L01",
    "title": "周末你有什么打算",
    "goal": "dam olish kuni rejalari haqida gapirish",
    "intro_text": "Bu dars dam olish kuni rejalari haqida gapirishga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 结果补语“好” va “一……也/都 + 不/没……”表示否定 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "周末",
                        "pinyin": "zhōumò",
                        "pos": "n.",
                        "meaning": "dam olish kuni"
                },
                {
                        "no": 2,
                        "zh": "打算",
                        "pinyin": "dǎsuàn",
                        "pos": "v./n.",
                        "meaning": "reja qilmoq, reja"
                },
                {
                        "no": 3,
                        "zh": "作业",
                        "pinyin": "zuòyè",
                        "pos": "n.",
                        "meaning": "uy vazifasi"
                },
                {
                        "no": 4,
                        "zh": "着急",
                        "pinyin": "zháojí",
                        "pos": "adj.",
                        "meaning": "xavotirli, shoshayotgan"
                },
                {
                        "no": 5,
                        "zh": "地图",
                        "pinyin": "dìtú",
                        "pos": "n.",
                        "meaning": "xarita"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Weekend plan",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "周末你有什么打算？",
                                        "pinyin": "",
                                        "translation": "Dam olish kuni uchun qanday rejang bor?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我想先写作业，然后跟朋友出去。",
                                        "pinyin": "",
                                        "translation": "Avval uy vazifamni qilaman, keyin do'stim bilan chiqaman."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Preparing things",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "去公园要不要带地图？",
                                        "pinyin": "",
                                        "translation": "Parkka borganda xarita olib ketamizmi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "不用着急，我都准备好了。",
                                        "pinyin": "",
                                        "translation": "Xavotir olma, hammasini tayyorlab bo'ldim."
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
                        "title_zh": "结果补语“好”",
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
                        "title_zh": "“一……也/都 + 不/没……”表示否定",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "周末你有什么打算。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有周末和打算。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 周末 va 打算 ishlatilgan."
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
                                        "prompt": "dam olish kuni",
                                        "answer": "周末",
                                        "pinyin": "zhōumò"
                                },
                                {
                                        "prompt": "reja qilmoq, reja",
                                        "answer": "打算",
                                        "pinyin": "dǎsuàn"
                                },
                                {
                                        "prompt": "uy vazifasi",
                                        "answer": "作业",
                                        "pinyin": "zuòyè"
                                },
                                {
                                        "prompt": "xavotirli, shoshayotgan",
                                        "answer": "着急",
                                        "pinyin": "zháojí"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "周末",
                                        "answer": "dam olish kuni",
                                        "pinyin": "zhōumò"
                                },
                                {
                                        "prompt": "打算",
                                        "answer": "reja qilmoq, reja",
                                        "pinyin": "dǎsuàn"
                                },
                                {
                                        "prompt": "作业",
                                        "answer": "uy vazifasi",
                                        "pinyin": "zuòyè"
                                },
                                {
                                        "prompt": "着急",
                                        "answer": "xavotirli, shoshayotgan",
                                        "pinyin": "zháojí"
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
                                "周末",
                                "打算",
                                "作业",
                                "着急"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "dam olish kuni",
                                "reja qilmoq, reja",
                                "uy vazifasi",
                                "xavotirli, shoshayotgan"
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
                                "周末",
                                "打算",
                                "作业"
                        ],
                        "example": "周末 和 打算 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "周末你有什么打算"
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
