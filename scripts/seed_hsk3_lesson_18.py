import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 18,
    "lesson_code": "HSK3-L18",
    "title": "我相信他们会同意的",
    "goal": json.dumps({"uz": "ishonch, shartlar va mavzular haqida gapirish", "ru": "разговор об убеждении, условиях и темах", "tj": "гуфтугӯ дар бораи боварӣ, шартҳо ва мавзӯҳо"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda ishonch, shartlar va mavzular haqida gapirish o'rgatiladi. 5 ta asosiy so'z va 只要……就…… hamda 介词«关于» grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён разговору об убеждении, условиях и темах. Вводятся 5 ключевых слов и грамматические конструкции 只要……就…… и предлог «关于».", "tj": "Ин дарс ба гуфтугӯ дар бораи боварӣ, шартҳо ва мавзӯҳо бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии 只要……就…… ва пешояндаки «关于» омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "相信",
                        "pinyin": "xiāngxìn",
                        "pos": "v.",
                        "uz": "ishonmoq; e'tiqod qilmoq",
                        "ru": "верить; доверять",
                        "tj": "бовар кардан; эътимод доштан"
                },
                {
                        "no": 2,
                        "zh": "同意",
                        "pinyin": "tóngyì",
                        "pos": "v.",
                        "uz": "rozi bo'lmoq; kelishmoq",
                        "ru": "соглашаться",
                        "tj": "розӣ будан; мувофиқ будан"
                },
                {
                        "no": 3,
                        "zh": "关于",
                        "pinyin": "guānyú",
                        "pos": "prep.",
                        "uz": "haqida; to'g'risida",
                        "ru": "о; насчёт",
                        "tj": "дар бораи; оид ба"
                },
                {
                        "no": 4,
                        "zh": "机会",
                        "pinyin": "jīhuì",
                        "pos": "n.",
                        "uz": "imkoniyat; fursat",
                        "ru": "возможность; шанс",
                        "tj": "имконият; фурсат"
                },
                {
                        "no": 5,
                        "zh": "国家",
                        "pinyin": "guójiā",
                        "pos": "n.",
                        "uz": "mamlakat; davlat",
                        "ru": "страна; государство",
                        "tj": "кишвар; давлат"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Taklif haqida",
                        "scene_ru": "О предложении",
                        "scene_tj": "Дар бораи пешниҳод",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "我相信他们会同意的。",
                                        "pinyin": "Wǒ xiāngxìn tāmen huì tóngyì de.",
                                        "uz": "Men ular rozi bo'lishiga ishonaman.",
                                        "ru": "Я верю, что они согласятся.",
                                        "tj": "Ман боварам ҳаст, ки онҳо розӣ хоҳанд шуд."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "只要你说明理由，他们就会考虑。",
                                        "pinyin": "Zhǐyào nǐ shuōmíng lǐyóu, tāmen jiù huì kǎolǜ.",
                                        "uz": "Faqat sababini tushuntirsangiz, ular o'ylashadi.",
                                        "ru": "Лишь бы ты объяснил причины — они рассмотрят.",
                                        "tj": "Танҳо сабаби худро шарҳ деҳед, онҳо фикр мекунанд."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Mamlakat haqida",
                        "scene_ru": "О стране",
                        "scene_tj": "Дар бораи кишвар",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你想写关于哪个国家的文章？",
                                        "pinyin": "Nǐ xiǎng xiě guānyú nǎ gè guójiā de wénzhāng?",
                                        "uz": "Qaysi mamlakat haqida maqola yozmoqchisiz?",
                                        "ru": "О какой стране ты хочешь написать статью?",
                                        "tj": "Дар бораи кадом кишвар мехоҳед мақола нависед?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我想写一个我很感兴趣的国家。",
                                        "pinyin": "Wǒ xiǎng xiě yí gè wǒ hěn gǎn xìngqù de guójiā.",
                                        "uz": "Men o'zimni qiziqtiradigan mamlakat haqida yozmoqchiman.",
                                        "ru": "Хочу написать о стране, которая мне очень интересна.",
                                        "tj": "Мехоҳам дар бораи кишваре нависам, ки барам хеле ҷолиб аст."
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
                        "title_zh": "只要……就……",
                        "title_uz": "Faqat…… bo'lsa, …… bo'ladi",
                        "title_ru": "Лишь……, то……",
                        "title_tj": "Танҳо……, он гоҳ……",
                        "rule_uz": "Bu shakl yetarli shartni va kutilgan natijani ifodalaydi.",
                        "rule_ru": "Эта конструкция выражает достаточное условие и ожидаемый результат.",
                        "rule_tj": "Ин намуна шарти кифоя ва натиҷаи интизоршударо ифода мекунад.",
                        "examples": [
                                {
                                        "zh": "只要你努力，就会进步。",
                                        "pinyin": "Zhǐyào nǐ nǔlì, jiù huì jìnbù.",
                                        "uz": "Faqat harakat qilsangiz, taraqqiy qilasiz.",
                                        "ru": "Лишь бы ты старался — добьёшься прогресса.",
                                        "tj": "Танҳо кӯшиш кунед, пешрафт хоҳед кард."
                                },
                                {
                                        "zh": "只要有时间，我就来。",
                                        "pinyin": "Zhǐyào yǒu shíjiān, wǒ jiù lái.",
                                        "uz": "Vaqt bo'lsa, albatta kelaman.",
                                        "ru": "Лишь будет время — я приду.",
                                        "tj": "Танҳо вақт бошад, мераям."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "介词“关于”",
                        "title_uz": "«关于» ko'makchisi (haqida)",
                        "title_ru": "Предлог «关于» (о; насчёт)",
                        "title_tj": "Пешоянди «关于» (дар бораи)",
                        "rule_uz": "关于 so'zi jumlaning qismlarini tabiiy va ma'noli bog'lash uchun ishlatiladi.",
                        "rule_ru": "Предлог 关于 используется для связи частей предложения с темой или предметом обсуждения.",
                        "rule_tj": "Пешоянди 关于 барои пайвастани қисмҳои ҷумла бо мавзӯи гуфтугӯ истифода мешавад.",
                        "examples": [
                                {
                                        "zh": "关于这个问题，我们要认真讨论。",
                                        "pinyin": "Guānyú zhège wèntí, wǒmen yào rènzhēn tǎolùn.",
                                        "uz": "Bu masala haqida jiddiy muhokama qilishimiz kerak.",
                                        "ru": "По данному вопросу нам нужно серьёзно обсудить.",
                                        "tj": "Дар бораи ин масъала бояд ҷиддӣ муҳокима кунем."
                                },
                                {
                                        "zh": "他写了一本关于中国文化的书。",
                                        "pinyin": "Tā xiě le yī běn guānyú zhōngguó wénhuà de shū.",
                                        "uz": "U Xitoy madaniyati haqida kitob yozdi.",
                                        "ru": "Он написал книгу о китайской культуре.",
                                        "tj": "Вай як китоб дар бораи фарҳанги Чин навишт."
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
                                        "prompt_uz": "ishonmoq; e'tiqod qilmoq",
                                        "prompt_ru": "верить; доверять",
                                        "prompt_tj": "бовар кардан; эътимод доштан",
                                        "answer": "相信",
                                        "pinyin": "xiāngxìn"
                                },
                                {
                                        "prompt_uz": "rozi bo'lmoq; kelishmoq",
                                        "prompt_ru": "соглашаться",
                                        "prompt_tj": "розӣ будан; мувофиқ будан",
                                        "answer": "同意",
                                        "pinyin": "tóngyì"
                                },
                                {
                                        "prompt_uz": "haqida; to'g'risida",
                                        "prompt_ru": "о; насчёт",
                                        "prompt_tj": "дар бораи; оид ба",
                                        "answer": "关于",
                                        "pinyin": "guānyú"
                                },
                                {
                                        "prompt_uz": "imkoniyat; fursat",
                                        "prompt_ru": "возможность; шанс",
                                        "prompt_tj": "имконият; фурсат",
                                        "answer": "机会",
                                        "pinyin": "jīhuì"
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
                                        "prompt_uz": "相信",
                                        "prompt_ru": "相信",
                                        "prompt_tj": "相信",
                                        "answer": "ishonmoq / верить / бовар кардан",
                                        "pinyin": "xiāngxìn"
                                },
                                {
                                        "prompt_uz": "同意",
                                        "prompt_ru": "同意",
                                        "prompt_tj": "同意",
                                        "answer": "rozi bo'lmoq / соглашаться / розӣ будан",
                                        "pinyin": "tóngyì"
                                },
                                {
                                        "prompt_uz": "关于",
                                        "prompt_ru": "关于",
                                        "prompt_tj": "关于",
                                        "answer": "haqida / о / дар бораи",
                                        "pinyin": "guānyú"
                                },
                                {
                                        "prompt_uz": "机会",
                                        "prompt_ru": "机会",
                                        "prompt_tj": "机会",
                                        "answer": "imkoniyat / возможность / имконият",
                                        "pinyin": "jīhuì"
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
                        "answers": ["相信", "同意", "关于", "机会"]
                },
                {
                        "no": 2,
                        "answers": [
                                "ishonmoq / верить / бовар кардан",
                                "rozi bo'lmoq / соглашаться / розӣ будан",
                                "haqida / о / дар бораи",
                                "imkoniyat / возможность / имконият"
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
                        "words": ["相信", "同意", "关于"],
                        "example": "我相信只要你说明理由，他们就会同意关于这个计划的建议。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Men ular rozi bo'lishiga ishonaman",
                        "topic_ru": "Я верю, что они согласятся",
                        "topic_tj": "Ман боварам ҳаст, ки онҳо розӣ хоҳанд шуд"
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
