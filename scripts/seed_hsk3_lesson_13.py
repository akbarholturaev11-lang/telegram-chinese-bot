import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 13,
    "lesson_code": "HSK3-L13",
    "title": "我是走回来的",
    "goal": "yo'nalish va bir vaqtdagi ikki harakatni ifodalash",
    "intro_text": "Bu dars yo'nalish va bir vaqtdagi ikki harakatni ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 复合趋向补语 va 一边……一边…… kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "礼物",
                        "pinyin": "lǐwù",
                        "pos": "n.",
                        "meaning": "sovg'a"
                },
                {
                        "no": 2,
                        "zh": "奶奶",
                        "pinyin": "nǎinai",
                        "pos": "n.",
                        "meaning": "buvi"
                },
                {
                        "no": 3,
                        "zh": "遇到",
                        "pinyin": "yùdào",
                        "pos": "v.",
                        "meaning": "uchratmoq"
                },
                {
                        "no": 4,
                        "zh": "一边",
                        "pinyin": "yìbiān",
                        "pos": "adv.",
                        "meaning": "bir tomondan, bir paytning o'zida"
                },
                {
                        "no": 5,
                        "zh": "愿意",
                        "pinyin": "yuànyì",
                        "pos": "v.",
                        "meaning": "xohlamoq, rozi bo'lmoq"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Walking back",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你怎么回来的？",
                                        "pinyin": "",
                                        "translation": "Qanday qaytding?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我是走回来的。",
                                        "pinyin": "",
                                        "translation": "Men piyoda qaytdim."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "On the way",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "路上你遇到谁了？",
                                        "pinyin": "",
                                        "translation": "Yo'lda kimni uchratding?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我一边走一边给奶奶买礼物。",
                                        "pinyin": "",
                                        "translation": "Men yurib ketib, bir vaqtning o'zida buvimga sovg'a oldim."
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
                        "title_zh": "复合趋向补语",
                        "explanation": "Bu mavzu harakatning qaysi tomonga yo'nalganini yoki natijada qayerga kelganini ko'rsatadi.",
                        "examples": [
                                {
                                        "zh": "我是走回来的。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有礼物和奶奶。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 礼物 va 奶奶 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "一边……一边……",
                        "explanation": "Bu qolip bir vaqtning o'zida ikki harakat ketayotganini bildiradi.",
                        "examples": [
                                {
                                        "zh": "我一边走一边听音乐。",
                                        "pinyin": "",
                                        "meaning": "Men yurib ketib bir vaqtning o'zida musiqa tinglayman."
                                },
                                {
                                        "zh": "她一边做饭一边说话。",
                                        "pinyin": "",
                                        "meaning": "U ovqat pishirib turib gaplashadi."
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
                                        "prompt": "sovg'a",
                                        "answer": "礼物",
                                        "pinyin": "lǐwù"
                                },
                                {
                                        "prompt": "buvi",
                                        "answer": "奶奶",
                                        "pinyin": "nǎinai"
                                },
                                {
                                        "prompt": "uchratmoq",
                                        "answer": "遇到",
                                        "pinyin": "yùdào"
                                },
                                {
                                        "prompt": "bir tomondan, bir paytning o'zida",
                                        "answer": "一边",
                                        "pinyin": "yìbiān"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "礼物",
                                        "answer": "sovg'a",
                                        "pinyin": "lǐwù"
                                },
                                {
                                        "prompt": "奶奶",
                                        "answer": "buvi",
                                        "pinyin": "nǎinai"
                                },
                                {
                                        "prompt": "遇到",
                                        "answer": "uchratmoq",
                                        "pinyin": "yùdào"
                                },
                                {
                                        "prompt": "一边",
                                        "answer": "bir tomondan, bir paytning o'zida",
                                        "pinyin": "yìbiān"
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
                                "礼物",
                                "奶奶",
                                "遇到",
                                "一边"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "sovg'a",
                                "buvi",
                                "uchratmoq",
                                "bir tomondan, bir paytning o'zida"
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
                                "礼物",
                                "奶奶",
                                "遇到"
                        ],
                        "example": "礼物 和 奶奶 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "我是走回来的"
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
