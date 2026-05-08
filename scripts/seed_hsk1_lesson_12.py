import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 12,
    "lesson_code": "HSK1-L12",
    "title": "明天天气怎么样",
    "goal": json.dumps({
        "uz": "Ob-havo haqida gapirganda, so'roq so'zi chíníní va h...",
        "tj": "Сухан дар бораи обу ҳаво, калимаи саволии 怎么样 ва сохтмони 太...了",
        "ru": "Говоря о погоде, вопросительном слове 怎么样 и конструкции 太...了."
}, ensure_ascii=False),
    "intro_text": json.dumps({
        "uz": "O'n ikkinchi darsda siz ob-havo haqida qanday gapirishni o'rganasiz, shàngín bilan shtatlar haqida so'rashni va hài...yín konstruktsiyasidan foydalanishni o'rganasiz. 13 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси дувоздаҳ шумо мефаҳмед, ки чӣ тавр дар бораи обу ҳаво сӯҳбат кунед, дар бораи иёлатҳо бо 怎么样 пурсед ва сохти 太...了-ро истифода баред. 13 калимаи нав, 3 муколама.",
        "ru": "На двенадцатом уроке вы научитесь говорить о погоде, спрашивать о штатах с помощью 怎么样 и использовать конструкцию 太...了. 13 новых слов, 3 диалога."
}, ensure_ascii=False),

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "天气",
                "pinyin": "tiānqì",
                "pos": "n.",
                "meaning": {
                        "uz": "ob-havo",
                        "tj": "обу ҳаво",
                        "ru": "погода"
                }
        },
        {
                "no": 2,
                "zh": "怎么样",
                "pinyin": "zěnmeyàng",
                "pos": "pron.",
                "meaning": {
                        "uz": "qanday, qanday",
                        "tj": "чи тавр, чй гуна аст",
                        "ru": "как, на что это похоже"
                }
        },
        {
                "no": 3,
                "zh": "太",
                "pinyin": "tài",
                "pos": "adv.",
                "meaning": {
                        "uz": "ham, nihoyatda",
                        "tj": "низ бениҳоят",
                        "ru": "тоже, чрезвычайно"
                }
        },
        {
                "no": 4,
                "zh": "热",
                "pinyin": "rè",
                "pos": "adj.",
                "meaning": {
                        "uz": "issiq",
                        "tj": "гарм",
                        "ru": "горячий"
                }
        },
        {
                "no": 5,
                "zh": "冷",
                "pinyin": "lěng",
                "pos": "adj.",
                "meaning": {
                        "uz": "sovuq",
                        "tj": "сард",
                        "ru": "холодный"
                }
        },
        {
                "no": 6,
                "zh": "下雨",
                "pinyin": "xià yǔ",
                "pos": "v.",
                "meaning": {
                        "uz": "yomg'ir",
                        "tj": "борон кардан",
                        "ru": "дождь"
                }
        },
        {
                "no": 7,
                "zh": "小姐",
                "pinyin": "xiǎojiě",
                "pos": "n.",
                "meaning": {
                        "uz": "Xonim, yosh xonim",
                        "tj": "Хонум, хонуми ҷавон",
                        "ru": "Мисс, юная леди"
                }
        },
        {
                "no": 8,
                "zh": "来",
                "pinyin": "lái",
                "pos": "v.",
                "meaning": {
                        "uz": "kelish",
                        "tj": "омадан",
                        "ru": "прийти"
                }
        },
        {
                "no": 9,
                "zh": "身体",
                "pinyin": "shēntǐ",
                "pos": "n.",
                "meaning": {
                        "uz": "tana, sog'liq",
                        "tj": "ҷисм, саломатӣ",
                        "ru": "тело, здоровье"
                }
        },
        {
                "no": 10,
                "zh": "爱",
                "pinyin": "ài",
                "pos": "v.",
                "meaning": {
                        "uz": "sevmoq, yoqtirmoq",
                        "tj": "дӯст доштан, дӯст доштан",
                        "ru": "любить, нравиться"
                }
        },
        {
                "no": 11,
                "zh": "些",
                "pinyin": "xiē",
                "pos": "m.",
                "meaning": {
                        "uz": "ba'zi, bir nechta",
                        "tj": "баъзе, чанде",
                        "ru": "некоторые, несколько"
                }
        },
        {
                "no": 12,
                "zh": "水果",
                "pinyin": "shuǐguǒ",
                "pos": "n.",
                "meaning": {
                        "uz": "meva",
                        "tj": "мева",
                        "ru": "фрукты"
                }
        },
        {
                "no": 13,
                "zh": "水",
                "pinyin": "shuǐ",
                "pos": "n.",
                "meaning": {
                        "uz": "suv",
                        "tj": "об",
                        "ru": "вода"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Yo'lda — ob-havo muhokamasi",
                        "tj": "Дар рох — мухокимаи обу хаво",
                        "ru": "В дороге - обсуждение погоды"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "昨天北京的天气怎么样？",
                                "pinyin": "Zuótiān Běijīng de tiānqì zěnmeyàng?",
                                "translation": {
                                        "uz": "Pekinda kecha ob-havo qanday edi?",
                                        "tj": "Дирӯз дар Пекин ҳаво чӣ гуна буд?",
                                        "ru": "Какая погода была вчера в Пекине?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "太热了。",
                                "pinyin": "Tài rè le.",
                                "translation": {
                                        "uz": "Bu juda issiq edi.",
                                        "tj": "Хеле гарм буд.",
                                        "ru": "Было очень жарко."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "明天呢？明天天气怎么样？",
                                "pinyin": "Míngtiān ne? Míngtiān tiānqì zěnmeyàng?",
                                "translation": {
                                        "uz": "Ertaga-chi? Ob-havo qanday bo'ladi?",
                                        "tj": "Дар бораи пагоҳ чӣ гуфтан мумкин аст? Ҳаво чӣ гуна хоҳад буд?",
                                        "ru": "А что насчет завтра? Какая будет погода?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "明天天气很好，不冷不热。",
                                "pinyin": "Míngtiān tiānqì hěn hǎo, bù lěng bú rè.",
                                "translation": {
                                        "uz": "Ertaga havo yaxshi bo'ladi, na sovuq, na issiq.",
                                        "tj": "Пагох хаво хуб мешавад, на хунуку на гарм.",
                                        "ru": "Завтра погода будет хорошая: ни холодно, ни жарко."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Sport zalda — yomg'ir va sovuq",
                        "tj": "Дар толори варзишӣ борон меборад ва сард аст",
                        "ru": "В спортзале дождь и холодно"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "今天会下雨吗？",
                                "pinyin": "Jīntiān huì xià yǔ ma?",
                                "translation": {
                                        "uz": "Bugun yomg'ir yog'adimi?",
                                        "tj": "Оё имрӯз борон меборад?",
                                        "ru": "Будет ли сегодня дождь?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "今天不会下雨。",
                                "pinyin": "Jīntiān bú huì xià yǔ.",
                                "translation": {
                                        "uz": "Bugun yomg'ir yog'maydi.",
                                        "tj": "Имрӯз борон намеборад.",
                                        "ru": "Сегодня дождя не будет."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "王小姐今天会来吗？",
                                "pinyin": "Wáng xiǎojiě jīntiān huì lái ma?",
                                "translation": {
                                        "uz": "Miss Vang bugun keladimi?",
                                        "tj": "Оё мисс Ванг имрӯз меояд?",
                                        "ru": "Мисс Ван придет сегодня?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "不会来，天气太冷了。",
                                "pinyin": "Bú huì lái, tiānqì tài lěng le.",
                                "translation": {
                                        "uz": "U kelmaydi, havo juda sovuq.",
                                        "tj": "Вай намеояд, ҳаво хеле сард аст.",
                                        "ru": "Она не придет, погода слишком холодная."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Kasalxonada — sog'liq haqida",
                        "tj": "Дар беморхона — дар бораи саломатй",
                        "ru": "В больнице – о здоровье"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你身体怎么样？",
                                "pinyin": "Nǐ shēntǐ zěnmeyàng?",
                                "translation": {
                                        "uz": "Salomatligingiz qanday?",
                                        "tj": "Саломатии шумо чӣ гуна аст?",
                                        "ru": "Как твое здоровье?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我身体不太好。天气太热了，不爱吃饭。",
                                "pinyin": "Wǒ shēntǐ bú tài hǎo. Tiānqì tài rè le, bú ài chī fàn.",
                                "translation": {
                                        "uz": "Mening sog'ligim unchalik yaxshi emas. Havo juda issiq va ovqat iste'mol qilmoqchi emasman.",
                                        "tj": "Саломатиам чандон хуб нест. Ҳаво хеле гарм аст ва ман намехӯрам.",
                                        "ru": "У меня не очень хорошее здоровье. Погода слишком жаркая, и мне не хочется есть."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你多吃些水果，多喝水。",
                                "pinyin": "Nǐ duō chī xiē shuǐguǒ, duō hē shuǐ.",
                                "translation": {
                                        "uz": "Ko'proq meva iste'mol qiling va ko'proq suv iching.",
                                        "tj": "Бештар мева бихӯред ва бештар об нӯшед.",
                                        "ru": "Ешьте больше фруктов и пейте больше воды."
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "谢谢你，医生。",
                                "pinyin": "Xièxie nǐ, yīshēng.",
                                "translation": {
                                        "uz": "Rahmat, doktor.",
                                        "tj": "Ташаккур, духтур.",
                                        "ru": "Спасибо, доктор."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "怎么样 — Holat so'roq olmoshi",
                "explanation": {
                        "rule_uz": "zěnmeyàng (zěnmeyàng) — holat, sifat yoki fikr haqida so‘rash uchun ishlatiladi.\nTuzilishi: Mavzu + língín?\n\nlìnìnìnín？— Ob-havo qanday?\nshīngīngīnīnīn？— Sog'ligingiz qanday?\nshīngīngīngīngīngīn？— Xitoychangiz qanday?",
                        "rule_tj": "怎么样(zěnmeyàng) — барои пурсидан дар бораи ҳолат, сифат ё андеша.\nСохтор: Мавзӯъ + 怎么样?\n\n天气怎么样？— Ҳаво чӣ гуна аст?\n你身体怎么样？— Саломатии шумо чӣ гуна аст?\n你的汉语怎么样？— Чинии шумо чӣ гуна аст?",
                        "rule_ru": "怎么样(zěnmeyàng) — используется, чтобы спросить о состоянии, качестве или мнении.\nСтруктура: Тема + 怎么样?\n\n天气怎么样？ — Какая погода?\n你身体怎么样？ — Как твое здоровье?\n你的汉语怎么样？ — Как твой китайский?"
                },
                "examples": [
                        {
                                "zh": "明天天气怎么样？",
                                "pinyin": "Míngtiān tiānqì zěnmeyàng?",
                                "meaning": {
                                        "uz": "Ertaga ob-havo qanday bo'ladi?",
                                        "tj": "Пагоҳ ҳаво чӣ гуна хоҳад буд?",
                                        "ru": "Какая погода будет завтра?"
                                }
                        },
                        {
                                "zh": "你身体怎么样？",
                                "pinyin": "Nǐ shēntǐ zěnmeyàng?",
                                "meaning": {
                                        "uz": "Salomatligingiz qanday?",
                                        "tj": "Саломатии шумо чӣ гуна аст?",
                                        "ru": "Как твое здоровье?"
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "太……了 — Haddan tashqari",
                "explanation": {
                        "rule_uz": "tài (tài) + Sifat + mán - \"juda, nihoyatda\"\nSalbiy: shín + Sifat (yo'q)\n\nchàngāngānīn — Havo juda issiq.\n太冷了！ - Juda sovuq!\nchàngāngīdīnī - Mening sog'ligim unchalik yaxshi emas.",
                        "rule_tj": "太(tài) + Сифат + 了 — 'хеле, бениҳоят'\nМанфӣ: 不太 + Сифат (не 了)\n\n天气太热了。— Ҳаво хеле гарм аст.\n太冷了！ — Хеле сард!\n我身体不太好。— Саломатиам чандон хуб нест.",
                        "rule_ru": "太(tài) + прилагательное + 了 — «слишком, чрезвычайно»\nОтрицательное: 不太 + прилагательное (без 了).\n\n天气太热了。 — Погода очень жаркая.\n太冷了！ — Слишком холодно!\n我身体不太好。 — У меня не очень хорошее здоровье."
                },
                "examples": [
                        {
                                "zh": "太热了！",
                                "pinyin": "Tài rè le!",
                                "meaning": {
                                        "uz": "Juda issiq!",
                                        "tj": "Хеле гарм!",
                                        "ru": "Слишком жарко!"
                                }
                        },
                        {
                                "zh": "天气太冷了。",
                                "pinyin": "Tiānqì tài lěng le.",
                                "meaning": {
                                        "uz": "Havo juda sovuq.",
                                        "tj": "Ҳаво хеле сард аст.",
                                        "ru": "Погода слишком холодная."
                                }
                        },
                        {
                                "zh": "我不太好。",
                                "pinyin": "Wǒ bú tài hǎo.",
                                "meaning": {
                                        "uz": "Men unchalik yaxshi ish qilmayapman.",
                                        "tj": "Ман чандон хуб нестам.",
                                        "ru": "У меня дела идут не очень хорошо."
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "能愿动词 会 (2) — 会 ehtimollik bildiradi",
                "explanation": {
                        "rule_uz": "mán - kelajakda biror narsa sodir bo'lish ehtimolini ko'rsatadi.\n\nchàngāngāngīngīn？— Bugun yomg'ir yog'adimi?\nmìnìnìnì？— U keladimi?\nshín — boʻlmaydi, boʻlmaydi",
                        "rule_tj": "会 - эҳтимолияти рӯй додани чизе дар ояндаро нишон медиҳад.\n\n今天会下雨吗？— Оё имрӯз борон меборад?\n她会来吗？— Вай меояд?\n不会 — намешавад, намешавад",
                        "rule_ru": "会 — указывает на вероятность того, что что-то произойдет в будущем.\n\n今天会下雨吗？ — Сегодня будет дождь?\n她会来吗？ — Она придет?\n不会 — не будет, не произойдет"
                },
                "examples": [
                        {
                                "zh": "今天会下雨吗？",
                                "pinyin": "Jīntiān huì xià yǔ ma?",
                                "meaning": {
                                        "uz": "Bugun yomg'ir yog'adimi?",
                                        "tj": "Оё имрӯз борон меборад?",
                                        "ru": "Будет ли сегодня дождь?"
                                }
                        },
                        {
                                "zh": "明天会冷吗？",
                                "pinyin": "Míngtiān huì lěng ma?",
                                "meaning": {
                                        "uz": "Ertaga sovuq bo'ladimi?",
                                        "tj": "Пагох хаво хунук мешавад?",
                                        "ru": "Завтра будет холодно?"
                                }
                        },
                        {
                                "zh": "她今天不会来。",
                                "pinyin": "Tā jīntiān bú huì lái.",
                                "meaning": {
                                        "uz": "U bugun kelmaydi.",
                                        "tj": "Вай имрӯз намеояд.",
                                        "ru": "Она не придет сегодня."
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
                                        "uz": "Ertaga ob-havo qanday bo'ladi?",
                                        "tj": "Пагоҳ ҳаво чӣ гуна хоҳад буд?",
                                        "ru": "Какая погода будет завтра?"
                                },
                                "answer": "明天天气怎么样？",
                                "pinyin": "Míngtiān tiānqì zěnmeyàng?"
                        },
                        {
                                "prompt": {
                                        "uz": "Havo nihoyatda issiq.",
                                        "tj": "Ҳаво ниҳоят гарм аст.",
                                        "ru": "Погода очень жаркая."
                                },
                                "answer": "天气太热了。",
                                "pinyin": "Tiānqì tài rè le."
                        },
                        {
                                "prompt": {
                                        "uz": "Bugun yomg'ir yog'adimi?",
                                        "tj": "Оё имрӯз борон меборад?",
                                        "ru": "Будет ли сегодня дождь?"
                                },
                                "answer": "今天会下雨吗？",
                                "pinyin": "Jīntiān huì xià yǔ ma?"
                        },
                        {
                                "prompt": {
                                        "uz": "Salomatligingiz qanday?",
                                        "tj": "Саломатии шумо чӣ гуна аст?",
                                        "ru": "Как твое здоровье?"
                                },
                                "answer": "你身体怎么样？",
                                "pinyin": "Nǐ shēntǐ zěnmeyàng?"
                        },
                        {
                                "prompt": {
                                        "uz": "Ko'proq meva iste'mol qiling.",
                                        "tj": "Бештар мева бихӯред.",
                                        "ru": "Ешьте больше фруктов."
                                },
                                "answer": "多吃些水果。",
                                "pinyin": "Duō chī xiē shuǐguǒ."
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
                                "prompt": "天气___热了。",
                                "answer": "太",
                                "pinyin": "tài"
                        },
                        {
                                "prompt": "明天天气___？",
                                "answer": "怎么样",
                                "pinyin": "zěnmeyàng"
                        },
                        {
                                "prompt": "今天会___雨吗？",
                                "answer": "下",
                                "pinyin": "xià"
                        },
                        {
                                "prompt": "我身体不___好。",
                                "answer": "太",
                                "pinyin": "tài"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "明天天气怎么样？",
                        "天气太热了。",
                        "今天会下雨吗？",
                        "你身体怎么样？",
                        "多吃些水果。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "太",
                        "怎么样",
                        "下",
                        "太"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Bugungi ob-havo haqida 3-4 ta gap yozing:",
                        "tj": "Дар бораи обу ҳавои имрӯза 3–4 ҷумла нависед:",
                        "ru": "Напишите 3–4 предложения о сегодняшней погоде:"
                },
                "template": "今天天气___。天气___了。今天会___吗？",
                "words": [
                        "天气",
                        "太",
                        "了",
                        "热",
                        "冷",
                        "下雨",
                        "怎么样"
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
