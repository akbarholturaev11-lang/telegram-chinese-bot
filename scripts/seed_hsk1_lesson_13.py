import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk1",
    "lesson_order": 13,
    "lesson_code": "HSK1-L13",
    "title": "他在学做中国菜呢",
    "goal": {
        "uz": "Davom etilayotgan harakatlarni ifodalash (k...kì), telefon raqamlari va zarrachalar",
        "tj": "Ифодаи амалҳои ҷорӣ (在...呢), рақамҳои телефон ва заррача 吧",
        "ru": "Выражает текущие действия (在...呢), номера телефонов и частицу 吧."
    },
    "intro_text": {
        "uz": "O'n uchinchi darsda siz hozir sodir bo'layotgan harakatlarni qanday ifodalashni o'rganasiz. 10 ta yangi so'z, 3 ta dialog.",
        "tj": "Дар дарси сездаҳум шумо тарзи ифода кардани амалҳои ҳозира рӯйдодаро меомӯзед, сохтани 在...呢 ва заррачаи 吧-ро истифода баред. 10 калимаи нав, 3 муколама.",
        "ru": "На тринадцатом уроке вы научитесь выражать действия, происходящие прямо сейчас, используя конструкцию 在...呢 и частицу 吧. 10 новых слов, 3 диалога."
    },

    "vocabulary_json": json.dumps([
        {
                "no": 1,
                "zh": "喂",
                "pinyin": "wèi",
                "pos": "int.",
                "meaning": {
                        "uz": "salom (telefonda)",
                        "tj": "салом (бо телефон)",
                        "ru": "здравствуйте (по телефону)"
                }
        },
        {
                "no": 2,
                "zh": "也",
                "pinyin": "yě",
                "pos": "adv.",
                "meaning": {
                        "uz": "shuningdek, ham",
                        "tj": "инчунин, инчунин",
                        "ru": "также, тоже"
                }
        },
        {
                "no": 3,
                "zh": "学习",
                "pinyin": "xuéxí",
                "pos": "v.",
                "meaning": {
                        "uz": "o'rganish, o'rganish",
                        "tj": "омӯхтан, омӯхтан",
                        "ru": "учиться, учиться"
                }
        },
        {
                "no": 4,
                "zh": "上午",
                "pinyin": "shàngwǔ",
                "pos": "n.",
                "meaning": {
                        "uz": "ertalab (peshindan oldin)",
                        "tj": "субҳ (пеш аз нисфирӯзӣ)",
                        "ru": "утро (до полудня)"
                }
        },
        {
                "no": 5,
                "zh": "睡觉",
                "pinyin": "shuì jiào",
                "pos": "v.",
                "meaning": {
                        "uz": "uxlash",
                        "tj": "хобидан",
                        "ru": "спать"
                }
        },
        {
                "no": 6,
                "zh": "电视",
                "pinyin": "diànshì",
                "pos": "n.",
                "meaning": {
                        "uz": "televizor",
                        "tj": "телевизион",
                        "ru": "телевидение"
                }
        },
        {
                "no": 7,
                "zh": "喜欢",
                "pinyin": "xǐhuan",
                "pos": "v.",
                "meaning": {
                        "uz": "yoqtirmoq, zavqlanmoq",
                        "tj": "писанд омадан, лаззат бурдан",
                        "ru": "нравиться, наслаждаться"
                }
        },
        {
                "no": 8,
                "zh": "给",
                "pinyin": "gěi",
                "pos": "prep.",
                "meaning": {
                        "uz": "uchun, (kimdir) uchun",
                        "tj": "ба, барои (касе)",
                        "ru": "чтобы, для (кого-то)"
                }
        },
        {
                "no": 9,
                "zh": "打电话",
                "pinyin": "dǎ diànhuà",
                "pos": "v.",
                "meaning": {
                        "uz": "qo'ng'iroq qilish uchun",
                        "tj": "телефон кардан",
                        "ru": "позвонить по телефону"
                }
        },
        {
                "no": 10,
                "zh": "吧",
                "pinyin": "ba",
                "pos": "part.",
                "meaning": {
                        "uz": "takliflar yoki yumshoq buyruqlar uchun yumshatuvchi zarracha",
                        "tj": "зарраҳои нармкунанда барои пешниҳодҳо ё фармонҳои ҳалим",
                        "ru": "смягчающая частица для предложений или мягких команд"
                }
        }
], ensure_ascii=False),

    "dialogue_json": json.dumps([
        {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": {
                        "uz": "Telefonda — hozir nima qilyapsan",
                        "tj": "Дар телефон - шумо ҳоло чӣ кор карда истодаед?",
                        "ru": "По телефону - что ты сейчас делаешь?"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "喂，你在做什么呢？",
                                "pinyin": "Wèi, nǐ zài zuò shénme ne?",
                                "translation": {
                                        "uz": "Salom, hozir nima qilyapsiz?",
                                        "tj": "Салом, шумо ҳоло чӣ кор карда истодаед?",
                                        "ru": "Привет, чем ты сейчас занимаешься?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我在看书呢。",
                                "pinyin": "Wǒ zài kàn shū ne.",
                                "translation": {
                                        "uz": "Men hozir kitob o'qiyapman.",
                                        "tj": "Ман ҳозир китоб хонда истодаам.",
                                        "ru": "Я сейчас читаю книгу."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "大卫也在看书吗？",
                                "pinyin": "Dàwèi yě zài kàn shū ma?",
                                "translation": {
                                        "uz": "Dovud ham o'qiyaptimi?",
                                        "tj": "Оё Довуд низ мехонад?",
                                        "ru": "Дэвид тоже читает?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "他没看书，他在学做中国菜呢。",
                                "pinyin": "Tā méi kàn shū, tā zài xué zuò Zhōngguó cài ne.",
                                "translation": {
                                        "uz": "U o'qimaydi; u xitoy taomlarini pishirishni o'rganmoqda.",
                                        "tj": "Ӯ намехонад; пухтани таомхои хитоиро меомузад.",
                                        "ru": "Он не читает; он учится готовить китайскую еду."
                                }
                        }
                ]
        },
        {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": {
                        "uz": "Qahvaxonada — kecha nima qilding",
                        "tj": "Дар кафе — дируз чй кор кардй",
                        "ru": "В кафе - что ты делал вчера?"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "昨天上午你在做什么呢？",
                                "pinyin": "Zuótiān shàngwǔ nǐ zài zuò shénme ne?",
                                "translation": {
                                        "uz": "Kecha ertalab nima qilardingiz?",
                                        "tj": "Субҳи дирӯз шумо чӣ кор мекардед?",
                                        "ru": "Что ты делал вчера утром?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我在睡觉呢。你呢？",
                                "pinyin": "Wǒ zài shuì jiào ne. Nǐ ne?",
                                "translation": {
                                        "uz": "Uxlayotgandim. Sizchi?",
                                        "tj": "Ман хоб будам. Шумо чӣ?",
                                        "ru": "Я спал. А вы?"
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "我在家看电视呢。你喜欢看电视吗？",
                                "pinyin": "Wǒ zài jiā kàn diànshì ne. Nǐ xǐhuan kàn diànshì ma?",
                                "translation": {
                                        "uz": "Men uyda televizor ko'rayotgan edim. Televizor ko'rishni yoqtirasizmi?",
                                        "tj": "Ман дар хона телевизор тамошо мекардам. Оё шумо тамошои телевизорро дӯст медоред?",
                                        "ru": "Я смотрел телевизор дома. Тебе нравится смотреть телевизор?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "我不喜欢看电视，我喜欢看电影。",
                                "pinyin": "Wǒ bù xǐhuan kàn diànshì, wǒ xǐhuan kàn diànyǐng.",
                                "translation": {
                                        "uz": "Men televizor ko'rishni yoqtirmayman; Men kino tomosha qilishni yaxshi ko'raman.",
                                        "tj": "Ман тамошои телевизорро дӯст намедорам; Ман тамошои филмҳоро дӯст медорам.",
                                        "ru": "Я не люблю смотреть телевизор; Мне нравится смотреть фильмы."
                                }
                        }
                ]
        },
        {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": {
                        "uz": "Maktab ofisida — telefon raqami",
                        "tj": "Рақами телефон дар идораи мактаб",
                        "ru": "Телефон в офисе школы"
                },
                "dialogue": [
                        {
                                "speaker": "A",
                                "zh": "82304155，这是李老师的电话吗？",
                                "pinyin": "Bā èr sān líng sì yāo wǔ wǔ, zhè shì Lǐ lǎoshī de diànhuà ma?",
                                "translation": {
                                        "uz": "82304155, bu Li domlaning telefon raqamimi?",
                                        "tj": "82304155, ин рақами телефони муаллим Ли аст?",
                                        "ru": "82304155, это номер телефона Учителя Ли?"
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "不是。她的电话是82304156。",
                                "pinyin": "Bú shì. Tā de diànhuà shì bā èr sān líng sì yāo wǔ liù.",
                                "translation": {
                                        "uz": "Yo'q. Uning raqami 82304156.",
                                        "tj": "Не Рақами вай 82304156 аст.",
                                        "ru": "Нет. Ее номер 82304156."
                                }
                        },
                        {
                                "speaker": "A",
                                "zh": "好，我现在给她打电话。",
                                "pinyin": "Hǎo, wǒ xiànzài gěi tā dǎ diànhuà.",
                                "translation": {
                                        "uz": "OK, men unga hozir qo'ng'iroq qilaman.",
                                        "tj": "Хуб, ман ҳоло ба ӯ занг мезанам.",
                                        "ru": "Хорошо, я позвоню ей сейчас."
                                }
                        },
                        {
                                "speaker": "B",
                                "zh": "她在工作呢，你下午打吧。",
                                "pinyin": "Tā zài gōngzuò ne, nǐ xiàwǔ dǎ ba.",
                                "translation": {
                                        "uz": "U hozir ishlayapti; tushdan keyin qo'ng'iroq qiling.",
                                        "tj": "Вай хозир кор мекунад; нисфирӯзӣ занг занед.",
                                        "ru": "Она сейчас работает; позвони во второй половине дня."
                                }
                        }
                ]
        }
], ensure_ascii=False),

    "grammar_json": json.dumps([
        {
                "no": 1,
                "title_zh": "在……呢 — Hozirgi davom harakat",
                "explanation": {
                        "rule_uz": "Hozir bajarilayotgan amal uchun:\n1-tarkibiy tuzilma: nà + fe'l (+ ob'ekt)\n2-tuzilma: Fe'l + Ob'ekt + l\n3-tarkibiy tuzilma: mán + fe'l + lí (ta'kidli)\n\nMisol:\nmíngjīngjđဂ— Men hozir kitob o‘qiyapman.\nchàngāngāngāngāngāngī-U xitoy taomlarini pishirishni o'rganmoqda.\n\nInkor qilish: mí(yàng) + fe'l, no lí\nchàngāngīnī - U o'qimayapti.\nchàngàngìnīng — Ular ishlamayapti.",
                        "rule_tj": "Барои амале, ки ҳоло иҷро мешавад:\nСохтори 1: 在 + Феъл (+ Объект)\nСохтори 2: Феъл + Объект + 呢\nСохтори 3: 在 + Феъл + 呢 (таъкиднок)\n\nМисол:\n我在看书呢。— Ман ҳозир китоб мехонам.\n他在学做中国菜呢。— Вай пухтани таомҳои чиниро меомӯзад.\n\nИнкор: 没(在) + Феъл, нест 呢\n他没看书。— Вай намехонад.\n他们没在工作。— Онҳо кор намекунанд.",
                        "rule_ru": "Для действия, которое происходит прямо сейчас:\nСтруктура 1: 在 + глагол (+ объект)\nСтруктура 2: Глагол + Объект +呢\nСтруктура 3: 在 + глагол + 呢 (ударное слово)\n\nПример:\n我在看书呢。 — Я сейчас читаю книгу.\n他在学做中国菜呢。 — Он учится готовить китайскую еду.\n\nОтрицание: 没(在) + глагол, нет 呢.\n他没看书。 — Он не читает.\n他们没在工作。 — Они не работают."
                },
                "examples": [
                        {
                                "zh": "我在看书呢。",
                                "pinyin": "Wǒ zài kàn shū ne.",
                                "meaning": {
                                        "uz": "Men hozir kitob o'qiyapman.",
                                        "tj": "Ман ҳозир китоб хонда истодаам.",
                                        "ru": "Я сейчас читаю книгу."
                                }
                        },
                        {
                                "zh": "他在学做中国菜呢。",
                                "pinyin": "Tā zài xué zuò Zhōngguó cài ne.",
                                "meaning": {
                                        "uz": "U xitoy taomlarini pishirishni o'rganmoqda.",
                                        "tj": "У пухтани таомхои чиниро меомузад.",
                                        "ru": "Он учится готовить китайскую еду."
                                }
                        },
                        {
                                "zh": "她没在工作。",
                                "pinyin": "Tā méi zài gōngzuò.",
                                "meaning": {
                                        "uz": "U ishlamayapti.",
                                        "tj": "Вай кор намекунад.",
                                        "ru": "Она не работает."
                                }
                        }
                ]
        },
        {
                "no": 2,
                "title_zh": "也 — Ham ravishi",
                "explanation": {
                        "rule_uz": "yě(yě) — ‘shuningdek’ ma’nosini bildiradi.\nHar doim fe'l yoki modal fe'ldan oldin keladi.\n\nMisol:\ndàngāngīngīngīn？— Devid ham o‘qiyaptimi?\nmíngzhínjínjēng— Men ham film tomosha qilishni yaxshi koʻraman.\nmìnìnìnhì- U ham oʻqituvchi.",
                        "rule_tj": "也(yě) — маънои «инчунин» мебошад.\nҲамеша пеш аз феъл ё феъли модалӣ меояд.\n\nМисол:\n大卫也在看书吗？— Оё Довуд низ мехонад?\n我也喜欢看电影。— Ман ҳам тамошои филмҳоро дӯст медорам.\n她也是老师。— Вай хам муаллим аст.",
                        "rule_ru": "也(yě) — означает «тоже тоже».\nВсегда стоит перед глаголом или модальным глаголом.\n\nПример:\n大卫也在看书吗？ — Дэвид тоже читает?\n我也喜欢看电影。 — Еще я люблю смотреть фильмы.\n她也是老师。 — Она еще и учительница."
                },
                "examples": [
                        {
                                "zh": "大卫也在看书吗？",
                                "pinyin": "Dàwèi yě zài kàn shū ma?",
                                "meaning": {
                                        "uz": "Dovud ham o'qiyaptimi?",
                                        "tj": "Оё Довуд низ мехонад?",
                                        "ru": "Дэвид тоже читает?"
                                }
                        },
                        {
                                "zh": "我也喜欢中国菜。",
                                "pinyin": "Wǒ yě xǐhuan Zhōngguó cài.",
                                "meaning": {
                                        "uz": "Menga xitoy taomlari ham yoqadi.",
                                        "tj": "Ман инчунин хӯрокҳои чиниро дӯст медорам.",
                                        "ru": "Еще мне нравится китайская еда."
                                }
                        },
                        {
                                "zh": "她也是学生。",
                                "pinyin": "Tā yě shì xuésheng.",
                                "meaning": {
                                        "uz": "U ham talaba.",
                                        "tj": "Вай хам студент аст.",
                                        "ru": "Она тоже студентка."
                                }
                        }
                ]
        },
        {
                "no": 3,
                "title_zh": "吧 — Yumshatuvchi yukla",
                "explanation": {
                        "rule_uz": "lí(ba) — taklif, maslahat yoki yumshatilgan buyruqni bildiradi.\nGap oxirida keladi.\n\nMisol:\nshìnghànghàn — Tushdan keyin qo‘ng‘iroq qiling.\nchàngàngàngìnìnìnīng — Bugun uyda ovqatlanaylik.\nlínìnīk — Iltimos, joy oling.",
                        "rule_tj": "吧(ba) - пешниҳод, маслиҳат ё фармони нармшударо ифода мекунад.\nДар охири ҷумла меояд.\n\nМисол:\n你下午打吧。 — Нимаи дуюми рӯз занг занед.\n今天我们在家吃饭吧。— Имрӯз дар хона хӯрок мехӯрем.\n请坐吧。— Лутфан ҷой гиред.",
                        "rule_ru": "吧(ба) — выражает предложение, совет или смягченную команду.\nСтоит в конце предложения.\n\nПример:\n你下午打吧。 — Позвоните днем.\n今天我们在家吃饭吧。 — Давай сегодня поедим дома.\n请坐吧。 — Присаживайтесь, пожалуйста."
                },
                "examples": [
                        {
                                "zh": "你下午打吧。",
                                "pinyin": "Nǐ xiàwǔ dǎ ba.",
                                "meaning": {
                                        "uz": "Peshindan keyin qo'ng'iroq qiling.",
                                        "tj": "Нимаи нисфирӯзӣ занг занед.",
                                        "ru": "Позвоните во второй половине дня."
                                }
                        },
                        {
                                "zh": "我们一起去吧。",
                                "pinyin": "Wǒmen yīqǐ qù ba.",
                                "meaning": {
                                        "uz": "Keling, birga boraylik.",
                                        "tj": "Биёед якҷоя равем.",
                                        "ru": "Давайте пойдем вместе."
                                }
                        },
                        {
                                "zh": "请坐吧。",
                                "pinyin": "Qǐng zuò ba.",
                                "meaning": {
                                        "uz": "Iltimos, joy oling.",
                                        "tj": "Лутфан нишастед.",
                                        "ru": "Пожалуйста, присаживайтесь."
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
                                        "uz": "Hozir nima bilan bandsiz?",
                                        "tj": "Шумо ҳозир чи кор карда истодаед?",
                                        "ru": "Что ты сейчас делаешь?"
                                },
                                "answer": "你在做什么呢？",
                                "pinyin": "Nǐ zài zuò shénme ne?"
                        },
                        {
                                "prompt": {
                                        "uz": "Men hozir kitob o'qiyapman.",
                                        "tj": "Ман ҳозир китоб хонда истодаам.",
                                        "ru": "Я сейчас читаю книгу."
                                },
                                "answer": "我在看书呢。",
                                "pinyin": "Wǒ zài kàn shū ne."
                        },
                        {
                                "prompt": {
                                        "uz": "U ishlamayapti.",
                                        "tj": "Вай кор намекунад.",
                                        "ru": "Он не работает."
                                },
                                "answer": "他没在工作。",
                                "pinyin": "Tā méi zài gōngzuò."
                        },
                        {
                                "prompt": {
                                        "uz": "Men ham kino tomosha qilishni yaxshi ko'raman.",
                                        "tj": "Ман ҳам тамошои филмҳоро дӯст медорам.",
                                        "ru": "Я также люблю смотреть фильмы."
                                },
                                "answer": "我也喜欢看电影。",
                                "pinyin": "Wǒ yě xǐhuan kàn diànyǐng."
                        },
                        {
                                "prompt": {
                                        "uz": "Men unga hozir qo'ng'iroq qilaman.",
                                        "tj": "Ман ҳоло ба ӯ занг мезанам.",
                                        "ru": "Я позвоню ей сейчас."
                                },
                                "answer": "我现在给她打电话。",
                                "pinyin": "Wǒ xiànzài gěi tā dǎ diànhuà."
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
                                "prompt": "我___看书呢。",
                                "answer": "在",
                                "pinyin": "zài"
                        },
                        {
                                "prompt": "大卫___在看书吗？",
                                "answer": "也",
                                "pinyin": "yě"
                        },
                        {
                                "prompt": "他没___书，他在学做菜呢。",
                                "answer": "看",
                                "pinyin": "kàn"
                        },
                        {
                                "prompt": "你下午打___。",
                                "answer": "吧",
                                "pinyin": "ba"
                        }
                ]
        },
        {
                "no": 3,
                "type": "phone_numbers",
                "instruction": {
                        "uz": "Telefon raqamlarini xitoy tilida ovoz chiqarib o'qing:",
                        "tj": "Рақамҳои телефонро бо овози баланд бо забони чинӣ хонед:",
                        "ru": "Прочитайте вслух номера телефонов на китайском языке:"
                },
                "items": [
                        {
                                "prompt": {
                                        "uz": "8069478",
                                        "tj": "8069478",
                                        "ru": "8069478"
                                },
                                "answer": "bā líng liù jiǔ sì qī bā"
                        },
                        {
                                "prompt": {
                                        "uz": "13851897623",
                                        "tj": "13851897623",
                                        "ru": "13851897623"
                                },
                                "answer": "yāo sān bā wǔ yāo bā jiǔ liù èr sān"
                        },
                        {
                                "prompt": {
                                        "uz": "82304156",
                                        "tj": "82304156",
                                        "ru": "82304156"
                                },
                                "answer": "bā èr sān líng sì yāo wǔ liù"
                        }
                ]
        }
], ensure_ascii=False),

    "answers_json": json.dumps([
        {
                "no": 1,
                "answers": [
                        "你在做什么呢？",
                        "我在看书呢。",
                        "他没在工作。",
                        "我也喜欢看电影。",
                        "我现在给她打电话。"
                ]
        },
        {
                "no": 2,
                "answers": [
                        "在",
                        "也",
                        "看",
                        "吧"
                ]
        },
        {
                "no": 3,
                "answers": [
                        "bā líng liù jiǔ sì qī bā",
                        "yāo sān bā wǔ yāo bā jiǔ liù èr sān",
                        "bā èr sān líng sì yāo wǔ liù"
                ]
        }
], ensure_ascii=False),

    "homework_json": json.dumps([
        {
                "no": 1,
                "instruction": {
                        "uz": "Kecha ertalab nima qilardingiz? 3-4 gap yozing:",
                        "tj": "Субҳи дирӯз шумо чӣ кор мекардед? 3-4 ҷумла нависед:",
                        "ru": "Что ты делал вчера утром? Напишите 3–4 предложения:"
                },
                "template": "昨天上午我在___呢。我___喜欢___。",
                "words": [
                        "在",
                        "呢",
                        "也",
                        "喜欢",
                        "看书",
                        "看电视",
                        "睡觉",
                        "学习"
                ]
        },
        {
                "no": 2,
                "instruction": {
                        "uz": "Do'stingiz bilan telefon qo'ng'irog'i dialogini yozing (4 qator, l harfi bilan boshlang):",
                        "tj": "Бо дӯстатон муколамаи занги телефонӣ нависед (4 сатр, бо 喂 оғоз кунед):",
                        "ru": "Напишите диалог телефонного разговора с другом (4 строки, начинаются с 喂):"
                },
                "example": "A: 喂，你在做什么呢？\nB: 我在___呢。\nA: ___也在___吗？\nB: 她___，她在___呢。"
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
