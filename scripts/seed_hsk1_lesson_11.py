import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 11,
    "lesson_code": "HSK1-L11",
    "title": "现在几点",
    "goal": json.dumps({
        "uz": "Vaqt, zamon qo‘shimchalari va sn so‘zini aytish va so‘rash",
        "tj": "Гуфтан ва пурсидани вақт, сифатҳои замон ва калимаи 前",
        "ru": "Рассказывать и спрашивать время, наречия времени и слово 前."
}, ensure_ascii=False),
    "intro_text": json.dumps({
        "uz": "O'n birinchi darsda siz vaqtni aytishni, vaqt qo'shimchalarini qo'llashni va vaqtni ján so'zi bilan ifodalashni o'rganasiz. 11 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси ёздаҳум шумо мефаҳмед, ки чӣ гуна вақтро гуфтан, истифода бурдани сифатҳои вақт ва ифодаи вақтро бо калимаи 前. 11 калимаи нав, 3 муколама.",
        "ru": "На одиннадцатом уроке вы научитесь определять время, использовать наречия времени и выражать время с помощью слова前. 11 новых слов, 3 диалога."
}, ensure_ascii=False),

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "现在",
                "pinyin": "xiànzài",
                "pos": "n.",
                "meaning": {
                        "uz": "hozir, hozir",
                        "tj": "ҳозир, дар айни замон",
                        "ru": "сейчас, в данный момент"
                }
        },
        {
                "no": 2,
                "zh": "点",
                "pinyin": "diǎn",
                "pos": "m.",
                "meaning": {
                        "uz": "soat (soat uchun so'zni o'lchang)",
                        "tj": "соат (калимаи соатҳоро чен кунед)",
                        "ru": "часы (мерное слово для часов)"
                }
        },
        {
                "no": 3,
                "zh": "分",
                "pinyin": "fēn",
                "pos": "m.",
                "meaning": {
                        "uz": "daqiqa",
                        "tj": "дақиқа",
                        "ru": "минута"
                }
        },
        {
                "no": 4,
                "zh": "中午",
                "pinyin": "zhōngwǔ",
                "pos": "n.",
                "meaning": {
                        "uz": "peshin, peshin",
                        "tj": "нисфирӯзӣ, нисфирӯзӣ",
                        "ru": "полдень, полдень"
                }
        },
        {
                "no": 5,
                "zh": "吃饭",
                "pinyin": "chī fàn",
                "pos": "v.",
                "meaning": {
                        "uz": "ovqatlanmoq, ovqatlanmoq",
                        "tj": "хўрдан, хўрдан",
                        "ru": "поесть, перекусить"
                }
        },
        {
                "no": 6,
                "zh": "时候",
                "pinyin": "shíhou",
                "pos": "n.",
                "meaning": {
                        "uz": "vaqt, moment",
                        "tj": "вақт, лаҳза",
                        "ru": "время, момент"
                }
        },
        {
                "no": 7,
                "zh": "回",
                "pinyin": "huí",
                "pos": "v.",
                "meaning": {
                        "uz": "qaytmoq, qaytmoq",
                        "tj": "баргаштан, баргаштан",
                        "ru": "вернуться, вернуться"
                }
        },
        {
                "no": 8,
                "zh": "我们",
                "pinyin": "wǒmen",
                "pos": "pron.",
                "meaning": {
                        "uz": "biz, biz",
                        "tj": "мо, мо",
                        "ru": "мы, нас"
                }
        },
        {
                "no": 9,
                "zh": "电影",
                "pinyin": "diànyǐng",
                "pos": "n.",
                "meaning": {
                        "uz": "kino, kino",
                        "tj": "кино, фильм",
                        "ru": "фильм, фильм"
                }
        },
        {
                "no": 10,
                "zh": "住",
                "pinyin": "zhù",
                "pos": "v.",
                "meaning": {
                        "uz": "yashash, qolish",
                        "tj": "зиндагӣ кардан, мондан",
                        "ru": "жить, оставаться"
                }
        },
        {
                "no": 11,
                "zh": "前",
                "pinyin": "qián",
                "pos": "n.",
                "meaning": {
                        "uz": "oldin, oldin",
                        "tj": "пеш, пеш",
                        "ru": "прежде, прежде чем"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Kutubxonada — soat so'rash",
                        "tj": "Дар китобхона — соат талаб кунед",
                        "ru": "В библиотеке - попросить часы"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "现在几点？",
                                "pinyin": "Xiànzài jǐ diǎn?",
                                "translation": {
                                        "uz": "Hozir soat necha?",
                                        "tj": "Ҳоло соат чанд аст?",
                                        "ru": "Сколько сейчас времени?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "现在十点十分。",
                                "pinyin": "Xiànzài shí diǎn shí fēn.",
                                "translation": {
                                        "uz": "Soat o'ndan o'n o'tdi.",
                                        "tj": "Соат аз дах гузаштааст.",
                                        "ru": "Сейчас десять минут одиннадцатого."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "中午几点吃饭？",
                                "pinyin": "Zhōngwǔ jǐ diǎn chī fàn?",
                                "translation": {
                                        "uz": "Siz soat nechada tushlik qilasiz?",
                                        "tj": "Шумо соати чанд хӯроки нисфирӯзӣ мехӯред?",
                                        "ru": "В какое время ты обедаешь?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "十二点吃饭。",
                                "pinyin": "Shí'èr diǎn chī fàn.",
                                "translation": {
                                        "uz": "Biz soat o'n ikkida ovqatlanamiz.",
                                        "tj": "Мо соати дувоздаҳ хӯрок мехӯрем.",
                                        "ru": "Мы едим в двенадцать часов."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Uyda — otani kutish",
                        "tj": "Дар хона - интизори падар",
                        "ru": "Дома - жду отца"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "爸爸什么时候回家？",
                                "pinyin": "Bàba shénme shíhou huí jiā?",
                                "translation": {
                                        "uz": "Dadam qachon uyga keladi?",
                                        "tj": "Падар кай ба хона меояд?",
                                        "ru": "Когда папа возвращается домой?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "下午五点。",
                                "pinyin": "Xiàwǔ wǔ diǎn.",
                                "translation": {
                                        "uz": "Peshindan keyin soat beshda.",
                                        "tj": "Дар соати панҷи рӯз.",
                                        "ru": "В пять часов дня."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "我们什么时候去看电影？",
                                "pinyin": "Wǒmen shénme shíhou qù kàn diànyǐng?",
                                "translation": {
                                        "uz": "Qachon kino ko'ramiz?",
                                        "tj": "Мо кай филм тамошо мекунем?",
                                        "ru": "Когда мы собираемся посмотреть фильм?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "六点三十分。",
                                "pinyin": "Liù diǎn sānshí fēn.",
                                "translation": {
                                        "uz": "Olti o'ttizda.",
                                        "tj": "Дар шаш сӣ.",
                                        "ru": "В шесть тридцать."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Uyda — Pekin safari rejasi",
                        "tj": "Дар хона - нақшаи сафари Пекин",
                        "ru": "Дома - план путешествия по Пекину"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "我星期一去北京。",
                                "pinyin": "Wǒ xīngqī yī qù Běijīng.",
                                "translation": {
                                        "uz": "Dushanba kuni Pekinga boraman.",
                                        "tj": "Ман рӯзи душанбе ба Пекин меравам.",
                                        "ru": "Я собираюсь в Пекин в понедельник."
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "你想在北京住几天？",
                                "pinyin": "Nǐ xiǎng zài Běijīng zhù jǐ tiān?",
                                "translation": {
                                        "uz": "Pekinda necha kun qolishni rejalashtiryapsiz?",
                                        "tj": "Шумо чанд рӯз дар Пекин мондан мехоҳед?",
                                        "ru": "Сколько дней вы планируете провести в Пекине?"
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "住三天。",
                                "pinyin": "Zhù sān tiān.",
                                "translation": {
                                        "uz": "Uch kun.",
                                        "tj": "Се рӯз.",
                                        "ru": "Три дня."
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "星期五前能回家吗？",
                                "pinyin": "Xīngqī wǔ qián néng huí jiā ma?",
                                "translation": {
                                        "uz": "Juma kunigacha uyga qaytish mumkinmi?",
                                        "tj": "Оё шумо метавонед пеш аз ҷумъа ба хона баргардед?",
                                        "ru": "Сможешь ли ты вернуться домой до пятницы?"
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "能。",
                                "pinyin": "Néng.",
                                "translation": {
                                        "uz": "Ha, men qila olaman.",
                                        "tj": "Бале, ман метавонам.",
                                        "ru": "Да, я могу."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "时间的表达 — Vaqtni ifodalash",
                "explanation": {
                        "rule_uz": "Soat: i(diǎn)\nDaqiqa: fēn (fēn)\nTuzilishi: Njín yoki NíMín\n\nSoat 9:00 →\n10:10 → chángjčán\n5:30 → shīngīdīnčán\n2:05 → chíngjíníngín\n\nKunning qismlari:\nshàngwǔ shàngwǔ - ertalab (AM)\nzhōngwǔ - kunduzi\nxiàwǔ xiàwǔ - tushdan keyin (PM)\n\n2:00 → líng diǎn (liǎng diǎn), mín emas!",
                        "rule_tj": "Соат: 点(diǎn)\nдақиқа: 分(fēn)\nСохтор: N点 ё N点M分\n\n9:00 → 九点\n10:10 → 十点十分\n5:30 → 五点三十分\n2:05 → 两点零五分\n\nҚисмҳои рӯз:\n上午 shàngwǔ — саҳар (саҳ)\n中午 zhōngwǔ — нисфирӯзӣ\n下午 xiàwǔ — нисфирӯзӣ (PM)\n\n2:00 → 两点 (liǎng diǎn), на 二点!",
                        "rule_ru": "Час: 点(диан)\nМинута: 分(фэн)\nСтруктура: N点 или N点M分.\n\n9:00 → 九点\n10:10 → 十点十分\n5:30 → 五点三十分\n2:05 → 两点零五分\n\nЧасти дня:\n上午 shàngwǔ — утро (AM)\n中午 чжунво — полдень\n下午 xiàwǔ — полдень (после полудня)\n\n2:00 → 两点 (люнг динь), а не 二点!"
                },
                "examples": [
                        {
                                "zh": "现在九点。",
                                "pinyin": "Xiànzài jiǔ diǎn.",
                                "meaning": {
                                        "uz": "Hozir soat to'qqiz.",
                                        "tj": "Холо соати нух аст.",
                                        "ru": "Сейчас девять часов."
                                }
                        },
                        {
                                "zh": "下午三点十分。",
                                "pinyin": "Xiàwǔ sān diǎn shí fēn.",
                                "meaning": {
                                        "uz": "Tushdan keyin soat uchdan o‘n o‘tgan.",
                                        "tj": "Соати 10:3.",
                                        "ru": "Десять минут четвертого дня."
                                }
                        },
                        {
                                "zh": "上午两点半。",
                                "pinyin": "Shàngwǔ liǎng diǎn bàn.",
                                "meaning": {
                                        "uz": "Ertalab ikki o'ttiz.",
                                        "tj": "Соати ду сӣ саҳар.",
                                        "ru": "Два тридцать ночи."
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "时间词做状语 — Vaqt ravishi",
                "explanation": {
                        "rule_uz": "Vaqt so‘zi gapda ergash gap vazifasini bajarishi mumkin.\nOdatda mavzudan keyin yoki mavzudan oldin keladi.\n\n1-tarkibi: Mavzu + Vaqt + Fe'l\nchàngāngīngīng — Onam soat oltida ovqat pishiradi.\n\n2-tuzilma: Vaqt + Mavzu + Fe'l\nchàngāngāngīngīngīngīngīngīngīng - Biz tushlik paytida, o'n ikkida tushlik qilamiz.\n\nSavol: mīngīngīng — qachon?",
                        "rule_tj": "Калимаи вақт метавонад дар ҷумла ҳамчун таблиғ хидмат кунад.\nОн одатан пас аз мавзӯъ ё пеш аз мавзӯъ меояд.\n\nСохтори 1: Мавзӯъ + Вақт + Феъл\n妈妈六点做饭。— Модар соати шаш хӯрок мепазад.\n\nСохтори 2: Вақт + Мавзӯъ + Феъл\n中午十二点我们吃饭。— Мо нисфирӯзӣ соати дувоздаҳ хӯроки нисфирӯзӣ мехӯрем.\n\nСавол: 什么时候 — кай?",
                        "rule_ru": "Слово времени может служить наречием в предложении.\nОбычно оно стоит после подлежащего или перед подлежащим.\n\nСтруктура 1: Тема + Время + Глагол\n妈妈六点做饭。 — Мама готовит в шесть часов.\n\nСтруктура 2: Время + Подлежащее + Глагол.\n中午十二点我们吃饭。 — Мы обедаем в полдень, в двенадцать.\n\nВопрос: 什么时候 — когда?"
                },
                "examples": [
                        {
                                "zh": "他们六点吃饭。",
                                "pinyin": "Tāmen liù diǎn chī fàn.",
                                "meaning": {
                                        "uz": "Ular soat oltida ovqatlanadilar.",
                                        "tj": "Онҳо соати шаш хӯрок мехӯранд.",
                                        "ru": "Они едят в шесть часов."
                                }
                        },
                        {
                                "zh": "我星期一去北京。",
                                "pinyin": "Wǒ xīngqī yī qù Běijīng.",
                                "meaning": {
                                        "uz": "Dushanba kuni Pekinga boraman.",
                                        "tj": "Ман рӯзи душанбе ба Пекин меравам.",
                                        "ru": "Я собираюсь в Пекин в понедельник."
                                }
                        },
                        {
                                "zh": "你什么时候回家？",
                                "pinyin": "Nǐ shénme shíhou huí jiā?",
                                "meaning": {
                                        "uz": "Uyga qachon ketasiz?",
                                        "tj": "Шумо кай ба хона меравед?",
                                        "ru": "Когда ты собираешься домой?"
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "名词 前 — 前 vaqt belgisi",
                "explanation": {
                        "rule_uz": "qán(qián) — ma’lum bir hodisadan oldingi vaqtni bildiradi.\n\nshīngīn - uch kun oldin\nshīngīngīngī - bir hafta oldin\nlínín - soat to'rtdan oldin\nlíngìnìnči - juma kunidan oldin\n\nMisol:\nlíngàngìnìnė？— Jumagacha uyga qaytishingiz mumkinmi?\nchàngāngāngēng — Soat sakkizdan oldin maktabga boring.",
                        "rule_tj": "前(qián) — як лаҳзаи пеш аз ҳодисаи муайянро нишон медиҳад.\n\n三天前 — се рӯз пеш\n一个星期前 — як ҳафта пеш\n四点前 — то соати чор\n星期五前 — пеш аз ҷумъа\n\nМисол:\n星期五前能回家吗？— Оё шумо пеш аз ҷумъа ба хона баргашта метавонед?\n八点前去学校。— То соати ҳашт ба мактаб равед.",
                        "rule_ru": "前(цянь) — указывает момент времени перед определенным событием.\n\n三天前 — три дня назад\n一个星期前 — неделю назад\n四点前 — до четырех часов\n星期五前 — до пятницы\n\nПример:\n星期五前能回家吗？ — Ты сможешь вернуться домой до пятницы?\n八点前去学校。 — Идти в школу до восьми часов."
                },
                "examples": [
                        {
                                "zh": "星期五前能回家吗？",
                                "pinyin": "Xīngqī wǔ qián néng huí jiā ma?",
                                "meaning": {
                                        "uz": "Juma kunigacha uyga qaytish mumkinmi?",
                                        "tj": "Оё шумо метавонед пеш аз ҷумъа ба хона баргардед?",
                                        "ru": "Сможешь ли ты вернуться домой до пятницы?"
                                }
                        },
                        {
                                "zh": "三天前我在北京。",
                                "pinyin": "Sān tiān qián wǒ zài Běijīng.",
                                "meaning": {
                                        "uz": "Uch kun oldin men Pekinda edim.",
                                        "tj": "Се рӯз пеш ман дар Пекин будам.",
                                        "ru": "Три дня назад я был в Пекине."
                                }
                        },
                        {
                                "zh": "八点前来。",
                                "pinyin": "Bā diǎn qián lái.",
                                "meaning": {
                                        "uz": "Soat sakkizdan oldin keling.",
                                        "tj": "То соати ҳашт биёед.",
                                        "ru": "Приходите до восьми часов."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
                "no": 1,
                "type": "time_writing",
                "instruction": {
                        "uz": "Vaqtni xitoy tilida yozing:",
                        "tj": "Вақтро бо забони чинӣ нависед:",
                        "ru": "Напишите время по-китайски:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "9:00",
                                        "tj": "9:00",
                                        "ru": "9:00"
                                },
                                "answer": "九点",
                                "pinyin": "jiǔ diǎn"
                        },
                        {
                                "prompt": {
                                        "uz": "2:00",
                                        "tj": "2:00",
                                        "ru": "2:00"
                                },
                                "answer": "两点",
                                "pinyin": "liǎng diǎn"
                        },
                        {
                                "prompt": {
                                        "uz": "10:10",
                                        "tj": "10:10",
                                        "ru": "10:10"
                                },
                                "answer": "十点十分",
                                "pinyin": "shí diǎn shí fēn"
                        },
                        {
                                "prompt": {
                                        "uz": "6:30",
                                        "tj": "6:30",
                                        "ru": "6:30"
                                },
                                "answer": "六点三十分",
                                "pinyin": "liù diǎn sānshí fēn"
                        },
                        {
                                "prompt": {
                                        "uz": "PM 3:15",
                                        "tj": "СОАТИ 15:15",
                                        "ru": "ПМ 15:15"
                                },
                                "answer": "下午三点十五分",
                                "pinyin": "xiàwǔ sān diǎn shíwǔ fēn"
                        }
                ]
        },
        {
                "no": 2,
                "type": "translate_to_chinese",
                "instruction": {
                        "uz": "Xitoy tilida yozing:",
                        "tj": "Ба забони чинӣ нависед:",
                        "ru": "Напишите по-китайски:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "Hozir soat necha?",
                                        "tj": "Ҳоло соат чанд аст?",
                                        "ru": "Сколько сейчас времени?"
                                },
                                "answer": "现在几点？",
                                "pinyin": "Xiànzài jǐ diǎn?"
                        },
                        {
                                "prompt": {
                                        "uz": "Qachon kino ko'ramiz?",
                                        "tj": "Мо кай филм тамошо мекунем?",
                                        "ru": "Когда мы собираемся посмотреть фильм?"
                                },
                                "answer": "我们什么时候去看电影？",
                                "pinyin": "Wǒmen shénme shíhou qù kàn diànyǐng?"
                        },
                        {
                                "prompt": {
                                        "uz": "Juma kunigacha uyga qaytish mumkinmi?",
                                        "tj": "Оё шумо метавонед пеш аз ҷумъа ба хона баргардед?",
                                        "ru": "Сможешь ли ты вернуться домой до пятницы?"
                                },
                                "answer": "星期五前能回家吗？",
                                "pinyin": "Xīngqī wǔ qián néng huí jiā ma?"
                        },
                        {
                                "prompt": {
                                        "uz": "Pekinda uch kun qolaman.",
                                        "tj": "Ман се рӯз дар Пекин мемонам.",
                                        "ru": "Я пробуду в Пекине три дня."
                                },
                                "answer": "我在北京住三天。",
                                "pinyin": "Wǒ zài Běijīng zhù sān tiān."
                        }
                ]
        },
        {
                "no": 3,
                "type": "fill_blank",
                "instruction": {
                        "uz": "Bo'sh joyni to'ldiring:",
                        "tj": "Холиро пур кунед:",
                        "ru": "Заполните пробел:"
                },
                "items": [
                        {
                                "prompt": "现在___点___分？",
                                "answer": "几/几",
                                "pinyin": "jǐ/jǐ"
                        },
                        {
                                "prompt": "爸爸什么___回家？",
                                "answer": "时候",
                                "pinyin": "shíhou"
                        },
                        {
                                "prompt": "星期五___能回家吗？",
                                "answer": "前",
                                "pinyin": "qián"
                        },
                        {
                                "prompt": "我___一去北京。",
                                "answer": "星期",
                                "pinyin": "xīngqī"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "九点",
                        "两点",
                        "十点十分",
                        "六点三十分",
                        "下午三点十五分"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "现在几点？",
                        "我们什么时候去看电影？",
                        "星期五前能回家吗？",
                        "我在北京住三天。"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "几/几",
                        "时候",
                        "前",
                        "星期"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Kundalik jadvalingizni yozing (vaqt + faoliyat):",
                        "tj": "Ҷадвали ҳаррӯзаи худро нависед (вақт + фаъолият):",
                        "ru": "Напишите свой распорядок дня (время + активность):"
                },
                "template": "上午___点我___。中午___点我___。下午___点我___。",
                "words": [
                        "点",
                        "分",
                        "吃饭",
                        "去",
                        "回家",
                        "看书",
                        "工作"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Savollarga javob bering:",
                        "tj": "Ба саволхо ҷавоб додан:",
                        "ru": "Ответь на вопросы:"
                },
                "items": [
                        {
                                "prompt": "现在几点？",
                                "hint": "Say the current time"
                        },
                        {
                                "prompt": "你几点吃饭？",
                                "hint": "What time do you eat?"
                        },
                        {
                                "prompt": "你什么时候回家？",
                                "hint": "When are you going home?"
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
