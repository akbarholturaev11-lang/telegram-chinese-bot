import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 8,
    "lesson_code": "HSK1-L08",
    "title": "我想喝茶",
    "goal": {
        "uz": "Istaklarni ifodalash, narxlarni so'rash va so'zlarni o'lchashni o'rganish",
        "tj": "Изҳори хоҳишҳо, пурсидани нархҳо ва омӯхтани калимаҳо",
        "ru": "Выражение желаний, запрос цен и изучение мерных слов."
    },
    "intro_text": {
        "uz": "Sakkizinchi darsda siz màn modal fe'li yordamida istaklarni ifodalashni, narxlarni so'rashni (kínìnín?) va o'lchov so'zlaridan foydalanishni o'rganasiz. 15 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси ҳаштум шумо бо истифода аз феъли модалии 想 баён кардани хоҳишҳо, пурсидани нархҳо (多少钱?) ва калимаҳои андозагирии 个/口ро меомӯзед. 15 калимаи нав, 3 муколама.",
        "ru": "На восьмом уроке вы научитесь выражать пожелания с помощью модального глагола 想, спрашивать цену (多少钱?) и использовать измерительные слова 个/口. 15 новых слов, 3 диалога."
    },

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "想",
                "pinyin": "xiǎng",
                "pos": "mod.",
                "meaning": {
                        "uz": "istamoq, xohlamoq",
                        "tj": "хоҳиш кардан, хоҳиш кардан",
                        "ru": "хотеть, желать"
                }
        },
        {
                "no": 2,
                "zh": "喝",
                "pinyin": "hē",
                "pos": "v.",
                "meaning": {
                        "uz": "ichish",
                        "tj": "нӯшидан",
                        "ru": "пить"
                }
        },
        {
                "no": 3,
                "zh": "茶",
                "pinyin": "chá",
                "pos": "n.",
                "meaning": {
                        "uz": "choy",
                        "tj": "чой",
                        "ru": "чай"
                }
        },
        {
                "no": 4,
                "zh": "吃",
                "pinyin": "chī",
                "pos": "v.",
                "meaning": {
                        "uz": "yeyish",
                        "tj": "хӯрдан",
                        "ru": "есть"
                }
        },
        {
                "no": 5,
                "zh": "米饭",
                "pinyin": "mǐfàn",
                "pos": "n.",
                "meaning": {
                        "uz": "guruch, pishirilgan guruch",
                        "tj": "биринҷ, биринҷ пухта",
                        "ru": "рис, вареный рис"
                }
        },
        {
                "no": 6,
                "zh": "下午",
                "pinyin": "xiàwǔ",
                "pos": "n.",
                "meaning": {
                        "uz": "tushdan keyin",
                        "tj": "нисфирӯзӣ",
                        "ru": "полдень"
                }
        },
        {
                "no": 7,
                "zh": "商店",
                "pinyin": "shāngdiàn",
                "pos": "n.",
                "meaning": {
                        "uz": "do'kon, do'kon",
                        "tj": "мағоза, мағоза",
                        "ru": "магазин, магазин"
                }
        },
        {
                "no": 8,
                "zh": "买",
                "pinyin": "mǎi",
                "pos": "v.",
                "meaning": {
                        "uz": "sotib olish",
                        "tj": "харидан",
                        "ru": "купить"
                }
        },
        {
                "no": 9,
                "zh": "个",
                "pinyin": "gè",
                "pos": "m.",
                "meaning": {
                        "uz": "umumiy o'lchov so'zi (parcha/birlik)",
                        "tj": "калимаи ченаки умумӣ (порча/воҳид)",
                        "ru": "общее измерительное слово (шт./единица)"
                }
        },
        {
                "no": 10,
                "zh": "杯子",
                "pinyin": "bēizi",
                "pos": "n.",
                "meaning": {
                        "uz": "stakan, stakan",
                        "tj": "пиёла, шиша",
                        "ru": "чашка, стакан"
                }
        },
        {
                "no": 11,
                "zh": "这",
                "pinyin": "zhè",
                "pos": "pron.",
                "meaning": {
                        "uz": "bu (ko'rsatuvchi olmosh)",
                        "tj": "ин (ҷонишини намоишӣ)",
                        "ru": "это (указательное местоимение)"
                }
        },
        {
                "no": 12,
                "zh": "多少",
                "pinyin": "duōshao",
                "pos": "pron.",
                "meaning": {
                        "uz": "qancha, qancha (10+)",
                        "tj": "чанд, чанд (10+)",
                        "ru": "сколько, сколько (10+)"
                }
        },
        {
                "no": 13,
                "zh": "钱",
                "pinyin": "qián",
                "pos": "n.",
                "meaning": {
                        "uz": "pul",
                        "tj": "пул",
                        "ru": "деньги"
                }
        },
        {
                "no": 14,
                "zh": "块",
                "pinyin": "kuài",
                "pos": "m.",
                "meaning": {
                        "uz": "yuan (so'zlashuv tilida)",
                        "tj": "юан (забони гуфтугӯӣ)",
                        "ru": "юань (разговорный)"
                }
        },
        {
                "no": 15,
                "zh": "那",
                "pinyin": "nà",
                "pos": "pron.",
                "meaning": {
                        "uz": "bu (ko'rsatuvchi olmosh)",
                        "tj": "ки (ҷонишини намоишӣ)",
                        "ru": "что (указательное местоимение)"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Restoranда — nima ichish/yeyish",
                        "tj": "Дар тарабхона - чӣ бинӯшед/хӯред",
                        "ru": "В ресторане - что пить/есть"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你想喝什么？",
                                "pinyin": "Nǐ xiǎng hē shénme?",
                                "translation": {
                                        "uz": "Ichishga nima xohlaysiz?",
                                        "tj": "Шумо чӣ нӯшидан мехоҳед?",
                                        "ru": "Что бы вы хотели выпить?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我想喝茶。",
                                "pinyin": "Wǒ xiǎng hē chá.",
                                "translation": {
                                        "uz": "Men choy ichmoqchiman.",
                                        "tj": "Ман чой нӯшидан мехоҳам.",
                                        "ru": "Я бы хотел выпить чаю."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你想吃什么？",
                                "pinyin": "Nǐ xiǎng chī shénme?",
                                "translation": {
                                        "uz": "Nima yeyishni xohlaysiz?",
                                        "tj": "Шумо чӣ хӯрдан мехоҳед?",
                                        "ru": "Что бы вы хотели съесть?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我想吃米饭。",
                                "pinyin": "Wǒ xiǎng chī mǐfàn.",
                                "translation": {
                                        "uz": "Men guruch iste'mol qilmoqchiman.",
                                        "tj": "Ман мехоҳам биринҷ бихӯрам.",
                                        "ru": "Я хотел бы съесть рис."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Mehmonxonada — tushdan keyingi reja",
                        "tj": "Нақшаи нисфирӯзӣ дар меҳмонхона",
                        "ru": "План дня в отеле"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "下午你想做什么？",
                                "pinyin": "Xiàwǔ nǐ xiǎng zuò shénme?",
                                "translation": {
                                        "uz": "Bugun tushdan keyin nima qilishni xohlaysiz?",
                                        "tj": "Шумо ин нисфирӯзӣ чӣ кор кардан мехоҳед?",
                                        "ru": "Что ты хочешь сделать сегодня днем?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "下午我想去商店。",
                                "pinyin": "Xiàwǔ wǒ xiǎng qù shāngdiàn.",
                                "translation": {
                                        "uz": "Men bugun tushdan keyin do'konga bormoqchiman.",
                                        "tj": "Ман нисфирӯзӣ мехоҳам ба мағоза равам.",
                                        "ru": "Я хочу пойти в магазин сегодня днем."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你想买什么？",
                                "pinyin": "Nǐ xiǎng mǎi shénme?",
                                "translation": {
                                        "uz": "Nima sotib olmoqchisiz?",
                                        "tj": "Шумо чӣ харидан мехоҳед?",
                                        "ru": "Что вы хотите купить?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我想买一个杯子。",
                                "pinyin": "Wǒ xiǎng mǎi yī gè bēizi.",
                                "translation": {
                                        "uz": "Men bitta stakan sotib olmoqchiman.",
                                        "tj": "Ман мехоҳам як пиёла харам.",
                                        "ru": "Я хочу купить одну чашку."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Do'konda — narx so'rash",
                        "tj": "Дар магазин — нархро пурсед",
                        "ru": "В магазине - спросите цену"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你好！这个杯子多少钱？",
                                "pinyin": "Nǐ hǎo! Zhège bēizi duōshao qián?",
                                "translation": {
                                        "uz": "Salom! Bu kubok qancha turadi?",
                                        "tj": "Салом! Ин коса чанд пул аст?",
                                        "ru": "Привет! Сколько стоит эта чашка?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "28块。",
                                "pinyin": "Èrshíbā kuài.",
                                "translation": {
                                        "uz": "28 yuan.",
                                        "tj": "28 юан.",
                                        "ru": "28 юаней."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "那个杯子多少钱？",
                                "pinyin": "Nàge bēizi duōshao qián?",
                                "translation": {
                                        "uz": "Bu kubok qancha turadi?",
                                        "tj": "Ин коса чанд пул аст?",
                                        "ru": "Сколько стоит эта чашка?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "那个杯子18块钱。",
                                "pinyin": "Nàge bēizi shíbā kuài qián.",
                                "translation": {
                                        "uz": "Bu kubok 18 yuan.",
                                        "tj": "Ин коса 18 юан аст.",
                                        "ru": "Эта чашка стоит 18 юаней."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "能愿动词 想 — Modal fe'l 想",
                "explanation": {
                        "rule_uz": "xiǎng (xiǎng) — istak yoki rejani ifodalaydi.\nTuzilishi: Mavzu + mí + Fe'l + Ob'ekt\n\nTasdiqlovchi: chàngàngìnīlí— Men choy ichmoqchiman.\nSavol: mīngīngīnī？— Nima qilishni xohlaysiz?\n\nmí vs mí:\nchàngǎngǎngyǎk— Men xitoy tilida gaplashmoqchiman (istak).\nlíngīngīngīyī - Men xitoy tilida gaplasha olaman (qobiliyat).",
                        "rule_tj": "想(xiǎng) — изҳори хоҳиш ё нақша.\nСохтор: Мавзӯъ + 想 + Феъл + Объект\n\nТасдиқ: 我想喝茶。— Ман чой нӯшидан мехоҳам.\nСавол: 你想做什么？— Шумо чӣ кор кардан мехоҳед?\n\n想 против 会:\n我想说汉语。— Ман мехоҳам бо забони чинӣ ҳарф занам (хоҳиш).\n我会说汉语。— Ман бо забони чинӣ ҳарф зада метавонам (қобилият).",
                        "rule_ru": "想(xiώng) — выражает желание или план.\nСтруктура: Подлежащее + 想 + Глагол + Объект.\n\nУтвердительный вариант: 我想喝茶。 — Я хочу пить чай.\nВопрос: 你想做什么？ — Что вы хотите сделать?\n\n想 против 会:\n我想说汉语。 — Я хочу говорить по-китайски (желание).\n我会说汉语。 — Я говорю по-китайски (способность)."
                },
                "examples": [
                        {
                                "zh": "我想喝茶。",
                                "pinyin": "Wǒ xiǎng hē chá.",
                                "meaning": {
                                        "uz": "Men choy ichmoqchiman.",
                                        "tj": "Ман чой нӯшидан мехоҳам.",
                                        "ru": "Я хочу пить чай."
                                }
                        },
                        {
                                "zh": "她想去学校看书。",
                                "pinyin": "Tā xiǎng qù xuéxiào kàn shū.",
                                "meaning": {
                                        "uz": "U o'qish uchun maktabga bormoqchi.",
                                        "tj": "Вай мехоҳад, ки ба мактаб равад, то хонад.",
                                        "ru": "Она хочет пойти в школу, чтобы читать."
                                }
                        },
                        {
                                "zh": "你想买什么？",
                                "pinyin": "Nǐ xiǎng mǎi shénme?",
                                "meaning": {
                                        "uz": "Nima sotib olmoqchisiz?",
                                        "tj": "Шумо чӣ харидан мехоҳед?",
                                        "ru": "Что вы хотите купить?"
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "多少 — Qancha so'rog'i (10+)",
                "explanation": {
                        "rule_uz": "dàní(duōshao) — 10 dan katta raqamlar uchun soʻroq soʻzi.\nEslatma: jǐ(jǐ) 10 gacha bo'lgan raqamlar uchun; dàní (duōshao) 10 dan yuqori raqamlar uchun.\n\nSo'raladigan narx: ……kàngàng?\nlíngíngìnīngīng- Bu kubok qancha turadi?\n\nSo'raladigan miqdor:\nshnchnghìnīngīngānīn？ - Maktabingizda nechta o'quvchi bor?\nshíngìnìnīng？— Qancha pulingiz bor?",
                        "rule_tj": "多少(duōshao) — калимаи саволӣ барои ададҳои аз 10 зиёд.\nЭзоҳ: 几(jǐ) барои ададҳои то 10 аст; 多少(duōshao) барои рақамҳои аз 10 боло аст.\n\nНархи дархост: ……多少钱？\n这个杯子多少钱？— Ин пиёла чанд пул аст?\n\nМиқдори дархост:\n你们学校有多少学生？— Дар мактаби шумо чанд нафар хонанда таҳсил мекунад?\n你有多少钱？— Шумо чанд пул доред?",
                        "rule_ru": "多少(дуошао) — вопросительное слово для чисел больше 10.\nПримечание. 几(jϐ) — для чисел до 10; 多少(дуошао) — для чисел больше 10.\n\nЗапрашиваемая цена: ……多少钱？\n这个杯子多少钱？ — Сколько стоит эта чашка?\n\nЗапрашиваемое количество:\n你们学校有多少学生？ — Сколько учеников учится в вашей школе?\n你有多少钱？ — Сколько у тебя денег?"
                },
                "examples": [
                        {
                                "zh": "这个杯子多少钱？",
                                "pinyin": "Zhège bēizi duōshao qián?",
                                "meaning": {
                                        "uz": "Bu kubok qancha turadi?",
                                        "tj": "Ин коса чанд пул аст?",
                                        "ru": "Сколько стоит эта чашка?"
                                }
                        },
                        {
                                "zh": "你家有多少口人？",
                                "pinyin": "Nǐ jiā yǒu duōshao kǒu rén?",
                                "meaning": {
                                        "uz": "Oilangizda nechta odam bor?",
                                        "tj": "Дар оилаи шумо чанд нафар ҳастанд?",
                                        "ru": "Сколько человек в вашей семье?"
                                }
                        },
                        {
                                "zh": "一个苹果多少钱？",
                                "pinyin": "Yī gè píngguǒ duōshao qián?",
                                "meaning": {
                                        "uz": "Bitta olma qancha turadi?",
                                        "tj": "Як себ чанд пул аст?",
                                        "ru": "Сколько стоит одно яблоко?"
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "量词 个/口 — O'lchov so'zlar",
                "explanation": {
                        "rule_uz": "Xitoy tilida raqam va ot o'rtasida o'lchov so'zi talab qilinadi.\n\ny(gè) — eng umumiy oʻlchov soʻzi:\nshīdīngīngī - bir piyola\nshīngīngīn — uchta talaba\nshīngīngī - ikkita o'qituvchi\n\nkǒu (kǒu) - oila a'zolari uchun ishlatiladi:\nchàngān — uch kishilik oila\nlínín — olti kishilik oila",
                        "rule_tj": "Дар чинӣ калимаи андозагирӣ дар байни адад ва исм талаб карда мешавад.\n\n个(gè) — вожаи ченаки умумӣ:\n一个杯子 — як пиёла\n三个学生 — се нафар студентон\n两个老师 — ду муаллим\n\n口(kǒu) — барои аъзоёни оила истифода мешавад:\n三口人 — оилаи се нафар\n六口人 — оилаи шаш нафар",
                        "rule_ru": "В китайском языке между числом и существительным требуется мерное слово.\n\n个(гэ) — самое общее мерное слово:\n一个杯子 — одна чашка\n三个学生 — трое учеников\n两个老师 — два учителя\n\n口(kǒu) — используется для членов семьи:\n三口人 — семья из трёх человек\n六口人 — семья из шести человек."
                },
                "examples": [
                        {
                                "zh": "一个杯子",
                                "pinyin": "yī gè bēizi",
                                "meaning": {
                                        "uz": "bir stakan",
                                        "tj": "як пиёла",
                                        "ru": "одна чашка"
                                }
                        },
                        {
                                "zh": "五个学生",
                                "pinyin": "wǔ gè xuésheng",
                                "meaning": {
                                        "uz": "besh talaba",
                                        "tj": "панҷ донишҷӯ",
                                        "ru": "пять студентов"
                                }
                        },
                        {
                                "zh": "三口人",
                                "pinyin": "sān kǒu rén",
                                "meaning": {
                                        "uz": "uch kishilik oila",
                                        "tj": "оилаи се нафар",
                                        "ru": "семья из трех человек"
                                }
                        }
                ]
        },
        {
                "no": 4,
                "title_zh": "钱数的表达 — Pul miqdori",
                "explanation": {
                        "rule_uz": "Xitoy valyutasi: yīngī (Yenminbi, RMB)\nRasmiy: yuan (yuan)\nSo'zlashuv tili: qài (kuài)\n\nMisol:\n28kā = 28ān - 28 yuan\n18gín - 18 yuan (og'zaki shakl)\n\nlíngíngìnīngīng- Bu kubok qancha turadi?\n28kān - 28 yuan.",
                        "rule_tj": "Пули Чин: 人民币 (Ренминби, RMB)\nРасмӣ: 元 (юань)\nЗабони гуфтугӯӣ: 块(kuài)\n\nМисол:\n28块 = 28元 — 28 юан\n18块钱 — 18 юан (шакли гуфторӣ)\n\n这个杯子多少钱？— Ин пиёла чанд пул аст?\n28块。 — 28 юан.",
                        "rule_ru": "Китайская валюта: 人民币 (юань, юань).\nФормальный формат: 元(юань)\nРазговорный: 块(куай)\n\nПример:\n28块 = 28元 — 28 юаней\n18块钱 — 18 юаней (разговорная форма)\n\n这个杯子多少钱？ — Сколько стоит эта чашка?\n28块。 — 28 юаней."
                },
                "examples": [
                        {
                                "zh": "这个多少钱？",
                                "pinyin": "Zhège duōshao qián?",
                                "meaning": {
                                        "uz": "Bu qancha turadi?",
                                        "tj": "Ин чанд пул?",
                                        "ru": "Сколько это стоит?"
                                }
                        },
                        {
                                "zh": "28块钱。",
                                "pinyin": "Èrshíbā kuài qián.",
                                "meaning": {
                                        "uz": "28 yuan.",
                                        "tj": "28 юан.",
                                        "ru": "28 юаней."
                                }
                        },
                        {
                                "zh": "一百块。",
                                "pinyin": "Yìbǎi kuài.",
                                "meaning": {
                                        "uz": "100 yuan.",
                                        "tj": "100 юан.",
                                        "ru": "100 юаней."
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
                                        "uz": "Ichishga nima xohlaysiz?",
                                        "tj": "Шумо чӣ нӯшидан мехоҳед?",
                                        "ru": "Что бы вы хотели выпить?"
                                },
                                "answer": "你想喝什么？",
                                "pinyin": "Nǐ xiǎng hē shénme?"
                        },
                        {
                                "prompt": {
                                        "uz": "Men choy ichmoqchiman.",
                                        "tj": "Ман чой нӯшидан мехоҳам.",
                                        "ru": "Я бы хотел выпить чаю."
                                },
                                "answer": "我想喝茶。",
                                "pinyin": "Wǒ xiǎng hē chá."
                        },
                        {
                                "prompt": {
                                        "uz": "Bu kubok qancha turadi?",
                                        "tj": "Ин коса чанд пул аст?",
                                        "ru": "Сколько стоит эта чашка?"
                                },
                                "answer": "这个杯子多少钱？",
                                "pinyin": "Zhège bēizi duōshao qián?"
                        },
                        {
                                "prompt": {
                                        "uz": "28 yuan.",
                                        "tj": "28 юан.",
                                        "ru": "28 юаней."
                                },
                                "answer": "28块钱。",
                                "pinyin": "Èrshíbā kuài qián."
                        },
                        {
                                "prompt": {
                                        "uz": "Men bugun tushdan keyin do'konga bormoqchiman.",
                                        "tj": "Ман нисфирӯзӣ мехоҳам ба мағоза равам.",
                                        "ru": "Я хочу пойти в магазин сегодня днем."
                                },
                                "answer": "下午我想去商店。",
                                "pinyin": "Xiàwǔ wǒ xiǎng qù shāngdiàn."
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
                                "prompt": "你___喝什么？",
                                "answer": "想",
                                "pinyin": "xiǎng"
                        },
                        {
                                "prompt": "这___杯子多少钱？",
                                "answer": "个",
                                "pinyin": "gè"
                        },
                        {
                                "prompt": "___个杯子18块___。",
                                "answer": "那/钱",
                                "pinyin": "nà/qián"
                        },
                        {
                                "prompt": "我想买___个杯子。",
                                "answer": "一",
                                "pinyin": "yī"
                        }
                ]
        },
        {
                "no": 3,
                "type": "price_dialogue",
                "instruction": {
                        "uz": "Narxlar haqida so'rang va javob bering:",
                        "tj": "Дар бораи нархҳо пурсед ва ҷавоб диҳед:",
                        "ru": "Спросите и ответьте о ценах:"
                },
                "items": [
                        {
                                "prompt": "苹果(apple) — 5块/个",
                                "question": "这个苹果多少钱？",
                                "answer": "五块钱。"
                        },
                        {
                                "prompt": "书(book) — 35块",
                                "question": "这本书多少钱？",
                                "answer": "三十五块钱。"
                        },
                        {
                                "prompt": "茶(tea) — 18块",
                                "question": "这个茶多少钱？",
                                "answer": "十八块钱。"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "你想喝什么？",
                        "我想喝茶。",
                        "这个杯子多少钱？",
                        "28块钱。",
                        "下午我想去商店。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "想",
                        "个",
                        "那/钱",
                        "一"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "五块钱。",
                        "三十五块钱。",
                        "十八块钱。"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Bugungi kun uchun rejalaringizni yozing (máng, 3–4 jumladan foydalanib):",
                        "tj": "Нақшаҳои имрӯзаи худро нависед (бо истифода аз 想, 3–4 ҷумла):",
                        "ru": "Напишите свои планы на сегодня (используя 想, 3–4 предложения):"
                },
                "template": "今天下午我想___。我想___。我想买___。",
                "words": [
                        "想",
                        "喝",
                        "吃",
                        "去",
                        "买",
                        "茶",
                        "米饭",
                        "杯子"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Narxlar haqida so'ragan do'kon dialogini yozing (4 qator):",
                        "tj": "Муколамаи мағозаро дар бораи нархҳо нависед (4 сатр):",
                        "ru": "Напишите диалог магазина с вопросом о ценах (4 строки):"
                },
                "example": "A: 你好！___多少钱？\nB: ___块。\nA: ___多少钱？\nB: ___块钱。"
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
