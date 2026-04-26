import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 4,
    "lesson_code": "HSK3-L04",
    "title": "她总是笑着跟客人说话",
    "goal": "odat va bir paytdagi harakatlarni ifodalash",
    "intro_text": "Bu dars odat va bir paytdagi harakatlarni ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 又……又…… va 动作的伴随：V1着(O1)+V2(O2) kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "总是",
                        "pinyin": "zǒngshì",
                        "pos": "adv.",
                        "meaning": "doimo"
                },
                {
                        "no": 2,
                        "zh": "客人",
                        "pinyin": "kèrén",
                        "pos": "n.",
                        "meaning": "mehmon, mijoz"
                },
                {
                        "no": 3,
                        "zh": "照片",
                        "pinyin": "zhàopiàn",
                        "pos": "n.",
                        "meaning": "surat"
                },
                {
                        "no": 4,
                        "zh": "认真",
                        "pinyin": "rènzhēn",
                        "pos": "adj.",
                        "meaning": "jiddiy"
                },
                {
                        "no": 5,
                        "zh": "蛋糕",
                        "pinyin": "dàngāo",
                        "pos": "n.",
                        "meaning": "tort"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "At the shop",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "她总是笑着跟客人说话。",
                                        "pinyin": "",
                                        "translation": "U mijozlar bilan doim kulib gaplashadi."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "对，她服务很认真。",
                                        "pinyin": "",
                                        "translation": "Ha, u juda jiddiy xizmat ko'rsatadi."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "At a party",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "桌子上又有蛋糕又有水果。",
                                        "pinyin": "",
                                        "translation": "Stolda ham tort, ham meva bor."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我们先拍照片吧。",
                                        "pinyin": "",
                                        "translation": "Avval suratga tushaylik."
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
                        "title_zh": "又……又……",
                        "explanation": "Bu qolip ikki sifat yoki ikki holatni birga ta'kidlash uchun ishlatiladi.",
                        "examples": [
                                {
                                        "zh": "这个蛋糕又甜又新鲜。",
                                        "pinyin": "",
                                        "meaning": "Bu tort ham shirin, ham yangi."
                                },
                                {
                                        "zh": "她又认真又热情。",
                                        "pinyin": "",
                                        "meaning": "U ham jiddiy, ham iliq muomalali."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "动作的伴随：V1着(O1)+V2(O2)",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "她总是笑着跟客人说话。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有总是和客人。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 总是 va 客人 ishlatilgan."
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
                                        "prompt": "doimo",
                                        "answer": "总是",
                                        "pinyin": "zǒngshì"
                                },
                                {
                                        "prompt": "mehmon, mijoz",
                                        "answer": "客人",
                                        "pinyin": "kèrén"
                                },
                                {
                                        "prompt": "surat",
                                        "answer": "照片",
                                        "pinyin": "zhàopiàn"
                                },
                                {
                                        "prompt": "jiddiy",
                                        "answer": "认真",
                                        "pinyin": "rènzhēn"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "总是",
                                        "answer": "doimo",
                                        "pinyin": "zǒngshì"
                                },
                                {
                                        "prompt": "客人",
                                        "answer": "mehmon, mijoz",
                                        "pinyin": "kèrén"
                                },
                                {
                                        "prompt": "照片",
                                        "answer": "surat",
                                        "pinyin": "zhàopiàn"
                                },
                                {
                                        "prompt": "认真",
                                        "answer": "jiddiy",
                                        "pinyin": "rènzhēn"
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
                                "总是",
                                "客人",
                                "照片",
                                "认真"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "doimo",
                                "mehmon, mijoz",
                                "surat",
                                "jiddiy"
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
                                "总是",
                                "客人",
                                "照片"
                        ],
                        "example": "总是 和 客人 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "她总是笑着跟客人说话"
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
