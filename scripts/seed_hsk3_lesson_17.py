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
    "goal": json.dumps({"uz": "taklif, usullar va noaniq olmoshlardan foydalanish", "ru": "использование предложений, методов и неопределённых местоимений", "tj": "истифодаи пешниҳодҳо, усулҳо ва ҷонишинҳои номуайян"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda taklif, usullar va noaniq olmoshlardan foydalanish o'rgatiladi. 5 ta asosiy so'z va 双音节动词重叠 hamda 疑问代词活用 3 grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён предложениям, методам и неопределённым местоимениям. Вводятся 5 ключевых слов и грамматические конструкции 双音节动词重叠 и 疑问代词活用 3.", "tj": "Ин дарс ба истифодаи пешниҳодҳо, усулҳо ва ҷонишинҳои номуайян бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии 双音节动词重叠 ва 疑问代词活用 3 омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "请假",
                        "pinyin": "qǐngjià",
                        "pos": "v.",
                        "uz": "ta'til so'ramoq; ruxsat so'ramoq",
                        "ru": "просить выходной; брать отгул",
                        "tj": "рухсат пурсидан; таътил гирифтан"
                },
                {
                        "no": 2,
                        "zh": "邻居",
                        "pinyin": "línjū",
                        "pos": "n.",
                        "uz": "qo'shni",
                        "ru": "сосед",
                        "tj": "ҳамсоя"
                },
                {
                        "no": 3,
                        "zh": "办法",
                        "pinyin": "bànfǎ",
                        "pos": "n.",
                        "uz": "usul; yo'l",
                        "ru": "метод; способ",
                        "tj": "усул; роҳ"
                },
                {
                        "no": 4,
                        "zh": "决定",
                        "pinyin": "juédìng",
                        "pos": "v.",
                        "uz": "qaror qilmoq",
                        "ru": "решать",
                        "tj": "қарор кардан"
                },
                {
                        "no": 5,
                        "zh": "根据",
                        "pinyin": "gēnjù",
                        "pos": "prep./n.",
                        "uz": "asosida; muvofiq",
                        "ru": "на основе; согласно",
                        "tj": "дар асоси; мувофиқ"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Muammo haqida gaplashish",
                        "scene_ru": "Разговор о проблеме",
                        "scene_tj": "Гуфтугӯ дар бораи мушкилот",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "谁都有办法看好你的“病”。",
                                        "pinyin": "Shéi dōu yǒu bànfǎ kàn hǎo nǐ de “Bìng”.",
                                        "uz": "Har kim sizning \"kasalingizni\" davolash usulini biladi.",
                                        "ru": "У каждого найдётся способ вылечить вашу «болезнь».",
                                        "tj": "Ҳар кас роҳи табобати «бемории» шуморо медонад."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "真的吗？那我该怎么办？",
                                        "pinyin": "Zhēn de ma? Nà wǒ gāi zěnme bàn?",
                                        "uz": "Rostdanmi? Unda men nima qilishim kerak?",
                                        "ru": "Правда? Тогда что же мне делать?",
                                        "tj": "Воқеан? Пас ман чӣ кор кунам?"
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Qaror qabul qilish",
                        "scene_ru": "Принятие решения",
                        "scene_tj": "Қарор қабул кардан",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你可以根据医生的话决定。",
                                        "pinyin": "Nǐ kěyǐ gēnjù yīshēng de huà juédìng.",
                                        "uz": "Siz shifokor so'ziga asoslanib qaror qilishingiz mumkin.",
                                        "ru": "Ты можешь принять решение, основываясь на словах врача.",
                                        "tj": "Шумо метавонед дар асоси суханони духтур қарор кунед."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我先请假休息两天。",
                                        "pinyin": "Hǎo, wǒ xiān qǐngjià xiūxi liǎng tiān.",
                                        "uz": "Yaxshi, avval ikki kunlik ta'til so'rayman.",
                                        "ru": "Хорошо, сначала возьму два дня отгула для отдыха.",
                                        "tj": "Хуб, аввал ду рӯз таътил мегирам то истироҳат кунам."
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
                        "title_uz": "Ikki bo'g'inli fe'llarni takrorlash",
                        "title_ru": "Удвоение двусложных глаголов",
                        "title_tj": "Такрори феълҳои дуҳиҷо",
                        "rule_uz": "Bu mavzu fe'lni takrorlash ohangni yumshatishi yoki ma'noni yanada tabiiy qilishini ko'rsatadi.",
                        "rule_ru": "Эта тема показывает, как повторение глагола смягчает тон или делает смысл более естественным.",
                        "rule_tj": "Ин мавзӯ нишон медиҳад, ки такрори феъл оҳангро нармтар мекунад ё маъноро табиитар менамояд.",
                        "examples": [
                                {
                                        "zh": "我们讨论讨论这个问题吧。",
                                        "pinyin": "Wǒmen tǎolùn tǎolùn zhège wèntí ba.",
                                        "uz": "Keling, bu masalani bir muhokama qilib ko'raylik.",
                                        "ru": "Давайте немного обсудим этот вопрос.",
                                        "tj": "Биёед ин масъаларо каме муҳокима кунем."
                                },
                                {
                                        "zh": "你考虑考虑再决定。",
                                        "pinyin": "Nǐ kǎolǜ kǎolǜ zài juédìng.",
                                        "uz": "Bir o'ylang, keyin qaror qiling.",
                                        "ru": "Подумай немного, потом решай.",
                                        "tj": "Каме фикр кун, баъд қарор кун."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "疑问代词活用 3",
                        "title_uz": "So'roq olmoshlarining moslashgan qo'llanilishi 3",
                        "title_ru": "Гибкое употребление вопросительных местоимений 3",
                        "title_tj": "Истифодаи чандирии ҷонишинҳои пурсишӣ 3",
                        "rule_uz": "Bu mavzu so'roq olmoshlarining umumiy yoki noaniq ma'noda ishlatilishini ko'rsatadi.",
                        "rule_ru": "Эта тема показывает, как вопросительные местоимения могут использоваться с общим или неопределённым значением.",
                        "rule_tj": "Ин мавзӯ нишон медиҳад, ки ҷонишинҳои пурсишӣ метавонанд бо маъноии умумӣ ё номуайян истифода шаванд.",
                        "examples": [
                                {
                                        "zh": "你去哪儿我就去哪儿。",
                                        "pinyin": "Nǐ qù nǎr wǒ jiù qù nǎr.",
                                        "uz": "Qayerga borsangiz, men ham o'sha yerga boraman.",
                                        "ru": "Куда бы ты ни пошёл, я пойду туда же.",
                                        "tj": "Ба куҷо равед, ман ҳам ба он ҷо мераваам."
                                },
                                {
                                        "zh": "谁都可以参加。",
                                        "pinyin": "Shéi dōu kěyǐ cānjiā.",
                                        "uz": "Har kim qatnashishi mumkin.",
                                        "ru": "Любой может участвовать.",
                                        "tj": "Ҳар кас метавонад иштирок кунад."
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
                                        "prompt_uz": "ta'til so'ramoq; ruxsat so'ramoq",
                                        "prompt_ru": "просить выходной; брать отгул",
                                        "prompt_tj": "рухсат пурсидан; таътил гирифтан",
                                        "answer": "请假",
                                        "pinyin": "qǐngjià"
                                },
                                {
                                        "prompt_uz": "qo'shni",
                                        "prompt_ru": "сосед",
                                        "prompt_tj": "ҳамсоя",
                                        "answer": "邻居",
                                        "pinyin": "línjū"
                                },
                                {
                                        "prompt_uz": "usul; yo'l",
                                        "prompt_ru": "метод; способ",
                                        "prompt_tj": "усул; роҳ",
                                        "answer": "办法",
                                        "pinyin": "bànfǎ"
                                },
                                {
                                        "prompt_uz": "qaror qilmoq",
                                        "prompt_ru": "решать",
                                        "prompt_tj": "қарор кардан",
                                        "answer": "决定",
                                        "pinyin": "juédìng"
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
                                        "prompt_uz": "请假",
                                        "prompt_ru": "请假",
                                        "prompt_tj": "请假",
                                        "answer": "ta'til so'ramoq / просить выходной / рухсат пурсидан",
                                        "pinyin": "qǐngjià"
                                },
                                {
                                        "prompt_uz": "邻居",
                                        "prompt_ru": "邻居",
                                        "prompt_tj": "邻居",
                                        "answer": "qo'shni / сосед / ҳамсоя",
                                        "pinyin": "línjū"
                                },
                                {
                                        "prompt_uz": "办法",
                                        "prompt_ru": "办法",
                                        "prompt_tj": "办法",
                                        "answer": "usul / метод / усул",
                                        "pinyin": "bànfǎ"
                                },
                                {
                                        "prompt_uz": "决定",
                                        "prompt_ru": "决定",
                                        "prompt_tj": "决定",
                                        "answer": "qaror qilmoq / решать / қарор кардан",
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
                        "answers": ["请假", "邻居", "办法", "决定"]
                },
                {
                        "no": 2,
                        "answers": [
                                "ta'til so'ramoq / просить выходной / рухсат пурсидан",
                                "qo'shni / сосед / ҳамсоя",
                                "usul / метод / усул",
                                "qaror qilmoq / решать / қарор кардан"
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
                        "words": ["请假", "邻居", "办法"],
                        "example": "邻居帮我想了个办法，我决定请假休息。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Har kim sizning \"kasalingizni\" davolash usulini biladi",
                        "topic_ru": "У каждого найдётся способ вылечить вашу «болезнь»",
                        "topic_tj": "Ҳар кас роҳи табобати «бемории» шуморо медонад"
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
