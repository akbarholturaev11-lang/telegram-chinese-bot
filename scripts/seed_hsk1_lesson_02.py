import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 2,
    "lesson_code": "HSK1-L02",
    "title": "谢谢你",
    "goal": json.dumps({
        "uz": "Xitoy tilida minnatdorchilik bildirish va xayrlashishni o'rganing",
        "tj": "Бо забони чинӣ чӣ гуна изҳори миннатдорӣ кардан ва хайрухуш карданро омӯзед",
        "ru": "Научитесь выражать благодарность и прощаться на китайском языке."
}, ensure_ascii=False),
    "intro_text": json.dumps({
        "uz": "Ikkinchi darsda siz xitoy tilida minnatdorchilik bildirishni va xayrlashishni o'rganasiz. 4 ta yangi so'z, 3 ta dialog va neytral ohang qoidalari.",
        "tj": "Дар дарси дуюм шумо тарзи изҳори миннатдорӣ ва хайрбод бо забони чиниро меомӯзед. 4 калимаи нав, 3 муколама ва қоидаҳои оҳанги бетараф.",
        "ru": "На втором уроке вы научитесь выражать благодарность и прощаться на китайском языке. 4 новых слова, 3 диалога и правила нейтрального тона."
}, ensure_ascii=False),

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "谢谢",
                "pinyin": "xièxie",
                "pos": "v.",
                "meaning": {
                        "uz": "rahmat, rahmat",
                        "tj": "ташаккур, ташаккур",
                        "ru": "поблагодарить, спасибо"
                }
        },
        {
                "no": 2,
                "zh": "不",
                "pinyin": "bù",
                "pos": "adv.",
                "meaning": {
                        "uz": "yo'q, yo'q",
                        "tj": "не, не",
                        "ru": "нет, нет"
                }
        },
        {
                "no": 3,
                "zh": "不客气",
                "pinyin": "bú kèqi",
                "pos": "expr.",
                "meaning": {
                        "uz": "xush kelibsiz, muammo yo'q",
                        "tj": "хуш омадед, мушкиле нест",
                        "ru": "пожалуйста, без проблем"
                }
        },
        {
                "no": 4,
                "zh": "再见",
                "pinyin": "zàijiàn",
                "pos": "v.",
                "meaning": {
                        "uz": "xayr, ko'rishguncha",
                        "tj": "хайр, дидор",
                        "ru": "до свидания, увидимся"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Yordam uchun rahmat",
                        "tj": "Ташаккур барои кӯмак",
                        "ru": "Спасибо за помощь"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "谢谢！",
                                "pinyin": "Xièxie!",
                                "translation": {
                                        "uz": "Rahmat!",
                                        "tj": "Сипос!",
                                        "ru": "Спасибо!"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "不谢！",
                                "pinyin": "Bú xiè!",
                                "translation": {
                                        "uz": "Salomat bo'ling!",
                                        "tj": "Хушомадед!",
                                        "ru": "Пожалуйста!"
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Rasmiy rahmat",
                        "tj": "Ташаккури расмӣ",
                        "ru": "Официальное спасибо"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "谢谢你！",
                                "pinyin": "Xièxie nǐ!",
                                "translation": {
                                        "uz": "Rahmat!",
                                        "tj": "Сипос!",
                                        "ru": "Спасибо!"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "不客气！",
                                "pinyin": "Bú kèqi!",
                                "translation": {
                                        "uz": "Salomat bo'ling!",
                                        "tj": "Хушомадед!",
                                        "ru": "Пожалуйста!"
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Xayrlashuv",
                        "tj": "Алвидоъ",
                        "ru": "Xayrlashuv"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "再见！",
                                "pinyin": "Zàijiàn!",
                                "translation": {
                                        "uz": "Xayr. Salomat bo'ling!",
                                        "tj": "Хайр?",
                                        "ru": "До свидания!"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "再见！",
                                "pinyin": "Zàijiàn!",
                                "translation": {
                                        "uz": "Xayr. Salomat bo'ling!",
                                        "tj": "Хайр?",
                                        "ru": "До свидания!"
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "不 — Inkor yuklamasi",
                "explanation": {
                        "rule_uz": "y(bù) — inkor zarrasi (yo‘q, yo‘q).\nEslatma: shn 4-ton, lekin boshqa ohang-4 boʻgʻinidan oldin 2-tonga oʻzgaradi.\nbù + ohang 4 → bu + ohang 4\nMisol: shínhìmí → bú kèqi\nshíní → bú xiè",
                        "rule_tj": "不(bù) — заррачаи радкунанда (не, не).\nЭзоҳ: 不 оҳанги 4 аст, аммо пеш аз ҳиҷои дигар ба оҳанги 2 табдил меёбад.\nbù + оҳанги 4 → bú + оҳанги 4\nМисол: 不客气 → bú kèqi\n不谢 → bú xiè",
                        "rule_ru": "不(bù) — частица отрицания (нет, не).\nПримечание: 不 — это тон 4, но он меняется на тон 2 перед следующим слогом тона 4.\nbù + тон 4 → bú + тон 4\nПример: 不客气 → bú kèqi\n不谢 → бу сие"
                },
                "examples": [
                        {
                                "zh": "不谢",
                                "pinyin": "bú xiè",
                                "meaning": {
                                        "uz": "salomat bo'ling",
                                        "tj": "хушомадед",
                                        "ru": "пожалуйста"
                                }
                        },
                        {
                                "zh": "不客气",
                                "pinyin": "bú kèqi",
                                "meaning": {
                                        "uz": "salomat bo'ling",
                                        "tj": "хушомадед",
                                        "ru": "пожалуйста"
                                }
                        },
                        {
                                "zh": "不好",
                                "pinyin": "bù hǎo",
                                "meaning": {
                                        "uz": "yaxshi emas",
                                        "tj": "нағз не",
                                        "ru": "не хорошо"
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "轻声 — Neytral ton",
                "explanation": {
                        "rule_uz": "Xitoychada ham 5-ohang bor — neytral ohang (kánì).\nU qisqa va engil, ohang belgisi yo'q.\nKo'pincha qarindoshlik nuqtai nazaridan paydo bo'ladi.\nMisol: māma (māma), lānī(bàba), yéye (yéye), nǎinai (nǎinai)",
                        "rule_tj": "Чин низ оҳанги 5-ум дорад — оҳанги бетараф (轻声).\nОн кӯтоҳ ва сабук аст, бе аломати оҳанг.\nОн аксар вақт дар муносибатҳои хешутаборӣ зоҳир мешавад.\nМисол: 妈妈(māma), 爸爸(bàba), 爷爷(yéye), 奶奶(nǎinai)",
                        "rule_ru": "В китайском языке также есть пятый тон — нейтральный тон (轻声).\nОн короткий и легкий, без тона.\nЧасто это проявляется в терминах родства.\nПример: 妈妈(мама), 爸爸(баба), 爷爷(йе), 奶奶(найнай)"
                },
                "examples": [
                        {
                                "zh": "妈妈",
                                "pinyin": "māma",
                                "meaning": {
                                        "uz": "ona",
                                        "tj": "модар",
                                        "ru": "мать"
                                }
                        },
                        {
                                "zh": "爸爸",
                                "pinyin": "bàba",
                                "meaning": {
                                        "uz": "ota",
                                        "tj": "падар",
                                        "ru": "отец"
                                }
                        },
                        {
                                "zh": "爷爷",
                                "pinyin": "yéye",
                                "meaning": {
                                        "uz": "ota tomondan bobosi",
                                        "tj": "бобои падар",
                                        "ru": "дед по отцовской линии"
                                }
                        },
                        {
                                "zh": "奶奶",
                                "pinyin": "nǎinai",
                                "meaning": {
                                        "uz": "otaning buvisi",
                                        "tj": "бибии падар",
                                        "ru": "бабушка по отцовской линии"
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
                "no": 1,
                "type": "translate_to_chinese",
                "instruction": {
                        "uz": "Xitoy tilida yozing:",
                        "tj": "Ба забони чинӣ нависед:",
                        "ru": "Напишите по-китайски:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "Rahmat!",
                                        "tj": "Сипос!",
                                        "ru": "Спасибо!"
                                },
                                "answer": "谢谢！",
                                "pinyin": "Xièxie!"
                        },
                        {
                                "prompt": {
                                        "uz": "Rahmat (sizga)!",
                                        "tj": "Ташаккур (ба шумо)!",
                                        "ru": "Спасибо (вам)!"
                                },
                                "answer": "谢谢你！",
                                "pinyin": "Xièxie nǐ!"
                        },
                        {
                                "prompt": {
                                        "uz": "Salomat bo'ling!",
                                        "tj": "Хушомадед!",
                                        "ru": "Пожалуйста!"
                                },
                                "answer": "不客气！",
                                "pinyin": "Bú kèqi!"
                        },
                        {
                                "prompt": {
                                        "uz": "Xayr. Salomat bo'ling!",
                                        "tj": "Хайр?",
                                        "ru": "До свидания!"
                                },
                                "answer": "再见！",
                                "pinyin": "Zàijiàn!"
                        }
                ]
        },
        {
                "no": 2,
                "type": "fill_blank",
                "instruction": {
                        "uz": "Bo'sh joyni to'ldiring:",
                        "tj": "Холиро пур кунед:",
                        "ru": "Заполните пробел:"
                },
                "items": [
                        {
                                "prompt": "A: 谢谢你！  B: ___！",
                                "answer": "不客气",
                                "pinyin": "bú kèqi"
                        },
                        {
                                "prompt": "A: ___！     B: 再见！",
                                "answer": "再见",
                                "pinyin": "zàijiàn"
                        },
                        {
                                "prompt": "A: 谢谢！    B: ___！",
                                "answer": "不谢",
                                "pinyin": "bú xiè"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "谢谢！",
                        "谢谢你！",
                        "不客气！",
                        "再见！"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "不客气",
                        "再见",
                        "不谢"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Quyidagi so'zlardan foydalangan holda 2 ta to'liq dialog yozing:",
                        "tj": "Бо истифода аз калимаҳои зерин 2 муколамаи мукаммал нависед:",
                        "ru": "Напишите 2 полных диалога, используя следующие слова:"
                },
                "words": [
                        "谢谢",
                        "不客气",
                        "再见",
                        "你好"
                ],
                "example": "A: 你好！... A: 谢谢！B: 不客气！再见！B: 再见！"
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "(bù yoki bú) ning toʻgʻri talaffuzini yozing:",
                        "tj": "Талаффузи дурусти 不 (bù ё bú) -ро нависед:",
                        "ru": "Напишите правильное произношение 不 (bù или bú):"
                },
                "items": [
                        {
                                "prompt": "不好",
                                "answer": "bù hǎo"
                        },
                        {
                                "prompt": "不谢",
                                "answer": "bú xiè"
                        },
                        {
                                "prompt": "不客气",
                                "answer": "bú kèqi"
                        }
                ]
        }
], ensure_ascii=False),

    "is_active": True,
}


async def seed():
    async with SessionLocal() as session:
        existing = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])
        )
        if existing.scalar_one_or_none():
            print(f"Lesson {LESSON['lesson_code']} already exists, skipping.")
            return

        lesson = CourseLesson(**LESSON)
        session.add(lesson)
        await session.commit()
        print(f"\u2705 Lesson {LESSON['lesson_code']} \u2014 {LESSON['title']} created.")


if __name__ == "__main__":
    asyncio.run(seed())
