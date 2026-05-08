import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 15,
    "lesson_code": "HSK1-L15",
    "title": "我是坐飞机来的",
    "goal": {
        "uz": "mí……y konstruksiya - vaqt, joy va uslubni ta'kidlaydi",
        "tj": "Сохтмони 是……的 - вақт, ҷой ва услубро таъкид мекунад",
        "ru": "Конструкция 是……的 — подчеркивает время, место и манеру поведения."
    },
    "intro_text": {
        "uz": "O'n beshinchi darsda - yakuniy darsda siz biror narsa qachon, qayerda va qanday amalga oshirilganligini ta'kidlash uchun i…… y konstruktsiyasidan foydalanishni o'rganasiz. 9 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси понздаҳ - дарси ниҳоӣ - шумо истифодаи конструксияи 是……的-ро меомӯзед, то кай, дар куҷо ва чӣ гуна кореро таъкид кунед. 9 калимаи нав, 3 диалог.",
        "ru": "На пятнадцатом уроке — последнем уроке — вы научитесь использовать конструкцию 是……的, чтобы подчеркнуть, когда, где и как что-то было сделано. 9 новых слов, 3 диалога."
    },

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "认识",
                "pinyin": "rènshi",
                "pos": "v.",
                "meaning": {
                        "uz": "bilmoq, tanishmoq, tan olmoq",
                        "tj": "донистан, вохӯрдан, шинохтан",
                        "ru": "знать, встретиться, признать"
                }
        },
        {
                "no": 2,
                "zh": "年",
                "pinyin": "nián",
                "pos": "n.",
                "meaning": {
                        "uz": "yil",
                        "tj": "сол",
                        "ru": "год"
                }
        },
        {
                "no": 3,
                "zh": "大学",
                "pinyin": "dàxué",
                "pos": "n.",
                "meaning": {
                        "uz": "universitet, kollej",
                        "tj": "донишгоҳ, коллеҷ",
                        "ru": "университет, колледж"
                }
        },
        {
                "no": 4,
                "zh": "饭店",
                "pinyin": "fàndiàn",
                "pos": "n.",
                "meaning": {
                        "uz": "restoran, mehmonxona",
                        "tj": "тарабхона, меҳмонхона",
                        "ru": "ресторан, гостиница"
                }
        },
        {
                "no": 5,
                "zh": "出租车",
                "pinyin": "chūzūchē",
                "pos": "n.",
                "meaning": {
                        "uz": "taksi",
                        "tj": "такси",
                        "ru": "такси"
                }
        },
        {
                "no": 6,
                "zh": "一起",
                "pinyin": "yīqǐ",
                "pos": "adv.",
                "meaning": {
                        "uz": "birga",
                        "tj": "якҷоя",
                        "ru": "вместе"
                }
        },
        {
                "no": 7,
                "zh": "高兴",
                "pinyin": "gāoxìng",
                "pos": "adj.",
                "meaning": {
                        "uz": "xursand, xursand",
                        "tj": "шод, шод",
                        "ru": "счастлив, рад"
                }
        },
        {
                "no": 8,
                "zh": "听",
                "pinyin": "tīng",
                "pos": "v.",
                "meaning": {
                        "uz": "tinglamoq, eshitmoq",
                        "tj": "шунидан, шунидан",
                        "ru": "слушать, слышать"
                }
        },
        {
                "no": 9,
                "zh": "飞机",
                "pinyin": "fēijī",
                "pos": "n.",
                "meaning": {
                        "uz": "samolyot",
                        "tj": "ҳавопаймо",
                        "ru": "самолет"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Dasturxon yonida — qachon va qayerda tanishdingiz",
                        "tj": "Дар сари миз - кай ва дар куҷо вохӯрдед",
                        "ru": "За столом - когда и где вы встретились"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你和李小姐是什么时候认识的？",
                                "pinyin": "Nǐ hé Lǐ xiǎojiě shì shénme shíhou rènshi de?",
                                "translation": {
                                        "uz": "Miss Li bilan qachon uchrashgansiz?",
                                        "tj": "Шумо кай бо мисс Ли вохӯрдед?",
                                        "ru": "Когда вы познакомились с мисс Ли?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我们是2011年9月认识的。",
                                "pinyin": "Wǒmen shì èr líng yī yī nián jiǔ yuè rènshi de.",
                                "translation": {
                                        "uz": "Biz 2011 yil sentyabr oyida tanishgan edik.",
                                        "tj": "Мо моҳи сентябри соли 2011 вохӯрдем.",
                                        "ru": "Мы встретились в сентябре 2011 года."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "你们在哪儿认识的？",
                                "pinyin": "Nǐmen zài nǎr rènshi de?",
                                "translation": {
                                        "uz": "Ikkingiz qayerda uchrashdingiz?",
                                        "tj": "Ҳардуи шумо дар куҷо вохӯрдед?",
                                        "ru": "Где вы встретились?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我们是在学校认识的，她是我大学同学。",
                                "pinyin": "Wǒmen shì zài xuéxiào rènshi de, tā shì wǒ dàxué tóngxué.",
                                "translation": {
                                        "uz": "Biz maktabda uchrashdik; u mening universitet kursdoshim.",
                                        "tj": "Мо дар мактаб вохӯрдем; вай ҳамсинфи ман дар донишгоҳ аст.",
                                        "ru": "Мы встретились в школе; она моя однокурсница по университету."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Mehmonxona oldida — qanday keldingiz",
                        "tj": "Дар назди мехмонхона — чй хел омадй?",
                        "ru": "Перед отелем - как вы пришли?"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "你们是怎么来饭店的？",
                                "pinyin": "Nǐmen shì zěnme lái fàndiàn de?",
                                "translation": {
                                        "uz": "Restoranga qanday etib keldingiz?",
                                        "tj": "Чӣ тавр шумо ба тарабхона расидед?",
                                        "ru": "Как вы попали в ресторан?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我们是坐出租车来的。",
                                "pinyin": "Wǒmen shì zuò chūzūchē lái de.",
                                "translation": {
                                        "uz": "Biz taksida keldik.",
                                        "tj": "Мо бо такси омадем.",
                                        "ru": "Мы приехали на такси."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "李先生呢？",
                                "pinyin": "Lǐ xiānsheng ne?",
                                "translation": {
                                        "uz": "Janob Li haqida nima deyish mumkin?",
                                        "tj": "Дар бораи ҷаноби Ли чӣ гуфтан мумкин аст?",
                                        "ru": "А как насчет мистера Ли?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "他是和朋友一起开车来的。",
                                "pinyin": "Tā shì hé péngyou yīqǐ kāi chē lái de.",
                                "translation": {
                                        "uz": "U do'sti bilan birga mashinada keldi.",
                                        "tj": "Ӯ ҳамроҳи як дӯсташ бо мошин омад.",
                                        "ru": "Он приехал на машине вместе с другом."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Kompaniyada — samolyot bilan kelding",
                        "tj": "Дар корхона — шумо бо самолёт омадед",
                        "ru": "В компании - ты прилетел самолетом"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "很高兴认识您！李小姐。",
                                "pinyin": "Hěn gāoxìng rènshi nín! Lǐ xiǎojiě.",
                                "translation": {
                                        "uz": "Siz bilan tanishganimdan xursandman, miss Li!",
                                        "tj": "Бо шумо вохӯрдам, мисс Ли!",
                                        "ru": "Приятно познакомиться, мисс Ли!"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "认识你我也很高兴！",
                                "pinyin": "Rènshi nǐ wǒ yě hěn gāoxìng!",
                                "translation": {
                                        "uz": "Siz bilan tanishganimdan ham xursandman!",
                                        "tj": "Аз шиносоӣ бо шумо низ шодам!",
                                        "ru": "Мне тоже приятно познакомиться!"
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "听张先生说，您是坐飞机来北京的？",
                                "pinyin": "Tīng Zhāng xiānsheng shuō, nín shì zuò fēijī lái Běijīng de?",
                                "translation": {
                                        "uz": "Janob Chjan Pekinga samolyotda kelganingizni aytdimi?",
                                        "tj": "Чаноби Чжан кайд кард, ки шумо бо самолёт ба Пекин омадаед?",
                                        "ru": "Господин Чжан упомянул, что вы приехали в Пекин на самолете?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "是的。",
                                "pinyin": "Shì de.",
                                "translation": {
                                        "uz": "Bu to'g'ri.",
                                        "tj": "Ин дуруст аст.",
                                        "ru": "Это верно."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "是……的 — Vaqt, joy va usulni ta'kidlash",
                "explanation": {
                        "rule_uz": "y……y konstruksiya allaqachon sodir bo‘lgan harakatning vaqtini, joyini yoki uslubini ta’kidlash uchun ishlatiladi.\n\nTuzilishi:\nMavzu + mí + [Vaqt/Joy/Usul] + Fe'l + lín\n\nVaqtni ta'kidlash:\n2011 yīngīngīyīng — Biz 2011 yilda tanishganmiz.\n\nBelgilangan joy:\nlíngīngīngīngīngīngīnkīng — Biz maktabda uchrashdik.\n\nTa'kidlash usuli:\nlíngyǎngǎngyín — Men samolyotda keldim.\n\nInkor qilish: shīngī……lán\nlíngčičičičičičiči — Men taksida kelganim yo'q.",
                        "rule_tj": "Сохтмони 是……的 барои таъкид кардани вақт, ҷой ё тарзи амале, ки аллакай рух додааст, истифода мешавад.\n\nСохтор:\nМавзӯъ + 是 + [Вақт/Ҷой/тартиб] + Феъл + 的\n\nВақти таъкид:\n我们是2011年认识的。— Мо соли 2011 шинос шуда будем.\n\nҶои таъкид:\n我们是在学校认识的。— Мо дар мактаб вохӯрдем.\n\nТарзи таъкид:\n我是坐飞机来的。— Ман бо ҳавопаймо омадам.\n\nИнкор: 不是……的\n我不是坐出租车来的。— Ман бо такси наомадаам.",
                        "rule_ru": "Конструкция 是……的 используется для подчеркивания времени, места или способа уже произошедшего действия.\n\nСтруктура:\nТема + 是 + [Время/Место/Манера] + Глагол + 的\n\nПодчеркивая время:\n我们是2011年认识的。 — Мы познакомились в 2011 году.\n\nПодчеркивающее место:\n我们是在学校认识的。 — Мы познакомились в школе.\n\nПодчеркивающая манера:\n我是坐飞机来的。 — Я прилетел на самолете.\n\nОтрицание: 不是……的\n我不是坐出租车来的。 — Я приехал не на такси."
                },
                "examples": [
                        {
                                "zh": "我们是2011年认识的。",
                                "pinyin": "Wǒmen shì èr líng yī yī nián rènshi de.",
                                "meaning": {
                                        "uz": "Biz 2011 yilda tanishganmiz.",
                                        "tj": "Мо соли 2011 вохӯрдем.",
                                        "ru": "Мы встретились в 2011 году."
                                }
                        },
                        {
                                "zh": "我是坐飞机来的。",
                                "pinyin": "Wǒ shì zuò fēijī lái de.",
                                "meaning": {
                                        "uz": "Men samolyotda keldim.",
                                        "tj": "Ман бо ҳавопаймо омадам.",
                                        "ru": "Я прилетел на самолете."
                                }
                        },
                        {
                                "zh": "她是在北京买的。",
                                "pinyin": "Tā shì zài Běijīng mǎi de.",
                                "meaning": {
                                        "uz": "U uni Pekinda sotib olgan.",
                                        "tj": "Вай онро дар Пекин харидааст.",
                                        "ru": "Она купила его в Пекине."
                                }
                        },
                        {
                                "zh": "我们不是坐出租车来的。",
                                "pinyin": "Wǒmen bú shì zuò chūzūchē lái de.",
                                "meaning": {
                                        "uz": "Biz taksida kelmadik.",
                                        "tj": "Мо бо таксӣ наомадаем.",
                                        "ru": "Мы приехали не на такси."
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "日期的表达(2) — To'liq sana ifodalash",
                "explanation": {
                        "rule_uz": "Xitoy tilida to'liq sana kattadan eng kichik birlikka qarab ifodalanadi:\nYil + Oy + Kun + Haftaning kuni\n\nO'qish yillari: har bir raqam alohida o'qiladi\n2011 → yīngyīshīn (èr líng yī yī nián)\n2024 → yīngčiči (èr líng èr sì nián)\n\nTo'liq misol:\n2011-yil 9-mín 10ín，mēngjēng\n2011 yil, 10 sentyabr, chorshanba",
                        "rule_tj": "Дар чинӣ санаи пурра аз воҳиди калон то хурдтарин ифода карда мешавад:\nСол + моҳ + рӯз + рӯзи ҳафта\n\nСолҳои хониш: ҳар як рақам алоҳида хонда мешавад\n2011 → 二零一一年 (èr líng yī yī nián)\n2024 → 二零二四年 (èr líng èr sì nián)\n\nНамунаи пурра:\n2011 年9月10号，星期三\nСоли 2011, 10 сентябр, чоршанбе",
                        "rule_ru": "В китайском языке полная дата выражается от наибольшей к наименьшей единице:\nГод + Месяц + Число + День недели\n\nЧтение года: каждая цифра читается отдельно\n2011 → 二零一一年 (èr líng yī yī nián)\n2024 → 二零二四年 (èr líng èr sì nián)\n\nПолный пример:\n9 октября 2011 г., 10 октября 2011 г.\n2011 год, 10 сентября, среда"
                },
                "examples": [
                        {
                                "zh": "2011年9月认识的",
                                "pinyin": "èr líng yī yī nián jiǔ yuè rènshi de",
                                "meaning": {
                                        "uz": "2011 yil sentyabr oyida uchrashgan",
                                        "tj": "моҳи сентябри соли 2011 мулоқот карданд",
                                        "ru": "встретились в сентябре 2011 года"
                                }
                        },
                        {
                                "zh": "今天是2024年4月26号。",
                                "pinyin": "Jīntiān shì èr líng èr sì nián sì yuè èrshíliù hào.",
                                "meaning": {
                                        "uz": "Bugun 2024 yil 26 aprel.",
                                        "tj": "Имрӯз 26 апрели соли 2024.",
                                        "ru": "Сегодня 26 апреля 2024 года."
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
                        "uz": "Xitoy tilida yozing (kì……yáng yordamida):",
                        "tj": "Ба забони чинӣ нависед (бо истифода аз 是……的):",
                        "ru": "Напишите по-китайски (используя 是……的):"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "Biz 2011 yilda tanishganmiz.",
                                        "tj": "Мо соли 2011 вохӯрдем.",
                                        "ru": "Мы встретились в 2011 году."
                                },
                                "answer": "我们是2011年认识的。",
                                "pinyin": "Wǒmen shì èr líng yī yī nián rènshi de."
                        },
                        {
                                "prompt": {
                                        "uz": "Men samolyotda keldim.",
                                        "tj": "Ман бо ҳавопаймо омадам.",
                                        "ru": "Я прилетел на самолете."
                                },
                                "answer": "我是坐飞机来的。",
                                "pinyin": "Wǒ shì zuò fēijī lái de."
                        },
                        {
                                "prompt": {
                                        "uz": "Restoranga qanday etib keldingiz?",
                                        "tj": "Чӣ тавр шумо ба тарабхона расидед?",
                                        "ru": "Как вы попали в ресторан?"
                                },
                                "answer": "你是怎么来饭店的？",
                                "pinyin": "Nǐ shì zěnme lái fàndiàn de?"
                        },
                        {
                                "prompt": {
                                        "uz": "Biz taksida keldik.",
                                        "tj": "Мо бо такси омадем.",
                                        "ru": "Мы приехали на такси."
                                },
                                "answer": "我们是坐出租车来的。",
                                "pinyin": "Wǒmen shì zuò chūzūchē lái de."
                        },
                        {
                                "prompt": {
                                        "uz": "U do'sti bilan birga keldi.",
                                        "tj": "Ӯ бо як дӯсташ ҷамъ омад.",
                                        "ru": "Он пришел вместе с другом."
                                },
                                "answer": "他是和朋友一起来的。",
                                "pinyin": "Tā shì hé péngyou yīqǐ lái de."
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
                                "prompt": "你们___什么时候认识的？",
                                "answer": "是",
                                "pinyin": "shì"
                        },
                        {
                                "prompt": "我是坐飞机来___。",
                                "answer": "的",
                                "pinyin": "de"
                        },
                        {
                                "prompt": "他们是___学校认识的。",
                                "answer": "在",
                                "pinyin": "zài"
                        },
                        {
                                "prompt": "我不___坐出租车来的。",
                                "answer": "是",
                                "pinyin": "shì"
                        }
                ]
        },
        {
                "no": 3,
                "type": "emphasis",
                "instruction": {
                        "uz": "mí……yán yordamida urgʻu qoʻshing:",
                        "tj": "Бо истифода аз 是……的 таъкид илова кунед:",
                        "ru": "Добавьте акцент, используя 是……的:"
                },
                "items": [
                        {
                                "prompt": "我坐飞机来。(emphasise manner)",
                                "answer": "我是坐飞机来的。",
                                "pinyin": "Wǒ shì zuò fēijī lái de."
                        },
                        {
                                "prompt": "他们在北京认识。(emphasise place)",
                                "answer": "他们是在北京认识的。",
                                "pinyin": "Tāmen shì zài Běijīng rènshi de."
                        },
                        {
                                "prompt": "我2011年来中国。(emphasise time)",
                                "answer": "我是2011年来中国的。",
                                "pinyin": "Wǒ shì èr líng yī yī nián lái Zhōngguó de."
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "我们是2011年认识的。",
                        "我是坐飞机来的。",
                        "你是怎么来饭店的？",
                        "我们是坐出租车来的。",
                        "他是和朋友一起来的。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "是",
                        "的",
                        "在",
                        "是"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "我是坐飞机来的。",
                        "他们是在北京认识的。",
                        "我是2011年来中国的。"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "mí……yán yordamida oʻzingiz haqingizda 4 ta gap yozing:",
                        "tj": "Бо истифода аз 是……的 дар бораи худ 4 ҷумла нависед:",
                        "ru": "Напишите 4 предложения о себе, используя 是……的:"
                },
                "template": "我是___年___的。我是在___认识___的。我是坐___来___的。",
                "words": [
                        "是",
                        "的",
                        "在",
                        "年",
                        "坐",
                        "飞机",
                        "出租车",
                        "认识"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Do'stingizga hí……yán yordamida savollar bering:",
                        "tj": "Бо истифода аз 是……的 ба дӯсти худ саволҳо диҳед:",
                        "ru": "Задавайте вопросы другу, используя 是……的:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "Ikkingiz qachon uchrashdingiz?",
                                        "tj": "Ҳардуи шумо кай вохӯрдед?",
                                        "ru": "Когда вы встретились?"
                                },
                                "example": "你们是什么时候认识的？"
                        },
                        {
                                "prompt": {
                                        "uz": "Ikkingiz qayerda uchrashdingiz?",
                                        "tj": "Ҳардуи шумо дар куҷо вохӯрдед?",
                                        "ru": "Где вы встретились?"
                                },
                                "example": "你们是在哪儿认识的？"
                        },
                        {
                                "prompt": {
                                        "uz": "U bu erga qanday keldi?",
                                        "tj": "Чӣ тавр ӯ ба ин ҷо расид?",
                                        "ru": "Как он сюда попал?"
                                },
                                "example": "他是怎么来的？"
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
