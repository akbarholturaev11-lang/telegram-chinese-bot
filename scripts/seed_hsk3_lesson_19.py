import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 19,
    "lesson_code": "HSK3-L19",
    "title": "你没看出来吗",
    "goal": json.dumps({"uz": "natijadagi yo'nalish va sababiyatni ifodalash", "ru": "выражение результирующего направления и причинности", "tj": "ифода кардани самти натиҷавӣ ва сабабият"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda natijadagi yo'nalish va sababiyatni ifodalash o'rgatiladi. 5 ta asosiy so'z va 趋向补语的引申义 hamda «使»«叫»«让» grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению результирующего направления и причинности. Вводятся 5 ключевых слов и грамматические конструкции 趋向补语的引申义 и «使»«叫»«让».", "tj": "Ин дарс ба ифода кардани самти натиҷавӣ ва сабабият бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии 趋向补语的引申义 ва «使»«叫»«让» омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "认出来",
                        "pinyin": "rènchūlai",
                        "pos": "v.",
                        "uz": "tanib olmoq; aniqlash",
                        "ru": "узнать; опознать",
                        "tj": "шинохтан; муайян кардан"
                },
                {
                        "no": 2,
                        "zh": "耳朵",
                        "pinyin": "ěrduo",
                        "pos": "n.",
                        "uz": "quloq",
                        "ru": "ухо",
                        "tj": "гӯш"
                },
                {
                        "no": 3,
                        "zh": "船",
                        "pinyin": "chuán",
                        "pos": "n.",
                        "uz": "qayiq; kema",
                        "ru": "лодка; корабль",
                        "tj": "қаиқ; киштӣ"
                },
                {
                        "no": 4,
                        "zh": "黄河",
                        "pinyin": "Huánghé",
                        "pos": "n.",
                        "uz": "Sariq daryo",
                        "ru": "Жёлтая река",
                        "tj": "Дарёи Зард"
                },
                {
                        "no": 5,
                        "zh": "经过",
                        "pinyin": "jīngguò",
                        "pos": "v.",
                        "uz": "yonidan o'tmoq; o'tib ketmoq",
                        "ru": "проходить мимо; миновать",
                        "tj": "аз паҳлӯи гузаштан; убур кардан"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Kimnidir tanib olish",
                        "scene_ru": "Узнавание кого-то",
                        "scene_tj": "Шинохтани касе",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你没看出来吗？",
                                        "pinyin": "Nǐ méi kàn chūlai ma?",
                                        "uz": "Tanib olmadingizmi?",
                                        "ru": "Ты разве не узнал?",
                                        "tj": "Шумо нашинохтед?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "没有，他戴了帽子，我一下没认出来。",
                                        "pinyin": "Méiyǒu, tā dài le màozi, wǒ yíxià méi rènchūlai.",
                                        "uz": "Yo'q, u shapka kiygan edi, men darhol taniydim olmadim.",
                                        "ru": "Нет, он был в шапке — я сразу не узнал.",
                                        "tj": "Не, вай кулоҳ пӯшида буд, ман якбора нашинохтам."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Daryoda",
                        "scene_ru": "На реке",
                        "scene_tj": "Дар дарё",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "这条船经过黄河的时候很慢。",
                                        "pinyin": "Zhè tiáo chuán jīngguò Huánghé de shíhou hěn màn.",
                                        "uz": "Bu qayiq Sariq daryodan o'tayotganda juda sekin edi.",
                                        "ru": "Эта лодка шла очень медленно, когда проходила Жёлтую реку.",
                                        "tj": "Ин қаиқ ҳангоми убур аз Дарёи Зард хеле сусттар буд."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "风太大了，让大家都很紧张。",
                                        "pinyin": "Fēng tài dà le, ràng dàjiā dōu hěn jǐnzhāng.",
                                        "uz": "Shamol juda kuchli edi, hammani hayajonga soldi.",
                                        "ru": "Ветер был слишком сильным, отчего все очень нервничали.",
                                        "tj": "Шамол хеле тунд буд, ки ҳамаро изтироб кард."
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
                        "title_zh": "趋向补语的引申义",
                        "title_uz": "Yo'nalish to'ldiruvchisining kengaytirilgan ma'nosi",
                        "title_ru": "Расширенное значение направительного дополнения",
                        "title_tj": "Маъноии васеъшудаи иловаи самт",
                        "rule_uz": "Bu mavzu yo'nalish to'ldiruvchisining kengaytirilgan ma'nosini ko'rsatadi — harfiy harakatni emas, balki sezilgan natijani bildiradi.",
                        "rule_ru": "Эта тема показывает расширенное значение направительного дополнения — указывает на воспринимаемый результат, а не буквальное движение.",
                        "rule_tj": "Ин мавзӯ маъноии васеъшудаи иловаи самтро нишон медиҳад — натиҷаи дарккардашударо ифода мекунад, на ҳаракати аслӣ."
                        ,
                        "examples": [
                                {
                                        "zh": "你没看出来吗？",
                                        "pinyin": "Nǐ méi kàn chūlai ma?",
                                        "uz": "Tanib olmadingizmi?",
                                        "ru": "Ты разве не узнал?",
                                        "tj": "Шумо нашинохтед?"
                                },
                                {
                                        "zh": "我听出来了，是她的声音。",
                                        "pinyin": "Wǒ tīng chūlai le, shì tā de shēngyīn.",
                                        "uz": "Men tanidim, bu uning ovozi.",
                                        "ru": "Я узнал — это её голос.",
                                        "tj": "Ман шинохтам, ин овози вай аст."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "«使»«叫»«让»",
                        "title_uz": "«使»«叫»«让» — birovni biror narsa qildirish",
                        "title_ru": "«使»«叫»«让» — каузативные глаголы",
                        "title_tj": "«使»«叫»«让» — феълҳои сабабӣ",
                        "rule_uz": "Bu so'zlar biror kishini yoki narsani biror holat yoki harakatga undashni bildiradi.",
                        "rule_ru": "Эти слова указывают на то, что кто-то или что-то заставляет человека оказаться в каком-либо состоянии или выполнить действие.",
                        "rule_tj": "Ин калимаҳо нишон медиҳанд, ки касе ё чизе боис мешавад, ки шахс дар ҳолате бошад ё амале иҷро кунад.",
                        "examples": [
                                {
                                        "zh": "风太大了，让大家都很紧张。",
                                        "pinyin": "Fēng tài dà le, ràng dàjiā dōu hěn jǐnzhāng.",
                                        "uz": "Shamol juda kuchli edi, hammani hayajonga soldi.",
                                        "ru": "Ветер был слишком сильным, отчего все нервничали.",
                                        "tj": "Шамол хеле тунд буд, ки ҳамаро изтироб кард."
                                },
                                {
                                        "zh": "这个消息使他很高兴。",
                                        "pinyin": "Zhège xiāoxi shǐ tā hěn gāoxìng.",
                                        "uz": "Bu xabar uni juda quvontirdi.",
                                        "ru": "Эта новость очень его обрадовала.",
                                        "tj": "Ин хабар вайро хеле шод кард."
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
                        "instruction_uz": "Quyidagi so'zlarni xitoycha yozing:",
                        "instruction_ru": "Напишите китайский для следующих слов:",
                        "instruction_tj": "Калимаҳои зеринро ба хитоӣ нависед:",
                        "items": [
                                {
                                        "prompt_uz": "tanib olmoq; aniqlash",
                                        "prompt_ru": "узнать; опознать",
                                        "prompt_tj": "шинохтан; муайян кардан",
                                        "answer": "认出来",
                                        "pinyin": "rènchūlai"
                                },
                                {
                                        "prompt_uz": "quloq",
                                        "prompt_ru": "ухо",
                                        "prompt_tj": "гӯш",
                                        "answer": "耳朵",
                                        "pinyin": "ěrduo"
                                },
                                {
                                        "prompt_uz": "qayiq; kema",
                                        "prompt_ru": "лодка; корабль",
                                        "prompt_tj": "қаиқ; киштӣ",
                                        "answer": "船",
                                        "pinyin": "chuán"
                                },
                                {
                                        "prompt_uz": "Sariq daryo",
                                        "prompt_ru": "Жёлтая река",
                                        "prompt_tj": "Дарёи Зард",
                                        "answer": "黄河",
                                        "pinyin": "Huánghé"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction_uz": "Quyidagi xitoycha so'zlarni tarjima qiling:",
                        "instruction_ru": "Переведите следующие китайские слова:",
                        "instruction_tj": "Калимаҳои зерини хитоиро тарҷума кунед:",
                        "items": [
                                {
                                        "prompt_uz": "认出来",
                                        "prompt_ru": "认出来",
                                        "prompt_tj": "认出来",
                                        "answer": "tanib olmoq / узнать / шинохтан",
                                        "pinyin": "rènchūlai"
                                },
                                {
                                        "prompt_uz": "耳朵",
                                        "prompt_ru": "耳朵",
                                        "prompt_tj": "耳朵",
                                        "answer": "quloq / ухо / гӯш",
                                        "pinyin": "ěrduo"
                                },
                                {
                                        "prompt_uz": "船",
                                        "prompt_ru": "船",
                                        "prompt_tj": "船",
                                        "answer": "qayiq / лодка / қаиқ",
                                        "pinyin": "chuán"
                                },
                                {
                                        "prompt_uz": "黄河",
                                        "prompt_ru": "黄河",
                                        "prompt_tj": "黄河",
                                        "answer": "Sariq daryo / Жёлтая река / Дарёи Зард",
                                        "pinyin": "Huánghé"
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
                        "answers": ["认出来", "耳朵", "船", "黄河"]
                },
                {
                        "no": 2,
                        "answers": [
                                "tanib olmoq / узнать / шинохтан",
                                "quloq / ухо / гӯш",
                                "qayiq / лодка / қаиқ",
                                "Sariq daryo / Жёлтая река / Дарёи Зард"
                        ]
                }
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
                {
                        "no": 1,
                        "instruction_uz": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                        "instruction_ru": "Составьте 3 предложения, используя следующие слова:",
                        "instruction_tj": "Бо истифода аз калимаҳои зерин 3 ҷумла созед:",
                        "words": ["认出来", "耳朵", "船"],
                        "example": "我用耳朵听出来了，那条船上有熟悉的声音。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Tanib olmadingizmi?",
                        "topic_ru": "Ты разве не узнал?",
                        "topic_tj": "Шумо нашинохтед?"
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
            for key, value in LESSON.items():
                setattr(existing, key, value)
            print(f"updated: {LESSON['lesson_code']}")
        else:
            session.add(CourseLesson(**LESSON))
            print(f"inserted: {LESSON['lesson_code']}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(upsert_lesson())
