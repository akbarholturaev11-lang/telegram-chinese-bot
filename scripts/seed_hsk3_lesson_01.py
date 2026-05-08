import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 1,
    "lesson_code": "HSK3-L01",
    "title": "周末你有什么打算",
    "goal": json.dumps({"uz": "dam olish kunlari rejalari haqida gapirish", "ru": "говорить о планах на выходные", "tj": "дар бораи нақшаҳои охири ҳафта сӯҳбат кардан"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu dars dam olish kunlari rejalari haqida gaplashishga bag'ishlangan. Unda 5 ta asosiy so'z o'rganiladi va 好 natija to'ldiruvchisi hamda 一......也/都 + 不/没...... inkor qolipi kabi grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён разговорам о планах на выходные. В нём изучаются 5 ключевых слов и рассматриваются грамматические темы: результативное дополнение 好 и конструкция 一......也/都 + 不/没...... для выражения отрицания.", "tj": "Ин дарс ба сӯҳбат дар бораи нақшаҳои охири ҳафта бахшида шудааст. Дар он 5 калимаи асосӣ омӯхта мешавад ва мавзӯҳои грамматикии иловаи натиҷавӣ 好 ва қолаби инкорӣ 一......也/都 + 不/没...... баррасӣ мегарданд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "周末",
                        "pinyin": "zhōumò",
                        "pos": "n.",
                        "uz": "dam olish kuni, hafta oxiri",
                        "ru": "выходные (дни)",
                        "tj": "охири ҳафта, рӯзҳои истироҳат"
                },
                {
                        "no": 2,
                        "zh": "打算",
                        "pinyin": "dǎsuàn",
                        "pos": "v./n.",
                        "uz": "reja qilmoq; reja",
                        "ru": "планировать; план",
                        "tj": "нақша кашидан; нақша"
                },
                {
                        "no": 3,
                        "zh": "作业",
                        "pinyin": "zuòyè",
                        "pos": "n.",
                        "uz": "uy vazifasi",
                        "ru": "домашнее задание",
                        "tj": "вазифаи хонагӣ"
                },
                {
                        "no": 4,
                        "zh": "着急",
                        "pinyin": "zháojí",
                        "pos": "adj.",
                        "uz": "tashvishlanmoq, xavotir olmoq",
                        "ru": "беспокоиться, нервничать",
                        "tj": "ташвиш кашидан, нигарон будан"
                },
                {
                        "no": 5,
                        "zh": "地图",
                        "pinyin": "dìtú",
                        "pos": "n.",
                        "uz": "xarita",
                        "ru": "карта",
                        "tj": "харита"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Dam olish kuni rejasi",
                        "scene_ru": "План на выходные",
                        "scene_tj": "Нақшаи охири ҳафта",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "周末你有什么打算？",
                                        "pinyin": "",
                                        "uz": "Dam olish kunlari nima qilmoqchisiz?",
                                        "ru": "Какие у тебя планы на выходные?",
                                        "tj": "Охири ҳафта чӣ нақша дорӣ?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "我想先写作业，然后跟朋友出去。",
                                        "pinyin": "",
                                        "uz": "Avval uy vazifasini qilmoqchiman, keyin do'st bilan chiqmoqchiman.",
                                        "ru": "Сначала хочу сделать домашнее задание, потом выйти с другом.",
                                        "tj": "Аввал мехоҳам вазифаи хонагиро анҷом диҳам, сипас бо дӯст берун равам."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Narsalarni tayyorlash",
                        "scene_ru": "Подготовка вещей",
                        "scene_tj": "Тайёр кардани чизҳо",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "去公园要不要带地图？",
                                        "pinyin": "",
                                        "uz": "Parka borishda xarita olib borishimiz kerakmi?",
                                        "ru": "Нужно ли брать карту в парк?",
                                        "tj": "Ба бӯстон рафтан хариту лозим аст?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "不用着急，我都准备好了。",
                                        "pinyin": "",
                                        "uz": "Xavotir olmang, men hamma narsani tayyorladim.",
                                        "ru": "Не беспокойтесь, я всё уже подготовил.",
                                        "tj": "Ташвиш накашед, ман ҳама чизро тайёр кардаам."
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
                        "title_zh": "结果补语“好”",
                        "title_uz": "Natija to'ldiruvchisi “好”",
                        "title_ru": "Результативное дополнение «好»",
                        "title_tj": "Иловаи натиҷавӣ «好»",
                        "rule_uz": "Bu qolip biror harakatning muvaffaqiyatli yoki to'liq bajarilganligini bildiradi.",
                        "rule_ru": "Эта конструкция указывает на то, что действие выполнено успешно или полностью.",
                        "rule_tj": "Ин қолаб нишон медиҳад, ки амал бомуваффақият ё пурра иҷро шудааст.",
                        "examples": [
                                {
                                        "zh": "我准备好了。",
                                        "pinyin": "",
                                        "uz": "Men tayyor bo'ldim.",
                                        "ru": "Я готов.",
                                        "tj": "Ман тайёрам."
                                },
                                {
                                        "zh": "电影票买好了。",
                                        "pinyin": "",
                                        "uz": "Kino chiptasi sotib olindi.",
                                        "ru": "Билеты в кино куплены.",
                                        "tj": "Чиптаи кино харидорӣ шуд."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "一......也/都 + 不/没......表示否定",
                        "title_uz": "一......也/都 + 不/没...... inkor ifodalash",
                        "title_ru": "一......也/都 + 不/没...... для выражения отрицания",
                        "title_tj": "一......也/都 + 不/没...... барои ифодаи инкор",
                        "rule_uz": "Bu grammatik mavzu dars asosiy gap qoliplarini mashq qilishga yordam beradi.",
                        "rule_ru": "Эта грамматическая тема помогает отработать основные конструкции урока.",
                        "rule_tj": "Ин мавзӯи грамматикӣ ба машқ кардани қолабҳои асосии дарс кӯмак мекунад.",
                        "examples": [
                                {
                                        "zh": "周末你有什么打算。",
                                        "pinyin": "",
                                        "uz": "Darsning asosiy qolipi.",
                                        "ru": "Основная конструкция урока.",
                                        "tj": "Қолаби асосии дарс."
                                },
                                {
                                        "zh": "这个句子里有周末和打算。",
                                        "pinyin": "",
                                        "uz": "Bu gapda 周末 va 打算 so'zlari bor.",
                                        "ru": "В этом предложении используются слова 周末 и 打算.",
                                        "tj": "Дар ин ҷумла калимаҳои 周末 ва 打算 истифода шудаанд."
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
                        "instruction_uz": "Quyidagi so'zlarning xitoychasini yozing:",
                        "instruction_ru": "Запишите по-китайски следующие слова:",
                        "instruction_tj": "Калимаҳои зеринро бо хитоӣ нависед:",
                        "items": [
                                {
                                        "prompt_uz": "dam olish kuni",
                                        "prompt_ru": "выходные",
                                        "prompt_tj": "охири ҳафта",
                                        "answer": "周末",
                                        "pinyin": "zhōumò"
                                },
                                {
                                        "prompt_uz": "reja qilmoq; reja",
                                        "prompt_ru": "планировать; план",
                                        "prompt_tj": "нақша кашидан; нақша",
                                        "answer": "打算",
                                        "pinyin": "dǎsuàn"
                                },
                                {
                                        "prompt_uz": "uy vazifasi",
                                        "prompt_ru": "домашнее задание",
                                        "prompt_tj": "вазифаи хонагӣ",
                                        "answer": "作业",
                                        "pinyin": "zuòyè"
                                },
                                {
                                        "prompt_uz": "tashvishlanmoq",
                                        "prompt_ru": "беспокоиться",
                                        "prompt_tj": "ташвиш кашидан",
                                        "answer": "着急",
                                        "pinyin": "zháojí"
                                }
                        ]
                },
                {
                        "no": 2,
                        "type": "translate_to_uzbek",
                        "instruction_uz": "Quyidagi so'zlarning ma'nosini yozing:",
                        "instruction_ru": "Запишите значение следующих слов:",
                        "instruction_tj": "Маънои калимаҳои зеринро нависед:",
                        "items": [
                                {
                                        "prompt_uz": "周末",
                                        "prompt_ru": "周末",
                                        "prompt_tj": "周末",
                                        "answer": "周末",
                                        "pinyin": "zhōumò"
                                },
                                {
                                        "prompt_uz": "打算",
                                        "prompt_ru": "打算",
                                        "prompt_tj": "打算",
                                        "answer": "打算",
                                        "pinyin": "dǎsuàn"
                                },
                                {
                                        "prompt_uz": "作业",
                                        "prompt_ru": "作业",
                                        "prompt_tj": "作业",
                                        "answer": "作业",
                                        "pinyin": "zuòyè"
                                },
                                {
                                        "prompt_uz": "着急",
                                        "prompt_ru": "着急",
                                        "prompt_tj": "着急",
                                        "answer": "着急",
                                        "pinyin": "zháojí"
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
                                "周末",
                                "打算",
                                "作业",
                                "着急"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "周末",
                                "打算",
                                "作业",
                                "着急"
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
                        "instruction_tj": "Бо истифода аз калимаҳои зерин 3 ҷумла тартиб диҳед:",
                        "words": [
                                "周末",
                                "打算",
                                "作业"
                        ],
                        "topic_uz": "周末 va 打算 so'zlarini bir gapda ishlatish mumkin.",
                        "topic_ru": "Слова 周末 и 打算 можно использовать в одном предложении.",
                        "topic_tj": "Калимаҳои 周末 ва 打算 метавонанд дар як ҷумла истифода шаванд."
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий абзац из 4-5 предложений по теме урока:",
                        "instruction_tj": "Дар мавзӯи дарс матни кӯтоҳи 4-5 ҷумлагӣ нависед:",
                        "topic_uz": "周末你有什么打算",
                        "topic_ru": "周末你有什么打算",
                        "topic_tj": "周末你有什么打算"
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
