import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 16,
    "lesson_code": "HSK3-L16",
    "title": "我现在累得下了班就想睡觉",
    "goal": "natijaviy holat va shartni ifodalash",
    "intro_text": "Bu dars natijaviy holat va shartni ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 如果……（的话），（S）就…… va 复杂的状态补语 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "累",
                        "pinyin": "lèi",
                        "pos": "adj.",
                        "meaning": "charchagan"
                },
                {
                        "no": 2,
                        "zh": "睡觉",
                        "pinyin": "shuìjiào",
                        "pos": "v.",
                        "meaning": "uxlamoq"
                },
                {
                        "no": 3,
                        "zh": "如果",
                        "pinyin": "rúguǒ",
                        "pos": "conj.",
                        "meaning": "agar"
                },
                {
                        "no": 4,
                        "zh": "城市",
                        "pinyin": "chéngshì",
                        "pos": "n.",
                        "meaning": "shahar"
                },
                {
                        "no": 5,
                        "zh": "检查",
                        "pinyin": "jiǎnchá",
                        "pos": "v.",
                        "meaning": "tekshirmoq"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "After work",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你今天怎么这么累？",
                                        "pinyin": "",
                                        "translation": "Bugun nega bunchalik charchading?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我现在累得下了班就想睡觉。",
                                        "pinyin": "",
                                        "translation": "Men hozir shunchalik charchadimki, ishdan keyin faqat uxlagim keladi."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Advice",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "如果你这么累，就早点休息吧。",
                                        "pinyin": "",
                                        "translation": "Agar shunchalik charchagan bo'lsang, erta dam ol."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，明天我再去检查。",
                                        "pinyin": "",
                                        "translation": "Xo'p, ertaga yana tekshiruvga boraman."
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
                        "title_zh": "如果……（的话），（S）就……",
                        "explanation": "Bu qolip shart va natijani bitta gapda bog'lash uchun ishlatiladi.",
                        "examples": [
                                {
                                        "zh": "如果你累了，就早点睡觉。",
                                        "pinyin": "",
                                        "meaning": "Agar charchagan bo'lsang, erta uxlaysan."
                                },
                                {
                                        "zh": "如果下雨的话，我们就不出去。",
                                        "pinyin": "",
                                        "meaning": "Agar yomg'ir yog'sa, tashqariga chiqmaymiz."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "复杂的状态补语",
                        "explanation": "Bu qolip harakat yoki holatning darajasini batafsilroq tasvirlaydi.",
                        "examples": [
                                {
                                        "zh": "我现在累得下了班就想睡觉。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有累和睡觉。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 累 va 睡觉 ishlatilgan."
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
                                        "prompt": "charchagan",
                                        "answer": "累",
                                        "pinyin": "lèi"
                                },
                                {
                                        "prompt": "uxlamoq",
                                        "answer": "睡觉",
                                        "pinyin": "shuìjiào"
                                },
                                {
                                        "prompt": "agar",
                                        "answer": "如果",
                                        "pinyin": "rúguǒ"
                                },
                                {
                                        "prompt": "shahar",
                                        "answer": "城市",
                                        "pinyin": "chéngshì"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "累",
                                        "answer": "charchagan",
                                        "pinyin": "lèi"
                                },
                                {
                                        "prompt": "睡觉",
                                        "answer": "uxlamoq",
                                        "pinyin": "shuìjiào"
                                },
                                {
                                        "prompt": "如果",
                                        "answer": "agar",
                                        "pinyin": "rúguǒ"
                                },
                                {
                                        "prompt": "城市",
                                        "answer": "shahar",
                                        "pinyin": "chéngshì"
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
                                "累",
                                "睡觉",
                                "如果",
                                "城市"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "charchagan",
                                "uxlamoq",
                                "agar",
                                "shahar"
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
                                "累",
                                "睡觉",
                                "如果"
                        ],
                        "example": "累 和 睡觉 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "我现在累得下了班就想睡觉"
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
