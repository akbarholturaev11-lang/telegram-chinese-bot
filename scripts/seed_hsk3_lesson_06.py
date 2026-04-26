import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 6,
    "lesson_code": "HSK3-L06",
    "title": "怎么突然找不到了",
    "goal": "yo'qolgan narsani qidirish va joy haqida so'rash",
    "intro_text": "Bu dars yo'qolgan narsani qidirish va joy haqida so'rashga bag'ishlangan. Unda 5 ta tayanch so'z ishlatiladi hamda 可能补语：V得/不 + Complements va “呢”问处所 kabi asosiy grammatik qoliplar ko'rib chiqiladi.",
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "眼镜",
                        "pinyin": "yǎnjìng",
                        "pos": "n.",
                        "meaning": "ko'zoynak"
                },
                {
                        "no": 2,
                        "zh": "突然",
                        "pinyin": "tūrán",
                        "pos": "adv.",
                        "meaning": "birdan"
                },
                {
                        "no": 3,
                        "zh": "离开",
                        "pinyin": "líkāi",
                        "pos": "v.",
                        "meaning": "ketmoq"
                },
                {
                        "no": 4,
                        "zh": "公园",
                        "pinyin": "gōngyuán",
                        "pos": "n.",
                        "meaning": "park"
                },
                {
                        "no": 5,
                        "zh": "明白",
                        "pinyin": "míngbai",
                        "pos": "v./adj.",
                        "meaning": "tushunmoq, ravshan"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_label_zh": "Looking for glasses",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "我的眼镜怎么突然找不到了？",
                                        "pinyin": "",
                                        "translation": "Ko'zoynagim nega birdan topilmay qoldi?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "你刚才是不是离开教室了？",
                                        "pinyin": "",
                                        "translation": "Sen hozirgina sinfdan chiqib ketmadingmi?"
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_label_zh": "Asking location",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "小王呢？",
                                        "pinyin": "",
                                        "translation": "Xiao Wang qayerda?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "他在公园那边，等会儿回来。",
                                        "pinyin": "",
                                        "translation": "U park tomonda, saldan keyin qaytadi."
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
                        "title_zh": "可能补语：V得/不 + Complements",
                        "explanation": "Bu grammatika mavzusi darsdagi asosiy gap qoliplarini amalda ishlatishga yordam beradi.",
                        "examples": [
                                {
                                        "zh": "怎么突然找不到了。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有眼镜和突然。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 眼镜 va 突然 ishlatilgan."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "“呢”问处所",
                        "explanation": "Bu qo'llanish joy, holat yoki davom etayotgan savolni yumshoq tarzda so'rashda ishlatiladi.",
                        "examples": [
                                {
                                        "zh": "怎么突然找不到了。",
                                        "pinyin": "",
                                        "meaning": "Dars sarlavhasidagi asosiy qolip."
                                },
                                {
                                        "zh": "这个句子里有眼镜和突然。",
                                        "pinyin": "",
                                        "meaning": "Bu gapda 眼镜 va 突然 ishlatilgan."
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
                                        "prompt": "ko'zoynak",
                                        "answer": "眼镜",
                                        "pinyin": "yǎnjìng"
                                },
                                {
                                        "prompt": "birdan",
                                        "answer": "突然",
                                        "pinyin": "tūrán"
                                },
                                {
                                        "prompt": "ketmoq",
                                        "answer": "离开",
                                        "pinyin": "líkāi"
                                },
                                {
                                        "prompt": "park",
                                        "answer": "公园",
                                        "pinyin": "gōngyuán"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                        "items": [
                                {
                                        "prompt": "眼镜",
                                        "answer": "ko'zoynak",
                                        "pinyin": "yǎnjìng"
                                },
                                {
                                        "prompt": "突然",
                                        "answer": "birdan",
                                        "pinyin": "tūrán"
                                },
                                {
                                        "prompt": "离开",
                                        "answer": "ketmoq",
                                        "pinyin": "líkāi"
                                },
                                {
                                        "prompt": "公园",
                                        "answer": "park",
                                        "pinyin": "gōngyuán"
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
                                "眼镜",
                                "突然",
                                "离开",
                                "公园"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "ko'zoynak",
                                "birdan",
                                "ketmoq",
                                "park"
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
                                "眼镜",
                                "突然",
                                "离开"
                        ],
                        "example": "眼镜 和 突然 可以出现在同一个句子里。"
                },
                {
                        "no": 2,
                        "instruction": "Dars mavzusi haqida 4-5 gaplik kichik matn yozing:",
                        "topic": "怎么突然找不到了"
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
