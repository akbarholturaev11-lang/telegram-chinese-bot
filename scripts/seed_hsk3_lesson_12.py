import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 12,
    "lesson_code": "HSK3-L12",
    "title": "把重要的东西放在我这儿吧",
    "goal": json.dumps({"uz": "biror narsani joyda qoldirish va topshirishni ifodalash", "ru": "выражение оставления чего-либо в месте и передачи вещей", "tj": "ифода кардани гузоштани чизе дар ҷое ва супоридани ашё"}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu darsda biror narsani joyda qoldirish va topshirishni ifodalash o'rgatiladi. 5 ta asosiy so'z va «才»和«就» hamda «把»字句 2：A 把 B + V + 在/到/给…… grammatik mavzular ko'rib chiqiladi.", "ru": "Этот урок посвящён выражению оставления чего-либо в месте и передачи вещей. Вводятся 5 ключевых слов и грамматические конструкции «才»和«就» и «把»字句 2：A 把 B + V + 在/到/给……", "tj": "Ин дарс ба ифода кардани гузоштани чизе дар ҷое ва супоридани ашё бахшида шудааст. 5 калимаи асосӣ ва намунаҳои грамматикии «才»和«就» ва «把»字句 2：A 把 B + V + 在/到/给…… омӯхта мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps(
        [
                {
                        "no": 1,
                        "zh": "行李箱",
                        "pinyin": "xínglixiāng",
                        "pos": "n.",
                        "uz": "chemodan",
                        "ru": "чемодан",
                        "tj": "чамадон"
                },
                {
                        "no": 2,
                        "zh": "护照",
                        "pinyin": "hùzhào",
                        "pos": "n.",
                        "uz": "pasport",
                        "ru": "паспорт",
                        "tj": "шиноснома"
                },
                {
                        "no": 3,
                        "zh": "起飞",
                        "pinyin": "qǐfēi",
                        "pos": "v.",
                        "uz": "uchib ketmoq (samolyot)",
                        "ru": "взлетать (самолёт)",
                        "tj": "парвоз кардан (тайёра)"
                },
                {
                        "no": 4,
                        "zh": "司机",
                        "pinyin": "sījī",
                        "pos": "n.",
                        "uz": "haydovchi",
                        "ru": "водитель",
                        "tj": "ронанда"
                },
                {
                        "no": 5,
                        "zh": "黑板",
                        "pinyin": "hēibǎn",
                        "pos": "n.",
                        "uz": "qora taxta",
                        "ru": "доска (классная)",
                        "tj": "тахтаи сиёҳ"
                }
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
                {
                        "block_no": 1,
                        "section_label": "课文 1",
                        "scene_uz": "Aeroportda",
                        "scene_ru": "В аэропорту",
                        "scene_tj": "Дар фурудгоҳ",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "把重要的东西放在我这儿吧。",
                                        "pinyin": "Bǎ zhòngyào de dōngxi fàng zài wǒ zhèr ba.",
                                        "uz": "Muhim narsalarni menda qoldiring.",
                                        "ru": "Оставь важные вещи у меня.",
                                        "tj": "Чизҳои муҳимро пеши ман бигзор."
                                },
                                {
                                        "speaker": "B",
                                        "zh": "好，护照和票我先给你。",
                                        "pinyin": "Hǎo, hùzhào hé piào wǒ xiān gěi nǐ.",
                                        "uz": "Yaxshi, pasport va chiptani avval sizga beraman.",
                                        "ru": "Хорошо, паспорт и билеты сначала отдам тебе.",
                                        "tj": "Хуб, шиносномаву чиптаро аввал ба шумо медиҳам."
                                }
                        ]
                },
                {
                        "block_no": 2,
                        "section_label": "课文 2",
                        "scene_uz": "Darsdan oldin",
                        "scene_ru": "Перед уроком",
                        "scene_tj": "Пеш аз дарс",
                        "dialogue": [
                                {
                                        "speaker": "A",
                                        "zh": "司机什么时候到？",
                                        "pinyin": "Sījī shénme shíhou dào?",
                                        "uz": "Haydovchi qachon keladi?",
                                        "ru": "Когда приедет водитель?",
                                        "tj": "Ронанда кай мерасад?"
                                },
                                {
                                        "speaker": "B",
                                        "zh": "他到了以后，我们就出发。",
                                        "pinyin": "Tā dào le yǐhòu, wǒmen jiù chūfā.",
                                        "uz": "U kelgandan keyin jo'naymiz.",
                                        "ru": "После его приезда мы сразу отправимся.",
                                        "tj": "Пас аз расидани вай, мо рост мебароем."
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
                        "title_zh": "«才»和«就»",
                        "title_uz": "«才» va «就» farqi",
                        "title_ru": "Разница между «才» и «就»",
                        "title_tj": "Фарқи «才» ва «就»",
                        "rule_uz": "才 – kutilganidan kech yoki qiyin bo'lgan holatda ishlatiladi. 就 – tez yoki oson amalga oshganini bildiradi.",
                        "rule_ru": "才 используется, когда что-то произошло позже или с большим трудом, чем ожидалось. 就 указывает на быстрое или лёгкое выполнение.",
                        "rule_tj": "才 вақте истифода мешавад, ки чизе дертар ё душвортар аз интизор рух додааст. 就 нишон медиҳад, ки амал зуд ё осон иҷро шудааст.",
                        "examples": [
                                {
                                        "zh": "他十点才到。",
                                        "pinyin": "Tā shí diǎn cái dào.",
                                        "uz": "U soat o'nda(da nihoyat) keldi.",
                                        "ru": "Он приехал только в десять (и то наконец-то).",
                                        "tj": "Вай соати даҳ (нихоят) расид."
                                },
                                {
                                        "zh": "他八点就到了。",
                                        "pinyin": "Tā bā diǎn jiù dào le.",
                                        "uz": "U soat sakkizda(oq) keldi.",
                                        "ru": "Он приехал уже в восемь.",
                                        "tj": "Вай соати ҳашт (барвақт) расид."
                                }
                        ]
                },
                {
                        "no": 2,
                        "title_zh": "«把»字句 2：A 把 B + V + 在/到/给……",
                        "title_uz": "«把» li gap 2: A 把 B + fe'l + 在/到/给…",
                        "title_ru": "Конструкция с «把» 2: A 把 B + глагол + 在/到/给…",
                        "title_tj": "Ҷумла бо «把» 2: A 把 B + феъл + 在/到/给…",
                        "rule_uz": "Bu tuzilma ob'ektni joy, yo'nalish yoki qabul qiluvchi bilan birga ifodalash uchun ishlatiladi.",
                        "rule_ru": "Эта конструкция используется для указания места, направления или получателя в результате действия.",
                        "rule_tj": "Ин сохтор барои нишон додани макон, самт ё гиранда дар натиҷаи амал истифода мешавад.",
                        "examples": [
                                {
                                        "zh": "把重要的东西放在我这儿吧。",
                                        "pinyin": "Bǎ zhòngyào de dōngxi fàng zài wǒ zhèr ba.",
                                        "uz": "Muhim narsalarni menda qoldiring.",
                                        "ru": "Оставь важные вещи у меня.",
                                        "tj": "Чизҳои муҳимро пеши ман бигзор."
                                },
                                {
                                        "zh": "请把行李箱放到那边。",
                                        "pinyin": "Qǐng bǎ xínglixiāng fàng dào nà biān.",
                                        "uz": "Iltimos, chemodonni u yonga qo'ying.",
                                        "ru": "Пожалуйста, поставьте чемодан туда.",
                                        "tj": "Лутфан чамадонро он тараф гузоред."
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
                                        "prompt_uz": "chemodan",
                                        "prompt_ru": "чемодан",
                                        "prompt_tj": "чамадон",
                                        "answer": "行李箱",
                                        "pinyin": "xínglixiāng"
                                },
                                {
                                        "prompt_uz": "pasport",
                                        "prompt_ru": "паспорт",
                                        "prompt_tj": "шиноснома",
                                        "answer": "护照",
                                        "pinyin": "hùzhào"
                                },
                                {
                                        "prompt_uz": "uchib ketmoq (samolyot)",
                                        "prompt_ru": "взлетать (самолёт)",
                                        "prompt_tj": "парвоз кардан (тайёра)",
                                        "answer": "起飞",
                                        "pinyin": "qǐfēi"
                                },
                                {
                                        "prompt_uz": "haydovchi",
                                        "prompt_ru": "водитель",
                                        "prompt_tj": "ронанда",
                                        "answer": "司机",
                                        "pinyin": "sījī"
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
                                        "prompt_uz": "行李箱",
                                        "prompt_ru": "行李箱",
                                        "prompt_tj": "行李箱",
                                        "answer": "chemodan / чемодан / чамадон",
                                        "pinyin": "xínglixiāng"
                                },
                                {
                                        "prompt_uz": "护照",
                                        "prompt_ru": "护照",
                                        "prompt_tj": "护照",
                                        "answer": "pasport / паспорт / шиноснома",
                                        "pinyin": "hùzhào"
                                },
                                {
                                        "prompt_uz": "起飞",
                                        "prompt_ru": "起飞",
                                        "prompt_tj": "起飞",
                                        "answer": "uchib ketmoq / взлетать / парвоз кардан",
                                        "pinyin": "qǐfēi"
                                },
                                {
                                        "prompt_uz": "司机",
                                        "prompt_ru": "司机",
                                        "prompt_tj": "司机",
                                        "answer": "haydovchi / водитель / ронанда",
                                        "pinyin": "sījī"
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
                        "answers": ["行李箱", "护照", "起飞", "司机"]
                },
                {
                        "no": 2,
                        "answers": [
                                "chemodan / чемодан / чамадон",
                                "pasport / паспорт / шиноснома",
                                "uchib ketmoq / взлетать / парвоз кардан",
                                "haydovchi / водитель / ронанда"
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
                        "words": ["行李箱", "护照", "起飞"],
                        "example": "把护照和行李箱准备好，飞机马上起飞。"
                },
                {
                        "no": 2,
                        "instruction_uz": "Dars mavzusi bo'yicha 4-5 ta gapdan iborat qisqa matn yozing:",
                        "instruction_ru": "Напишите короткий текст из 4–5 предложений по теме урока:",
                        "instruction_tj": "Дар бораи мавзӯи дарс матни кӯтоҳ аз 4-5 ҷумла нависед:",
                        "topic_uz": "Muhim narsalarni menda qoldiring",
                        "topic_ru": "Оставь важные вещи у меня",
                        "topic_tj": "Чизҳои муҳимро пеши ман бигзор"
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
