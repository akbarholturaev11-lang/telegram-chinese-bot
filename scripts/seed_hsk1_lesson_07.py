import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 7,
    "lesson_code": "HSK1-L07",
    "title": "今天几号",
    "goal": {
        "uz": "O'rganish sanalari, hafta kunlari va ketma-ket fe'l jumlalari",
        "tj": "Санаҳои омӯзиш, рӯзҳои ҳафта ва ҷумлаҳои феълии силсилавӣ",
        "ru": "Изучаем даты, дни недели и предложения с последовательными глаголами."
    },
    "intro_text": {
        "uz": "Ettinchi darsda siz bugungi sanani, haftaning kunlarini va j+joy+harakat qurilishini aytishni o'rganasiz. 12 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси ҳафтум шумо гуфтани санаи имрӯза, рӯзҳои ҳафта ва сохтани 去+ҷои+амалро меомӯзед. 12 калимаи нав, 3 муколама.",
        "ru": "На седьмом уроке вы научитесь произносить сегодняшнее число, дни недели и конструкцию 去+место+действие. 12 новых слов, 3 диалога."
    },

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "请",
                "pinyin": "qǐng",
                "pos": "v.",
                "meaning": {
                        "uz": "iltimos, so'rasam maylimi",
                        "tj": "лутфан, ман метавонам пурсам",
                        "ru": "пожалуйста, могу ли я спросить"
                }
        },
        {
                "no": 2,
                "zh": "问",
                "pinyin": "wèn",
                "pos": "v.",
                "meaning": {
                        "uz": "so'rash",
                        "tj": "пурсидан",
                        "ru": "спросить"
                }
        },
        {
                "no": 3,
                "zh": "今天",
                "pinyin": "jīntiān",
                "pos": "n.",
                "meaning": {
                        "uz": "bugun",
                        "tj": "имруз",
                        "ru": "сегодня"
                }
        },
        {
                "no": 4,
                "zh": "号",
                "pinyin": "hào",
                "pos": "n.",
                "meaning": {
                        "uz": "sana (oy kuni)",
                        "tj": "сана (рӯзи моҳ)",
                        "ru": "дата (день месяца)"
                }
        },
        {
                "no": 5,
                "zh": "月",
                "pinyin": "yuè",
                "pos": "n.",
                "meaning": {
                        "uz": "oy (yanvar, fevral va boshqalar)",
                        "tj": "моҳ (январ, феврал ва ғ.)",
                        "ru": "месяц (январь, февраль и т. д.)"
                }
        },
        {
                "no": 6,
                "zh": "星期",
                "pinyin": "xīngqī",
                "pos": "n.",
                "meaning": {
                        "uz": "hafta, haftaning kuni",
                        "tj": "ҳафта, рӯзи ҳафта",
                        "ru": "неделя, день недели"
                }
        },
        {
                "no": 7,
                "zh": "昨天",
                "pinyin": "zuótiān",
                "pos": "n.",
                "meaning": {
                        "uz": "kecha",
                        "tj": "дируз",
                        "ru": "вчера"
                }
        },
        {
                "no": 8,
                "zh": "明天",
                "pinyin": "míngtiān",
                "pos": "n.",
                "meaning": {
                        "uz": "ertaga",
                        "tj": "фардо",
                        "ru": "завтра"
                }
        },
        {
                "no": 9,
                "zh": "去",
                "pinyin": "qù",
                "pos": "v.",
                "meaning": {
                        "uz": "borish",
                        "tj": "рафтан",
                        "ru": "идти"
                }
        },
        {
                "no": 10,
                "zh": "学校",
                "pinyin": "xuéxiào",
                "pos": "n.",
                "meaning": {
                        "uz": "maktab",
                        "tj": "мактаб",
                        "ru": "школа"
                }
        },
        {
                "no": 11,
                "zh": "看",
                "pinyin": "kàn",
                "pos": "v.",
                "meaning": {
                        "uz": "qaramoq, tomosha qilmoq, o‘qimoq",
                        "tj": "дидан, тамошо кардан, хондан",
                        "ru": "смотреть, смотреть, читать"
                }
        },
        {
                "no": 12,
                "zh": "书",
                "pinyin": "shū",
                "pos": "n.",
                "meaning": {
                        "uz": "kitob",
                        "tj": "китоб",
                        "ru": "книга"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Bankda — bugungi sana",
                        "tj": "Дар банк — санаи имруза",
                        "ru": "В банке - сегодняшняя дата"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "请问，今天几号？",
                                "pinyin": "Qǐngwèn, jīntiān jǐ hào?",
                                "translation": {
                                        "uz": "Kechirasiz, bugungi sana nima?",
                                        "tj": "Мебахшед, имрӯз чӣ гуна аст?",
                                        "ru": "Простите, какое сегодня число?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "今天9月1号。",
                                "pinyin": "Jīntiān jiǔ yuè yī hào.",
                                "translation": {
                                        "uz": "Bugun 1 sentyabr.",
                                        "tj": "Имрӯз 1 сентябр аст.",
                                        "ru": "Сегодня 1 сентября."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "今天星期几？",
                                "pinyin": "Jīntiān xīngqī jǐ?",
                                "translation": {
                                        "uz": "Bugun haftaning qaysi kuni?",
                                        "tj": "Имрӯз кадом рӯзи ҳафта аст?",
                                        "ru": "Какой сегодня день недели?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "星期三。",
                                "pinyin": "Xīngqī sān.",
                                "translation": {
                                        "uz": "chorshanba.",
                                        "tj": "Чоршанбе.",
                                        "ru": "Среда."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Taqvimga qarab — kecha va ertaga",
                        "tj": "Мувофики таквим — дируз ва фардо",
                        "ru": "По календарю - вчера и завтра"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "昨天是几月几号？",
                                "pinyin": "Zuótiān shì jǐ yuè jǐ hào?",
                                "translation": {
                                        "uz": "Kecha qaysi oy va kun edi?",
                                        "tj": "Дирӯз кадом моҳу рӯз буд?",
                                        "ru": "Какой месяц и день был вчера?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "昨天是8月31号，星期二。",
                                "pinyin": "Zuótiān shì bā yuè sānshíyī hào, xīngqī èr.",
                                "translation": {
                                        "uz": "Kecha 31-avgust, seshanba edi.",
                                        "tj": "Дируз 31 август, сешанбе буд.",
                                        "ru": "Вчера было 31 августа, вторник."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "明天呢？",
                                "pinyin": "Míngtiān ne?",
                                "translation": {
                                        "uz": "Va ertaga?",
                                        "tj": "Ва фардо?",
                                        "ru": "А завтра?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "明天是9月2号，星期四。",
                                "pinyin": "Míngtiān shì jiǔ yuè èr hào, xīngqī sì.",
                                "translation": {
                                        "uz": "Ertaga 2 sentyabr, payshanba.",
                                        "tj": "Пагоҳ 2 сентябр, панҷшанбе.",
                                        "ru": "Завтра 2 сентября, четверг."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Qahvaxonada — ertangi reja",
                        "tj": "Нақшаи фардо дар қаҳвахона аст",
                        "ru": "План на завтра в кафе"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "明天星期六，你去学校吗？",
                                "pinyin": "Míngtiān xīngqī liù, nǐ qù xuéxiào ma?",
                                "translation": {
                                        "uz": "Ertaga shanba - maktabga borasizmi?",
                                        "tj": "Пагох рузи шанбе — шумо ба мактаб меравед?",
                                        "ru": "Завтра суббота, ты идешь в школу?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我去学校。",
                                "pinyin": "Wǒ qù xuéxiào.",
                                "translation": {
                                        "uz": "Men maktabga ketyapman.",
                                        "tj": "Ман ба мактаб меравам.",
                                        "ru": "Я иду в школу."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你去学校做什么？",
                                "pinyin": "Nǐ qù xuéxiào zuò shénme?",
                                "translation": {
                                        "uz": "Nima qilish uchun maktabga borasiz?",
                                        "tj": "Шумо барои чӣ кор кардан ба мактаб меравед?",
                                        "ru": "Что ты собираешься делать в школу?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我去学校看书。",
                                "pinyin": "Wǒ qù xuéxiào kàn shū.",
                                "translation": {
                                        "uz": "Men maktabga o'qish uchun ketyapman.",
                                        "tj": "Ман барои хондан ба мактаб меравам.",
                                        "ru": "Я иду в школу читать."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "日期的表达 — Sana ifodalash",
                "explanation": {
                        "rule_uz": "Xitoy tilida sanalar kattadan eng kichik birlikka qarab ifodalanadi:\nYil → Oy → Kun → Haftaning kuni\n\nOy: shīngī(yanvar) ~ dīngīmī(dekabr)\nKun: 1-chi (1-chi) ~ 31-chi (31-chi)\n\nHafta kunlari:\ndushanba\nseshanba\nchorshanba\npayshanba\nJuma\nshanba\nyakshanba\n\nMisol: 9mí1jín，míngínshī - 1-sentyabr, chorshanba",
                        "rule_tj": "Дар чинӣ санаҳо аз воҳиди калон ба хурдтарин ифода карда мешаванд:\nСол → Моҳ → Рӯз → Рӯзи ҳафта\n\nМоҳ: 一月(январ) ~ 十二月(декабр)\nРӯзи: 1号(1-ум) ~ 31号(31-ум)\n\nРӯзҳои ҳафта:\n星期一 Душанбе\n星期二 Сешанбе\n星期三 Чоршанбе\n星期四 Панҷшанбе\n星期五 Ҷумъа\n星期六 Шанбе\n星期日/星期天 Якшанбе\n\nМисол: 9月1号，星期三 - 1 сентябр, чоршанбе",
                        "rule_ru": "В китайском языке даты выражаются от наибольшей к наименьшей единице:\nГод → Месяц → День → День недели\n\nМесяц: 一月(январь) ~ 十二月(декабрь)\nДень: 1 号 (1-го числа) ~ 31 号 (31-го числа)\n\nДни недели:\n星期一 понедельник\n星期二 вторник\n星期三 среда\n星期四 Четверг\nНачало пятницы\n星期六 Суббота\n星期日/星期天 воскресенье\n\nПример: 9月1号，星期三 — 1 сентября, среда."
                },
                "examples": [
                        {
                                "zh": "今天9月1号，星期三。",
                                "pinyin": "Jīntiān jiǔ yuè yī hào, xīngqī sān.",
                                "meaning": {
                                        "uz": "Bugun 1-sentabr, chorshanba.",
                                        "tj": "Имрӯз 1 сентябр, чоршанбе аст.",
                                        "ru": "Сегодня 1 сентября, среда."
                                }
                        },
                        {
                                "zh": "明天星期六。",
                                "pinyin": "Míngtiān xīngqī liù.",
                                "meaning": {
                                        "uz": "Ertaga shanba.",
                                        "tj": "Пагоҳ рӯзи шанбе аст.",
                                        "ru": "Завтра суббота."
                                }
                        },
                        {
                                "zh": "昨天8月31号。",
                                "pinyin": "Zuótiān bā yuè sānshíyī hào.",
                                "meaning": {
                                        "uz": "Kecha 31 avgust edi.",
                                        "tj": "Дируз 31 август буд.",
                                        "ru": "Вчера было 31 августа."
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "名词谓语句 — Ot kesimli gap",
                "explanation": {
                        "rule_uz": "Ot yoki son predikat vazifasini bajarishi mumkin (máng shart emas).\nKo'pincha yosh, sana va vaqtni ifodalash uchun ishlatiladi.\n\nMisol:\nmēng 9mī 1kīn。— Bugun 1-sentabr. (9mí1jí - ot predikati)\nchànghànghìnì- Ertaga chorshanba.\nlíngíngyēngči 33ján— Mening xitoy tili o'qituvchim 33 yoshda.",
                        "rule_tj": "Исм ё рақам метавонад ҳамчун предикат хизмат кунад (是 лозим нест).\nАксар вақт барои ифодаи синну сол, сана ва вақт истифода мешавад.\n\nМисол:\n今天9月1号。 — Имрӯз 1 сентябр аст. (9月1号 предикати исм аст)\n明天星期三。 — Пагоҳ рӯзи чоршанбе.\n我的汉语老师33岁。— Муаллими хитоии ман 33 сола аст.",
                        "rule_ru": "Сказуемым может служить существительное или число (是 не требуется).\nЧасто используется для обозначения возраста, даты и времени.\n\nПример:\n今天9月1号。 — Сегодня 1 сентября. (9月1号 — существительное-сказуемое)\n明天星期三。 — Завтра среда.\n我的汉语老师33岁。 — Моему учителю китайского 33 года."
                },
                "examples": [
                        {
                                "zh": "今天9月1号。",
                                "pinyin": "Jīntiān jiǔ yuè yī hào.",
                                "meaning": {
                                        "uz": "Bugun 1 sentyabr.",
                                        "tj": "Имрӯз 1 сентябр аст.",
                                        "ru": "Сегодня 1 сентября."
                                }
                        },
                        {
                                "zh": "明天星期三。",
                                "pinyin": "Míngtiān xīngqī sān.",
                                "meaning": {
                                        "uz": "Ertaga chorshanba.",
                                        "tj": "Пагоҳ рӯзи чоршанбе аст.",
                                        "ru": "Завтра среда."
                                }
                        },
                        {
                                "zh": "她今年二十岁。",
                                "pinyin": "Tā jīnnián èrshí suì.",
                                "meaning": {
                                        "uz": "Bu yil u yigirma yoshda.",
                                        "tj": "Вай имсол бистсола шуд.",
                                        "ru": "В этом году ей исполнится двадцать лет."
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "连动句 — 去+joy+nima qilish",
                "explanation": {
                        "rule_uz": "Ketma-ket fe'l gap: birinchi harakat ikkinchisining maqsadini ifodalaydi.\nTuzilishi: Mavzu + tín + Joy + Fe'l + Ob'ekt\n\nMisol:\nchàngāngīngīnīk— Men o‘qish uchun maktabga boraman.\nchàngāngāngāngāngīngīngīng— Men Xitoyga xitoy tilini o‘rganish uchun boraman.\n\nSavol: chàngàngìnìnìnìnì？— Qayerga ketyapsiz va nima qilmoqchisiz?",
                        "rule_tj": "Ҷумлаи феъли қаторӣ: амали аввал ҳадафи дуюмро ифода мекунад.\nСохтор: Мавзӯъ + 去 + Ҷой + Феъл + Объект\n\nМисол:\n我去学校看书。— Ман барои хондан ба мактаб меравам.\n我去中国学习汉语。— Ман барои омӯзиши забони чинӣ ба Чин меравам.\n\nСавол: 你去哪儿做什么？— Куҷо меравед ва чӣ кор мекунед?",
                        "rule_ru": "Серийное глагольное предложение: первое действие выражает цель второго.\nСтруктура: Подлежащее + 去 + Место + Глагол + Объект.\n\nПример:\n我去学校看书。 — Я хожу в школу читать.\n我去中国学习汉语。 — Я еду в Китай изучать китайский язык.\n\nВопрос: 你去哪儿做什么？ — Куда вы собираетесь и что будете делать?"
                },
                "examples": [
                        {
                                "zh": "我去学校看书。",
                                "pinyin": "Wǒ qù xuéxiào kàn shū.",
                                "meaning": {
                                        "uz": "Men o'qish uchun maktabga boraman.",
                                        "tj": "Ман барои хондан ба мактаб меравам.",
                                        "ru": "Я хожу в школу читать."
                                }
                        },
                        {
                                "zh": "她去学校学汉语。",
                                "pinyin": "Tā qù xuéxiào xué Hànyǔ.",
                                "meaning": {
                                        "uz": "U xitoy tilini o‘rganish uchun maktabga boradi.",
                                        "tj": "Вай барои омӯзиши хитоӣ ба мактаб меравад.",
                                        "ru": "Она ходит в школу, чтобы изучать китайский язык."
                                }
                        },
                        {
                                "zh": "你去哪儿做什么？",
                                "pinyin": "Nǐ qù nǎr zuò shénme?",
                                "meaning": {
                                        "uz": "Qayerga ketyapsiz va nima qilasiz?",
                                        "tj": "Шумо куҷо меравед ва чӣ кор хоҳед кард?",
                                        "ru": "Куда ты идешь и что будешь делать?"
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "exercise_json": json.dumps([
        {
                "no": 1,
                "type": "date_writing",
                "instruction": {
                        "uz": "Xitoy tilida yozing:",
                        "tj": "Ба забони чинӣ нависед:",
                        "ru": "Напишите по-китайски:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "3-mart, dushanba",
                                        "tj": "3 март, Душанбе",
                                        "ru": "3 марта, понедельник"
                                },
                                "answer": "3月3号，星期一",
                                "pinyin": "sān yuè sān hào, xīngqī yī"
                        },
                        {
                                "prompt": {
                                        "uz": "15-may, juma",
                                        "tj": "15 май, ҷумъа",
                                        "ru": "15 мая, пятница"
                                },
                                "answer": "5月15号，星期五",
                                "pinyin": "wǔ yuè shíwǔ hào, xīngqī wǔ"
                        },
                        {
                                "prompt": {
                                        "uz": "31 dekabr, yakshanba",
                                        "tj": "31 декабрь, якшанбе",
                                        "ru": "31 декабря, воскресенье"
                                },
                                "answer": "12月31号，星期日",
                                "pinyin": "shí'èr yuè sānshíyī hào, xīngqīrì"
                        },
                        {
                                "prompt": {
                                        "uz": "Bugungi sana nima?",
                                        "tj": "Рӯзи имрӯз чист?",
                                        "ru": "Какое сегодня число?"
                                },
                                "answer": "今天几号？",
                                "pinyin": "Jīntiān jǐ hào?"
                        },
                        {
                                "prompt": {
                                        "uz": "Bugun haftaning qaysi kuni?",
                                        "tj": "Имрӯз кадом рӯзи ҳафта аст?",
                                        "ru": "Какой сегодня день недели?"
                                },
                                "answer": "今天星期几？",
                                "pinyin": "Jīntiān xīngqī jǐ?"
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
                                        "uz": "Kechirasiz, bugungi sana nima?",
                                        "tj": "Мебахшед, имрӯз чӣ гуна аст?",
                                        "ru": "Простите, какое сегодня число?"
                                },
                                "answer": "请问，今天几号？",
                                "pinyin": "Qǐngwèn, jīntiān jǐ hào?"
                        },
                        {
                                "prompt": {
                                        "uz": "Ertaga shanba - maktabga borasizmi?",
                                        "tj": "Пагох рузи шанбе — шумо ба мактаб меравед?",
                                        "ru": "Завтра суббота, ты идешь в школу?"
                                },
                                "answer": "明天星期六，你去学校吗？",
                                "pinyin": "Míngtiān xīngqī liù, nǐ qù xuéxiào ma?"
                        },
                        {
                                "prompt": {
                                        "uz": "Men maktabga o'qish uchun ketyapman.",
                                        "tj": "Ман барои хондан ба мактаб меравам.",
                                        "ru": "Я иду в школу читать."
                                },
                                "answer": "我去学校看书。",
                                "pinyin": "Wǒ qù xuéxiào kàn shū."
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
                                "prompt": "今天___月___号，___期___。",
                                "answer": "enter today's date",
                                "pinyin": "write today's date"
                        },
                        {
                                "prompt": "我___学校___书。",
                                "answer": "去/看",
                                "pinyin": "qù/kàn"
                        },
                        {
                                "prompt": "___天是9月2号，星期四。",
                                "answer": "明",
                                "pinyin": "míng"
                        },
                        {
                                "prompt": "请___，今天星期几？",
                                "answer": "问",
                                "pinyin": "wèn"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "3月3号，星期一",
                        "5月15号，星期五",
                        "12月31号，星期日",
                        "今天几号？",
                        "今天星期几？"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "请问，今天几号？",
                        "明天星期六，你去学校吗？",
                        "我去学校看书。"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "today's date",
                        "去/看",
                        "明",
                        "问"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Bugungi, kechagi va ertangi sanalarni yozing:",
                        "tj": "Санаҳои имрӯз, дирӯз ва фардоро нависед:",
                        "ru": "Напишите сегодняшнюю, вчерашнюю и завтрашнюю даты:"
                },
                "template": "昨天是___月___号，星期___。今天是___月___号，星期___。明天是___月___号，星期___。"
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Ertangi kun uchun rejalaringizni yozing (y+joy+harakat yordamida):",
                        "tj": "Нақшаҳои худро барои фардо нависед (бо истифода аз 去+ҷой+амал):",
                        "ru": "Напишите свои планы на завтра (используя 去+место+действие):"
                },
                "example": "明天我去___。",
                "words": [
                        "去",
                        "学校",
                        "看书",
                        "说汉语",
                        "做中国菜"
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
