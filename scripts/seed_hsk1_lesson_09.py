import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 9,
    "lesson_code": "HSK1-L09",
    "title": "你儿子在哪儿工作",
    "goal": {
        "uz": "Joylashuv va ish joyi haqida so'rash, fe'l va predlog'i",
        "tj": "Пурсидан дар бораи макон ва ҷои кор, феъл ва пешванди 在",
        "ru": "В вопросе о местонахождении и рабочем месте используется глагол и предлог在."
    },
    "intro_text": {
        "uz": "To'qqizinchi darsda siz birovning qayerdaligini, qayerda ishlayotganimizni va l ning ikkita ishlatilishini so'rashni o'rganasiz. 14 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси нӯҳум шумо пурсиданро меомӯзед, ки касе дар куҷост, мо дар куҷо кор мекунем ва ду истифодаи 在. 14 калимаи нав, 3 муколама.",
        "ru": "На девятом уроке вы научитесь спрашивать, где кто-то находится, где мы работаем, а также два варианта использования 在. 14 новых слов, 3 диалога."
    },

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "小",
                "pinyin": "xiǎo",
                "pos": "adj.",
                "meaning": {
                        "uz": "kichik, kichik",
                        "tj": "хурд, хурд",
                        "ru": "маленький, маленький"
                }
        },
        {
                "no": 2,
                "zh": "猫",
                "pinyin": "māo",
                "pos": "n.",
                "meaning": {
                        "uz": "mushuk",
                        "tj": "гурба",
                        "ru": "кот"
                }
        },
        {
                "no": 3,
                "zh": "在",
                "pinyin": "zài",
                "pos": "v./prep.",
                "meaning": {
                        "uz": "bo'lmoq / da, in (joy belgisi)",
                        "tj": "будан дар / дар, дар (нишонакунандаи ҷойгиршавӣ)",
                        "ru": "находиться в / у, в (маркере местоположения)"
                }
        },
        {
                "no": 4,
                "zh": "哪儿",
                "pinyin": "nǎr",
                "pos": "pron.",
                "meaning": {
                        "uz": "qayerda",
                        "tj": "дар куҷо",
                        "ru": "где"
                }
        },
        {
                "no": 5,
                "zh": "狗",
                "pinyin": "gǒu",
                "pos": "n.",
                "meaning": {
                        "uz": "it",
                        "tj": "саг",
                        "ru": "собака"
                }
        },
        {
                "no": 6,
                "zh": "椅子",
                "pinyin": "yǐzi",
                "pos": "n.",
                "meaning": {
                        "uz": "stul",
                        "tj": "курсӣ",
                        "ru": "стул"
                }
        },
        {
                "no": 7,
                "zh": "下面",
                "pinyin": "xiàmian",
                "pos": "n.",
                "meaning": {
                        "uz": "pastda, ostida",
                        "tj": "поён, дар зер",
                        "ru": "ниже, под"
                }
        },
        {
                "no": 8,
                "zh": "工作",
                "pinyin": "gōngzuò",
                "pos": "v./n.",
                "meaning": {
                        "uz": "ishlash / ishlash, ish",
                        "tj": "кор кардан / кор кардан, кор кардан",
                        "ru": "работать / работать, работа"
                }
        },
        {
                "no": 9,
                "zh": "儿子",
                "pinyin": "érzi",
                "pos": "n.",
                "meaning": {
                        "uz": "o'g'lim",
                        "tj": "писар",
                        "ru": "сын"
                }
        },
        {
                "no": 10,
                "zh": "医院",
                "pinyin": "yīyuàn",
                "pos": "n.",
                "meaning": {
                        "uz": "kasalxona",
                        "tj": "беморхона",
                        "ru": "больница"
                }
        },
        {
                "no": 11,
                "zh": "医生",
                "pinyin": "yīshēng",
                "pos": "n.",
                "meaning": {
                        "uz": "shifokor",
                        "tj": "духтур",
                        "ru": "врач"
                }
        },
        {
                "no": 12,
                "zh": "爸爸",
                "pinyin": "bàba",
                "pos": "n.",
                "meaning": {
                        "uz": "ota, dada",
                        "tj": "падар, падар",
                        "ru": "отец, папа"
                }
        },
        {
                "no": 13,
                "zh": "家",
                "pinyin": "jiā",
                "pos": "n.",
                "meaning": {
                        "uz": "uy, oila",
                        "tj": "хона, оила",
                        "ru": "дом, семья"
                }
        },
        {
                "no": 14,
                "zh": "那儿",
                "pinyin": "nàr",
                "pos": "pron.",
                "meaning": {
                        "uz": "u yerda, u yerda",
                        "tj": "он ҷо, он ҷо",
                        "ru": "там, там"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Uyda — mushuk va it qayerda",
                        "tj": "Дар хона - гурба ва саг куҷост",
                        "ru": "Дома - где кот и собака"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "小猫在哪儿？",
                                "pinyin": "Xiǎo māo zài nǎr?",
                                "translation": {
                                        "uz": "Mushuk qayerda?",
                                        "tj": "Гурба куҷост?",
                                        "ru": "Где кот?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "小猫在那儿。",
                                "pinyin": "Xiǎo māo zài nàr.",
                                "translation": {
                                        "uz": "Mushuk u yerda.",
                                        "tj": "Гурба дар он ҷост.",
                                        "ru": "Кот там."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "小狗在哪儿？",
                                "pinyin": "Xiǎo gǒu zài nǎr?",
                                "translation": {
                                        "uz": "It qayerda?",
                                        "tj": "Саг дар куҷост?",
                                        "ru": "Где собака?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "小狗在椅子下面。",
                                "pinyin": "Xiǎo gǒu zài yǐzi xiàmian.",
                                "translation": {
                                        "uz": "It stul ostida.",
                                        "tj": "Саг дар зери курсӣ аст.",
                                        "ru": "Собака под стулом."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Temir yo'l stansiyasida — ish joyi",
                        "tj": "Ҷои кор дар истгоҳи роҳи оҳан",
                        "ru": "Рабочее место на вокзале"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你在哪儿工作？",
                                "pinyin": "Nǐ zài nǎr gōngzuò?",
                                "translation": {
                                        "uz": "Qayerda ishlaysiz?",
                                        "tj": "Ту дар куҷо кор мекунӣ?",
                                        "ru": "Где ты работаешь?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我在学校工作。",
                                "pinyin": "Wǒ zài xuéxiào gōngzuò.",
                                "translation": {
                                        "uz": "Men maktabda ishlayman.",
                                        "tj": "Ман дар мактаб кор мекунам.",
                                        "ru": "Я работаю в школе."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你儿子在哪儿工作？",
                                "pinyin": "Nǐ érzi zài nǎr gōngzuò?",
                                "translation": {
                                        "uz": "O'g'lingiz qayerda ishlaydi?",
                                        "tj": "Писари шумо дар куҷо кор мекунад?",
                                        "ru": "Где работает ваш сын?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我儿子在医院工作，他是医生。",
                                "pinyin": "Wǒ érzi zài yīyuàn gōngzuò, tā shì yīshēng.",
                                "translation": {
                                        "uz": "O'g'lim kasalxonada ishlaydi - u shifokor.",
                                        "tj": "Писари ман дар беморхона кор мекунад - ӯ духтур аст.",
                                        "ru": "Мой сын работает в больнице — он врач."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Telefonda — ota qayerda",
                        "tj": "Дар телефон - падар куҷост?",
                        "ru": "По телефону - где отец?"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你爸爸在家吗？",
                                "pinyin": "Nǐ bàba zài jiā ma?",
                                "translation": {
                                        "uz": "Otangiz uydami?",
                                        "tj": "Падари шумо дар хона аст?",
                                        "ru": "Твой отец дома?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "不在家。",
                                "pinyin": "Bú zài jiā.",
                                "translation": {
                                        "uz": "U uyda emas.",
                                        "tj": "Ӯ дар хона нест.",
                                        "ru": "Его нет дома."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "他在哪儿呢？",
                                "pinyin": "Tā zài nǎr ne?",
                                "translation": {
                                        "uz": "U qayerda?",
                                        "tj": "Пас ӯ дар куҷост?",
                                        "ru": "Где он тогда?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "他在医院。",
                                "pinyin": "Tā zài yīyuàn.",
                                "translation": {
                                        "uz": "U kasalxonada.",
                                        "tj": "Ӯ дар беморхона аст.",
                                        "ru": "Он в больнице."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "动词 在 — Fe'l 在 (joylashuv)",
                "explanation": {
                        "rule_uz": "zài (zài) - fe'l sifatida, biror narsa/kimdir qaerda joylashganligini bildiradi.\nTuzilishi: Mavzu + l + Joy\n\nMisol:\nlíngínhín-mhu — Mushuk shu yerda.\nchàngàngǐnēng — Do'stim maktabda.\nchàngāngīnīng — Onam uyda.\n\nSalbiy: Mavzu + shín + Joy\nlíngzhīdīngī - Dadam uyda yo'q.",
                        "rule_tj": "在(zài) — ҳамчун феъл, дар куҷо будани чизе/касеро нишон медиҳад.\nСохтор: Мавзӯъ + 在 + Ҷой\n\nМисол:\n小猫在那儿。— Гурба дар он ҷост.\n我朋友在学校。— Дӯсти ман дар мактаб аст.\n我妈妈在家。— Модарам дар хона аст.\n\nМанфӣ: Мавзӯъ + 不在 + Ҷой\n爸爸不在家。— Падар дар хона нест.",
                        "rule_ru": "在(zài) — как глагол, указывает, где находится что-то/кто-то.\nСтруктура: Тема + 在 + Место.\n\nПример:\n小猫在那儿。 — Кот там.\n我朋友在学校。 — Мой друг в школе.\n我妈妈在家。 — Моя мама дома.\n\nОтрицательное: Тема + 不在 + Место.\n爸爸不在家。 — Отца нет дома."
                },
                "examples": [
                        {
                                "zh": "小猫在那儿。",
                                "pinyin": "Xiǎo māo zài nàr.",
                                "meaning": {
                                        "uz": "Mushuk u yerda.",
                                        "tj": "Гурба дар он ҷост.",
                                        "ru": "Кот там."
                                }
                        },
                        {
                                "zh": "我朋友在学校。",
                                "pinyin": "Wǒ péngyou zài xuéxiào.",
                                "meaning": {
                                        "uz": "Mening do'stim maktabda.",
                                        "tj": "Дӯсти ман дар мактаб аст.",
                                        "ru": "Мой друг в школе."
                                }
                        },
                        {
                                "zh": "爸爸不在家。",
                                "pinyin": "Bàba bú zài jiā.",
                                "meaning": {
                                        "uz": "Ota uyda yo'q.",
                                        "tj": "Падар дар хона нест.",
                                        "ru": "Отца нет дома."
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "哪儿 — Qayerda so'roq olmoshi",
                "explanation": {
                        "rule_uz": "nǎr (nǎr) — joylashuv haqida soʻrash uchun soʻroq soʻz.\nTuzilishi: Mavzu + lín + lín?\n\nMisol:\nlíngāngāngān？ - Mushuk qayerda?\nchàngàngìnìnīng？— Qayerda ishlaysiz?\nchàngàngìnżn？— U qayerda?",
                        "rule_tj": "哪儿(nǎr) — калимаи пурсиш барои пурсиш дар бораи макон.\nСохтор: Мавзӯъ + 在 + 哪儿?\n\nМисол:\n小猫在哪儿？ — Гурба куҷост?\n你在哪儿工作？— Шумо дар куҷо кор мекунед?\n他在哪儿呢？— Вай дар куҷост?",
                        "rule_ru": "哪儿(nǎr) — вопросительное слово, обозначающее местоположение.\nСтруктура: Подлежащее +在+哪儿?\n\nПример:\n小猫在哪儿？ — Где кот?\n你在哪儿工作？ — Где ты работаешь?\n他在哪儿呢？ — Где он?"
                },
                "examples": [
                        {
                                "zh": "你在哪儿工作？",
                                "pinyin": "Nǐ zài nǎr gōngzuò?",
                                "meaning": {
                                        "uz": "Qayerda ishlaysiz?",
                                        "tj": "Ту дар куҷо кор мекунӣ?",
                                        "ru": "Где ты работаешь?"
                                }
                        },
                        {
                                "zh": "小狗在哪儿？",
                                "pinyin": "Xiǎo gǒu zài nǎr?",
                                "meaning": {
                                        "uz": "It qayerda?",
                                        "tj": "Саг дар куҷост?",
                                        "ru": "Где собака?"
                                }
                        },
                        {
                                "zh": "他爸爸在哪儿呢？",
                                "pinyin": "Tā bàba zài nǎr ne?",
                                "meaning": {
                                        "uz": "Uning otasi qayerda?",
                                        "tj": "Падараш дар куҷост?",
                                        "ru": "Где его отец?"
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "介词 在 — Predlog 在 (joy bildiradi)",
                "explanation": {
                        "rule_uz": "zài (zài) — bosh gap sifatida fe’ldan oldin kelib, harakatning qayerda sodir bo‘lishini bildiradi.\nTuzilishi: Mavzu + ln + Joy + Fe'l\n\nMisol:\nmíngīngīngīngīngīng — O‘g‘lim kasalxonada ishlaydi.\nchàngàngāngāngāngīng — Ular maktabda o‘qiydilar.\nlíngàngǎngǎngkí— Men do'stimnikida choy ichyapman.\n\nFarqi:\nlíngìnīng (fe'l fín) - U kasalxonada.\nchàngīngīnīkī (Predpozitsiya) - U kasalxonada ishlaydi.",
                        "rule_tj": "在(zài) — ҳамчун пешванд, пеш аз феъл омада, дар куҷо сурат гирифтани амалро нишон медиҳад.\nСохтор: Мавзӯъ + 在 + Ҷой + Феъл\n\nМисол:\n我儿子在医院工作。— Писари ман дар беморхона кор мекунад.\n他们在学校看书。— Дар мактаб мехонанд.\n我在朋友家喝茶。— Ман дар ҷои дӯстам чой менӯшам.\n\nФарқият:\n她在医院。(Феъли 在) — Вай дар беморхона аст.\n她在医院工作。(Пешванди 在) — Вай дар беморхона кор мекунад.",
                        "rule_ru": "在(zài) — предлог, стоит перед глаголом и указывает, где происходит действие.\nСтруктура: Подлежащее + 在 + Место + Глагол.\n\nПример:\n我儿子在医院工作。 — Мой сын работает в больнице.\n他们在学校看书。 — Они читают в школе.\n我在朋友家喝茶。 — Я пью чай у моего друга.\n\nРазница:\n她在医院。(глагол在) — Она в больнице.\n她在医院工作。(предлог在) — Она работает в больнице."
                },
                "examples": [
                        {
                                "zh": "我儿子在医院工作。",
                                "pinyin": "Wǒ érzi zài yīyuàn gōngzuò.",
                                "meaning": {
                                        "uz": "O'g'lim kasalxonada ishlaydi.",
                                        "tj": "Писарам дар беморхона кор мекунад.",
                                        "ru": "Мой сын работает в больнице."
                                }
                        },
                        {
                                "zh": "他们在学校看书。",
                                "pinyin": "Tāmen zài xuéxiào kàn shū.",
                                "meaning": {
                                        "uz": "Ular maktabda o'qiydilar.",
                                        "tj": "Онҳо дар мактаб мехонанд.",
                                        "ru": "Они читают в школе."
                                }
                        },
                        {
                                "zh": "我在家喝茶。",
                                "pinyin": "Wǒ zài jiā hē chá.",
                                "meaning": {
                                        "uz": "Men uyda choy ichaman.",
                                        "tj": "Ман дар хона чой менӯшам.",
                                        "ru": "Я пью чай дома."
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
                                        "uz": "Mushuk qayerda?",
                                        "tj": "Гурба куҷост?",
                                        "ru": "Где кот?"
                                },
                                "answer": "小猫在哪儿？",
                                "pinyin": "Xiǎo māo zài nǎr?"
                        },
                        {
                                "prompt": {
                                        "uz": "It stul ostida.",
                                        "tj": "Саг дар зери курсӣ аст.",
                                        "ru": "Собака под стулом."
                                },
                                "answer": "小狗在椅子下面。",
                                "pinyin": "Xiǎo gǒu zài yǐzi xiàmian."
                        },
                        {
                                "prompt": {
                                        "uz": "Qayerda ishlaysiz?",
                                        "tj": "Ту дар куҷо кор мекунӣ?",
                                        "ru": "Где ты работаешь?"
                                },
                                "answer": "你在哪儿工作？",
                                "pinyin": "Nǐ zài nǎr gōngzuò?"
                        },
                        {
                                "prompt": {
                                        "uz": "O'g'lim kasalxonada ishlaydi.",
                                        "tj": "Писарам дар беморхона кор мекунад.",
                                        "ru": "Мой сын работает в больнице."
                                },
                                "answer": "我儿子在医院工作。",
                                "pinyin": "Wǒ érzi zài yīyuàn gōngzuò."
                        },
                        {
                                "prompt": {
                                        "uz": "Otangiz uydami?",
                                        "tj": "Падари шумо дар хона аст?",
                                        "ru": "Твой отец дома?"
                                },
                                "answer": "你爸爸在家吗？",
                                "pinyin": "Nǐ bàba zài jiā ma?"
                        },
                        {
                                "prompt": {
                                        "uz": "U uyda emas - kasalxonada.",
                                        "tj": "Ӯ дар хона нест - дар беморхона аст.",
                                        "ru": "Его нет дома — он в больнице."
                                },
                                "answer": "不在家，他在医院。",
                                "pinyin": "Bú zài jiā, tā zài yīyuàn."
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
                                "prompt": "小猫___那儿。",
                                "answer": "在",
                                "pinyin": "zài"
                        },
                        {
                                "prompt": "你___哪儿工作？",
                                "answer": "在",
                                "pinyin": "zài"
                        },
                        {
                                "prompt": "小狗在椅子___面。",
                                "answer": "下",
                                "pinyin": "xià"
                        },
                        {
                                "prompt": "我儿子在医院___，他是医生。",
                                "answer": "工作",
                                "pinyin": "gōngzuò"
                        }
                ]
        },
        {
                "no": 3,
                "type": "make_sentence",
                "instruction": {
                        "uz": "Berilgan so‘zlardan gap tuzing:",
                        "tj": "Аз калимаҳои додашуда ҷумла созед:",
                        "ru": "Составьте предложение из данных слов:"
                },
                "items": [
                        {
                                "words": [
                                        "在",
                                        "医院",
                                        "工作",
                                        "我妈妈"
                                ],
                                "answer": "我妈妈在医院工作。",
                                "pinyin": "Wǒ māma zài yīyuàn gōngzuò."
                        },
                        {
                                "words": [
                                        "哪儿",
                                        "在",
                                        "小猫",
                                        "？"
                                ],
                                "answer": "小猫在哪儿？",
                                "pinyin": "Xiǎo māo zài nǎr?"
                        },
                        {
                                "words": [
                                        "在",
                                        "家",
                                        "不",
                                        "爸爸"
                                ],
                                "answer": "爸爸不在家。",
                                "pinyin": "Bàba bú zài jiā."
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "小猫在哪儿？",
                        "小狗在椅子下面。",
                        "你在哪儿工作？",
                        "我儿子在医院工作。",
                        "你爸爸在家吗？",
                        "不在家，他在医院。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "在",
                        "在",
                        "下",
                        "工作"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "我妈妈在医院工作。",
                        "小猫在哪儿？",
                        "爸爸不在家。"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Oila a'zolaringiz haqida 4 ta jumla yozing (ular qayerda ishlaydilar):",
                        "tj": "Дар бораи аъзоёни оилаи худ 4 ҷумла нависед (онҳо дар куҷо кор мекунанд):",
                        "ru": "Напишите 4 предложения о членах вашей семьи (где они работают/находятся):"
                },
                "template": "我___在___工作/在___。",
                "words": [
                        "在",
                        "工作",
                        "医院",
                        "学校",
                        "家",
                        "商店"
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
                                "prompt": "你在哪儿工作/学习？",
                                "hint": "Where do you work or study?"
                        },
                        {
                                "prompt": "你爸爸在哪儿工作？",
                                "hint": "Where does your father work?"
                        },
                        {
                                "prompt": "你现在在哪儿？",
                                "hint": "Where are you right now?"
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
