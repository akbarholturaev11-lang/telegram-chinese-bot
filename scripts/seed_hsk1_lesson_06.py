import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 6,
    "lesson_code": "HSK1-L06",
    "title": "我会说汉语",
    "goal": {
        "uz": "Qobiliyat va malakalar haqida so‘zlash, modal fe’l shn",
        "tj": "Гап дар бораи кобилият ва махорат, феъли модали 会",
        "ru": "Говоря о способностях и навыках, модальный глагол 会"
    },
    "intro_text": {
        "uz": "Oltinchi darsda siz modal fe'l mín, sifatdosh predikativ jumlalar va so'roq so'zlaridan foydalanib qobiliyatlarni ifodalashni o'rganasiz. 12 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси шашум шумо ифодаи қобилиятҳоро бо истифода аз феъли модалии 会, ҷумлаҳои предикати сифатӣ ва калимаи саволии 怎么 меомӯзед. 12 калимаи нав, 3 муколама.",
        "ru": "На шестом уроке вы научитесь выражать способности с помощью модального глагола 会, прилагательных-сказуемых и вопросительного слова 怎么. 12 новых слов, 3 диалога."
    },

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "会",
                "pinyin": "huì",
                "pos": "mod.",
                "meaning": {
                        "uz": "qila olmoq, qila olmoq (o'rganish orqali)",
                        "tj": "тавонистан, тавонистан (тавассути омӯзиш)",
                        "ru": "может, иметь возможность (путем обучения)"
                }
        },
        {
                "no": 2,
                "zh": "说",
                "pinyin": "shuō",
                "pos": "v.",
                "meaning": {
                        "uz": "gapirmoq, aytmoq",
                        "tj": "гуфтан, гуфтан",
                        "ru": "говорить, сказать"
                }
        },
        {
                "no": 3,
                "zh": "妈妈",
                "pinyin": "māma",
                "pos": "n.",
                "meaning": {
                        "uz": "onam, onam",
                        "tj": "модар, модар",
                        "ru": "мать, мама"
                }
        },
        {
                "no": 4,
                "zh": "菜",
                "pinyin": "cài",
                "pos": "n.",
                "meaning": {
                        "uz": "idish, taom, sabzavot",
                        "tj": "табақ, ғизо, сабзавот",
                        "ru": "блюдо, еда, овощ"
                }
        },
        {
                "no": 5,
                "zh": "很",
                "pinyin": "hěn",
                "pos": "adv.",
                "meaning": {
                        "uz": "juda, juda",
                        "tj": "хеле, хеле",
                        "ru": "очень, вполне"
                }
        },
        {
                "no": 6,
                "zh": "好吃",
                "pinyin": "hǎochī",
                "pos": "adj.",
                "meaning": {
                        "uz": "mazali, mazali",
                        "tj": "болаззат, болаззат",
                        "ru": "вкусно, вкусно"
                }
        },
        {
                "no": 7,
                "zh": "做",
                "pinyin": "zuò",
                "pos": "v.",
                "meaning": {
                        "uz": "qilmoq, qilmoq, tayyorlamoq",
                        "tj": "кардан, кардан, тайёр кардан",
                        "ru": "делать, делать, готовить"
                }
        },
        {
                "no": 8,
                "zh": "写",
                "pinyin": "xiě",
                "pos": "v.",
                "meaning": {
                        "uz": "yozish",
                        "tj": "навиштан",
                        "ru": "писать"
                }
        },
        {
                "no": 9,
                "zh": "汉字",
                "pinyin": "Hànzì",
                "pos": "n.",
                "meaning": {
                        "uz": "Xitoy belgilar",
                        "tj": "Аломатҳои чинӣ",
                        "ru": "Китайские иероглифы"
                }
        },
        {
                "no": 10,
                "zh": "字",
                "pinyin": "zì",
                "pos": "n.",
                "meaning": {
                        "uz": "belgi, harf",
                        "tj": "характер, харф",
                        "ru": "персонаж, буква"
                }
        },
        {
                "no": 11,
                "zh": "怎么",
                "pinyin": "zěnme",
                "pos": "pron.",
                "meaning": {
                        "uz": "qanday, qanday tarzda",
                        "tj": "чи тавр, бо кадом рох",
                        "ru": "как, каким образом"
                }
        },
        {
                "no": 12,
                "zh": "读",
                "pinyin": "dú",
                "pos": "v.",
                "meaning": {
                        "uz": "o'qish (baland ovozda)",
                        "tj": "хондан (бо овози баланд)",
                        "ru": "читать (вслух)"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Maktabda — xitoy tilida gapirish",
                        "tj": "Дар мактаб бо хитоӣ гап мезананд",
                        "ru": "Говорим по-китайски в школе"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你会说汉语吗？",
                                "pinyin": "Nǐ huì shuō Hànyǔ ma?",
                                "translation": {
                                        "uz": "Siz xitoycha gapira olasizmi?",
                                        "tj": "Шумо метавонед бо хитоӣ ҳарф занед?",
                                        "ru": "Вы можете говорить по-китайски?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我会说汉语。",
                                "pinyin": "Wǒ huì shuō Hànyǔ.",
                                "translation": {
                                        "uz": "Men xitoycha gapira olaman.",
                                        "tj": "Ман метавонам хитоӣ гап занам.",
                                        "ru": "Я могу говорить по-китайски."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你妈妈会说汉语吗？",
                                "pinyin": "Nǐ māma huì shuō Hànyǔ ma?",
                                "translation": {
                                        "uz": "Onangiz xitoycha gapira oladimi?",
                                        "tj": "Оё модарат бо хитоӣ гап зада метавонад?",
                                        "ru": "Твоя мама говорит по-китайски?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "她不会说。",
                                "pinyin": "Tā bú huì shuō.",
                                "translation": {
                                        "uz": "U gapira olmaydi.",
                                        "tj": "Вай наметавонад ҳарф занад.",
                                        "ru": "Она не может говорить на этом языке."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Oshxonada — xitoy taomi",
                        "tj": "Хӯрокҳои чинӣ дар ошхона",
                        "ru": "Китайская еда на кухне"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "中国菜好吃吗？",
                                "pinyin": "Zhōngguó cài hǎochī ma?",
                                "translation": {
                                        "uz": "Xitoy taomlari mazalimi?",
                                        "tj": "Оё ғизои чинӣ болаззат аст?",
                                        "ru": "Китайская еда вкусная?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "中国菜很好吃。",
                                "pinyin": "Zhōngguó cài hěn hǎochī.",
                                "translation": {
                                        "uz": "Xitoy taomlari juda mazali.",
                                        "tj": "Хӯрокҳои чинӣ хеле болаззат аст.",
                                        "ru": "Китайская еда очень вкусная."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你会做中国菜吗？",
                                "pinyin": "Nǐ huì zuò Zhōngguó cài ma?",
                                "translation": {
                                        "uz": "Xitoy taomlarini pishira olasizmi?",
                                        "tj": "Метавонед хӯроки чинӣ пухтан?",
                                        "ru": "Умеете ли вы готовить китайскую еду?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我不会做。",
                                "pinyin": "Wǒ bú huì zuò.",
                                "translation": {
                                        "uz": "Men uni pishirolmayman.",
                                        "tj": "Ман онро пухта наметавонам.",
                                        "ru": "Я не умею его готовить."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Kutubxonada — xitoy yozuvi",
                        "tj": "Дар китобхона — хатти хитой",
                        "ru": "В библиотеке – китайское письмо."
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你会写汉字吗？",
                                "pinyin": "Nǐ huì xiě Hànzì ma?",
                                "translation": {
                                        "uz": "Xitoycha belgilarni yoza olasizmi?",
                                        "tj": "Метавонед ҳарфҳои чиниро нависед?",
                                        "ru": "Умеете ли вы писать китайские иероглифы?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我会写。",
                                "pinyin": "Wǒ huì xiě.",
                                "translation": {
                                        "uz": "Men ularni yozishim mumkin.",
                                        "tj": "Ман метавонам онҳоро нависам.",
                                        "ru": "Я могу их написать."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "这个字怎么写？",
                                "pinyin": "Zhège zì zěnme xiě?",
                                "translation": {
                                        "uz": "Bu belgini qanday yozasiz?",
                                        "tj": "Шумо ин хислатро чӣ гуна менависед?",
                                        "ru": "Как написать этого персонажа?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "对不起，这个字我会读，不会写。",
                                "pinyin": "Duìbuqǐ, zhège zì wǒ huì dú, bú huì xiě.",
                                "translation": {
                                        "uz": "Kechirasiz, men bu belgini o'qiyman, lekin yoza olmayman.",
                                        "tj": "Бубахшед, ман ин аломатро хонда метавонам, аммо навишта наметавонам.",
                                        "ru": "Извините, я могу прочитать этот символ, но не могу его написать."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "能愿动词 会 — Modal fe'l 会",
                "explanation": {
                        "rule_uz": "mín(huì) — oʻrganish orqali erishilgan qobiliyatni ifodalaydi.\nTuzilishi: Mavzu + (shč)jn + Fe'l\n\nTasdiqlovchi: chàngìǎngǎní— Men xitoy tilida gaplasha olaman.\nSalbiy: chàngāngāngāngāngāngīng- xitoy taomlarini pishirolmayman.\nSavol: xingčičičiči？— Xitoy belgilarini yoza olasizmi?\n\nEslatma: inkor qilish uchun dzhčī dan foydalaning; Ha/Yo'q savollari uchun h dan foydalaning.",
                        "rule_tj": "会(huì) — кобилияти тавассути омузиш ба даст овардашударо ифода мекунад.\nСохтор: Мавзӯъ + (不)会 + Феъл\n\nТасдиқ: 我会说汉语。— Ман бо хитоӣ ҳарф зада метавонам.\nМанфӣ: 我不会做中国菜。— Ман хӯрокҳои чинӣ пухта наметавонам.\nСавол: 你会写汉字吗？— Оё шумо аломатҳои чиниро навишта метавонед?\n\nЭзоҳ: 不会 барои рад кардан истифода баред; Барои саволҳои ҳа/не 吗-ро истифода баред.",
                        "rule_ru": "会(huì) — выражает способности, приобретенные в результате обучения.\nСтруктура: Подлежащее + (不)会 + глагол.\n\nУтвердительный ответ: 我会说汉语。 — Я говорю по-китайски.\nОтрицательное: 我不会做中国菜。 — Я не умею готовить китайскую еду.\nВопрос: 你会写汉字吗？ — Можете ли вы написать китайские иероглифы?\n\nПримечание. Используйте 不会 для отрицания; используйте 吗 для вопросов типа «да/нет»."
                },
                "examples": [
                        {
                                "zh": "我会说汉语。",
                                "pinyin": "Wǒ huì shuō Hànyǔ.",
                                "meaning": {
                                        "uz": "Men xitoycha gapira olaman.",
                                        "tj": "Ман метавонам хитоӣ гап занам.",
                                        "ru": "Я могу говорить по-китайски."
                                }
                        },
                        {
                                "zh": "她不会做中国菜。",
                                "pinyin": "Tā bú huì zuò Zhōngguó cài.",
                                "meaning": {
                                        "uz": "U xitoy taomlarini pishirolmaydi.",
                                        "tj": "Вай хӯроки чинӣ пухта наметавонад.",
                                        "ru": "Она не умеет готовить китайскую еду."
                                }
                        },
                        {
                                "zh": "你会写汉字吗？",
                                "pinyin": "Nǐ huì xiě Hànzì ma?",
                                "meaning": {
                                        "uz": "Xitoycha belgilarni yoza olasizmi?",
                                        "tj": "Метавонед ҳарфҳои чиниро нависед?",
                                        "ru": "Умеете ли вы писать китайские иероглифы?"
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "形容词谓语句 — Sifat kesimli gap",
                "explanation": {
                        "rule_uz": "Sifat yuklamasi: Mavzu + lín/shč + Sifat\n\nXitoy tilida sifatlar gapning predikati bo‘lib xizmat qilishi mumkin.\nTasdiqlovchi jumlalarda hěn (hěn) odatda ishlatiladi:\nchàngāngāngāngī - Xitoy taomlari juda mazali.\n\nInkor jumlalarda shín ishlatiladi (káng shart emas):\nchàngāngāngčičičiči — Onamning xitoy tili yaxshi emas.\n\nIzoh: jàn ko‘pincha semantik jihatdan zaif va grammatik talabni qondirish uchun ishlatiladi.",
                        "rule_tj": "Предикати сифат: Мавзӯъ + 很/不 + Сифат\n\nДар чинӣ сифатҳо метавонанд ҳамчун предикати ҳукм хидмат кунанд.\nДар ҷумлаҳои тасдиқ одатан 很(hěn) истифода мешавад:\n中国菜很好吃。— Хӯрокҳои чинӣ хеле болаззат аст.\n\nДар ҷумлаҳои манфӣ 不 истифода мешавад (很 лозим нест):\n我妈妈的汉语不好。— Хитоии модарам хуб нест.\n\nЭзоҳ: 很 аксар вақт аз ҷиҳати маъно заиф аст ва барои қонеъ кардани талаботи грамматикӣ истифода мешавад.",
                        "rule_ru": "Прилагательное сказуемое: Подлежащее + 很/不 + прилагательное.\n\nВ китайском языке прилагательные могут выступать в роли сказуемых в предложении.\nВ утвердительных предложениях обычно используется 很(hěn):\n中国菜很好吃。 — Китайская еда очень вкусная.\n\nВ отрицательных предложениях используется 不 (很 не обязателен):\n我妈妈的汉语不好。 — Моя мать плохо говорит по-китайски.\n\nПримечание. 很 часто семантически слаб и используется для удовлетворения грамматических требований."
                },
                "examples": [
                        {
                                "zh": "中国菜很好吃。",
                                "pinyin": "Zhōngguó cài hěn hǎochī.",
                                "meaning": {
                                        "uz": "Xitoy taomlari juda mazali.",
                                        "tj": "Хӯрокҳои чинӣ хеле болаззат аст.",
                                        "ru": "Китайская еда очень вкусная."
                                }
                        },
                        {
                                "zh": "她的汉语很好。",
                                "pinyin": "Tā de Hànyǔ hěn hǎo.",
                                "meaning": {
                                        "uz": "Uning xitoy tili juda yaxshi.",
                                        "tj": "Хитоии вай хеле хуб аст.",
                                        "ru": "Ее китайский очень хорош."
                                }
                        },
                        {
                                "zh": "我妈妈的汉语不好。",
                                "pinyin": "Wǒ māma de Hànyǔ bù hǎo.",
                                "meaning": {
                                        "uz": "Onamning xitoy tili yaxshi emas.",
                                        "tj": "Хитоии модарам хуб нест.",
                                        "ru": "Моя мать плохо говорит по-китайски."
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "怎么 — Qanday so'roq olmoshi",
                "explanation": {
                        "rule_uz": "zěnme (zěnme) — fe’ldan oldin qo‘yiladi, ish-harakatning bajarilishini so‘raydi.\nTuzilishi: Mavzu + míní + Fe'l?\n\nMisol:\nlínghìnìnínĆ？— Bu belgini qanday yozasiz?\nlāngāngāngīngīng？— Bu qahramonni qanday o'qiysiz?\nchàngāngāngāngāngī - Xitoy taomlarini qanday pishirasiz?",
                        "rule_tj": "怎么(zěnme) — placed before a verb, asks about the manner of an action.\nStructure: Subject + 怎么 + Verb?\n\nExample:\n这个字怎么写？— How do you write this character?\n这个字怎么读？— How do you read this character?\n中国菜怎么做？— How do you cook Chinese food?",
                        "rule_ru": "怎么(zěnme) — placed before a verb, asks about the manner of an action.\nStructure: Subject + 怎么 + Verb?\n\nExample:\n这个字怎么写？— How do you write this character?\n这个字怎么读？— How do you read this character?\n中国菜怎么做？— How do you cook Chinese food?"
                },
                "examples": [
                        {
                                "zh": "这个字怎么写？",
                                "pinyin": "Zhège zì zěnme xiě?",
                                "meaning": {
                                        "uz": "Bu belgini qanday yozasiz?",
                                        "tj": "Шумо ин хислатро чӣ гуна менависед?",
                                        "ru": "Как написать этого персонажа?"
                                }
                        },
                        {
                                "zh": "这个字怎么读？",
                                "pinyin": "Zhège zì zěnme dú?",
                                "meaning": {
                                        "uz": "How do you read this character?",
                                        "tj": "Шумо ин хислатро чӣ гуна мехонед?",
                                        "ru": "Как вы читаете этого персонажа?"
                                }
                        },
                        {
                                "zh": "汉语怎么说？",
                                "pinyin": "Hànyǔ zěnme shuō?",
                                "meaning": {
                                        "uz": "Buni xitoy tilida qanday aytasiz?",
                                        "tj": "Чӣ тавр шумо онро дар Чин мегӯед?",
                                        "ru": "Как сказать по-китайски?"
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
                                        "uz": "Siz xitoycha gapira olasizmi?",
                                        "tj": "Шумо метавонед бо хитоӣ ҳарф занед?",
                                        "ru": "Вы можете говорить по-китайски?"
                                },
                                "answer": "你会说汉语吗？",
                                "pinyin": "Nǐ huì shuō Hànyǔ ma?"
                        },
                        {
                                "prompt": {
                                        "uz": "Men xitoycha gapira olaman.",
                                        "tj": "Ман метавонам хитоӣ гап занам.",
                                        "ru": "Я могу говорить по-китайски."
                                },
                                "answer": "我会说汉语。",
                                "pinyin": "Wǒ huì shuō Hànyǔ."
                        },
                        {
                                "prompt": {
                                        "uz": "Xitoy taomlari juda mazali.",
                                        "tj": "Хӯрокҳои чинӣ хеле болаззат аст.",
                                        "ru": "Китайская еда очень вкусная."
                                },
                                "answer": "中国菜很好吃。",
                                "pinyin": "Zhōngguó cài hěn hǎochī."
                        },
                        {
                                "prompt": {
                                        "uz": "Men Xitoy taomlarini pishirolmayman.",
                                        "tj": "Ман хӯроки чинӣ пухта наметавонам.",
                                        "ru": "Я не умею готовить китайскую еду."
                                },
                                "answer": "我不会做中国菜。",
                                "pinyin": "Wǒ bú huì zuò Zhōngguó cài."
                        },
                        {
                                "prompt": {
                                        "uz": "Bu belgini qanday yozasiz?",
                                        "tj": "Шумо ин хислатро чӣ гуна менависед?",
                                        "ru": "Как написать этого персонажа?"
                                },
                                "answer": "这个字怎么写？",
                                "pinyin": "Zhège zì zěnme xiě?"
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
                                "prompt": "你___说汉语吗？",
                                "answer": "会",
                                "pinyin": "huì"
                        },
                        {
                                "prompt": "中国菜___好吃。",
                                "answer": "很",
                                "pinyin": "hěn"
                        },
                        {
                                "prompt": "这个字___写？",
                                "answer": "怎么",
                                "pinyin": "zěnme"
                        },
                        {
                                "prompt": "我会___，不会___。",
                                "answer": "读/写",
                                "pinyin": "dú/xiě"
                        }
                ]
        },
        {
                "no": 3,
                "type": "make_negative",
                "instruction": {
                        "uz": "Salbiy gapga aylantiring:",
                        "tj": "Ба ҳукми манфӣ табдил диҳед:",
                        "ru": "Превратитесь в отрицательное предложение:"
                },
                "items": [
                        {
                                "prompt": "我会说汉语。",
                                "answer": "我不会说汉语。",
                                "pinyin": "Wǒ bú huì shuō Hànyǔ."
                        },
                        {
                                "prompt": "中国菜很好吃。",
                                "answer": "中国菜不好吃。",
                                "pinyin": "Zhōngguó cài bù hǎochī."
                        },
                        {
                                "prompt": "她会写汉字。",
                                "answer": "她不会写汉字。",
                                "pinyin": "Tā bú huì xiě Hànzì."
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "你会说汉语吗？",
                        "我会说汉语。",
                        "中国菜很好吃。",
                        "我不会做中国菜。",
                        "这个字怎么写？"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "会",
                        "很",
                        "怎么",
                        "读/写"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "我不会说汉语。",
                        "中国菜不好吃。",
                        "她不会写汉字。"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "O'zingiz haqingizda 4 ta jumla yozing (nima qila olasiz/ qila olmaysiz):",
                        "tj": "Дар бораи худ 4 ҷумла нависед (чизе шумо метавонед/кор карда наметавонед):",
                        "ru": "Напишите 4 предложения о себе (что вы можете/не можете делать):"
                },
                "template": "我会___。我不会___。我___会___吗？",
                "words": [
                        "会",
                        "不会",
                        "说",
                        "写",
                        "做",
                        "读",
                        "汉语",
                        "汉字",
                        "中国菜"
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
                                "prompt": "你会说汉语吗？",
                                "hint": "Yes or no, with a full sentence"
                        },
                        {
                                "prompt": "中国菜好吃吗？",
                                "hint": "Share your own opinion"
                        },
                        {
                                "prompt": "这个字怎么写？ (好)",
                                "hint": "Describe how to write the character Hǎo — good"
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
