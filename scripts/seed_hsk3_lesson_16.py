import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 16,
    "lesson_code": "HSK3-L16",
    "title": "我现在累得下了班就想睡觉",
    "goal": json.dumps({"uz": "natijadagi holatlar va shartlarni ifodalash", "ru": "выражение результирующих состояний и условий", "tj": "ифода кардани ҳолатҳои натиҷавӣ ва шартҳо"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda natijadagi holatlar va shartlarni ifodalash o'rgatiladi. 5 ta asosiy so'z va 如果……（的话），（S）就…… hamda 复杂的状态补语 grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению результирующих состояний и условий. Вводятся 5 ключевых слов и грамматические конструкции 如果……（的话），（S）就…… и 复杂的状态补语.", "tj": "Ин дарс ба ифода кардани ҳолатҳои натиҷавӣ ва шартҳо бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии 如果……（的话），（S）就…… ва 复杂的状态补语 омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "累",
                        "pinyin": "lèi",
                        "pos": "adj.",
                        "uz": "charchagan; toliqgan",
                        "ru": "усталый; уставший",
                        "tj": "монда; хаста"
                },
                {
                        "no": 2,
                        "zh": "睡觉",
                        "pinyin": "shuìjiào",
                        "pos": "v.",
                        "uz": "uxlamoq",
                        "ru": "спать",
                        "tj": "хоб кардан"
                },
                {
                        "no": 3,
                        "zh": "如果",
                        "pinyin": "rúguǒ",
                        "pos": "conj.",
                        "uz": "agar",
                        "ru": "если",
                        "tj": "агар"
                },
                {
                        "no": 4,
                        "zh": "城市",
                        "pinyin": "chéngshì",
                        "pos": "n.",
                        "uz": "shahar",
                        "ru": "город",
                        "tj": "шаҳр"
                },
                {
                        "no": 5,
                        "zh": "检查",
                        "pinyin": "jiǎnchá",
                        "pos": "v.",
                        "uz": "tekshirmoq; ko'zdan kechirilmoq",
                        "ru": "проверять; осматривать",
                        "tj": "санҷидан; муоина кардан"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Ishdan keyin",
                        "scene_ru": "После работы",
                        "scene_tj": "Баъд аз кор",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你今天怎么这么累？",
                                        "pinyin": "Nǐ jīntiān zěnme zhème lèi?",
                                        "uz": "Bugun nima uchun buncha charchadingiz?",
                                        "ru": "Почему ты сегодня такой усталый?",
                                        "tj": "Имрӯз чаро ин қадар хастаед?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我现在累得下了班就想睡觉。",
                                        "pinyin": "Wǒ xiànzài lèi de xià le bān jiù xiǎng shuìjiào.",
                                        "uz": "Men hozir shunday charchaganman, ishdan chiqqandan keyin uxlagim keladi.",
                                        "ru": "Я сейчас так устал, что после работы сразу хочу спать.",
                                        "tj": "Ман ҳоло он қадар монда шудаам, ки баъди кор фавран мехоҳам хоб кунам."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Maslahat",
                        "scene_ru": "Совет",
                        "scene_tj": "Маслиҳат",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "如果你这么累，就早点休息吧。",
                                        "pinyin": "Rúguǒ nǐ zhème lèi, jiù zǎo diǎn xiūxi ba.",
                                        "uz": "Agar shunday charchaganingiz bo'lsa, erta dam oling.",
                                        "ru": "Если ты так устал, ляг пораньше отдохнуть.",
                                        "tj": "Агар ин қадар монда бошед, барвақттар истироҳат кунед."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，明天我再去检查。",
                                        "pinyin": "Hǎo, míngtiān wǒ zài qù jiǎnchá.",
                                        "uz": "Yaxshi, ertaga yana tekshirishga boraman.",
                                        "ru": "Ладно, завтра снова пойду на проверку.",
                                        "tj": "Хуб, фардо боз муоина мекунам."
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
                        "title_zh": "如果……（的话），（S）就……",
                        "title_uz": "Agar…… (bo'lsa), (S) ……",
                        "title_ru": "Если…… (то), (S) ……",
                        "title_tj": "Агар…… (бошад), (S) ……",
                        "rule_uz": "Bu shakl bitta jumla ichida shart va uning natijasini bog'lash uchun ishlatiladi.",
                        "rule_ru": "Эта конструкция используется для связи условия и его результата в одном предложении.",
                        "rule_tj": "Ин намуна барои пайвастани шарт ва натиҷааш дар як ҷумла истифода мешавад.",
                        "examples": [
                                {
                                        "zh": "如果你累了，就早点睡觉。",
                                        "pinyin": "Rúguǒ nǐ lèi le, jiù zǎo diǎn shuìjiào.",
                                        "uz": "Agar charchagan bo'lsangiz, erta uxlang.",
                                        "ru": "Если устал, ложись пораньше.",
                                        "tj": "Агар монда бошед, барвақттар хоб кунед."
                                },
                                {
                                        "zh": "如果下雨的话，我们就不出去。",
                                        "pinyin": "Rúguǒ xià yǔ de huà, wǒmen jiù bù chūqù.",
                                        "uz": "Agar yomg'ir yog'sa, biz chiqmaymiz.",
                                        "ru": "Если пойдёт дождь, мы не выйдем.",
                                        "tj": "Агар борон борад, мо намебароем."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "复杂的状态补语",
                        "title_uz": "Murakkab hol to'ldiruvchisi",
                        "title_ru": "Сложное дополнение состояния",
                        "title_tj": "Иловаи мураккаби ҳол",
                        "rule_uz": "Bu shakl harakat yoki holatning darajasini batafsil tasvirlaydi.",
                        "rule_ru": "Эта конструкция описывает степень действия или состояния в большем объёме деталей.",
                        "rule_tj": "Ин намуна дараҷаи амал ё ҳолатро бо тафсилот тавсиф мекунад.",
                        "examples": [
                                {
                                        "zh": "我现在累得下了班就想睡觉。",
                                        "pinyin": "Wǒ xiànzài lèi de xià le bān jiù xiǎng shuìjiào.",
                                        "uz": "Men hozir shunday charchaganman, ishdan chiqqandan keyin uxlagim keladi.",
                                        "ru": "Я сейчас так устал, что после работы сразу хочу спать.",
                                        "tj": "Ман ҳоло он қадар монда шудаам, ки баъди кор фавран мехоҳам хоб кунам."
                                },
                                {
                                        "zh": "他高兴得跳了起来。",
                                        "pinyin": "Tā gāoxìng de tiào le qǐlai.",
                                        "uz": "U shu qadar quvonganidan sakrab ketdi.",
                                        "ru": "Он так обрадовался, что подпрыгнул.",
                                        "tj": "Вай он қадар шод шуд, ки ҷаҳид."
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
                                        "prompt_uz": "charchagan; toliqgan",
                                        "prompt_ru": "усталый; уставший",
                                        "prompt_tj": "монда; хаста",
                                        "answer": "累",
                                        "pinyin": "lèi"
                                },
                                {
                                        "prompt_uz": "uxlamoq",
                                        "prompt_ru": "спать",
                                        "prompt_tj": "хоб кардан",
                                        "answer": "睡觉",
                                        "pinyin": "shuìjiào"
                                },
                                {
                                        "prompt_uz": "agar",
                                        "prompt_ru": "если",
                                        "prompt_tj": "агар",
                                        "answer": "如果",
                                        "pinyin": "rúguǒ"
                                },
                                {
                                        "prompt_uz": "shahar",
                                        "prompt_ru": "город",
                                        "prompt_tj": "шаҳр",
                                        "answer": "城市",
                                        "pinyin": "chéngshì"
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
                                        "prompt_uz": "累",
                                        "prompt_ru": "累",
                                        "prompt_tj": "累",
                                        "answer": "charchagan / усталый / монда",
                                        "pinyin": "lèi"
                                },
                                {
                                        "prompt_uz": "睡觉",
                                        "prompt_ru": "睡觉",
                                        "prompt_tj": "睡觉",
                                        "answer": "uxlamoq / спать / хоб кардан",
                                        "pinyin": "shuìjiào"
                                },
                                {
                                        "prompt_uz": "如果",
                                        "prompt_ru": "如果",
                                        "prompt_tj": "如果",
                                        "answer": "agar / если / агар",
                                        "pinyin": "rúguǒ"
                                },
                                {
                                        "prompt_uz": "城市",
                                        "prompt_ru": "城市",
                                        "prompt_tj": "城市",
                                        "answer": "shahar / город / шаҳр",
                                        "pinyin": "chéngshì"
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
                        "answers": ["累", "睡觉", "如果", "城市"]
                },
                {
                        "no": 2,
                        "answers": [
                                "charchagan / усталый / монда",
                                "uxlamoq / спать / хоб кардан",
                                "agar / если / агар",
                                "shahar / город / шаҳр"
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
                        "words": ["累", "睡觉", "如果"],
                        "example": "如果你太累了，就早点睡觉吧。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Men hozir shunday charchaganman, ishdan chiqqandan keyin uxlagim keladi",
                        "topic_ru": "Я сейчас так устал, что после работы сразу хочу спать",
                        "topic_tj": "Ман ҳоло он қадар монда шудаам, ки баъди кор фавран мехоҳам хоб кунам"
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
