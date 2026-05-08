import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 2,
    "lesson_code": "HSK3-L02",
    "title": "他什么时候回来",
    "goal": json.dumps({"uz": "qaytish va ketma-ket harakatlarni ifodalash", "ru": "выражение возвращения и последовательных действий", "tj": "ифодаи баргаштан ва амалҳои пайдарпай"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu dars qaytish va ketma-ket harakatlarni ifodalashga bag'ishlangan. Unda 5 ta asosiy so'z o'rganiladi va oddiy yo'nalish to'ldiruvchilari hamda ikki harakatning ketma-ket sodir bo'lishi kabi grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению возвращения и последовательных действий. В нём изучаются 5 ключевых слов и рассматриваются грамматические темы: простые направленные дополнения и два действия, следующие одно за другим.", "tj": "Ин дарс ба ифодаи баргаштан ва амалҳои пайдарпай бахшида шудааст. Дар он 5 калимаи асосӣ омӯхта мешавад ва мавзӯҳои грамматикии иловаҳои самтнок ва ду амали пайдарпай баррасӣ мегарданд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "回来",
                        "pinyin": "huílai",
                        "pos": "v.",
                        "uz": "qaytib kelmoq",
                        "ru": "вернуться, прийти обратно",
                        "tj": "баргаштан, бозгаштан"
                },
                {
                        "no": 2,
                        "zh": "办公室",
                        "pinyin": "bàngōngshì",
                        "pos": "n.",
                        "uz": "idora, ofis",
                        "ru": "офис, кабинет",
                        "tj": "идора, кабинет"
                },
                {
                        "no": 3,
                        "zh": "拿",
                        "pinyin": "ná",
                        "pos": "v.",
                        "uz": "olmoq, ko'tarmoq",
                        "ru": "брать, взять",
                        "tj": "гирифтан, бардоштан"
                },
                {
                        "no": 4,
                        "zh": "伞",
                        "pinyin": "sǎn",
                        "pos": "n.",
                        "uz": "soyabon",
                        "ru": "зонт",
                        "tj": "чатр"
                },
                {
                        "no": 5,
                        "zh": "腿",
                        "pinyin": "tuǐ",
                        "pos": "n.",
                        "uz": "oyoq (son)",
                        "ru": "нога (бедро/голень)",
                        "tj": "по, ронак"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Idorada kutish",
                        "scene_ru": "Ожидание в офисе",
                        "scene_tj": "Интизор шудан дар идора",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "他什么时候回来？",
                                        "pinyin": "",
                                        "uz": "U qachon qaytib keladi?",
                                        "ru": "Когда он вернётся?",
                                        "tj": "Вай кай бармегардад?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "他先去办公室拿文件，马上就回来。",
                                        "pinyin": "",
                                        "uz": "U avval idoraga hujjat olishga ketdi, hozir qaytadi.",
                                        "ru": "Он сначала пошёл в офис за документами, сейчас вернётся.",
                                        "tj": "Вай аввал ба идора барои ҳуҷҷат рафт, ҳозир бармегардад."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Yomg'irli kunda",
                        "scene_ru": "В дождливый день",
                        "scene_tj": "Дар рӯзи борондор",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "外边下雨了，你把伞拿回来了吗？",
                                        "pinyin": "",
                                        "uz": "Tashqarida yomg'ir yog'yapti, soyabonni olib keldingizmi?",
                                        "ru": "На улице дождь, ты принёс зонт обратно?",
                                        "tj": "Берун борон меборад, чатрро баргардондӣ?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "拿回来了，不过我的腿还有点儿疼。",
                                        "pinyin": "",
                                        "uz": "Olib keldim, lekin oyog'im hali biroz og'riydi.",
                                        "ru": "Принёс, но моя нога ещё немного болит.",
                                        "tj": "Оvardам, аммо пои ман ҳанӯз каме дард мекунад."
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
                        "title_zh": "简单趋向补语",
                        "title_uz": "Oddiy yo'nalish to'ldiruvchisi",
                        "title_ru": "Простое направленное дополнение",
                        "title_tj": "Иловаи самтноки содда",
                        "rule_uz": "Bu mavzu harakatning yo'nalishini yoki sub'ekt harakatdan keyin qayerda ekanligini ko'rsatadi.",
                        "rule_ru": "Эта тема показывает направление движения действия или где субъект оказывается в результате.",
                        "rule_tj": "Ин мавзӯ самти ҳаракати амал ё ҷойеро, ки субъект дар натиҷа қарор мегирад, нишон медиҳад.",
                        "examples": [
                                {
                                        "zh": "他什么时候回来。",
                                        "pinyin": "",
                                        "uz": "Darsning asosiy qolipi.",
                                        "ru": "Основная конструкция урока.",
                                        "tj": "Қолаби асосии дарс."
                                },
                                {
                                        "zh": "这个句子里有回来和办公室。",
                                        "pinyin": "",
                                        "uz": "Bu gapda 回来 va 办公室 so'zlari bor.",
                                        "ru": "В этом предложении используются слова 回来 и 办公室.",
                                        "tj": "Дар ин ҷумла калимаҳои 回来 ва 办公室 истифода шудаанд."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "两个动作连续发生",
                        "title_uz": "Ikki harakatning ketma-ket sodir bo'lishi",
                        "title_ru": "Два действия, следующие одно за другим",
                        "title_tj": "Ду амали пайдарпай",
                        "rule_uz": "Bu grammatik mavzu dars asosiy gap qoliplarini mashq qilishga yordam beradi.",
                        "rule_ru": "Эта грамматическая тема помогает отработать основные конструкции урока.",
                        "rule_tj": "Ин мавзӯи грамматикӣ ба машқ кардани қолабҳои асосии дарс кӯмак мекунад.",
                        "examples": [
                                {
                                        "zh": "他什么时候回来。",
                                        "pinyin": "",
                                        "uz": "Darsning asosiy qolipi.",
                                        "ru": "Основная конструкция урока.",
                                        "tj": "Қолаби асосии дарс."
                                },
                                {
                                        "zh": "这个句子里有回来和办公室。",
                                        "pinyin": "",
                                        "uz": "Bu gapda 回来 va 办公室 so'zlari bor.",
                                        "ru": "В этом предложении используются слова 回来 и 办公室.",
                                        "tj": "Дар ин ҷумла калимаҳои 回来 ва 办公室 истифода шудаанд."
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
                                        "prompt_uz": "qaytib kelmoq",
                                        "prompt_ru": "вернуться",
                                        "prompt_tj": "баргаштан",
                                        "answer": "回来",
                                        "pinyin": "huílai"
                                },
                                {
                                        "prompt_uz": "idora, ofis",
                                        "prompt_ru": "офис",
                                        "prompt_tj": "идора",
                                        "answer": "办公室",
                                        "pinyin": "bàngōngshì"
                                },
                                {
                                        "prompt_uz": "olmoq, ko'tarmoq",
                                        "prompt_ru": "брать",
                                        "prompt_tj": "гирифтан",
                                        "answer": "拿",
                                        "pinyin": "ná"
                                },
                                {
                                        "prompt_uz": "soyabon",
                                        "prompt_ru": "зонт",
                                        "prompt_tj": "чатр",
                                        "answer": "伞",
                                        "pinyin": "sǎn"
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
                                        "prompt_uz": "回来",
                                        "prompt_ru": "回来",
                                        "prompt_tj": "回来",
                                        "answer": "回来",
                                        "pinyin": "huílai"
                                },
                                {
                                        "prompt_uz": "办公室",
                                        "prompt_ru": "办公室",
                                        "prompt_tj": "办公室",
                                        "answer": "办公室",
                                        "pinyin": "bàngōngshì"
                                },
                                {
                                        "prompt_uz": "拿",
                                        "prompt_ru": "拿",
                                        "prompt_tj": "拿",
                                        "answer": "拿",
                                        "pinyin": "ná"
                                },
                                {
                                        "prompt_uz": "伞",
                                        "prompt_ru": "伞",
                                        "prompt_tj": "伞",
                                        "answer": "伞",
                                        "pinyin": "sǎn"
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
                                "回来",
                                "办公室",
                                "拿",
                                "伞"
                        ]
                },
                {
                        "no": 2,
                        "answers": [
                                "回来",
                                "办公室",
                                "拿",
                                "伞"
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
                                "回来",
                                "办公室",
                                "拿"
                        ],
                        "topic_uz": "回来 va 办公室 so'zlarini bir gapda ishlatish mumkin.",
                        "topic_ru": "Слова 回来 и 办公室 можно использовать в одном предложении.",
                        "topic_tj": "Калимаҳои 回来 ва 办公室 метавонанд дар як ҷумла истифода шаванд."
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий абзац из 4-5 предложений по теме урока:",
                        "instruction_tj": "Дар мавзӯи дарс матни кӯтоҳи 4-5 ҷумлагӣ нависед:",
                        "topic_uz": "他什么时候回来",
                        "topic_ru": "他什么时候回来",
                        "topic_tj": "他什么时候回来"
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
