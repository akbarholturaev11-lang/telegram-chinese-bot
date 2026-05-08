import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 11,
    "lesson_code": "HSK3-L11",
    "title": "别忘了把空调关了",
    "goal": json.dumps({"uz": "eslatma berish va 把 gaplar tuzilmasidan foydalanish", "ru": "давать напоминания и использовать конструкцию с 把", "tj": "додани хотиррасонӣ ва истифодаи сохтори ҷумла бо 把"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda eslatma berish va 把 gaplar tuzilmasidan foydalanish o'rgatiladi. 5 ta asosiy so'z va «把»字句 1：A 把 B + V + …… hamda 概数的表达 2：左右 grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён напоминаниям и конструкции с 把. Вводятся 5 ключевых слов и грамматические конструкции «把»字句 1：A 把 B + V + …… и 概数的表达 2：左右.", "tj": "Ин дарс ба додани хотиррасонӣ ва истифодаи сохтори ҷумла бо 把 бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии «把»字句 1：A 把 B + V + …… ва 概数的表达 2：左右 омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "空调",
                        "pinyin": "kōngtiáo",
                        "pos": "n.",
                        "uz": "konditsioner",
                        "ru": "кондиционер",
                        "tj": "кондитсионер"
                },
                {
                        "no": 2,
                        "zh": "图书馆",
                        "pinyin": "túshūguǎn",
                        "pos": "n.",
                        "uz": "kutubxona",
                        "ru": "библиотека",
                        "tj": "китобхона"
                },
                {
                        "no": 3,
                        "zh": "词典",
                        "pinyin": "cídiǎn",
                        "pos": "n.",
                        "uz": "lug'at",
                        "ru": "словарь",
                        "tj": "луғат"
                },
                {
                        "no": 4,
                        "zh": "地铁",
                        "pinyin": "dìtiě",
                        "pos": "n.",
                        "uz": "metro",
                        "ru": "метро",
                        "tj": "метро"
                },
                {
                        "no": 5,
                        "zh": "关",
                        "pinyin": "guān",
                        "pos": "v.",
                        "uz": "yopmoq; o'chirmoq",
                        "ru": "закрывать; выключать",
                        "tj": "пӯшидан; хомӯш кардан"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Ketishdan oldin",
                        "scene_ru": "Перед уходом",
                        "scene_tj": "Пеш аз рафтан",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "别忘了把空调关了。",
                                        "pinyin": "Bié wàngle bǎ kōngtiáo guān le.",
                                        "uz": "Konditsionerni o'chirishni unutma.",
                                        "ru": "Не забудь выключить кондиционер.",
                                        "tj": "Фаромӯш накун кондитсионерро хомӯш кун."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，我把门也关上。",
                                        "pinyin": "Hǎo, wǒ bǎ mén yě guān shang.",
                                        "uz": "Yaxshi, eshikni ham yopaman.",
                                        "ru": "Хорошо, я и дверь закрою.",
                                        "tj": "Хуб, дарро ҳам мепӯшам."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Kutubxonada",
                        "scene_ru": "В библиотеке",
                        "scene_tj": "Дар китобхона",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "你要借这本词典吗？",
                                        "pinyin": "Nǐ yào jiè zhè běn cídiǎn ma?",
                                        "uz": "Bu lug'atni olmoqchimisiz?",
                                        "ru": "Ты хочешь взять этот словарь?",
                                        "tj": "Оё шумо мехоҳед ин луғатро қарз гиред?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "要，坐地铁过去大概二十分钟左右。",
                                        "pinyin": "Yào, zuò dìtiě guòqù dàgài èrshí fēnzhōng zuǒyòu.",
                                        "uz": "Ha, metro bilan borish taxminan yigirma daqiqa.",
                                        "ru": "Да, на метро туда примерно двадцать минут.",
                                        "tj": "Бале, бо метро тақрибан бист дақиқа роҳ аст."
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
                        "title_zh": "«把»字句 1：A 把 B + V + ……",
                        "title_uz": "«把» li gap 1: A 把 B + fe'l + …",
                        "title_ru": "Конструкция с «把» 1: A 把 B + глагол + …",
                        "title_tj": "Ҷумла бо «把» 1: A 把 B + феъл + …",
                        "rule_uz": "Bu tuzilma ta'sirlangan ob'ektni oldinga chiqaradi va natijani yoki yo'nalishni ta'kidlaydi.",
                        "rule_ru": "Эта конструкция выносит объект воздействия на первый план, чтобы подчеркнуть результат или направление действия.",
                        "rule_tj": "Ин сохтор объекти таъсиррасонидашударо ба пеш меорад ва натиҷа ё самти амалро таъкид мекунад.",
                        "examples": [
                                {
                                        "zh": "别忘了把空调关了。",
                                        "pinyin": "Bié wàngle bǎ kōngtiáo guān le.",
                                        "uz": "Konditsionerni o'chirishni unutma.",
                                        "ru": "Не забудь выключить кондиционер.",
                                        "tj": "Фаромӯш накун кондитсионерро хомӯш кун."
                                },
                                {
                                        "zh": "请把词典放在桌子上。",
                                        "pinyin": "Qǐng bǎ cídiǎn fàng zài zhuōzi shang.",
                                        "uz": "Iltimos, lug'atni stol ustiga qo'ying.",
                                        "ru": "Пожалуйста, положите словарь на стол.",
                                        "tj": "Лутфан луғатро рӯи мизро гузоред."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "概数的表达 2：左右",
                        "title_uz": "Taxminiy sonlar ifodalash 2: 左右 (taxminan)",
                        "title_ru": "Выражение приблизительных чисел 2: 左右 (примерно)",
                        "title_tj": "Ифода кардани рақамҳои тахминӣ 2: 左右 (тақрибан)",
                        "rule_uz": "左右 so'zi raqam yoki vaqtning taxminiy ekanligini bildiradi.",
                        "rule_ru": "Слово 左右 указывает на то, что число или время является приблизительным.",
                        "rule_tj": "Калимаи 左右 нишон медиҳад, ки рақам ё вақт тахминӣ аст.",
                        "examples": [
                                {
                                        "zh": "坐地铁大概二十分钟左右。",
                                        "pinyin": "Zuò dìtiě dàgài èrshí fēnzhōng zuǒyòu.",
                                        "uz": "Metro bilan taxminan yigirma daqiqa.",
                                        "ru": "На метро примерно двадцать минут.",
                                        "tj": "Бо метро тақрибан бист дақиқа."
                                },
                                {
                                        "zh": "他三十岁左右。",
                                        "pinyin": "Tā sānshí suì zuǒyòu.",
                                        "uz": "U taxminan o'ttiz yoshda.",
                                        "ru": "Ему примерно тридцать лет.",
                                        "tj": "Вай тақрибан си сол дорад."
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
                                        "prompt_uz": "konditsioner",
                                        "prompt_ru": "кондиционер",
                                        "prompt_tj": "кондитсионер",
                                        "answer": "空调",
                                        "pinyin": "kōngtiáo"
                                },
                                {
                                        "prompt_uz": "kutubxona",
                                        "prompt_ru": "библиотека",
                                        "prompt_tj": "китобхона",
                                        "answer": "图书馆",
                                        "pinyin": "túshūguǎn"
                                },
                                {
                                        "prompt_uz": "lug'at",
                                        "prompt_ru": "словарь",
                                        "prompt_tj": "луғат",
                                        "answer": "词典",
                                        "pinyin": "cídiǎn"
                                },
                                {
                                        "prompt_uz": "metro",
                                        "prompt_ru": "метро",
                                        "prompt_tj": "метро",
                                        "answer": "地铁",
                                        "pinyin": "dìtiě"
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
                                        "prompt_uz": "空调",
                                        "prompt_ru": "空调",
                                        "prompt_tj": "空调",
                                        "answer": "konditsioner / кондиционер / кондитсионер",
                                        "pinyin": "kōngtiáo"
                                },
                                {
                                        "prompt_uz": "图书馆",
                                        "prompt_ru": "图书馆",
                                        "prompt_tj": "图书馆",
                                        "answer": "kutubxona / библиотека / китобхона",
                                        "pinyin": "túshūguǎn"
                                },
                                {
                                        "prompt_uz": "词典",
                                        "prompt_ru": "词典",
                                        "prompt_tj": "词典",
                                        "answer": "lug'at / словарь / луғат",
                                        "pinyin": "cídiǎn"
                                },
                                {
                                        "prompt_uz": "地铁",
                                        "prompt_ru": "地铁",
                                        "prompt_tj": "地铁",
                                        "answer": "metro / метро / метро",
                                        "pinyin": "dìtiě"
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
                        "answers": ["空调", "图书馆", "词典", "地铁"]
                },
                {
                        "no": 2,
                        "answers": [
                                "konditsioner / кондиционер / кондитсионер",
                                "kutubxona / библиотека / китобхона",
                                "lug'at / словарь / луғат",
                                "metro / метро / метро"
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
                        "words": ["空调", "图书馆", "词典"],
                        "example": "别忘了把空调关了，然后去图书馆。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Konditsionerni o'chirishni unutma",
                        "topic_ru": "Не забудь выключить кондиционер",
                        "topic_tj": "Фаромӯш накун кондитсионерро хомӯш кун"
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
