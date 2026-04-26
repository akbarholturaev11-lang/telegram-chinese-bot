import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 20,
    "lesson_code": "HSK3-L20",
    "title": "我被他影响了",
    "goal": "passiv va cheklovchi shartlarni ishlatish",
    "intro_text": "Bu dars passiv va cheklovchi shartlarni ishlatishga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda “被”字句 va 只有……才…… kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "被",
                        "pinyin": "bèi",
                        "pos": "prep.",
                        "meaning": "tomonidan, passiv ko'rsatkich"
                },
                {
                        "no": 2,
                        "zh": "影响",
                        "pinyin": "yǐngxiǎng",
                        "pos": "v./n.",
                        "meaning": "ta'sir qilmoq, ta'sir"
                },
                {
                        "no": 3,
                        "zh": "解决",
                        "pinyin": "jiějué",
                        "pos": "v.",
                        "meaning": "hal qilmoq"
                },
                {
                        "no": 4,
                        "zh": "关心",
                        "pinyin": "guānxīn",
                        "pos": "v.",
                        "meaning": "qiziqmoq, g'amxo'rlik qilmoq"
                },
                {
                        "no": 5,
                        "zh": "照相机",
                        "pinyin": "zhàoxiàngjī",
                        "pos": "n.",
                        "meaning": "fotoapparat"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Talking about influence",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你怎么开始认真学习了？",
                                        "pinyin": "",
                                        "translation": "Sen nega jiddiy o'qishni boshlading?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我被他影响了。",
                                        "pinyin": "",
                                        "translation": "Men unga ta'sirlanib qoldim."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Solving a problem",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "这个问题怎么解决？",
                                        "pinyin": "",
                                        "translation": "Bu muammoni qanday hal qilamiz?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "只有大家一起努力，才会解决。",
                                        "pinyin": "",
                                        "translation": "Faqat hamma birga harakat qilsa, hal bo'ladi."
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
                        "title_zh": "“被”字句",
                        "explanation": "Bu tuzilma passiv ma'noni beradi va ish kimga ta'sir qilganini ko'rsatadi.",
                        "examples": [
                                {
                                        "zh": "我被他影响了。",
                                        "pinyin": "",
                                        "meaning": "Men unga ta'sirlanib qoldim."
                                },
                                {
                                        "zh": "他被老师表扬了。",
                                        "pinyin": "",
                                        "meaning": "U ustoz tomonidan maqtaldi."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "只有……才……",
                        "explanation": "Bu qolip yagona zarur shartni alohida ta'kidlaydi.",
                        "examples": [
                                {
                                        "zh": "只有认真学习，才会成功。",
                                        "pinyin": "",
                                        "meaning": "Faqat jiddiy o'qisang, muvaffaqiyat qozonasan."
                                },
                                {
                                        "zh": "只有解决问题，大家才放心。",
                                        "pinyin": "",
                                        "meaning": "Faqat muammo hal bo'lsa, hamma xotirjam bo'ladi."
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
                                        "prompt": "tomonidan, passiv ko'rsatkich",
                                        "answer": "被",
                                        "pinyin": "bèi"
                                },
                                {
                                        "prompt": "ta'sir qilmoq, ta'sir",
                                        "answer": "影响",
                                        "pinyin": "yǐngxiǎng"
                                },
                                {
                                        "prompt": "hal qilmoq",
                                        "answer": "解决",
                                        "pinyin": "jiějué"
                                },
                                {
                                        "prompt": "qiziqmoq, g'amxo'rlik qilmoq",
                                        "answer": "关心",
                                        "pinyin": "guānxīn"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "被",
                                        "answer": "tomonidan, passiv ko'rsatkich",
                                        "pinyin": "bèi"
                                },
                                {
                                        "prompt": "影响",
                                        "answer": "ta'sir qilmoq, ta'sir",
                                        "pinyin": "yǐngxiǎng"
                                },
                                {
                                        "prompt": "解决",
                                        "answer": "hal qilmoq",
                                        "pinyin": "jiějué"
                                },
                                {
                                        "prompt": "关心",
                                        "answer": "qiziqmoq, g'amxo'rlik qilmoq",
                                        "pinyin": "guānxīn"
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
                                "被",
                                "影响",
                                "解决",
                                "关心"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "tomonidan, passiv ko'rsatkich",
                                "ta'sir qilmoq, ta'sir",
                                "hal qilmoq",
                                "qiziqmoq, g'amxo'rlik qilmoq"
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
                                "被",
                                "影响",
                                "解决"
                        ],
                        "example": "被 和 影响 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "我被他影响了"
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
