import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 5,
    "lesson_code": "HSK1-L05",
    "title": "她女儿今年二十岁",
    "goal": {
        "uz": "Yosh va oila a'zolari haqida gapiring va 100 gacha raqamlarni o'rganing",
        "tj": "Дар бораи синну сол ва аъзоёни оила сӯҳбат кунед ва рақамҳои то 100-ро омӯзед",
        "ru": "Поговорите о возрасте и членах семьи и выучите числа до 100."
    },
    "intro_text": {
        "uz": "Beshinchi darsda siz birovning yoshini so'rash va aytishni, oila a'zolarining soni haqida gapirishni va 100 tagacha raqamlarni o'rganishni o'rganasiz. 10 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси панчум шумо чи тавр пурсидан ва гуфтани синну соли касеро меомузед, дар бораи шумораи аъзоёни оила гап мезанед, шуморахои то 100-ро меомузед. 10 калимаи нав, 3 муколама.",
        "ru": "На пятом уроке вы научитесь спрашивать и называть чей-то возраст, говорить о количестве членов семьи, а также выучите числа до 100. 10 новых слов, 3 диалога."
    },

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "家",
                "pinyin": "jiā",
                "pos": "n.",
                "meaning": {
                        "uz": "oila, uy",
                        "tj": "оила, хона",
                        "ru": "семья, дом"
                }
        },
        {
                "no": 2,
                "zh": "有",
                "pinyin": "yǒu",
                "pos": "v.",
                "meaning": {
                        "uz": "ega bo'lmoq, bor",
                        "tj": "доштан, вуҷуд дорад",
                        "ru": "иметь, есть"
                }
        },
        {
                "no": 3,
                "zh": "口",
                "pinyin": "kǒu",
                "pos": "m.",
                "meaning": {
                        "uz": "oila a'zolari uchun so'zni o'lchash",
                        "tj": "чен кардани калима барои аъзоёни оила",
                        "ru": "мерное слово для членов семьи"
                }
        },
        {
                "no": 4,
                "zh": "女儿",
                "pinyin": "nǚ'ér",
                "pos": "n.",
                "meaning": {
                        "uz": "qizim",
                        "tj": "духтар",
                        "ru": "дочь"
                }
        },
        {
                "no": 5,
                "zh": "几",
                "pinyin": "jǐ",
                "pos": "pron.",
                "meaning": {
                        "uz": "qancha (10 tagacha)",
                        "tj": "чанд (то 10)",
                        "ru": "сколько (до 10)"
                }
        },
        {
                "no": 6,
                "zh": "岁",
                "pinyin": "suì",
                "pos": "m.",
                "meaning": {
                        "uz": "yosh (yosh uchun so'zni o'lchash)",
                        "tj": "сола (калимаи ченак барои синну сол)",
                        "ru": "лет (измеряемое слово для возраста)"
                }
        },
        {
                "no": 7,
                "zh": "了",
                "pinyin": "le",
                "pos": "part.",
                "meaning": {
                        "uz": "holatni o'zgartiruvchi zarracha",
                        "tj": "заррачаи ҳолати тағирёбанда",
                        "ru": "частица, меняющая состояние"
                }
        },
        {
                "no": 8,
                "zh": "今年",
                "pinyin": "jīnnián",
                "pos": "n.",
                "meaning": {
                        "uz": "bu yil",
                        "tj": "дар ҳамин сол",
                        "ru": "в этом году"
                }
        },
        {
                "no": 9,
                "zh": "多",
                "pinyin": "duō",
                "pos": "adv.",
                "meaning": {
                        "uz": "ko'p, qanday (daraja)",
                        "tj": "бисёр, чӣ гуна (дараҷа)",
                        "ru": "много, как (степень)"
                }
        },
        {
                "no": 10,
                "zh": "大",
                "pinyin": "dà",
                "pos": "adj.",
                "meaning": {
                        "uz": "katta, qari (yoshida)",
                        "tj": "калон, пир (дар синну сол)",
                        "ru": "большой, старый (по возрасту)"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Maktabda — oila a'zolari",
                        "tj": "Дар мактаб — аъзоёни оила",
                        "ru": "В школе – члены семьи"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你家有几口人？",
                                "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?",
                                "translation": {
                                        "uz": "Oilangizda nechta odam bor?",
                                        "tj": "Дар оилаи шумо чанд нафар ҳастанд?",
                                        "ru": "Сколько человек в вашей семье?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我家有三口人。",
                                "pinyin": "Wǒ jiā yǒu sān kǒu rén.",
                                "translation": {
                                        "uz": "Mening oilamda uch kishi bor.",
                                        "tj": "Дар оилаи ман се нафар ҳастанд.",
                                        "ru": "В моей семье три человека."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Ofisda — yosh so'rash",
                        "tj": "Дар идора — синну солро пурсед",
                        "ru": "В офисе - спроси возраст"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你女儿几岁了？",
                                "pinyin": "Nǐ nǚ'ér jǐ suì le?",
                                "translation": {
                                        "uz": "Qizingiz necha yoshda?",
                                        "tj": "Духтари шумо чандсола аст?",
                                        "ru": "Сколько лет вашей дочери?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "她今年四岁了。",
                                "pinyin": "Tā jīnnián sì suì le.",
                                "translation": {
                                        "uz": "Bu yil u to'rt yoshda.",
                                        "tj": "Вай имсол чорсола шуд.",
                                        "ru": "В этом году ей четыре года."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Ofisda — kattalar yoshi",
                        "tj": "Дар идора — ба камол расидан",
                        "ru": "В офисе - взрослая жизнь"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "李老师多大了？",
                                "pinyin": "Lǐ lǎoshī duō dà le?",
                                "translation": {
                                        "uz": "O'qituvchi Li necha yoshda?",
                                        "tj": "Муаллим Ли чандсола аст?",
                                        "ru": "Сколько лет Учителю Ли?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "她今年五十岁了。",
                                "pinyin": "Tā jīnnián wǔshí suì le.",
                                "translation": {
                                        "uz": "Bu yil u ellik yoshda.",
                                        "tj": "Вай имсол панчохсола шуд.",
                                        "ru": "В этом году ей исполнится пятьдесят лет."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "她女儿呢？",
                                "pinyin": "Tā nǚ'ér ne?",
                                "translation": {
                                        "uz": "Uning qizi-chi?",
                                        "tj": "Дар бораи духтараш чӣ гуфтан мумкин аст?",
                                        "ru": "А что насчет ее дочери?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "她女儿今年二十岁。",
                                "pinyin": "Tā nǚ'ér jīnnián èrshí suì.",
                                "translation": {
                                        "uz": "Qizi bu yil yigirma yoshda.",
                                        "tj": "Духтараш имсол бистсола шуд.",
                                        "ru": "В этом году ее дочери исполнится двадцать лет."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "几 — Necha? (10 gacha)",
                "explanation": {
                        "rule_uz": "jǐ(jǐ) — 10 dan kichik sonlar uchun soʻroq soʻzi.\nTuzilishi: Mavzu + lín + nć + O'lchov so'zi + Ism?\n\nMisol:\nshnhànghìnīng？— Oilangizda nechta odam bor?\nshíngčičnīngīngīngī？— Sizda nechta xitoy o'qituvchisi bor?\nchàngìnìnīnī？— Qizingiz necha yoshda?",
                        "rule_tj": "几(jǐ) — калимаи саволӣ барои ададҳои зери 10.\nСохтор: Мавзӯъ + 有 + 几 + Калимаи андоза + Исм?\n\nМисол:\n你家有几口人？— Дар оилаи шумо чанд нафар ҳастанд?\n你有几个汉语老师？— Шумо чанд муаллими чинӣ доред?\n你女儿几岁了？— Духтаратон чандсола аст?",
                        "rule_ru": "几(jϐ) — вопросительное слово для чисел до 10.\nСтруктура: Подлежащее + 有 + 几 + Мерное слово + Существительное?\n\nПример:\n你家有几口人？ — Сколько человек в вашей семье?\n你有几个汉语老师？ — Сколько у вас учителей китайского языка?\n你女儿几岁了？ — Сколько лет вашей дочери?"
                },
                "examples": [
                        {
                                "zh": "你家有几口人？",
                                "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?",
                                "meaning": {
                                        "uz": "Oilangizda nechta odam bor?",
                                        "tj": "Дар оилаи шумо чанд нафар ҳастанд?",
                                        "ru": "Сколько человек в вашей семье?"
                                }
                        },
                        {
                                "zh": "你有几个朋友？",
                                "pinyin": "Nǐ yǒu jǐ ge péngyou?",
                                "meaning": {
                                        "uz": "Qancha do'stingiz bor?",
                                        "tj": "Шумо чанд дӯст доред?",
                                        "ru": "Сколько у тебя друзей?"
                                }
                        },
                        {
                                "zh": "她有几岁了？",
                                "pinyin": "Tā yǒu jǐ suì le?",
                                "meaning": {
                                        "uz": "Uning yoshi nechida?",
                                        "tj": "Ин зан чандсола?",
                                        "ru": "Сколько ей лет?"
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "100 gacha raqamlar",
                "explanation": {
                        "rule_uz": "1-10: yī yī yīr y sān sān sì y y wǔ líliù yīqī yībā yjiǔ shí\n\nO'nlab:\n20 = yán (èrshí)\n30 = sānshí (sānshí)\n50 = yán (wǔshí)\n99 = yǔshíjiǔ (jiǔshíjiǔ)\n\nAralash raqamlar:\n23 = yānīsān (èrshísān)\n56 = shínčán (wǔshíliù)\n88 = dānčán (bashíbā)",
                        "rule_tj": "1-10: 一yī 二èr 三sān 四sì 五wǔ 六liù 七qī 八bā 九jiǔ 十shí\n\nДаҳҳо:\n20 = 二十 (èrshí)\n30 = 三十 (sānshí)\n50 = 五十 (wǔshí)\n99 = 九十九 (jiǔshíjiǔ)\n\nРақамҳои омехта:\n23 = 二十三 (èrshísān)\n56 = 五十六 (wǔshíliù)\n88 = 八十八 (bāshíbā)",
                        "rule_ru": "1-10: 一yī 二èr 三сан 四sì 五wٔ 六liù 七qī 八bā 九jiٔ 十shí\n\nДесятки:\n20 = 二十 (эрши)\n30 = 三十 (санши)\n50 = 五十 (уши)\n99 = 九十九 (джиушиджиу)\n\nСмешанные числа:\n23 = 二十三 (эршисан)\n56 = 五十六 (ушилиу)\n88 = 八十八 (башиба)"
                },
                "examples": [
                        {
                                "zh": "二十",
                                "pinyin": "èrshí",
                                "meaning": {
                                        "uz": "20",
                                        "tj": "20",
                                        "ru": "20"
                                }
                        },
                        {
                                "zh": "五十",
                                "pinyin": "wǔshí",
                                "meaning": {
                                        "uz": "50",
                                        "tj": "50",
                                        "ru": "50"
                                }
                        },
                        {
                                "zh": "二十三",
                                "pinyin": "èrshísān",
                                "meaning": {
                                        "uz": "23",
                                        "tj": "23",
                                        "ru": "23"
                                }
                        },
                        {
                                "zh": "九十九",
                                "pinyin": "jiǔshíjiǔ",
                                "meaning": {
                                        "uz": "99",
                                        "tj": "99",
                                        "ru": "99"
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "了 — O'zgarish yuklamasi",
                "explanation": {
                        "rule_uz": "mán(le) — gap oxirida qoʻyilgan yangi holat yoki oʻzgarishni bildiradi.\n\nMisol:\nchàngāngāngāngānī - Bu yil u ellik yoshga to'ldi (yangi shtat).\nchàngìnìnězínīk — Qizim to‘rt yoshga to‘ldi.\n\nhàngìnī？— Nechchi yoshdasiz? (yosh so'ramoqda)",
                        "rule_tj": "了(le) — дар охири љумла љойгиршуда њолати нав ё таѓйиротро нишон медињад.\n\nМисол:\n她今年五十岁了。— Вай имсол панҷоҳсола шуд (давлати нав).\n我女儿四岁了。— Духтарам чорсола шуд.\n\n多大了？— Шумо чандсола шудед? (синну сол пурсед)",
                        "rule_ru": "了(le) — ставится в конце предложения и указывает на новое состояние или изменение.\n\nПример:\n她今年五十岁了。 — В этом году ей исполнилось пятьдесят (новый штат).\n我女儿四岁了。 — Моей дочери исполнилось четыре года.\n\n多大了？— Сколько тебе лет исполнилось? (спрашивает возраст)"
                },
                "examples": [
                        {
                                "zh": "她今年二十岁了。",
                                "pinyin": "Tā jīnnián èrshí suì le.",
                                "meaning": {
                                        "uz": "Bu yil u yigirma yoshga to'ldi.",
                                        "tj": "Вай имсол бистсола шуд.",
                                        "ru": "В этом году ей исполнилось двадцать."
                                }
                        },
                        {
                                "zh": "他五十岁了。",
                                "pinyin": "Tā wǔshí suì le.",
                                "meaning": {
                                        "uz": "U ellik yoshga kirdi.",
                                        "tj": "Вай панчохсола шуд.",
                                        "ru": "Ему исполнилось пятьдесят."
                                }
                        },
                        {
                                "zh": "你多大了？",
                                "pinyin": "Nǐ duō dà le?",
                                "meaning": {
                                        "uz": "Yoshingiz nechida?",
                                        "tj": "Ту чанд сола?",
                                        "ru": "Сколько тебе лет?"
                                }
                        }
                ]
        },
        {
                "no": 4,
                "title_zh": "多大 — Yosh so'rash",
                "explanation": {
                        "rule_uz": "dài (duō dà) — kattalarning yoshini soʻrash uchun ishlatiladi.\njǐ suì (jǐ suì) — bolalarning (10 yoshgacha) yoshini soʻrash uchun ishlatiladi.\n\nVoyaga etganlar: mēngāngīn？— Yoshingiz nechada?\nBolalar: mìnīngīngīnīnī？— Qizingiz necha yoshda?",
                        "rule_tj": "多大(duō dà) — синну соли калонсолонро мепурсид.\n几岁(jǐ suì) — синну соли кӯдаконро (то 10-сола) мепурсид.\n\nКалонсолон: 你多大了？— Шумо чандсолаед?\nКӯдакон: 你女儿几岁了？— Духтаратон чандсола аст?",
                        "rule_ru": "多大(дуо да) — спрашивают возраст взрослых.\n几岁(jǐ suì) — спрашивают возраст детей (до 10 лет).\n\nВзрослые: 你多大了？ — Сколько тебе лет?\nДети: 你女儿几岁了？ — Сколько лет вашей дочери?"
                },
                "examples": [
                        {
                                "zh": "你多大了？",
                                "pinyin": "Nǐ duō dà le?",
                                "meaning": {
                                        "uz": "Yoshingiz nechida? (kattalar)",
                                        "tj": "Ту чанд сола? (калонсолон)",
                                        "ru": "Сколько тебе лет? (взрослые)"
                                }
                        },
                        {
                                "zh": "她女儿几岁了？",
                                "pinyin": "Tā nǚ'ér jǐ suì le?",
                                "meaning": {
                                        "uz": "Uning qizi necha yoshda? (bola)",
                                        "tj": "Духтараш чандсола аст? (кӯдак)",
                                        "ru": "Сколько лет ее дочери? (ребенок)"
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
                "no": 1,
                "type": "numbers",
                "instruction": {
                        "uz": "Raqamlarni xitoy tilida yozing:",
                        "tj": "Рақамҳоро ба забони чинӣ нависед:",
                        "ru": "Напишите цифры на китайском языке:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "25",
                                        "tj": "25",
                                        "ru": "25"
                                },
                                "answer": "二十五",
                                "pinyin": "èrshíwǔ"
                        },
                        {
                                "prompt": {
                                        "uz": "38",
                                        "tj": "38",
                                        "ru": "38"
                                },
                                "answer": "三十八",
                                "pinyin": "sānshíbā"
                        },
                        {
                                "prompt": {
                                        "uz": "50",
                                        "tj": "50",
                                        "ru": "50"
                                },
                                "answer": "五十",
                                "pinyin": "wǔshí"
                        },
                        {
                                "prompt": {
                                        "uz": "99",
                                        "tj": "99",
                                        "ru": "99"
                                },
                                "answer": "九十九",
                                "pinyin": "jiǔshíjiǔ"
                        },
                        {
                                "prompt": {
                                        "uz": "100",
                                        "tj": "100",
                                        "ru": "100"
                                },
                                "answer": "一百",
                                "pinyin": "yìbǎi"
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
                                        "uz": "Oilangizda nechta odam bor?",
                                        "tj": "Дар оилаи шумо чанд нафар ҳастанд?",
                                        "ru": "Сколько человек в вашей семье?"
                                },
                                "answer": "你家有几口人？",
                                "pinyin": "Nǐ jiā yǒu jǐ kǒu rén?"
                        },
                        {
                                "prompt": {
                                        "uz": "Oilamizda besh kishi bor.",
                                        "tj": "Дар оилаи мо панҷ нафар ҳастем.",
                                        "ru": "В нашей семье пять человек."
                                },
                                "answer": "我家有五口人。",
                                "pinyin": "Wǒ jiā yǒu wǔ kǒu rén."
                        },
                        {
                                "prompt": {
                                        "uz": "Yoshingiz nechida?",
                                        "tj": "Ту чанд сола?",
                                        "ru": "Сколько тебе лет?"
                                },
                                "answer": "你多大了？",
                                "pinyin": "Nǐ duō dà le?"
                        },
                        {
                                "prompt": {
                                        "uz": "Bu yil u yigirma yoshda.",
                                        "tj": "Вай имсол бистсола шуд.",
                                        "ru": "В этом году ей исполнится двадцать лет."
                                },
                                "answer": "她今年二十岁了。",
                                "pinyin": "Tā jīnnián èrshí suì le."
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
                                "prompt": "你家___几口人？",
                                "answer": "有",
                                "pinyin": "yǒu"
                        },
                        {
                                "prompt": "李老师今年五十___了。",
                                "answer": "岁",
                                "pinyin": "suì"
                        },
                        {
                                "prompt": "你女儿___岁了？",
                                "answer": "几",
                                "pinyin": "jǐ"
                        },
                        {
                                "prompt": "李老师___大了？",
                                "answer": "多",
                                "pinyin": "duō"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "二十五",
                        "三十八",
                        "五十",
                        "九十九",
                        "一百"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "你家有几口人？",
                        "我家有五口人。",
                        "你多大了？",
                        "她今年二十岁了。"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "有",
                        "岁",
                        "几",
                        "多"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "O'z oilangiz haqida 3-4 ta jumla yozing:",
                        "tj": "Дар бораи оилаи худ 3-4 ҷумла нависед:",
                        "ru": "Напишите 3-4 предложения о своей семье:"
                },
                "template": "我家有___口人。我今年___岁了。我___有女儿/儿子。",
                "words": [
                        "家",
                        "有",
                        "口",
                        "岁",
                        "今年",
                        "了"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Raqamlarni xitoy tilida yozing:",
                        "tj": "Рақамҳоро ба забони чинӣ нависед:",
                        "ru": "Напишите цифры на китайском языке:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "17",
                                        "tj": "17",
                                        "ru": "17"
                                },
                                "answer": "十七"
                        },
                        {
                                "prompt": {
                                        "uz": "43",
                                        "tj": "43",
                                        "ru": "43"
                                },
                                "answer": "四十三"
                        },
                        {
                                "prompt": {
                                        "uz": "68",
                                        "tj": "68",
                                        "ru": "68"
                                },
                                "answer": "六十八"
                        },
                        {
                                "prompt": {
                                        "uz": "100",
                                        "tj": "100",
                                        "ru": "100"
                                },
                                "answer": "一百"
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
