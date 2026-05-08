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
    "goal": json.dumps({"uz": "harakat yo'nalishi va bir vaqtda bajarilayotgan harakatlarni ifodalash", "ru": "выражение направления движения и одновременных действий", "tj": "ифода кардани самти ҳаракат ва амалҳои ҳамзамон"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda harakat yo'nalishi va bir vaqtda bajarilayotgan harakatlarni ifodalash o'rgatiladi. 5 ta asosiy so'z va 复合趋向补语 hamda 一边……一边…… grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению направления движения и одновременных действий. Вводятся 5 ключевых слов и грамматические конструкции 复合趋向补语 и 一边……一边……", "tj": "Ин дарс ба ифода кардани самти ҳаракат ва амалҳои ҳамзамон бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии 复合趋向补语 ва 一边……一边…… омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "礼物",
                        "pinyin": "lǐwù",
                        "pos": "n.",
                        "uz": "sovg'a; hadya",
                        "ru": "подарок",
                        "tj": "тӯҳфа; ҳадя"
                },
                {
                        "no": 2,
                        "zh": "奶奶",
                        "pinyin": "nǎinai",
                        "pos": "n.",
                        "uz": "buvi (ota tomonidan)",
                        "ru": "бабушка (по отцу)",
                        "tj": "момо (аз тарафи падар)"
                },
                {
                        "no": 3,
                        "zh": "遇到",
                        "pinyin": "yùdào",
                        "pos": "v.",
                        "uz": "uchramoq; ro'para kelmoq",
                        "ru": "встретить; натолкнуться",
                        "tj": "вохӯрдан; рӯ ба рӯ шудан"
                },
                {
                        "no": 4,
                        "zh": "一边",
                        "pinyin": "yìbiān",
                        "pos": "adv.",
                        "uz": "bir vaqtda; bir paytda",
                        "ru": "одновременно; в то же время",
                        "tj": "ҳамзамон; дар як вақт"
                },
                {
                        "no": 5,
                        "zh": "愿意",
                        "pinyin": "yuànyì",
                        "pos": "v.",
                        "uz": "rozi bo'lmoq; tayyorligini bildirmoq",
                        "ru": "быть готовым; соглашаться",
                        "tj": "розӣ будан; омодагӣ доштан"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Piyoda qaytib kelish",
                        "scene_ru": "Возвращение пешком",
                        "scene_tj": "Баргаштан бо пой",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你怎么回来的？",
                                        "pinyin": "Nǐ zěnme huí lái de?",
                                        "uz": "Qanday qaytib keldingiz?",
                                        "ru": "Как ты вернулся?",
                                        "tj": "Чӣ тавр баргаштед?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我是走回来的。",
                                        "pinyin": "Wǒ shì zǒu huí lái de.",
                                        "uz": "Men piyoda qaytib keldim.",
                                        "ru": "Я вернулся пешком.",
                                        "tj": "Ман бо пой баргаштам."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Yo'lda",
                        "scene_ru": "В дороге",
                        "scene_tj": "Дар роҳ",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "路上你遇到谁了？",
                                        "pinyin": "Lù shang nǐ yùdào shéi le?",
                                        "uz": "Yo'lda kimni uchratdingiz?",
                                        "ru": "Кого ты встретил по дороге?",
                                        "tj": "Дар роҳ бо кӣ вохӯрдед?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我一边走一边给奶奶买礼物。",
                                        "pinyin": "Wǒ yìbiān zǒu yìbiān gěi nǎinai mǎi lǐwù.",
                                        "uz": "Men yura-yura buvimdga sovg'a sotib oldim.",
                                        "ru": "Я шёл и одновременно купил подарок бабушке.",
                                        "tj": "Ман рафта-рафта барои момо тӯҳфа харидам."
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
                        "title_uz": "Murakkab yo'nalish to'ldiruvchisi",
                        "title_ru": "Сложное направительное дополнение",
                        "title_tj": "Иловаи самти мураккаб",
                        "rule_uz": "Bu mavzu harakatning yo'nalishini yoki sub'ektning natijada qayerga tushganini bildiradi.",
                        "rule_ru": "Эта тема показывает направление действия или конечное положение субъекта как результат действия.",
                        "rule_tj": "Ин мавзӯ самти амал ё мавқеи ниҳоии субъектро дар натиҷаи амал нишон медиҳад.",
                        "examples": [
                                {
                                        "zh": "我是走回来的。",
                                        "pinyin": "Wǒ shì zǒu huí lái de.",
                                        "uz": "Men piyoda qaytib keldim.",
                                        "ru": "Я вернулся пешком.",
                                        "tj": "Ман бо пой баргаштам."
                                },
                                {
                                        "zh": "他跑进来了。",
                                        "pinyin": "Tā pǎo jìn lái le.",
                                        "uz": "U yugura-yugura kirdi.",
                                        "ru": "Он вбежал.",
                                        "tj": "Вай давон-давон даромад."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "一边……一边……",
                        "title_uz": "一边……一边…… (bir vaqtda ikki harakat)",
                        "title_ru": "一边……一边…… (два действия одновременно)",
                        "title_tj": "一边……一边…… (ду амали ҳамзамон)",
                        "rule_uz": "Bu shakl ikki harakatning bir vaqtda bajarilishini bildiradi.",
                        "rule_ru": "Эта конструкция указывает на то, что два действия выполняются одновременно.",
                        "rule_tj": "Ин намуна нишон медиҳад, ки ду амал дар як вақт иҷро мешаванд.",
                        "examples": [
                                {
                                        "zh": "我一边走一边听音乐。",
                                        "pinyin": "Wǒ yìbiān zǒu yìbiān tīng yīnyuè.",
                                        "uz": "Men yura-yura musiqa tinglayapman.",
                                        "ru": "Я иду и одновременно слушаю музыку.",
                                        "tj": "Ман рафта-рафта мусиқа мегӯшам."
                                },
                                {
                                        "zh": "她一边做饭一边说话。",
                                        "pinyin": "Tā yìbiān zuòfàn yìbiān shuōhuà.",
                                        "uz": "U ovqat pishira-pishira gaplashmoqda.",
                                        "ru": "Она готовит еду и одновременно разговаривает.",
                                        "tj": "Вай хӯрок пухта-пухта гап мезанад."
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
                                        "prompt_uz": "sovg'a; hadya",
                                        "prompt_ru": "подарок",
                                        "prompt_tj": "тӯҳфа; ҳадя",
                                        "answer": "礼物",
                                        "pinyin": "lǐwù"
                                },
                                {
                                        "prompt_uz": "buvi (ota tomonidan)",
                                        "prompt_ru": "бабушка (по отцу)",
                                        "prompt_tj": "момо (аз тарафи падар)",
                                        "answer": "奶奶",
                                        "pinyin": "nǎinai"
                                },
                                {
                                        "prompt_uz": "uchramoq; ro'para kelmoq",
                                        "prompt_ru": "встретить; натолкнуться",
                                        "prompt_tj": "вохӯрдан; рӯ ба рӯ шудан",
                                        "answer": "遇到",
                                        "pinyin": "yùdào"
                                },
                                {
                                        "prompt_uz": "bir vaqtda; bir paytda",
                                        "prompt_ru": "одновременно; в то же время",
                                        "prompt_tj": "ҳамзамон; дар як вақт",
                                        "answer": "一边",
                                        "pinyin": "yìbiān"
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
                                        "prompt_uz": "礼物",
                                        "prompt_ru": "礼物",
                                        "prompt_tj": "礼物",
                                        "answer": "sovg'a / подарок / тӯҳфа",
                                        "pinyin": "lǐwù"
                                },
                                {
                                        "prompt_uz": "奶奶",
                                        "prompt_ru": "奶奶",
                                        "prompt_tj": "奶奶",
                                        "answer": "buvi / бабушка / момо",
                                        "pinyin": "nǎinai"
                                },
                                {
                                        "prompt_uz": "遇到",
                                        "prompt_ru": "遇到",
                                        "prompt_tj": "遇到",
                                        "answer": "uchramoq / встретить / вохӯрдан",
                                        "pinyin": "yùdào"
                                },
                                {
                                        "prompt_uz": "一边",
                                        "prompt_ru": "一边",
                                        "prompt_tj": "一边",
                                        "answer": "bir vaqtda / одновременно / ҳамзамон",
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
                        "answers": ["礼物", "奶奶", "遇到", "一边"]
                },
                {
                        "no": 2,
                        "answers": [
                                "sovg'a / подарок / тӯҳфа",
                                "buvi / бабушка / момо",
                                "uchramoq / встретить / вохӯрдан",
                                "bir vaqtda / одновременно / ҳамзамон"
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
                        "words": ["礼物", "奶奶", "遇到"],
                        "example": "我回来的路上遇到了朋友，还给奶奶买了礼物。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Men piyoda qaytib keldim",
                        "topic_ru": "Я вернулся пешком",
                        "topic_tj": "Ман бо пой баргаштам"
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
