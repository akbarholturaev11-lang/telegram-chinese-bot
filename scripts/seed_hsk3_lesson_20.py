import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 20,
    "lesson_code": "HSK3-L20",
    "title": "我被他影响了",
    "goal": json.dumps({"uz": "passiv nisbat va cheklovchi shartlardan foydalanish", "ru": "использование страдательного залога и ограничительных условий", "tj": "истифодаи садои маҷҳул ва шартҳои маҳдудкунанда"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda passiv nisbat va cheklovchi shartlardan foydalanish o'rgatiladi. 5 ta asosiy so'z va «被»字句 hamda 只有……才…… grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён использованию страдательного залога и ограничительных условий. Вводятся 5 ключевых слов и грамматические конструкции «被»字句 и 只有……才……", "tj": "Ин дарс ба истифодаи садои маҷҳул ва шартҳои маҳдудкунанда бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии «被»字句 ва 只有……才…… омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "被",
                        "pinyin": "bèi",
                        "pos": "prep.",
                        "uz": "tomonidan (passiv belgisi)",
                        "ru": "(маркер пассивного залога)",
                        "tj": "аз тарафи (нишонаи садои маҷҳул)"
                },
                {
                        "no": 2,
                        "zh": "影响",
                        "pinyin": "yǐngxiǎng",
                        "pos": "v./n.",
                        "uz": "ta'sir qilmoq; ta'sir",
                        "ru": "влиять; влияние",
                        "tj": "таъсир расонидан; таъсир"
                },
                {
                        "no": 3,
                        "zh": "解决",
                        "pinyin": "jiějué",
                        "pos": "v.",
                        "uz": "hal qilmoq; yechmoq",
                        "ru": "решать; разрешать",
                        "tj": "ҳал кардан; бартараф кардан"
                },
                {
                        "no": 4,
                        "zh": "关心",
                        "pinyin": "guānxīn",
                        "pos": "v.",
                        "uz": "g'amxo'rlik qilmoq; e'tibor bermoq",
                        "ru": "заботиться; проявлять внимание",
                        "tj": "ғамхорӣ кардан; диққат зоҳир кардан"
                },
                {
                        "no": 5,
                        "zh": "照相机",
                        "pinyin": "zhàoxiàngjī",
                        "pos": "n.",
                        "uz": "fotoaparat",
                        "ru": "фотоаппарат",
                        "tj": "фотоаппарат"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Ta'sir haqida gaplashish",
                        "scene_ru": "Разговор о влиянии",
                        "scene_tj": "Гуфтугӯ дар бораи таъсир",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你怎么开始认真学习了？",
                                        "pinyin": "Nǐ zěnme kāishǐ rènzhēn xuéxí le?",
                                        "uz": "Siz qanday qilib jiddiy o'qishni boshladingiz?",
                                        "ru": "Как ты начал серьёзно учиться?",
                                        "tj": "Шумо чӣ тавр ба ҷиддӣ хондан шурӯъ кардед?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我被他影响了。",
                                        "pinyin": "Wǒ bèi tā yǐngxiǎng le.",
                                        "uz": "U meni ta'sir ostiga oldi.",
                                        "ru": "На меня повлиял он.",
                                        "tj": "Вай ба ман таъсир расонд."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Muammoni hal qilish",
                        "scene_ru": "Решение проблемы",
                        "scene_tj": "Ҳал кардани мушкилот",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "这个问题怎么解决？",
                                        "pinyin": "Zhège wèntí zěnme jiějué?",
                                        "uz": "Bu muammoni qanday hal qilish kerak?",
                                        "ru": "Как решить эту проблему?",
                                        "tj": "Ин мушкилотро чӣ тавр ҳал кунем?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "只有大家一起努力，才会解决。",
                                        "pinyin": "Zhǐyǒu dàjiā yìqǐ nǔlì, cái huì jiějué.",
                                        "uz": "Faqat hamma birgalikda harakat qilsagina hal bo'ladi.",
                                        "ru": "Только если все будут стараться вместе — решится.",
                                        "tj": "Танҳо агар ҳама якҷоя кӯшиш кунанд, ҳал мешавад."
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
                        "title_zh": "«被»字句",
                        "title_uz": "«被» li passiv gap",
                        "title_ru": "Конструкция страдательного залога с «被»",
                        "title_tj": "Ҷумлаи маҷҳули бо «被»",
                        "rule_uz": "Bu tuzilma passiv ma'noni ifodalaydi va harakatdan ta'sirlangan shaxs yoki narsani ko'rsatadi.",
                        "rule_ru": "Эта конструкция выражает пассивное значение и показывает, кто или что подвергается действию.",
                        "rule_tj": "Ин сохтор маъноии маҷҳулро ифода мекунад ва нишон медиҳад, ки кӣ ё чӣ дар натиҷаи амал таъсир мебинад.",
                        "examples": [
                                {
                                        "zh": "我被他影响了。",
                                        "pinyin": "Wǒ bèi tā yǐngxiǎng le.",
                                        "uz": "U meni ta'sir ostiga oldi.",
                                        "ru": "На меня повлиял он.",
                                        "tj": "Вай ба ман таъсир расонд."
                                },
                                {
                                        "zh": "他被老师表扬了。",
                                        "pinyin": "Tā bèi lǎoshī biǎoyáng le.",
                                        "uz": "Uni o'qituvchi maqtadi.",
                                        "ru": "Его похвалил учитель.",
                                        "tj": "Муаллим вайро таъриф кард."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "只有……才……",
                        "title_uz": "Faqat…… bo'lgandagina, ……",
                        "title_ru": "Только……, тогда/лишь тогда……",
                        "title_tj": "Танҳо……, он вақт……",
                        "rule_uz": "Bu shakl yagona zaruriy shartni ta'kidlaydi.",
                        "rule_ru": "Эта конструкция подчёркивает единственное необходимое условие.",
                        "rule_tj": "Ин намуна шарти ягонаи зарурӣро таъкид мекунад.",
                        "examples": [
                                {
                                        "zh": "只有认真学习，才会成功。",
                                        "pinyin": "Zhǐyǒu rènzhēn xuéxí, cái huì chénggōng.",
                                        "uz": "Faqat jiddiy o'qiganingizda muvaffaqiyat qo'lga kiradi.",
                                        "ru": "Только учась серьёзно — добьёшься успеха.",
                                        "tj": "Танҳо бо ҷиддият хондан муваффақият меояд."
                                },
                                {
                                        "zh": "只有解决问题，大家才放心。",
                                        "pinyin": "Zhǐyǒu jiějué wèntí, dàjiā cái fàngxīn.",
                                        "uz": "Faqat muammo hal bo'lgandagina hammasi tinchlanadi.",
                                        "ru": "Только когда проблема будет решена — все успокоятся.",
                                        "tj": "Танҳо вақте ки мушкилот ҳал шавад, ҳама оромӣ меёбанд."
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
                                        "prompt_uz": "tomonidan (passiv belgisi)",
                                        "prompt_ru": "маркер пассивного залога",
                                        "prompt_tj": "нишонаи садои маҷҳул",
                                        "answer": "被",
                                        "pinyin": "bèi"
                                },
                                {
                                        "prompt_uz": "ta'sir qilmoq; ta'sir",
                                        "prompt_ru": "влиять; влияние",
                                        "prompt_tj": "таъсир расонидан; таъсир",
                                        "answer": "影响",
                                        "pinyin": "yǐngxiǎng"
                                },
                                {
                                        "prompt_uz": "hal qilmoq; yechmoq",
                                        "prompt_ru": "решать; разрешать",
                                        "prompt_tj": "ҳал кардан; бартараф кардан",
                                        "answer": "解决",
                                        "pinyin": "jiějué"
                                },
                                {
                                        "prompt_uz": "g'amxo'rlik qilmoq; e'tibor bermoq",
                                        "prompt_ru": "заботиться; проявлять внимание",
                                        "prompt_tj": "ғамхорӣ кардан; диққат зоҳир кардан",
                                        "answer": "关心",
                                        "pinyin": "guānxīn"
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
                                        "prompt_uz": "被",
                                        "prompt_ru": "被",
                                        "prompt_tj": "被",
                                        "answer": "tomonidan (passiv) / маркер пассива / нишонаи маҷҳул",
                                        "pinyin": "bèi"
                                },
                                {
                                        "prompt_uz": "影响",
                                        "prompt_ru": "影响",
                                        "prompt_tj": "影响",
                                        "answer": "ta'sir qilmoq / влиять / таъсир расонидан",
                                        "pinyin": "yǐngxiǎng"
                                },
                                {
                                        "prompt_uz": "解决",
                                        "prompt_ru": "解决",
                                        "prompt_tj": "解决",
                                        "answer": "hal qilmoq / решать / ҳал кардан",
                                        "pinyin": "jiějué"
                                },
                                {
                                        "prompt_uz": "关心",
                                        "prompt_ru": "关心",
                                        "prompt_tj": "关心",
                                        "answer": "g'amxo'rlik qilmoq / заботиться / ғамхорӣ кардан",
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
                        "answers": ["被", "影响", "解决", "关心"]
                },
                {
                        "no": 2,
                        "answers": [
                                "tomonidan (passiv) / маркер пассива / нишонаи маҷҳул",
                                "ta'sir qilmoq / влиять / таъсир расонидан",
                                "hal qilmoq / решать / ҳал кардан",
                                "g'amxo'rlik qilmoq / заботиться / ғамхорӣ кардан"
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
                        "words": ["被", "影响", "解决"],
                        "example": "只有大家一起努力，这个问题才能被解决。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "U meni ta'sir ostiga oldi",
                        "topic_ru": "На меня повлиял он",
                        "topic_tj": "Вай ба ман таъсир расонд"
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
