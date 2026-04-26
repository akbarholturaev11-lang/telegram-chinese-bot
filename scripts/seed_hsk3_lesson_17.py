import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 17,
    "lesson_code": "HSK3-L17",
    "title": "谁都有办法看好你的“病”",
    "goal": "taklif, usul va umumiy ma'nodagi olmoshlarni ishlatish",
    "intro_text": "Bu dars taklif, usul va umumiy ma'nodagi olmoshlarni ishlatishga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 双音节动词重叠 va 疑问代词活用 3 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "请假",
                        "pinyin": "qǐngjià",
                        "pos": "v.",
                        "meaning": "ta'til so'ramoq"
                },
                {
                        "no": 2,
                        "zh": "邻居",
                        "pinyin": "línjū",
                        "pos": "n.",
                        "meaning": "qo'shni"
                },
                {
                        "no": 3,
                        "zh": "办法",
                        "pinyin": "bànfǎ",
                        "pos": "n.",
                        "meaning": "usul"
                },
                {
                        "no": 4,
                        "zh": "决定",
                        "pinyin": "juédìng",
                        "pos": "v.",
                        "meaning": "qaror qilmoq"
                },
                {
                        "no": 5,
                        "zh": "根据",
                        "pinyin": "gēnjù",
                        "pos": "prep./n.",
                        "meaning": "asosida"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Talking about a problem",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "谁都有办法看好你的“病”。",
                                        "pinyin": "",
                                        "translation": "Har kim sening “kasaling”ni tuzatishning yo'lini topa oladi."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "真的吗？那我该怎么办？",
                                        "pinyin": "",
                                        "translation": "Rostdanmi? Unda men nima qilay?"
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Making a decision",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你可以根据医生的话决定。",
                                        "pinyin": "",
                                        "translation": "Doktorning gapiga qarab qaror qilishing mumkin."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我先请假休息两天。",
                                        "pinyin": "",
                                        "translation": "Xo'p, avval ikki kun dam olish uchun ruxsat so'rayman."
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
                        "title_zh": "双音节动词重叠",
                        "explanation": "Bu mavzu takroriy shakl orqali ohangni yumshatish yoki ma'noni tabiiyroq qilishni ko'rsatadi.",
                        "examples": [
                                {
                                        "zh": "谁都有办法看好你的“病”。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有请假和邻居。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 请假 va 邻居 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "疑问代词活用 3",
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
                                        "prompt": "ta'til so'ramoq",
                                        "answer": "请假",
                                        "pinyin": "qǐngjià"
                                },
                                {
                                        "prompt": "qo'shni",
                                        "answer": "邻居",
                                        "pinyin": "línjū"
                                },
                                {
                                        "prompt": "usul",
                                        "answer": "办法",
                                        "pinyin": "bànfǎ"
                                },
                                {
                                        "prompt": "qaror qilmoq",
                                        "answer": "决定",
                                        "pinyin": "juédìng"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "请假",
                                        "answer": "ta'til so'ramoq",
                                        "pinyin": "qǐngjià"
                                },
                                {
                                        "prompt": "邻居",
                                        "answer": "qo'shni",
                                        "pinyin": "línjū"
                                },
                                {
                                        "prompt": "办法",
                                        "answer": "usul",
                                        "pinyin": "bànfǎ"
                                },
                                {
                                        "prompt": "决定",
                                        "answer": "qaror qilmoq",
                                        "pinyin": "juédìng"
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
                                "请假",
                                "邻居",
                                "办法",
                                "决定"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "ta'til so'ramoq",
                                "qo'shni",
                                "usul",
                                "qaror qilmoq"
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
                                "请假",
                                "邻居",
                                "办法"
                        ],
                        "example": "请假 和 邻居 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "谁都有办法看好你的“病”"
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
