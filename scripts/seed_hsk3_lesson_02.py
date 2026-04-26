import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 2,
    "lesson_code": "HSK3-L02",
    "title": "他什么时候回来",
    "goal": "qaytish va ketma-ket harakatlarni ifodalash",
    "intro_text": "Bu dars qaytish va ketma-ket harakatlarni ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 简单趋向补语 va 两个动作连续发生 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "回来",
                        "pinyin": "huílai",
                        "pos": "v.",
                        "meaning": "qaytib kelmoq"
                },
                {
                        "no": 2,
                        "zh": "办公室",
                        "pinyin": "bàngōngshì",
                        "pos": "n.",
                        "meaning": "ofis"
                },
                {
                        "no": 3,
                        "zh": "拿",
                        "pinyin": "ná",
                        "pos": "v.",
                        "meaning": "olmoq"
                },
                {
                        "no": 4,
                        "zh": "伞",
                        "pinyin": "sǎn",
                        "pos": "n.",
                        "meaning": "soyabon"
                },
                {
                        "no": 5,
                        "zh": "腿",
                        "pinyin": "tuǐ",
                        "pos": "n.",
                        "meaning": "oyoq"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Waiting in the office",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "他什么时候回来？",
                                        "pinyin": "",
                                        "translation": "U qachon qaytib keladi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "他先去办公室拿文件，马上就回来。",
                                        "pinyin": "",
                                        "translation": "U avval ofisga hujjat olgani ketdi, hozir qaytadi."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "On a rainy day",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "外边下雨了，你把伞拿回来了吗？",
                                        "pinyin": "",
                                        "translation": "Tashqarida yomg'ir yog'yapti, soyabonni olib keldingmi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "拿回来了，不过我的腿还有点儿疼。",
                                        "pinyin": "",
                                        "translation": "Olib keldim, lekin oyog'im hali biroz og'riyapti."
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
                        "title_zh": "简单趋向补语",
                        "explanation": "Bu mavzu harakatning qaysi tomonga yo'nalganini yoki natijada qayerga kelganini ko'rsatadi.",
                        "examples": [
                                {
                                        "zh": "他什么时候回来。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有回来和办公室。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 回来 va 办公室 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "两个动作连续发生",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "他什么时候回来。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有回来和办公室。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 回来 va 办公室 ishlatilgan."
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
                                        "prompt": "qaytib kelmoq",
                                        "answer": "回来",
                                        "pinyin": "huílai"
                                },
                                {
                                        "prompt": "ofis",
                                        "answer": "办公室",
                                        "pinyin": "bàngōngshì"
                                },
                                {
                                        "prompt": "olmoq",
                                        "answer": "拿",
                                        "pinyin": "ná"
                                },
                                {
                                        "prompt": "soyabon",
                                        "answer": "伞",
                                        "pinyin": "sǎn"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "回来",
                                        "answer": "qaytib kelmoq",
                                        "pinyin": "huílai"
                                },
                                {
                                        "prompt": "办公室",
                                        "answer": "ofis",
                                        "pinyin": "bàngōngshì"
                                },
                                {
                                        "prompt": "拿",
                                        "answer": "olmoq",
                                        "pinyin": "ná"
                                },
                                {
                                        "prompt": "伞",
                                        "answer": "soyabon",
                                        "pinyin": "sǎn"
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
                                "回来",
                                "办公室",
                                "拿",
                                "伞"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "qaytib kelmoq",
                                "ofis",
                                "olmoq",
                                "soyabon"
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
                                "回来",
                                "办公室",
                                "拿"
                        ],
                        "example": "回来 和 办公室 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "他什么时候回来"
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
