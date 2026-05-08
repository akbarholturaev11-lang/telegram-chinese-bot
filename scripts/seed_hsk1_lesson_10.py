import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 10,
    "lesson_code": "HSK1-L10",
    "title": "我能坐这儿吗",
    "goal": json.dumps({
        "uz": "Joyni ifodalovchi, mí-jumlalar, modal fe'l va bog'lovchilar",
        "tj": "Ифодаи ҷойгиршавӣ, 有-ҷумла, феъли модалӣ 能 ва пайвандаки 和",
        "ru": "Выражение местоположения, 有-предложения, модальный глагол 能 и союз 和"
}, ensure_ascii=False),
    "intro_text": json.dumps({
        "uz": "O'ninchi darsda siz narsalarning qayerdaligini aytishni, mavjudlikni mài bilan ifodalashni, modal fe'l va bog'lovchini ishlatishni o'rganasiz. 12 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси даҳум шумо гуфтанро меомӯзед, ки чизҳо дар куҷо ҳастанд, мавҷудиятро бо 有 ифода кунед, феъли модалии 能 ва пайвандаки 和-ро истифода баред. 12 калимаи нав, 3 муколама.",
        "ru": "На десятом уроке вы научитесь говорить, где находятся вещи, выражать существование с помощью 有, использовать модальный глагол 能 и союз 和. 12 новых слов, 3 диалога."
}, ensure_ascii=False),

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "桌子",
                "pinyin": "zhuōzi",
                "pos": "n.",
                "meaning": {
                        "uz": "stol, stol",
                        "tj": "миз, миз",
                        "ru": "стол, письменный стол"
                }
        },
        {
                "no": 2,
                "zh": "上",
                "pinyin": "shàng",
                "pos": "n.",
                "meaning": {
                        "uz": "tepasida, tepasida",
                        "tj": "болои, боло",
                        "ru": "поверх, выше"
                }
        },
        {
                "no": 3,
                "zh": "电脑",
                "pinyin": "diànnǎo",
                "pos": "n.",
                "meaning": {
                        "uz": "kompyuter",
                        "tj": "компютер",
                        "ru": "компьютер"
                }
        },
        {
                "no": 4,
                "zh": "和",
                "pinyin": "hé",
                "pos": "conj.",
                "meaning": {
                        "uz": "va, bilan",
                        "tj": "ва, бо",
                        "ru": "и, с"
                }
        },
        {
                "no": 5,
                "zh": "本",
                "pinyin": "běn",
                "pos": "m.",
                "meaning": {
                        "uz": "kitoblar uchun so'zni o'lchash",
                        "tj": "калимаро барои китобҳо чен кунед",
                        "ru": "измерить слово для книг"
                }
        },
        {
                "no": 6,
                "zh": "里",
                "pinyin": "lǐ",
                "pos": "n.",
                "meaning": {
                        "uz": "ichida, ichida",
                        "tj": "дарун, дарун",
                        "ru": "внутри, внутри"
                }
        },
        {
                "no": 7,
                "zh": "前面",
                "pinyin": "qiánmiàn",
                "pos": "n.",
                "meaning": {
                        "uz": "oldida, oldida",
                        "tj": "пеш, дар пеш",
                        "ru": "перед, перед"
                }
        },
        {
                "no": 8,
                "zh": "后面",
                "pinyin": "hòumiàn",
                "pos": "n.",
                "meaning": {
                        "uz": "orqaga, orqaga",
                        "tj": "пушт, пас",
                        "ru": "назад, позади"
                }
        },
        {
                "no": 9,
                "zh": "这儿",
                "pinyin": "zhèr",
                "pos": "pron.",
                "meaning": {
                        "uz": "Bu yerga",
                        "tj": "Ин ҷо",
                        "ru": "здесь"
                }
        },
        {
                "no": 10,
                "zh": "没有",
                "pinyin": "méiyǒu",
                "pos": "adv.",
                "meaning": {
                        "uz": "yo'q, yo'q",
                        "tj": "нест, надорад",
                        "ru": "нет, не имеет"
                }
        },
        {
                "no": 11,
                "zh": "能",
                "pinyin": "néng",
                "pos": "mod.",
                "meaning": {
                        "uz": "mumkin, may (qobiliyat/ruxsat)",
                        "tj": "метавонад, мумкин (қобилият/иҷозат)",
                        "ru": "может, может (возможность/разрешение)"
                }
        },
        {
                "no": 12,
                "zh": "坐",
                "pinyin": "zuò",
                "pos": "v.",
                "meaning": {
                        "uz": "o'tirish",
                        "tj": "нишастан",
                        "ru": "сидеть"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Ofisda — stol ustida nima bor",
                        "tj": "Дар кабинет — он чи дар руи миз аст",
                        "ru": "В офисе – что на столе"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "桌子上有什么？",
                                "pinyin": "Zhuōzi shàng yǒu shénme?",
                                "translation": {
                                        "uz": "Stolda nima bor?",
                                        "tj": "Дар рӯи миз чӣ аст?",
                                        "ru": "Что находится на столе?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "桌子上有一个电脑和一本书。",
                                "pinyin": "Zhuōzi shàng yǒu yī gè diànnǎo hé yī běn shū.",
                                "translation": {
                                        "uz": "Stolda kompyuter va kitob bor.",
                                        "tj": "Дар болои миз компютер ва китоб гузошта шудааст.",
                                        "ru": "На столе компьютер и книга."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "杯子在哪儿？",
                                "pinyin": "Bēizi zài nǎr?",
                                "translation": {
                                        "uz": "Kubok qayerda?",
                                        "tj": "Коса дар куҷост?",
                                        "ru": "Где чашка?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "杯子在桌子里。",
                                "pinyin": "Bēizi zài zhuōzi lǐ.",
                                "translation": {
                                        "uz": "Kubok stol ichida.",
                                        "tj": "Коса дар дохили миз аст.",
                                        "ru": "Чашка находится внутри стола."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Sport zalda — oldida va orqasida kim",
                        "tj": "Дар зал — кй дар пешу акиб",
                        "ru": "В зале – кто впереди и сзади"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "前面那个人叫什么名字？",
                                "pinyin": "Qiánmiàn nàge rén jiào shénme míngzi?",
                                "translation": {
                                        "uz": "Oldindagi odamning ismi nima?",
                                        "tj": "Номи шахсе, ки дар пеш аст?",
                                        "ru": "Как зовут человека впереди?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "她叫王方，在医院工作。",
                                "pinyin": "Tā jiào Wáng Fāng, zài yīyuàn gōngzuò.",
                                "translation": {
                                        "uz": "Uning ismi Vang Fang - u kasalxonada ishlaydi.",
                                        "tj": "Номи вай Ван Фанг аст - вай дар беморхона кор мекунад.",
                                        "ru": "Ее зовут Ван Фан — она работает в больнице."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "后面那个人呢？他叫什么名字？",
                                "pinyin": "Hòumiàn nàge rén ne? Tā jiào shénme míngzi?",
                                "translation": {
                                        "uz": "Va orqadagi odam? Uning ismi nima?",
                                        "tj": "Ва шахсе, ки дар паси он аст? Номи ӯ чист?",
                                        "ru": "А человек сзади? Как его зовут?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "他叫谢朋，在商店工作。",
                                "pinyin": "Tā jiào Xiè Péng, zài shāngdiàn gōngzuò.",
                                "translation": {
                                        "uz": "Uning ismi Xie Peng - do'konda ishlaydi.",
                                        "tj": "Номи ӯ Си Пенг аст - ӯ дар мағоза кор мекунад.",
                                        "ru": "Его зовут Се Пэн — он работает в магазине."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Kutubxonada — o'tirish so'rash",
                        "tj": "Дар китобхона нишинед",
                        "ru": "Попросите посидеть в библиотеке"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "这儿有人吗？",
                                "pinyin": "Zhèr yǒu rén ma?",
                                "translation": {
                                        "uz": "Bu erda kimdir o'tiradimi?",
                                        "tj": "Оё касе дар ин ҷо нишастааст?",
                                        "ru": "Здесь кто-нибудь сидит?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "没有。",
                                "pinyin": "Méiyǒu.",
                                "translation": {
                                        "uz": "Yo'q.",
                                        "tj": "Не.",
                                        "ru": "Нет."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "我能坐这儿吗？",
                                "pinyin": "Wǒ néng zuò zhèr ma?",
                                "translation": {
                                        "uz": "Shu yerda o‘tirsam maylimi?",
                                        "tj": "Метавонам дар ин ҷо нишинам?",
                                        "ru": "Можно мне посидеть здесь?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "请坐。",
                                "pinyin": "Qǐng zuò.",
                                "translation": {
                                        "uz": "Iltimos, davom eting.",
                                        "tj": "Лутфан, пеш равед.",
                                        "ru": "Пожалуйста, продолжайте."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "有字句 — 有 gapi (mavjudlik)",
                "explanation": {
                        "rule_uz": "yǒu (yǒu) - biror narsa/kimdir ma'lum bir joyda mavjudligini bildiradi.\nTuzilishi: Joy + mí + Narsa/Shaxs\n\nMisol:\nchàngāngāngāngāngāngīshīng — Stolda kompyuter bor.\nchàngāngīnīnīnīnīnī— Maktab ichida do‘kon bor.\n\nSalbiy: méiyǒu (méiyǒu)\nlíngīngīngīngīngēng — Kreslo ostida it yo'q.\nlíngíngínė？ — língín— Bu yerda kimdir bormi? — Yoʻq.",
                        "rule_tj": "有(yǒu) — нишон медиҳад, ки чизе/касе дар ҷои муайян вуҷуд дорад.\nСохтор: Ҷой + 有 + Чиз/Шахс\n\nМисол:\n桌子上有一个电脑。— Дар болои миз компютер ҳаст.\n学校里有一个商店。— Дар дохили мактаб мағоза мавҷуд аст.\n\nМанфӣ: 没有 (méiyǒu)\n椅子下面没有小狗。— Дар зери курсӣ саг нест.\n这儿有人吗？ — 没有。— Дар ин ҷо касе ҳаст? — Не.",
                        "rule_ru": "有(yǒu) — указывает на то, что что-то/кто-то существует в определенном месте.\nСтруктура: Место + 有 + Вещь/Человек.\n\nПример:\n桌子上有一个电脑。 — На столе стоит компьютер.\n学校里有一个商店。 — Внутри школы есть магазин.\n\nОтрицательный: 没有 (мэйю).\n椅子下面没有小狗。 — Под стулом нет собаки.\n这儿有人吗？ — 没有。— Есть здесь кто-нибудь? - Нет."
                },
                "examples": [
                        {
                                "zh": "桌子上有一个电脑。",
                                "pinyin": "Zhuōzi shàng yǒu yī gè diànnǎo.",
                                "meaning": {
                                        "uz": "Stolda kompyuter bor.",
                                        "tj": "Дар болои миз компютер ҳаст.",
                                        "ru": "На столе стоит компьютер."
                                }
                        },
                        {
                                "zh": "学校里没有商店。",
                                "pinyin": "Xuéxiào lǐ méiyǒu shāngdiàn.",
                                "meaning": {
                                        "uz": "Maktabda do'kon yo'q.",
                                        "tj": "Дар мактаб магазин нест.",
                                        "ru": "В школе нет магазина."
                                }
                        },
                        {
                                "zh": "这儿有人吗？",
                                "pinyin": "Zhèr yǒu rén ma?",
                                "meaning": {
                                        "uz": "Bu yerda kimdir bormi?",
                                        "tj": "Дар ин ҷо касе ҳаст?",
                                        "ru": "Есть здесь кто-нибудь?"
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "连词 和 — Bog'lovchi 和",
                "explanation": {
                        "rule_uz": "hé(hé) — ikkita ot yoki olmoshni ('va', 'bilan') bog'laydi.\nTuzilishi: ism 1 + sẖ + ot2\n\nMisol:\nshīngīngīngīngīngī - kompyuter va kitob\nlíngjínín — ota va ona\nchàngàngàngàngíngíngíngjíngjíngjíngín\n\nIzoh: nôi faqat ot va olmoshlarni bog'laydi -\nu fe’l va gaplarni bog‘lay olmaydi.",
                        "rule_tj": "和(hé) — ду исм ё чонишинро мепайвандад ('ва', 'бо').\nСохтор: Исм1 + 和 + Исм2\n\nМисол:\n一个电脑和一本书 — компютер ва китоб\n爸爸和妈妈 — падар ва модар\n我有一个中国朋友和一个美国朋友。\n\nЭзоҳ: 和 танҳо исмҳо ва ҷонишинҳоро мепайвандад -\nон феълхо ва чумлахоро пайваст карда наметавонад.",
                        "rule_ru": "和(hé) — соединяет два существительных или местоимения («и», «с»).\nСтруктура: Существительное1 +和 + Существительное2\n\nПример:\n一个电脑和一本书 — компьютер и книга\n爸爸和妈妈 — отец и мать\n我有一个中国朋友和一个美国朋友。\n\nПримечание: 和 соединяет только существительные и местоимения.\nон не может соединять глаголы или предложения."
                },
                "examples": [
                        {
                                "zh": "电脑和书",
                                "pinyin": "diànnǎo hé shū",
                                "meaning": {
                                        "uz": "kompyuter va kitob",
                                        "tj": "компютер ва китоб",
                                        "ru": "компьютер и книга"
                                }
                        },
                        {
                                "zh": "爸爸和妈妈",
                                "pinyin": "bàba hé māma",
                                "meaning": {
                                        "uz": "ota va ona",
                                        "tj": "падар ва модар",
                                        "ru": "отец и мать"
                                }
                        },
                        {
                                "zh": "我有一个中国朋友和一个美国朋友。",
                                "pinyin": "Wǒ yǒu yī gè Zhōngguó péngyou hé yī gè Měiguó péngyou.",
                                "meaning": {
                                        "uz": "Mening xitoylik do'stim va amerikalik do'stim bor.",
                                        "tj": "Ман як дӯсти чинӣ ва як дӯсти амрикоӣ дорам.",
                                        "ru": "У меня есть друг-китайец и друг-американец."
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "能愿动词 能 — Modal fe'l 能",
                "explanation": {
                        "rule_uz": "néng (néng) — qobiliyat yoki ruxsatni ifodalaydi.\nTuzilishi: Mavzu + lă + Fe'l\n\nMisol:\nlíngāngāngānė？— Shu yerda oʻtirsam maylimi?\nchàngāngāngāngāngānīn？— Ismingizni shu yerga yoza olasizmi?\n\nlí vs mí:\nmán - o'rganish orqali olingan qobiliyat (mahorat)\nlì — sharoitga qarab qobiliyat/ruxsat (mumkin/mumkin)",
                        "rule_tj": "能(néng) — қобилият ё иҷозатро ифода мекунад.\nСохтор: Мавзӯъ + 能 + Феъл\n\nМисол:\n我能坐这儿吗？— Метавонам дар ин ҷо шинам?\n你能在这儿写名字吗？— Метавонед номи худро дар ин ҷо нависед?\n\n能 vs 会:\n会 — қобилият, ки тавассути омӯзиш ба даст омадааст (маҳорат)\n能 — қобилият/иҷозат дар асоси шароит (метавонад/метавонад)",
                        "rule_ru": "能(нэн) — выражает способность или разрешение.\nСтруктура: Подлежащее + 能 + Глагол.\n\nПример:\n我能坐这儿吗？ — Могу я присесть здесь?\n你能在这儿写名字吗？ — Можете ли вы написать здесь свое имя?\n\n能 против 会:\n会 — способность, приобретенная посредством обучения (навык)\n能 — возможность/разрешение в зависимости от обстоятельств (можно/можно)"
                },
                "examples": [
                        {
                                "zh": "我能坐这儿吗？",
                                "pinyin": "Wǒ néng zuò zhèr ma?",
                                "meaning": {
                                        "uz": "Shu yerda o‘tirsam maylimi?",
                                        "tj": "Метавонам дар ин ҷо нишинам?",
                                        "ru": "Можно мне посидеть здесь?"
                                }
                        },
                        {
                                "zh": "你能在这儿工作吗？",
                                "pinyin": "Nǐ néng zài zhèr gōngzuò ma?",
                                "meaning": {
                                        "uz": "Bu yerda ishlay olasizmi?",
                                        "tj": "Метавонед дар ин ҷо кор кунед?",
                                        "ru": "Ты можешь здесь работать?"
                                }
                        },
                        {
                                "zh": "明天你能去商店吗？",
                                "pinyin": "Míngtiān nǐ néng qù shāngdiàn ma?",
                                "meaning": {
                                        "uz": "Ertaga do'konga bora olasizmi?",
                                        "tj": "Метавонед пагоҳ ба мағоза равед?",
                                        "ru": "Ты можешь пойти в магазин завтра?"
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
                                        "uz": "Stolda nima bor?",
                                        "tj": "Дар рӯи миз чӣ аст?",
                                        "ru": "Что находится на столе?"
                                },
                                "answer": "桌子上有什么？",
                                "pinyin": "Zhuōzi shàng yǒu shénme?"
                        },
                        {
                                "prompt": {
                                        "uz": "Stolda kitob va kompyuter bor.",
                                        "tj": "Дар болои миз китоб ва компютер гузошта шудааст.",
                                        "ru": "На столе книга и компьютер."
                                },
                                "answer": "桌子上有一本书和一个电脑。",
                                "pinyin": "Zhuōzi shàng yǒu yī běn shū hé yī gè diànnǎo."
                        },
                        {
                                "prompt": {
                                        "uz": "Bu erda kimdir o'tiradimi?",
                                        "tj": "Оё касе дар ин ҷо нишастааст?",
                                        "ru": "Здесь кто-нибудь сидит?"
                                },
                                "answer": "这儿有人吗？",
                                "pinyin": "Zhèr yǒu rén ma?"
                        },
                        {
                                "prompt": {
                                        "uz": "Shu yerda o‘tirsam maylimi?",
                                        "tj": "Метавонам дар ин ҷо нишинам?",
                                        "ru": "Можно мне посидеть здесь?"
                                },
                                "answer": "我能坐这儿吗？",
                                "pinyin": "Wǒ néng zuò zhèr ma?"
                        },
                        {
                                "prompt": {
                                        "uz": "Iltimos, davom eting.",
                                        "tj": "Лутфан, пеш равед.",
                                        "ru": "Пожалуйста, продолжайте."
                                },
                                "answer": "请坐。",
                                "pinyin": "Qǐng zuò."
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
                                "prompt": "桌子上___一个电脑和一本书。",
                                "answer": "有",
                                "pinyin": "yǒu"
                        },
                        {
                                "prompt": "这儿有人吗？___。",
                                "answer": "没有",
                                "pinyin": "méiyǒu"
                        },
                        {
                                "prompt": "我___坐这儿吗？",
                                "answer": "能",
                                "pinyin": "néng"
                        },
                        {
                                "prompt": "桌子上有电脑___书。",
                                "answer": "和",
                                "pinyin": "hé"
                        }
                ]
        },
        {
                "no": 3,
                "type": "location",
                "instruction": {
                        "uz": "U qayerdaligini ayting (shīngīnī/yīngīng/yīng):",
                        "tj": "Бигӯед, ки он дар куҷост (上/里/下面/前面/后面):",
                        "ru": "Скажи, где это (上/里/下面/前面/后面):"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "Kitob - stolda",
                                        "tj": "Китоб — дар руи миз",
                                        "ru": "Книга — на столе"
                                },
                                "answer": "书在桌子上。",
                                "pinyin": "Shū zài zhuōzi shàng."
                        },
                        {
                                "prompt": {
                                        "uz": "It - stul ostida",
                                        "tj": "Саг - дар зери кафедра",
                                        "ru": "Собака — под стулом"
                                },
                                "answer": "狗在椅子下面。",
                                "pinyin": "Gǒu zài yǐzi xiàmian."
                        },
                        {
                                "prompt": {
                                        "uz": "Kompyuter - stol ichida",
                                        "tj": "Компютер — дар дохили миз",
                                        "ru": "Компьютер — внутри стола"
                                },
                                "answer": "电脑在桌子里。",
                                "pinyin": "Diànnǎo zài zhuōzi lǐ."
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "桌子上有什么？",
                        "桌子上有一本书和一个电脑。",
                        "这儿有人吗？",
                        "我能坐这儿吗？",
                        "请坐。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "有",
                        "没有",
                        "能",
                        "和"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "书在桌子上。",
                        "狗在椅子下面。",
                        "电脑在桌子里。"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Xonangiz haqida 4 ta jumla yozing (mài yordamida):",
                        "tj": "Дар бораи ҳуҷраи худ 4 ҷумла нависед (бо истифода аз 有):",
                        "ru": "Напишите 4 предложения о своей комнате (используя 有):"
                },
                "template": "我的桌子上有___。桌子里有___。椅子___有___。",
                "words": [
                        "有",
                        "没有",
                        "上",
                        "里",
                        "下面",
                        "电脑",
                        "书",
                        "杯子"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "y dan foydalanib 3 ta savol yozing va ularga javob bering:",
                        "tj": "Бо истифода аз 能 3 савол нависед ва ба онҳо ҷавоб диҳед:",
                        "ru": "Напишите 3 вопроса, используя 能, и ответьте на них:"
                },
                "example": "A: 我能坐这儿吗？ B: 请坐。/ 对不起，不能。"
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
