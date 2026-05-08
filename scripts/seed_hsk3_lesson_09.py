import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 9,
    "lesson_code": "HSK3-L09",
    "title": "她的汉语说得跟中国人一样好",
    "goal": json.dumps({"uz": "darajada tenglikni taqqoslash orqali ifodalash", "ru": "выражение равенства по степени через сравнение", "tj": "ифода кардани баробарӣ дар дараҷа тавассути муқоиса"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda darajada tenglikni taqqoslash orqali ifodalash o'rgatiladi. 5 ta asosiy so'z va 越 A 越 B hamda 比较句 1：A 跟 B 一样 (+Adj) grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению равенства по степени через сравнение. Вводятся 5 ключевых слов и основные грамматические конструкции 越 A 越 B и 比较句 1：A 跟 B 一样 (+Adj).", "tj": "Ин дарс ба ифода кардани баробарӣ дар дараҷа тавассути муқоиса бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии 越 A 越 B ва 比较句 1：A 跟 B 一样 (+Adj) омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "中文",
                        "pinyin": "zhōngwén",
                        "pos": "n.",
                        "uz": "xitoy tili",
                        "ru": "китайский язык",
                        "tj": "забони чинӣ"
                },
                {
                        "no": 2,
                        "zh": "一样",
                        "pinyin": "yíyàng",
                        "pos": "adj.",
                        "uz": "bir xil; xuddi shunday",
                        "ru": "одинаковый; такой же",
                        "tj": "якхела; ҳамон тавр"
                },
                {
                        "no": 3,
                        "zh": "参加",
                        "pinyin": "cānjiā",
                        "pos": "v.",
                        "uz": "qatnashmoq; qo'shilmoq",
                        "ru": "участвовать; присоединяться",
                        "tj": "иштирок кардан; ҳамроҳ шудан"
                },
                {
                        "no": 4,
                        "zh": "放心",
                        "pinyin": "fàngxīn",
                        "pos": "v.",
                        "uz": "xotirjam bo'lmoq; ishonmoq",
                        "ru": "успокоиться; быть спокойным",
                        "tj": "оромӣ ёфтан; боварӣ доштан"
                },
                {
                        "no": 5,
                        "zh": "影响",
                        "pinyin": "yǐngxiǎng",
                        "pos": "v./n.",
                        "uz": "ta'sir qilmoq; ta'sir",
                        "ru": "влиять; влияние",
                        "tj": "таъсир расонидан; таъсир"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Til qobiliyati",
                        "scene_ru": "Языковые способности",
                        "scene_tj": "Қобилияти забонӣ",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "她的汉语说得跟中国人一样好。",
                                        "pinyin": "Tā de hànyǔ shuō de gēn zhōngguórén yíyàng hǎo.",
                                        "uz": "U xitoy tilida xitoyliklar kabi so'zlaydi.",
                                        "ru": "Она говорит по-китайски так же хорошо, как носители языка.",
                                        "tj": "Вай ба забони чинӣ мисли аҳли он кишвар сухан мегӯяд."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "是啊，所以大家都很放心。",
                                        "pinyin": "Shì a, suǒyǐ dàjiā dōu hěn fàngxīn.",
                                        "uz": "Ha, shuning uchun hammasi xotirjam.",
                                        "ru": "Да, поэтому все очень спокойны.",
                                        "tj": "Бале, аз ин рӯ ҳама хотирҷамъ аст."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Tadbirga qatnashish",
                        "scene_ru": "Участие в мероприятии",
                        "scene_tj": "Иштирок дар чорабинӣ",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "她会参加这次活动吗？",
                                        "pinyin": "Tā huì cānjiā zhè cì huódòng ma?",
                                        "uz": "U bu tadbirda qatnashadimi?",
                                        "ru": "Она будет участвовать в этом мероприятии?",
                                        "tj": "Оё вай дар ин чорабинӣ иштирок мекунад?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "会，她的表现越说越自然。",
                                        "pinyin": "Huì, tā de biǎoxiàn yuè shuō yuè zìrán.",
                                        "uz": "Ha, uning nutqi tobora tabiiyroq bo'lib bormoqda.",
                                        "ru": "Да, её речь становится всё более естественной.",
                                        "tj": "Бале, нутқи вай ҳар чи бештар табиӣ мешавад."
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
                        "title_uz": "Qanchalik A bo'lsa, shunchalik B bo'ladi",
                        "title_ru": "Чем больше A, тем больше B",
                        "title_tj": "Ҳар чи A, ҳамон қадар B",
                        "rule_uz": "Bu grammatik shakl biror holat yoki harakat o'sishi bilan boshqa bir narsa ham o'sishini ifodalaydi.",
                        "rule_ru": "Эта конструкция выражает нарастание одного качества или действия по мере нарастания другого.",
                        "rule_tj": "Ин намуна ифода мекунад, ки бо афзоиши як ҳол ё амал, дигаре низ меафзояд.",
                        "examples": [
                                {
                                        "zh": "她的表现越说越自然。",
                                        "pinyin": "Tā de biǎoxiàn yuè shuō yuè zìrán.",
                                        "uz": "Uning nutqi qancha gapirsa, shuncha tabiiy bo'ladi.",
                                        "ru": "Чем больше она говорит, тем естественнее её речь.",
                                        "tj": "Ҳар чи бештар гап мезанад, нутқаш табиитар мешавад."
                                },
                                {
                                        "zh": "天气越来越冷。",
                                        "pinyin": "Tiānqì yuè lái yuè lěng.",
                                        "uz": "Ob-havo tobora sovuqlashmoqda.",
                                        "ru": "Погода становится всё холоднее.",
                                        "tj": "Ҳаво ҳар чи сардтар мешавад."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "比较句 1：A 跟 B 一样 (+Adj)",
                        "title_uz": "Taqqoslash 1: A va B bir xil (+sifat)",
                        "title_ru": "Сравнение 1: A такой же, как B (+прилагательное)",
                        "title_tj": "Муқоиса 1: A ба монанди B (+сифат)",
                        "rule_uz": "Bu shakl ikki narsa yoki shaxsni darajasi bo'yicha taqqoslashda ishlatiladi.",
                        "rule_ru": "Эта конструкция используется для сравнения двух предметов или людей по степени признака.",
                        "rule_tj": "Ин намуна барои муқоисаи ду чиз ё шахс аз рӯи дараҷа истифода мешавад.",
                        "examples": [
                                {
                                        "zh": "她的汉语说得跟中国人一样好。",
                                        "pinyin": "Tā de hànyǔ shuō de gēn zhōngguórén yíyàng hǎo.",
                                        "uz": "U xitoy tilida xitoyliklar kabi so'zlaydi.",
                                        "ru": "Она говорит по-китайски так же хорошо, как носители языка.",
                                        "tj": "Вай ба забони чинӣ мисли аҳли он кишвар сухан мегӯяд."
                                },
                                {
                                        "zh": "这件衣服跟那件一样贵。",
                                        "pinyin": "Zhè jiàn yīfu gēn nà jiàn yíyàng guì.",
                                        "uz": "Bu kiyim o'sha kiyim kabi qimmat.",
                                        "ru": "Эта одежда такая же дорогая, как та.",
                                        "tj": "Ин либос ба монанди он либос гарон аст."
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
                                        "prompt_uz": "xitoy tili",
                                        "prompt_ru": "китайский язык",
                                        "prompt_tj": "забони чинӣ",
                                        "answer": "中文",
                                        "pinyin": "zhōngwén"
                                },
                                {
                                        "prompt_uz": "bir xil; xuddi shunday",
                                        "prompt_ru": "одинаковый; такой же",
                                        "prompt_tj": "якхела; ҳамон тавр",
                                        "answer": "一样",
                                        "pinyin": "yíyàng"
                                },
                                {
                                        "prompt_uz": "qatnashmoq; qo'shilmoq",
                                        "prompt_ru": "участвовать; присоединяться",
                                        "prompt_tj": "иштирок кардан; ҳамроҳ шудан",
                                        "answer": "参加",
                                        "pinyin": "cānjiā"
                                },
                                {
                                        "prompt_uz": "xotirjam bo'lmoq",
                                        "prompt_ru": "успокоиться; быть спокойным",
                                        "prompt_tj": "оромӣ ёфтан",
                                        "answer": "放心",
                                        "pinyin": "fàngxīn"
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
                                        "prompt_uz": "中文",
                                        "prompt_ru": "中文",
                                        "prompt_tj": "中文",
                                        "answer": "xitoy tili / китайский язык / забони чинӣ",
                                        "pinyin": "zhōngwén"
                                },
                                {
                                        "prompt_uz": "一样",
                                        "prompt_ru": "一样",
                                        "prompt_tj": "一样",
                                        "answer": "bir xil / одинаковый / якхела",
                                        "pinyin": "yíyàng"
                                },
                                {
                                        "prompt_uz": "参加",
                                        "prompt_ru": "参加",
                                        "prompt_tj": "参加",
                                        "answer": "qatnashmoq / участвовать / иштирок кардан",
                                        "pinyin": "cānjiā"
                                },
                                {
                                        "prompt_uz": "放心",
                                        "prompt_ru": "放心",
                                        "prompt_tj": "放心",
                                        "answer": "xotirjam bo'lmoq / успокоиться / оромӣ ёфтан",
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
                                "xitoy tili / китайский язык / забони чинӣ",
                                "bir xil / одинаковый / якхела",
                                "qatnashmoq / участвовать / иштирок кардан",
                                "xotirjam bo'lmoq / успокоиться / оромӣ ёфтан"
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
                        "words": ["中文", "一样", "参加"],
                        "example": "她的中文说得跟中国人一样好。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "U xitoy tilida xitoyliklar kabi gapiradi",
                        "topic_ru": "Она говорит по-китайски так же хорошо, как носители языка",
                        "topic_tj": "Вай ба забони чинӣ мисли аҳли он кишвар сухан мегӯяд"
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
