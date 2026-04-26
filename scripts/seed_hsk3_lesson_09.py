import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 9,
    "lesson_code": "HSK3-L09",
    "title": "她的汉语说得跟中国人一样好",
    "goal": "bir xil darajadagi qiyoslashni ifodalash",
    "intro_text": "Bu dars bir xil darajadagi qiyoslashni ifodalashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 越 A 越 B va 比较句 1：A 跟 B 一样 (+Adj) kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "中文",
                        "pinyin": "zhōngwén",
                        "pos": "n.",
                        "meaning": "xitoy tili"
                },
                {
                        "no": 2,
                        "zh": "一样",
                        "pinyin": "yíyàng",
                        "pos": "adj.",
                        "meaning": "bir xil"
                },
                {
                        "no": 3,
                        "zh": "参加",
                        "pinyin": "cānjiā",
                        "pos": "v.",
                        "meaning": "qatnashmoq"
                },
                {
                        "no": 4,
                        "zh": "放心",
                        "pinyin": "fàngxīn",
                        "pos": "v.",
                        "meaning": "ko'ngli joyiga tushmoq"
                },
                {
                        "no": 5,
                        "zh": "影响",
                        "pinyin": "yǐngxiǎng",
                        "pos": "v./n.",
                        "meaning": "ta'sir qilmoq, ta'sir"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Language ability",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "她的汉语说得跟中国人一样好。",
                                        "pinyin": "",
                                        "translation": "U xitoy tilini xuddi xitoylikdek yaxshi gapiradi."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "是啊，所以大家都很放心。",
                                        "pinyin": "",
                                        "translation": "Ha, shuning uchun hamma xotirjam."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Joining an event",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "她会参加这次活动吗？",
                                        "pinyin": "",
                                        "translation": "U bu tadbirga qatnashadimi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "会，她的表现越说越自然。",
                                        "pinyin": "",
                                        "translation": "Ha, bo'ladi, uning nutqi tobora tabiiylashyapti."
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
                        "title_zh": "越 A 越 B",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "她的汉语说得跟中国人一样好。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有中文和一样。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 中文 va 一样 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "比较句 1：A 跟 B 一样 (+Adj)",
                        "explanation": "Bu qolip ikki narsa yoki odamni daraja jihatidan qiyoslash uchun ishlatiladi.",
                        "examples": [
                                {
                                        "zh": "她的汉语说得跟中国人一样好。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi qiyoslash namunasi."
                                },
                                {
                                        "zh": "中文比一样更重要。",
                                        "pinyin": "",
                                        "meaning": "中文 一样dan ham muhimroq."
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
                                        "prompt": "xitoy tili",
                                        "answer": "中文",
                                        "pinyin": "zhōngwén"
                                },
                                {
                                        "prompt": "bir xil",
                                        "answer": "一样",
                                        "pinyin": "yíyàng"
                                },
                                {
                                        "prompt": "qatnashmoq",
                                        "answer": "参加",
                                        "pinyin": "cānjiā"
                                },
                                {
                                        "prompt": "ko'ngli joyiga tushmoq",
                                        "answer": "放心",
                                        "pinyin": "fàngxīn"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "中文",
                                        "answer": "xitoy tili",
                                        "pinyin": "zhōngwén"
                                },
                                {
                                        "prompt": "一样",
                                        "answer": "bir xil",
                                        "pinyin": "yíyàng"
                                },
                                {
                                        "prompt": "参加",
                                        "answer": "qatnashmoq",
                                        "pinyin": "cānjiā"
                                },
                                {
                                        "prompt": "放心",
                                        "answer": "ko'ngli joyiga tushmoq",
                                        "pinyin": "fàngxīn"
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
                                "中文",
                                "一样",
                                "参加",
                                "放心"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "xitoy tili",
                                "bir xil",
                                "qatnashmoq",
                                "ko'ngli joyiga tushmoq"
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
                                "中文",
                                "一样",
                                "参加"
                        ],
                        "example": "中文 和 一样 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "她的汉语说得跟中国人一样好"
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
