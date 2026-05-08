import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 14,
    "lesson_code": "HSK1-L14",
    "title": "她买了不少衣服",
    "goal": json.dumps({
        "uz": "Tugallangan harakatlar uchun zarracha z, vaqt belgisi sifatida z va qo‘shimchasi",
        "tj": "Зарра 了 барои амалҳои анҷомшуда, 后 ҳамчун аломати вақт ва зарфи 都",
        "ru": "Частица 了 обозначает завершенные действия, 后 как маркер времени и наречие 都."
}, ensure_ascii=False),
    "intro_text": json.dumps({
        "uz": "O'n to'rtinchi darsda siz tugallangan harakatni shn bilan, kelajak vaqtni xi bilan ifodalashni o'rganasiz va hun qo'shimchasidan foydalanasiz. 16 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси чордаҳум шумо ифода кардани амалҳои анҷомшударо бо 了, вақти ояндаро бо 后 меомӯзед ва зарфи 都ро истифода баред. 16 калимаи нав, 3 муколама.",
        "ru": "На четырнадцатом уроке вы научитесь выражать завершенные действия с помощью 了, будущее время с помощью 后 и использовать наречие 都. 16 новых слов, 3 диалога."
}, ensure_ascii=False),

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "东西",
                "pinyin": "dōngxi",
                "pos": "n.",
                "meaning": {
                        "uz": "narsa, buyum",
                        "tj": "ашё, ашё",
                        "ru": "вещь, предмет"
                }
        },
        {
                "no": 2,
                "zh": "一点儿",
                "pinyin": "yīdiǎnr",
                "pos": "num.",
                "meaning": {
                        "uz": "bir oz, bir oz",
                        "tj": "андаке, андаке",
                        "ru": "немного, немного"
                }
        },
        {
                "no": 3,
                "zh": "苹果",
                "pinyin": "píngguǒ",
                "pos": "n.",
                "meaning": {
                        "uz": "olma",
                        "tj": "себ",
                        "ru": "яблоко"
                }
        },
        {
                "no": 4,
                "zh": "看见",
                "pinyin": "kànjiàn",
                "pos": "v.",
                "meaning": {
                        "uz": "ko‘rmoq, ko‘rmoq",
                        "tj": "дидан, дидан",
                        "ru": "видеть, замечать"
                }
        },
        {
                "no": 5,
                "zh": "先生",
                "pinyin": "xiānsheng",
                "pos": "n.",
                "meaning": {
                        "uz": "Janob, ser",
                        "tj": "ҷаноби ҷаноб",
                        "ru": "Господин, сэр"
                }
        },
        {
                "no": 6,
                "zh": "开",
                "pinyin": "kāi",
                "pos": "v.",
                "meaning": {
                        "uz": "ochmoq, haydamoq (transport vositasi)",
                        "tj": "кушодан, рондан (нақлиёт)",
                        "ru": "открывать, водить (транспортное средство)"
                }
        },
        {
                "no": 7,
                "zh": "车",
                "pinyin": "chē",
                "pos": "n.",
                "meaning": {
                        "uz": "mashina, avtomobil",
                        "tj": "мошин, мошин",
                        "ru": "машина, транспортное средство"
                }
        },
        {
                "no": 8,
                "zh": "回来",
                "pinyin": "huílai",
                "pos": "v.",
                "meaning": {
                        "uz": "qaytib kelmoq, qaytmoq",
                        "tj": "баргаштан, баргаштан",
                        "ru": "вернуться, вернуться"
                }
        },
        {
                "no": 9,
                "zh": "分钟",
                "pinyin": "fēnzhōng",
                "pos": "n.",
                "meaning": {
                        "uz": "daqiqa (vaqt birligi)",
                        "tj": "дақиқа (воҳиди вақт)",
                        "ru": "минута (единица времени)"
                }
        },
        {
                "no": 10,
                "zh": "后",
                "pinyin": "hòu",
                "pos": "n.",
                "meaning": {
                        "uz": "keyin, keyin",
                        "tj": "баъд, баъд",
                        "ru": "после, позже"
                }
        },
        {
                "no": 11,
                "zh": "衣服",
                "pinyin": "yīfu",
                "pos": "n.",
                "meaning": {
                        "uz": "kiyim, kiyim",
                        "tj": "либос, либос",
                        "ru": "одежда, одежда"
                }
        },
        {
                "no": 12,
                "zh": "漂亮",
                "pinyin": "piàoliang",
                "pos": "adj.",
                "meaning": {
                        "uz": "chiroyli, chiroyli",
                        "tj": "зебо, зебо",
                        "ru": "красивый, красивый"
                }
        },
        {
                "no": 13,
                "zh": "啊",
                "pinyin": "a",
                "pos": "part.",
                "meaning": {
                        "uz": "ha, ha (undov zarrasi)",
                        "tj": "ҳа, ҳа (заррачаи нидоӣ)",
                        "ru": "ах, да (восклицательная частица)"
                }
        },
        {
                "no": 14,
                "zh": "少",
                "pinyin": "shǎo",
                "pos": "adj.",
                "meaning": {
                        "uz": "oz, oz",
                        "tj": "кам, кам",
                        "ru": "мало, мало"
                }
        },
        {
                "no": 15,
                "zh": "这些",
                "pinyin": "zhèxiē",
                "pos": "pron.",
                "meaning": {
                        "uz": "bular, bu narsalar",
                        "tj": "инҳо, ин чизҳо",
                        "ru": "эти, эти вещи"
                }
        },
        {
                "no": 16,
                "zh": "都",
                "pinyin": "dōu",
                "pos": "adv.",
                "meaning": {
                        "uz": "hammasi, ikkalasi",
                        "tj": "ҳама, ҳарду",
                        "ru": "все, оба"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Yotoqxonada — kecha nima qilding",
                        "tj": "Дар хонаи хоб - шумо шаби гузашта чӣ кор кардед?",
                        "ru": "В спальне, что ты делал вчера вечером?"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "昨天上午你去哪儿了？",
                                "pinyin": "Zuótiān shàngwǔ nǐ qù nǎr le?",
                                "translation": {
                                        "uz": "Kecha ertalab qaerga bordingiz?",
                                        "tj": "Субҳи дирӯз ба куҷо рафтӣ?",
                                        "ru": "Куда ты ходил вчера утром?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我去商店买东西了。",
                                "pinyin": "Wǒ qù shāngdiàn mǎi dōngxi le.",
                                "translation": {
                                        "uz": "Men narsalar sotib olish uchun do'konga bordim.",
                                        "tj": "Ман барои харидани чизҳо ба мағоза рафтам.",
                                        "ru": "Я пошел в магазин, чтобы купить вещи."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你买什么了？",
                                "pinyin": "Nǐ mǎi shénme le?",
                                "translation": {
                                        "uz": "Nima sotib oldingiz?",
                                        "tj": "Шумо чӣ харидед?",
                                        "ru": "Что ты купил?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我买了一点儿苹果。",
                                "pinyin": "Wǒ mǎile yīdiǎnr píngguǒ.",
                                "translation": {
                                        "uz": "Men bir nechta olma sotib oldim.",
                                        "tj": "Ман чанд себ харидаам.",
                                        "ru": "Я купил несколько яблок."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Kompaniyada — Zhang janobni ko'rdingizmi",
                        "tj": "Оё шумо ҷаноби Чжанро дар ширкат дидаед?",
                        "ru": "Вы видели г-на Чжана в компании?"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你看见张先生了吗？",
                                "pinyin": "Nǐ kànjiàn Zhāng xiānsheng le ma?",
                                "translation": {
                                        "uz": "Janob Chjanni ko'rdingizmi?",
                                        "tj": "Оё шумо ҷаноби Чжанро дидед?",
                                        "ru": "Вы видели г-на Чжана?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "看见了，他去学开车了。",
                                "pinyin": "Kànjiàn le, tā qù xué kāi chē le.",
                                "translation": {
                                        "uz": "Ha, men qildim; u haydashni o'rganish uchun ketdi.",
                                        "tj": "Бале ман кардам; барои омух-тани ​​ронандагй рафт.",
                                        "ru": "Да, я это сделал; он пошел учиться водить машину."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "他什么时候能回来？",
                                "pinyin": "Tā shénme shíhou néng huílai?",
                                "translation": {
                                        "uz": "U qachon qaytib kelishi mumkin?",
                                        "tj": "Вай кай метавонад баргардад?",
                                        "ru": "Когда он сможет вернуться?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "40分钟后回来。",
                                "pinyin": "Sìshí fēnzhōng hòu huílai.",
                                "translation": {
                                        "uz": "U 40 daqiqadan keyin qaytib keladi.",
                                        "tj": "Вай пас аз 40 дақиқа бармегардад.",
                                        "ru": "Он вернется через 40 минут."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Do'kon oldida — kiyimlar",
                        "tj": "Дар назди магазин — либос",
                        "ru": "Перед магазином - одежда"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "王方的衣服太漂亮了！",
                                "pinyin": "Wáng Fāng de yīfu tài piàoliang le!",
                                "translation": {
                                        "uz": "Vang Fangning kiyimlari juda chiroyli!",
                                        "tj": "Либосҳои Ван Фанг хеле зебоанд!",
                                        "ru": "Одежда Ван Фана такая красивая!"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "是啊，她买了不少衣服。",
                                "pinyin": "Shì a, tā mǎile bùshǎo yīfu.",
                                "translation": {
                                        "uz": "Ha, haqiqatan ham, u juda ko'p kiyim sotib oldi.",
                                        "tj": "Бале, вай хеле зиёд либос харид.",
                                        "ru": "Да, действительно, она купила довольно много одежды."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你买什么了？",
                                "pinyin": "Nǐ mǎi shénme le?",
                                "translation": {
                                        "uz": "Nima sotib oldingiz?",
                                        "tj": "Шумо чӣ харидед?",
                                        "ru": "Что ты купил?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我没买，这些都是王方的东西。",
                                "pinyin": "Wǒ méi mǎi, zhèxiē dōu shì Wáng Fāng de dōngxi.",
                                "translation": {
                                        "uz": "Men hech narsa sotib olmadim; bularning barchasi Vang Fangning narsalari.",
                                        "tj": "Ман чизе нахаридаам; ҳамаи ин чизҳои Ван Фанг мебошанд.",
                                        "ru": "Я ничего не покупал; все это вещи Ван Фана."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "了 — Harakat tugallangani",
                "explanation": {
                        "rule_uz": "Gap oxiridagi (le) ish-harakat sodir bo‘lgan yoki tugallanganligini bildiradi.\n\nTuzilishi:\nMavzu + fe'l + shn (jumla oxiri)\nMavzu + Fe'l + shn + Son/Sifat + Ism\n\nMisol:\nchànghìnẗyẆ。— Men do'konga bordim.\nmìnìnìnìnínì- U juda ko'p kiyim sotib oldi.\nlíngìnìnínínín— Men bir nechta olma sotib oldim.\n\nInkor: mí + fe'l (mán tushirilgan)\nmìnìnìnì。— Men hech narsa sotib olmadim.\nlínìnhìnẗ。— U doʻkonga bormadi.",
                        "rule_tj": "了(le) дар охири љумла нишон медињад, ки амале ба вуљуд омадааст ё ба анљом расидааст.\n\nСохтор:\nМавзӯъ + Феъл + 了 (охири ҷумла)\nМавзӯъ + Феъл + 了 + Шумора/Сиф + Исм\n\nМисол:\n我去商店了。— Ман ба мағоза рафтам.\n她买了不少衣服。— Вай либосҳои зиёде харид.\n我买了一点儿苹果。— Ман чанд себ харидаам.\n\nИнкор: 没 + Феъл (了 партофта мешавад)\n我没买。— Ман чизе нахаридаам.\n她没去商店。— Вай ба мағоза нарафт.",
                        "rule_ru": "了(le) в конце предложения указывает на то, что действие произошло или завершилось.\n\nСтруктура:\nПодлежащее + глагол + 了 (конец предложения)\nПодлежащее + глагол + 了 + число/прилагательное + существительное\n\nПример:\n我去商店了。 — Я пошел в магазин.\n她买了不少衣服。 — Она купила довольно много одежды.\n我买了一点儿苹果。 — Я купил несколько яблок.\n\nОтрицание: 没 + глагол (了 опускается)\n我没买。 — Я ничего не покупал.\n她没去商店。 — Она не пошла в магазин."
                },
                "examples": [
                        {
                                "zh": "我去商店了。",
                                "pinyin": "Wǒ qù shāngdiàn le.",
                                "meaning": {
                                        "uz": "Men do'konga bordim.",
                                        "tj": "Ман ба мағоза рафтам.",
                                        "ru": "Я пошел в магазин."
                                }
                        },
                        {
                                "zh": "她买了不少衣服。",
                                "pinyin": "Tā mǎile bùshǎo yīfu.",
                                "meaning": {
                                        "uz": "U juda ko'p kiyim sotib oldi.",
                                        "tj": "Вай хеле зиёд либос харид.",
                                        "ru": "Она купила довольно много одежды."
                                }
                        },
                        {
                                "zh": "我没买。",
                                "pinyin": "Wǒ méi mǎi.",
                                "meaning": {
                                        "uz": "Men hech narsa sotib olmadim.",
                                        "tj": "Ман чизе нахаридам.",
                                        "ru": "Я ничего не купил."
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "名词 后 — 后 vaqt belgisi",
                "explanation": {
                        "rule_uz": "hòu (hòu) - ma'lum bir voqeadan keyin vaqtni bildiradi.\n\n40kíngy — 40 daqiqada\nshīngī - uch kundan keyin\nshīngīngīngī - bir hafta ichida\nmīngān - soat beshdan keyin\n\nMisol:\n40hínghìnì- U 40 daqiqada qaytadi.\nchàngàngàngìnìnīng — Men uch kundan keyin Pekinga boraman.",
                        "rule_tj": "后(hòu) — як лаҳзаи пас аз як ҳодисаи муайянро нишон медиҳад.\n\n40分钟后 — дар 40 дакика\n三天后 — дар се рӯз\n一个星期后 — дар як ҳафта\n五点后 — баъди соати панч\n\nМисол:\n40分钟后回来。— Вай пас аз 40 дақиқа бармегардад.\n三天后我去北京。— Ман баъд аз се рӯз ба Пекин меравам.",
                        "rule_ru": "后(хоу) — указывает момент времени после определенного события.\n\n40分钟后 — за 40 минут\n三天后 — через три дня\n一个星期后 — через неделю\n五点后 — после пяти часов\n\nПример:\n40分钟后回来。 — Он вернется через 40 минут.\n三天后我去北京。 — Через три дня я поеду в Пекин."
                },
                "examples": [
                        {
                                "zh": "40分钟后回来。",
                                "pinyin": "Sìshí fēnzhōng hòu huílai.",
                                "meaning": {
                                        "uz": "U 40 daqiqadan keyin qaytib keladi.",
                                        "tj": "Вай пас аз 40 дақиқа бармегардад.",
                                        "ru": "Он вернется через 40 минут."
                                }
                        },
                        {
                                "zh": "三天后见。",
                                "pinyin": "Sān tiān hòu jiàn.",
                                "meaning": {
                                        "uz": "Uch kundan keyin ko'rishguncha.",
                                        "tj": "Пас аз се рӯз вомехӯрем.",
                                        "ru": "Увидимся через три дня."
                                }
                        },
                        {
                                "zh": "八点后能来吗？",
                                "pinyin": "Bā diǎn hòu néng lái ma?",
                                "meaning": {
                                        "uz": "Soat sakkizdan keyin kela olasizmi?",
                                        "tj": "Оё шумо метавонед баъд аз соати ҳашт биёед?",
                                        "ru": "Ты можешь прийти после восьми?"
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "副词 都 — Ravish 都 (hammasi)",
                "explanation": {
                        "rule_uz": "dōu (dōu) - \"hammasi, har ikkisi, har biri\" degan ma'noni anglatadi.\nMuhim: ro'yxatdagi narsalar yán dan oldin keladi.\n\nMisol:\nlīngīngīngīngīngīngīngīng- Bularning barchasi Vang Fangning narsalari.\nchàngìnìnìnìnīng。— Biz hammamiz xitoymiz.\nchàngànghànghìnēng — Ularning barchasi choy ichishni yaxshi ko'radilar.",
                        "rule_tj": "都(dōu) — маънои «ҳама, ҳарду, ҳар як».\nМуҳим: ашёҳои рӯйхатшуда ПЕШ АЗ 都 меоянд.\n\nМисол:\n这些都是王方的东西。— Ҳамаи ин чизҳои Ван Фанг мебошанд.\n我们都是中国人。— Мо ҳама чинӣ ҳастем.\n他们都喜欢喝茶。— Хама чойнуширо дуст медоранд.",
                        "rule_ru": "都(доу) — означает «все, оба, каждый».\nВажно: перечисленные элементы стоят ДО 都.\n\nПример:\n这些都是王方的东西。 — Все это вещи Ван Фана.\n我们都是中国人。 — Мы все китайцы.\n他们都喜欢喝茶。 — Они все любят пить чай."
                },
                "examples": [
                        {
                                "zh": "这些都是王方的东西。",
                                "pinyin": "Zhèxiē dōu shì Wáng Fāng de dōngxi.",
                                "meaning": {
                                        "uz": "Bularning barchasi Vang Fangning narsalari.",
                                        "tj": "Ҳамаи ин чизҳои Ван Фанг мебошанд.",
                                        "ru": "Все это вещи Ван Фана."
                                }
                        },
                        {
                                "zh": "我们都是中国人。",
                                "pinyin": "Wǒmen dōu shì Zhōngguó rén.",
                                "meaning": {
                                        "uz": "Hammamiz Xitoymiz.",
                                        "tj": "Мо ҳама чинӣ ҳастем.",
                                        "ru": "Мы все китайцы."
                                }
                        },
                        {
                                "zh": "他们都喜欢喝茶。",
                                "pinyin": "Tāmen dōu xǐhuan hē chá.",
                                "meaning": {
                                        "uz": "Ularning barchasi choy ichishni yaxshi ko'radilar.",
                                        "tj": "Хамаи онхо чойнуширо дуст медоранд.",
                                        "ru": "Они все любят пить чай."
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
                                        "uz": "Kecha ertalab qaerga bordingiz?",
                                        "tj": "Субҳи дирӯз ба куҷо рафтӣ?",
                                        "ru": "Куда ты ходил вчера утром?"
                                },
                                "answer": "昨天上午你去哪儿了？",
                                "pinyin": "Zuótiān shàngwǔ nǐ qù nǎr le?"
                        },
                        {
                                "prompt": {
                                        "uz": "Men narsalar sotib olish uchun do'konga bordim.",
                                        "tj": "Ман барои харидани чизҳо ба мағоза рафтам.",
                                        "ru": "Я пошел в магазин, чтобы купить вещи."
                                },
                                "answer": "我去商店买东西了。",
                                "pinyin": "Wǒ qù shāngdiàn mǎi dōngxi le."
                        },
                        {
                                "prompt": {
                                        "uz": "U juda ko'p kiyim sotib oldi.",
                                        "tj": "Вай хеле зиёд либос харид.",
                                        "ru": "Она купила довольно много одежды."
                                },
                                "answer": "她买了不少衣服。",
                                "pinyin": "Tā mǎile bùshǎo yīfu."
                        },
                        {
                                "prompt": {
                                        "uz": "U 40 daqiqadan keyin qaytib keladi.",
                                        "tj": "Вай пас аз 40 дақиқа бармегардад.",
                                        "ru": "Он вернется через 40 минут."
                                },
                                "answer": "40分钟后回来。",
                                "pinyin": "Sìshí fēnzhōng hòu huílai."
                        },
                        {
                                "prompt": {
                                        "uz": "Bularning barchasi uning narsalari.",
                                        "tj": "Ҳамаи ин чизҳои ӯст.",
                                        "ru": "Все это его вещи."
                                },
                                "answer": "这些都是他的东西。",
                                "pinyin": "Zhèxiē dōu shì tā de dōngxi."
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
                                "prompt": "我去商店买东西___。",
                                "answer": "了",
                                "pinyin": "le"
                        },
                        {
                                "prompt": "40分钟___回来。",
                                "answer": "后",
                                "pinyin": "hòu"
                        },
                        {
                                "prompt": "这些___是王方的东西。",
                                "answer": "都",
                                "pinyin": "dōu"
                        },
                        {
                                "prompt": "我___买，这些不是我的。",
                                "answer": "没",
                                "pinyin": "méi"
                        }
                ]
        },
        {
                "no": 3,
                "type": "negative",
                "instruction": {
                        "uz": "Gapni inkor qiling (mán yordamida):",
                        "tj": "Ҷумларо манфӣ кунед (бо истифода аз 没):",
                        "ru": "Сделайте предложение отрицательным (используя 没):"
                },
                "items": [
                        {
                                "prompt": "她买了不少衣服。",
                                "answer": "她没买衣服。",
                                "pinyin": "Tā méi mǎi yīfu."
                        },
                        {
                                "prompt": "我去商店了。",
                                "answer": "我没去商店。",
                                "pinyin": "Wǒ méi qù shāngdiàn."
                        },
                        {
                                "prompt": "他看见张先生了。",
                                "answer": "他没看见张先生。",
                                "pinyin": "Tā méi kànjiàn Zhāng xiānsheng."
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "昨天上午你去哪儿了？",
                        "我去商店买东西了。",
                        "她买了不少衣服。",
                        "40分钟后回来。",
                        "这些都是他的东西。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "了",
                        "后",
                        "都",
                        "没"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "她没买衣服。",
                        "我没去商店。",
                        "他没看见张先生。"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "y (4 jumla) yordamida kechagi kun haqida yozing:",
                        "tj": "Бо истифода аз 了 (4 ҷумла) дар бораи дирӯз нависед:",
                        "ru": "Напишите о вчерашнем дне, используя 了 (4 предложения):"
                },
                "template": "昨天我___了。我买了___。我没___。___后我回家了。",
                "words": [
                        "了",
                        "没",
                        "去",
                        "买",
                        "后",
                        "分钟"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "láng yordamida javob bering:",
                        "tj": "Бо истифода аз 都 ҷавоб диҳед:",
                        "ru": "Ответьте, используя 都:"
                },
                "items": [
                        {
                                "prompt": "你的朋友都是中国人吗？",
                                "hint": "Yes/no, use 都"
                        },
                        {
                                "prompt": "桌子上的东西都是谁的？",
                                "hint": "State whose things they are"
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
