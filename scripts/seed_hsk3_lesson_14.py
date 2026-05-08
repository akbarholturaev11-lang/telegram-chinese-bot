import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 14,
    "lesson_code": "HSK3-L14",
    "title": "你把水果拿过来",
    "goal": json.dumps({"uz": "buyruq, ketma-ketlik va yo'nalishni ifodalash", "ru": "выражение команд, последовательности и направления", "tj": "ифода кардани амр, пайдарпайӣ ва самт"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda buyruq, ketma-ketlik va yo'nalishni ifodalash o'rgatiladi. 5 ta asosiy so'z va «把»字句 3：A 把 B + V + 结果补语/趋向补语 hamda 先……，再/又……，然后…… grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению команд, последовательности и направления. Вводятся 5 ключевых слов и грамматические конструкции «把»字句 3：A 把 B + V + 结果补语/趋向补语 и 先……，再/又……，然后……", "tj": "Ин дарс ба ифода кардани амр, пайдарпайӣ ва самт бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии «把»字句 3：A 把 B + V + 结果补语/趋向补语 ва 先……，再/又……，然后…… омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "水果",
                        "pinyin": "shuǐguǒ",
                        "pos": "n.",
                        "uz": "meva",
                        "ru": "фрукты",
                        "tj": "мева"
                },
                {
                        "no": 2,
                        "zh": "打扫",
                        "pinyin": "dǎsǎo",
                        "pos": "v.",
                        "uz": "tozalamoq; supurmoq",
                        "ru": "убирать; подметать",
                        "tj": "тоза кардан; рӯфтан"
                },
                {
                        "no": 3,
                        "zh": "冰箱",
                        "pinyin": "bīngxiāng",
                        "pos": "n.",
                        "uz": "muzlatgich",
                        "ru": "холодильник",
                        "tj": "яхдон"
                },
                {
                        "no": 4,
                        "zh": "香蕉",
                        "pinyin": "xiāngjiāo",
                        "pos": "n.",
                        "uz": "banan",
                        "ru": "банан",
                        "tj": "банан"
                },
                {
                        "no": 5,
                        "zh": "月亮",
                        "pinyin": "yuèliang",
                        "pos": "n.",
                        "uz": "oy",
                        "ru": "луна",
                        "tj": "моҳ"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Oshxonada",
                        "scene_ru": "На кухне",
                        "scene_tj": "Дар ошхона",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你把水果拿过来。",
                                        "pinyin": "Nǐ bǎ shuǐguǒ ná guòlai.",
                                        "uz": "Mevalarni bu yerga olib kel.",
                                        "ru": "Принеси сюда фрукты.",
                                        "tj": "Меваҳоро ин ҷо биёр."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我先从冰箱里拿出来。",
                                        "pinyin": "Hǎo, wǒ xiān cóng bīngxiāng lǐ ná chūlái.",
                                        "uz": "Yaxshi, avval muzlatgichdan olib chiqaman.",
                                        "ru": "Хорошо, сначала достану из холодильника.",
                                        "tj": "Хуб, аввал аз яхдон бароварда мегирам."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Uy ishlari tartibi",
                        "scene_ru": "Порядок домашних дел",
                        "scene_tj": "Тартиби корҳои хонагӣ",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你先打扫桌子，然后洗水果。",
                                        "pinyin": "Nǐ xiān dǎsǎo zhuōzi, rán hòu xǐ shuǐguǒ.",
                                        "uz": "Avval stolni tozala, keyin mevalarni yuv.",
                                        "ru": "Сначала вытри стол, потом помой фрукты.",
                                        "tj": "Аввал мизро тоза кун, баъд меваҳоро биш."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "洗好了以后，我再拿香蕉过来。",
                                        "pinyin": "Xǐ hǎo le yǐhòu, wǒ zài ná xiāngjiāo guòlai.",
                                        "uz": "Yuvib bo'lgandan keyin, bananlarni olib kelaman.",
                                        "ru": "После мытья принесу бананы.",
                                        "tj": "Пас аз шустан, банонҳоро меорам."
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
                        "title_zh": "«把»字句 3：A 把 B + V + 结果补语/趋向补语",
                        "title_uz": "«把» li gap 3: A 把 B + fe'l + natija/yo'nalish to'ldiruvchisi",
                        "title_ru": "Конструкция с «把» 3: A 把 B + глагол + результирующее/направительное дополнение",
                        "title_tj": "Ҷумла бо «把» 3: A 把 B + феъл + иловаи натиҷа/самт",
                        "rule_uz": "Bu shakl ob'ektga nisbatan bajarilgan harakatning natijasini yoki yo'nalishini ko'rsatadi.",
                        "rule_ru": "Эта конструкция показывает результат или направление действия, совершённого над объектом.",
                        "rule_tj": "Ин сохтор натиҷа ё самти амале, ки нисбат ба объект иҷро шудааст, нишон медиҳад.",
                        "examples": [
                                {
                                        "zh": "你把水果拿过来。",
                                        "pinyin": "Nǐ bǎ shuǐguǒ ná guòlai.",
                                        "uz": "Mevalarni bu yerga olib kel.",
                                        "ru": "Принеси сюда фрукты.",
                                        "tj": "Меваҳоро ин ҷо биёр."
                                },
                                {
                                        "zh": "把书放回书架上。",
                                        "pinyin": "Bǎ shū fàng huí shūjià shang.",
                                        "uz": "Kitobni javonga qaytarib qo'y.",
                                        "ru": "Положи книгу обратно на полку.",
                                        "tj": "Китобро ба қафасаи китоб баргардон."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "先……，再/又……，然后……",
                        "title_uz": "Avval…, keyin…, so'ngra…",
                        "title_ru": "Сначала…, затем/снова…, потом…",
                        "title_tj": "Аввал…, баъд…, сипас…",
                        "rule_uz": "Bu grammatik shakl ketma-ket bajarilayotgan harakatlarni ifodalaydi.",
                        "rule_ru": "Эта конструкция выражает последовательность действий.",
                        "rule_tj": "Ин намуна пайдарпайии амалҳоро ифода мекунад.",
                        "examples": [
                                {
                                        "zh": "你先打扫桌子，然后洗水果。",
                                        "pinyin": "Nǐ xiān dǎsǎo zhuōzi, rán hòu xǐ shuǐguǒ.",
                                        "uz": "Avval stolni tozala, keyin mevalarni yuv.",
                                        "ru": "Сначала вытри стол, потом помой фрукты.",
                                        "tj": "Аввал мизро тоза кун, баъд меваҳоро биш."
                                },
                                {
                                        "zh": "先学习，再玩儿，然后睡觉。",
                                        "pinyin": "Xiān xuéxí, zài wánr, rán hòu shuìjiào.",
                                        "uz": "Avval o'qi, keyin o'yna, so'ngra uxla.",
                                        "ru": "Сначала учись, потом играй, затем ложись спать.",
                                        "tj": "Аввал дарс хон, баъд бозӣ кун, сипас хоб кун."
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
                                        "prompt_uz": "meva",
                                        "prompt_ru": "фрукты",
                                        "prompt_tj": "мева",
                                        "answer": "水果",
                                        "pinyin": "shuǐguǒ"
                                },
                                {
                                        "prompt_uz": "tozalamoq; supurmoq",
                                        "prompt_ru": "убирать; подметать",
                                        "prompt_tj": "тоза кардан; рӯфтан",
                                        "answer": "打扫",
                                        "pinyin": "dǎsǎo"
                                },
                                {
                                        "prompt_uz": "muzlatgich",
                                        "prompt_ru": "холодильник",
                                        "prompt_tj": "яхдон",
                                        "answer": "冰箱",
                                        "pinyin": "bīngxiāng"
                                },
                                {
                                        "prompt_uz": "banan",
                                        "prompt_ru": "банан",
                                        "prompt_tj": "банан",
                                        "answer": "香蕉",
                                        "pinyin": "xiāngjiāo"
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
                                        "prompt_uz": "水果",
                                        "prompt_ru": "水果",
                                        "prompt_tj": "水果",
                                        "answer": "meva / фрукты / мева",
                                        "pinyin": "shuǐguǒ"
                                },
                                {
                                        "prompt_uz": "打扫",
                                        "prompt_ru": "打扫",
                                        "prompt_tj": "打扫",
                                        "answer": "tozalamoq / убирать / тоза кардан",
                                        "pinyin": "dǎsǎo"
                                },
                                {
                                        "prompt_uz": "冰箱",
                                        "prompt_ru": "冰箱",
                                        "prompt_tj": "冰箱",
                                        "answer": "muzlatgich / холодильник / яхдон",
                                        "pinyin": "bīngxiāng"
                                },
                                {
                                        "prompt_uz": "香蕉",
                                        "prompt_ru": "香蕉",
                                        "prompt_tj": "香蕉",
                                        "answer": "banan / банан / банан",
                                        "pinyin": "xiāngjiāo"
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
                        "answers": ["水果", "打扫", "冰箱", "香蕉"]
                },
                {
                        "no": 2,
                        "answers": [
                                "meva / фрукты / мева",
                                "tozalamoq / убирать / тоза кардан",
                                "muzlatgich / холодильник / яхдон",
                                "banan / банан / банан"
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
                        "words": ["水果", "打扫", "冰箱"],
                        "example": "先把桌子打扫干净，然后把冰箱里的水果拿过来。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Mevalarni bu yerga olib kel",
                        "topic_ru": "Принеси сюда фрукты",
                        "topic_tj": "Меваҳоро ин ҷо биёр"
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
