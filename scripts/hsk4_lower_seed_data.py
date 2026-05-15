import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON_DATA = {
    12: {
        "title": "用心发现世界",
        "topic": {
            "uz": "hayotdagi muammolarni kuzatish va yangi yechim topish",
            "ru": "наблюдать жизнь и находить новые решения",
            "tj": "мушоҳидаи зиндагӣ ва ёфтани роҳҳои нави ҳал",
        },
        "grammar": ["并且", "对于", "总算", "偶尔", "弄"],
        "vocab": [
            ("规定", "guīdìng", "n./v.", "qoida, belgilamoq", "правило; устанавливать", "қоида; муқаррар кардан"),
            ("经验", "jīngyàn", "n.", "tajriba", "опыт", "таҷриба"),
            ("可惜", "kěxī", "adj.", "afsus, achinarli", "жаль, досадно", "афсӯс, дареғ"),
            ("全部", "quánbù", "n./adv.", "hammasi, butunlay", "всё, полностью", "ҳама, пурра"),
            ("也许", "yěxǔ", "adv.", "balki, ehtimol", "возможно, может быть", "шояд, эҳтимол"),
            ("商量", "shāngliang", "v.", "maslahatlashmoq", "советоваться, обсуждать", "маслиҳат кардан"),
            ("盐", "yán", "n.", "tuz", "соль", "намак"),
            ("保护", "bǎohù", "v.", "himoya qilmoq", "защищать", "ҳимоя кардан"),
            ("作用", "zuòyòng", "n.", "ta'sir, rol", "роль, эффект", "таъсир, нақш"),
            ("无法", "wúfǎ", "v.", "qila olmaslik", "не мочь, невозможно", "натавонистан"),
            ("总结", "zǒngjié", "v.", "xulosa qilmoq", "подводить итог", "хулоса кардан"),
            ("叶子", "yèzi", "n.", "barg", "лист", "барг"),
        ],
    },
    13: {
        "title": "喝着茶看京剧",
        "topic": {
            "uz": "xitoy madaniyati, Pekin operasi va an'analar",
            "ru": "китайская культура, пекинская опера и традиции",
            "tj": "фарҳанги чинӣ, операи Пекин ва анъанаҳо",
        },
        "grammar": ["大概", "着", "由", "进行", "随着"],
        "vocab": [
            ("京剧", "jīngjù", "n.", "Pekin operasi", "пекинская опера", "операи Пекин"),
            ("表演", "biǎoyǎn", "v./n.", "ijro etmoq, tomosha", "выступать; представление", "иҷро кардан; намоиш"),
            ("观众", "guānzhòng", "n.", "tomoshabin", "зритель", "тамошобин"),
            ("茶馆", "cháguǎn", "n.", "choyxona", "чайная", "чойхона"),
            ("大概", "dàgài", "adv.", "taxminan, ehtimol", "примерно, вероятно", "тақрибан, эҳтимол"),
            ("随着", "suízhe", "prep.", "... bilan birga", "по мере, вслед за", "бо гузашти, ҳамроҳи"),
            ("传统", "chuántǒng", "n./adj.", "an'ana, an'anaviy", "традиция, традиционный", "анъана, анъанавӣ"),
            ("文化", "wénhuà", "n.", "madaniyat", "культура", "фарҳанг"),
            ("进行", "jìnxíng", "v.", "olib bormoq, davom etmoq", "проводить, осуществлять", "гузарондан, иҷро кардан"),
            ("由", "yóu", "prep.", "tomonidan, ...dan", "кем-либо, от", "аз тарафи, аз"),
            ("脸谱", "liǎnpǔ", "n.", "opera yuz bo'yog'i", "театральный грим", "ороиши рӯйи саҳнавӣ"),
            ("艺术", "yìshù", "n.", "san'at", "искусство", "санъат"),
        ],
    },
    14: {
        "title": "保护地球母亲",
        "topic": {
            "uz": "atrof-muhitni himoya qilish va mas'uliyat",
            "ru": "защита окружающей среды и ответственность",
            "tj": "ҳифзи муҳити зист ва масъулият",
        },
        "grammar": ["够", "以", "既然", "于是", "什么的"],
        "vocab": [
            ("地球", "dìqiú", "n.", "Yer sayyorasi", "Земля, планета", "Замин, сайёра"),
            ("母亲", "mǔqīn", "n.", "ona", "мать", "модар"),
            ("环境", "huánjìng", "n.", "muhit", "окружающая среда", "муҳит"),
            ("污染", "wūrǎn", "v./n.", "ifloslanish, iflos qilmoq", "загрязнять; загрязнение", "ифлос кардан; ифлосшавӣ"),
            ("垃圾", "lājī", "n.", "chiqindi", "мусор", "партов"),
            ("节约", "jiéyuē", "v.", "tejamoq", "экономить", "сарфа кардан"),
            ("浪费", "làngfèi", "v.", "isrof qilmoq", "тратить впустую", "исроф кардан"),
            ("森林", "sēnlín", "n.", "o'rmon", "лес", "ҷангал"),
            ("既然", "jìrán", "conj.", "modomiki, ekan", "раз уж, поскольку", "модом ки"),
            ("于是", "yúshì", "conj.", "shundan keyin, natijada", "поэтому, тогда", "пас, бинобар ин"),
            ("足够", "zúgòu", "adj.", "yetarli", "достаточный", "кифоя, басанда"),
            ("责任", "zérèn", "n.", "mas'uliyat", "ответственность", "масъулият"),
        ],
    },
    15: {
        "title": "教育孩子的艺术",
        "topic": {
            "uz": "bolalarni tarbiyalashda muloqot va sabr",
            "ru": "общение и терпение в воспитании детей",
            "tj": "муошират ва сабр дар тарбияи кӯдакон",
        },
        "grammar": ["想起来", "弄", "千万", "来", "左右"],
        "vocab": [
            ("教育", "jiàoyù", "v./n.", "tarbiya bermoq, ta'lim", "воспитывать; образование", "тарбия кардан; маориф"),
            ("孩子", "háizi", "n.", "bola", "ребёнок", "кӯдак"),
            ("艺术", "yìshù", "n.", "san'at", "искусство", "санъат"),
            ("耐心", "nàixīn", "n./adj.", "sabr, sabrli", "терпение, терпеливый", "сабр, босабр"),
            ("想起来", "xiǎngqilai", "v.", "esiga tushmoq", "вспомнить", "ба ёд овардан"),
            ("弄", "nòng", "v.", "qilmoq, boshqarmoq", "делать, устраивать", "кардан, дуруст кардан"),
            ("千万", "qiānwàn", "adv.", "albatta, zinhor", "обязательно, ни в коем случае", "ҳатман, зинҳор"),
            ("左右", "zuǒyòu", "adv.", "atrofida, taxminan", "около, примерно", "тақрибан"),
            ("尊重", "zūnzhòng", "v.", "hurmat qilmoq", "уважать", "эҳтиром кардан"),
            ("鼓励", "gǔlì", "v.", "rag'batlantirmoq", "поощрять", "ҳавасманд кардан"),
            ("批评", "pīpíng", "v./n.", "tanqid qilmoq", "критиковать", "танқид кардан"),
            ("责任", "zérèn", "n.", "javobgarlik", "ответственность", "масъулият"),
        ],
    },
    16: {
        "title": "生活可以更美好",
        "topic": {
            "uz": "kundalik hayotni yaxshilash va jamoat odobi",
            "ru": "улучшение повседневной жизни и общественная вежливость",
            "tj": "беҳтар кардани зиндагии рӯзмарра ва одоби ҷамъиятӣ",
        },
        "grammar": ["了", "乱扔", "到底", "拿……来说", "趁"],
        "vocab": [
            ("生活", "shēnghuó", "n./v.", "hayot, yashamoq", "жизнь, жить", "зиндагӣ, зистан"),
            ("美好", "měihǎo", "adj.", "go'zal, yaxshi", "прекрасный", "зебо, хуб"),
            ("乱扔", "luànrēng", "v.", "har joyga tashlamoq", "бросать где попало", "ҳар ҷо партофтан"),
            ("垃圾", "lājī", "n.", "chiqindi", "мусор", "партов"),
            ("到底", "dàodǐ", "adv.", "axir, aslida", "в конце концов, всё-таки", "охир, дар асл"),
            ("公共", "gōnggòng", "adj.", "jamoatga oid", "общественный", "ҷамъиятӣ"),
            ("礼貌", "lǐmào", "n./adj.", "odob, odobli", "вежливость, вежливый", "одоб, боадаб"),
            ("排队", "páiduì", "v.", "navbatda turmoq", "стоять в очереди", "дар навбат истодан"),
            ("交通", "jiāotōng", "n.", "transport, yo'l harakati", "транспорт, движение", "нақлиёт, ҳаракат"),
            ("影响", "yǐngxiǎng", "v./n.", "ta'sir qilmoq", "влиять; влияние", "таъсир кардан"),
            ("改变", "gǎibiàn", "v.", "o'zgartirmoq", "изменять", "тағйир додан"),
            ("趁", "chèn", "prep.", "...dan foydalanib", "воспользовавшись", "истифода бурда"),
        ],
    },
    17: {
        "title": "人与自然",
        "topic": {
            "uz": "inson va tabiat o'rtasidagi muvozanat",
            "ru": "равновесие между человеком и природой",
            "tj": "тавозуни инсон ва табиат",
        },
        "grammar": ["到", "下", "想", "为了……而……", "仍然"],
        "vocab": [
            ("自然", "zìrán", "n./adj.", "tabiat, tabiiy", "природа; естественный", "табиат; табиӣ"),
            ("关系", "guānxi", "n.", "munosabat, aloqa", "отношение, связь", "муносибат, робита"),
            ("动物", "dòngwù", "n.", "hayvon", "животное", "ҳайвон"),
            ("植物", "zhíwù", "n.", "o'simlik", "растение", "растанӣ"),
            ("破坏", "pòhuài", "v.", "buzmoq, vayron qilmoq", "разрушать", "вайрон кардан"),
            ("保护", "bǎohù", "v.", "himoya qilmoq", "защищать", "ҳимоя кардан"),
            ("平衡", "pínghéng", "n./adj.", "muvozanat", "равновесие", "тавозун"),
            ("发展", "fāzhǎn", "v./n.", "rivojlanmoq", "развиваться; развитие", "рушд кардан"),
            ("仍然", "réngrán", "adv.", "hali ham, baribir", "по-прежнему, всё ещё", "ҳанӯз ҳам"),
            ("为了", "wèile", "prep.", "uchun, maqsadida", "для, ради", "барои"),
            ("减少", "jiǎnshǎo", "v.", "kamaytirmoq", "уменьшать", "кам кардан"),
            ("未来", "wèilái", "n.", "kelajak", "будущее", "оянда"),
        ],
    },
    18: {
        "title": "科技与世界",
        "topic": {
            "uz": "texnologiya dunyoni qanday o'zgartirishi",
            "ru": "как технологии меняют мир",
            "tj": "чӣ гуна технология ҷаҳонро тағйир медиҳад",
        },
        "grammar": ["爱", "免不了", "并非", "表示", "一旦"],
        "vocab": [
            ("科技", "kējì", "n.", "fan-texnika", "наука и техника", "илму технология"),
            ("世界", "shìjiè", "n.", "dunyo", "мир", "ҷаҳон"),
            ("网络", "wǎngluò", "n.", "internet tarmog'i", "сеть, интернет", "шабака, интернет"),
            ("信息", "xìnxī", "n.", "ma'lumot", "информация", "маълумот"),
            ("现代", "xiàndài", "n./adj.", "zamonaviy", "современный", "муосир"),
            ("方便", "fāngbiàn", "adj.", "qulay", "удобный", "қулай"),
            ("交流", "jiāoliú", "v./n.", "muloqot, almashuv", "общаться; обмен", "муошират; мубодила"),
            ("发明", "fāmíng", "v./n.", "ixtiro qilmoq", "изобретать; изобретение", "ихтироъ кардан"),
            ("研究", "yánjiū", "v./n.", "tadqiq qilmoq", "исследовать", "тадқиқ кардан"),
            ("表示", "biǎoshì", "v.", "bildirmoq, ifodalamoq", "выражать, указывать", "ифода кардан"),
            ("并非", "bìngfēi", "adv.", "mutlaqo emas", "вовсе не", "ҳеҷ нест"),
            ("一旦", "yídàn", "conj.", "agar bir kuni, ...sa", "как только, если вдруг", "агар, вақте ки"),
        ],
    },
    19: {
        "title": "生活的味道",
        "topic": {
            "uz": "hayotning ta'mi, tajriba va munosabat",
            "ru": "вкус жизни, опыт и отношение",
            "tj": "маззаи зиндагӣ, таҷриба ва муносибат",
        },
        "grammar": ["就不用说", "上", "由来", "总的来说", "在于"],
        "vocab": [
            ("味道", "wèidào", "n.", "ta'm, hid", "вкус, запах", "мазза, бӯй"),
            ("酸甜苦辣", "suān tián kǔ là", "idiom", "hayotning turli achchiq-chuchugi", "все радости и трудности", "ширинию талхии зиндагӣ"),
            ("经历", "jīnglì", "v./n.", "boshdan kechirmoq, tajriba", "переживать; опыт", "аз сар гузарондан; таҷриба"),
            ("回忆", "huíyì", "v./n.", "xotira, eslamoq", "воспоминание; вспоминать", "хотира; ёд кардан"),
            ("感受", "gǎnshòu", "v./n.", "his qilmoq, tuyg'u", "ощущать; впечатление", "ҳис кардан; эҳсос"),
            ("选择", "xuǎnzé", "v./n.", "tanlamoq", "выбирать; выбор", "интихоб кардан"),
            ("勇敢", "yǒnggǎn", "adj.", "jasur", "смелый", "ҷасур"),
            ("幸福", "xìngfú", "adj./n.", "baxtli, baxt", "счастье, счастливый", "хушбахтӣ, хушбахт"),
            ("由来", "yóulái", "n.", "kelib chiqish", "происхождение", "пайдоиш"),
            ("总的来说", "zǒng de lái shuō", "expr.", "umuman olganda", "в целом", "умуман"),
            ("在于", "zàiyú", "v.", "...da bo'lmoq, bog'liq", "заключаться в", "вобаста ба, дар он аст"),
            ("态度", "tàidu", "n.", "munosabat", "отношение", "муносибат"),
        ],
    },
    20: {
        "title": "路上的风景",
        "topic": {
            "uz": "yo'l, sayohat va jarayondan zavqlanish",
            "ru": "дорога, путешествие и радость процесса",
            "tj": "роҳ, сафар ва лаззати раванд",
        },
        "grammar": ["V着V着", "一边……一边……", "先", "起来", "V着"],
        "vocab": [
            ("路上", "lùshang", "n.", "yo'lda", "в пути, по дороге", "дар роҳ"),
            ("风景", "fēngjǐng", "n.", "manzara", "пейзаж", "манзара"),
            ("旅行", "lǚxíng", "v./n.", "sayohat qilmoq", "путешествовать", "сафар кардан"),
            ("出发", "chūfā", "v.", "yo'lga chiqmoq", "отправляться", "ба роҳ баромадан"),
            ("到达", "dàodá", "v.", "yetib bormoq", "прибывать", "расида омадан"),
            ("行李", "xíngli", "n.", "yuk", "багаж", "бор"),
            ("照片", "zhàopiàn", "n.", "rasm", "фотография", "акс"),
            ("目的地", "mùdìdì", "n.", "manzil", "пункт назначения", "мақсадгоҳ"),
            ("一边", "yìbiān", "adv.", "bir tomondan, ... bilan birga", "одновременно, с одной стороны", "ҳамзамон, аз як тараф"),
            ("起来", "qǐlai", "comp.", "boshlanmoq, ko'rinmoq", "начинать; казаться", "сар шудан; намудан"),
            ("经过", "jīngguò", "v./n.", "o'tmoq; jarayon", "проходить; процесс", "гузаштан; раванд"),
            ("发现", "fāxiàn", "v.", "kashf qilmoq, payqamoq", "обнаруживать", "пай бурдан"),
        ],
    },
}


def _goal(data: dict) -> dict:
    patterns = "、".join(data["grammar"])
    return {
        "uz": f"{data['topic']['uz']} haqida gapirish; {patterns} grammatik qoliplarini o'zlashtirish",
        "ru": f"говорить о теме: {data['topic']['ru']}; освоить конструкции {patterns}",
        "tj": f"гуфтугӯ дар бораи: {data['topic']['tj']}; азхуд кардани қолабҳои {patterns}",
    }


def _intro(data: dict) -> dict:
    patterns = "、".join(data["grammar"])
    return {
        "uz": f"Bu dars {data['topic']['uz']} mavzusiga bag'ishlangan. Asosiy grammatika: {patterns}.",
        "ru": f"Этот урок посвящён теме: {data['topic']['ru']}. Основная грамматика: {patterns}.",
        "tj": f"Ин дарс ба мавзӯи {data['topic']['tj']} бахшида шудааст. Грамматикаи асосӣ: {patterns}.",
    }


def _grammar_item(pattern: str, index: int) -> dict:
    return {
        "no": index,
        "title_zh": pattern,
        "title_uz": f"{pattern} qolipi",
        "title_ru": f"Конструкция {pattern}",
        "title_tj": f"Қолаби {pattern}",
        "rule_uz": f"{pattern} gapdagi ma'no va munosabatni aniqroq ko'rsatish uchun ishlatiladi. Uni kontekstdagi o'rniga qarab tarjima qiling.",
        "rule_ru": f"{pattern} используется, чтобы точнее показать смысл и связь в предложении. Переводите его по контексту.",
        "rule_tj": f"{pattern} барои дақиқтар нишон додани маъно ва робита дар ҷумла истифода мешавад. Онро аз рӯйи контекст тарҷума кунед.",
        "examples": [
            {
                "zh": f"我们今天练习“{pattern}”的用法。",
                "pinyin": "",
                "uz": f"Bugun “{pattern}” qo'llanishini mashq qilamiz.",
                "ru": f"Сегодня мы тренируем употребление “{pattern}”.",
                "tj": f"Имрӯз истифодаи “{pattern}”-ро машқ мекунем.",
            }
        ],
    }


def _dialogue_blocks(order: int, data: dict) -> list[dict]:
    title = data["title"]
    topic = data["topic"]
    first_word = data["vocab"][0][0]
    second_word = data["vocab"][1][0]
    first_pattern = data["grammar"][0]
    second_pattern = data["grammar"][1]

    return [
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_uz": f"{title} mavzusida qisqa suhbat",
            "scene_ru": f"Короткий разговор по теме «{title}»",
            "scene_tj": f"Сӯҳбати кӯтоҳ дар мавзӯи «{title}»",
            "dialogue": [
                {
                    "speaker": "老师",
                    "zh": f"今天我们学习第{order}课《{title}》。你觉得这个题目和生活有什么关系？",
                    "pinyin": "",
                    "uz": f"Bugun {order}-dars «{title}»ni o'rganamiz. Bu mavzu hayot bilan qanday bog'liq deb o'ylaysiz?",
                    "ru": f"Сегодня мы изучаем урок {order} «{title}». Как вы думаете, как эта тема связана с жизнью?",
                    "tj": f"Имрӯз дарси {order} «{title}»-ро меомӯзем. Ба фикри шумо ин мавзӯъ бо зиндагӣ чӣ робита дорад?",
                },
                {
                    "speaker": "学生",
                    "zh": f"我觉得它和{first_word}、{second_word}都有关系，并且能帮助我们表达自己的看法。",
                    "pinyin": "",
                    "uz": f"Menimcha, u {first_word} va {second_word} bilan bog'liq, bundan tashqari fikrimizni aytishga yordam beradi.",
                    "ru": f"Думаю, это связано с {first_word} и {second_word}, а также помогает выражать своё мнение.",
                    "tj": f"Ба фикрам, он бо {first_word} ва {second_word} робита дорад ва барои баён кардани фикр ёрӣ медиҳад.",
                },
                {
                    "speaker": "老师",
                    "zh": f"很好。请你用“{first_pattern}”说一个句子。",
                    "pinyin": "",
                    "uz": f"Yaxshi. “{first_pattern}” bilan bitta gap ayting.",
                    "ru": f"Хорошо. Составьте одно предложение с “{first_pattern}”.",
                    "tj": f"Хуб. Бо “{first_pattern}” як ҷумла гӯед.",
                },
                {
                    "speaker": "学生",
                    "zh": f"学习语言要注意词语，也要注意句子的意思。",
                    "pinyin": "",
                    "uz": "Til o'rganishda so'zlarga ham, gap ma'nosiga ham e'tibor berish kerak.",
                    "ru": "При изучении языка нужно обращать внимание и на слова, и на смысл предложения.",
                    "tj": "Дар омӯзиши забон ҳам ба калимаҳо ва ҳам ба маънои ҷумла диққат додан лозим.",
                },
            ],
            "grammar_notes": [_grammar_item(first_pattern, 1)],
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_uz": f"{topic['uz']} haqida fikr almashish",
            "scene_ru": f"Обмен мнениями: {topic['ru']}",
            "scene_tj": f"Мубодилаи фикр: {topic['tj']}",
            "dialogue": [
                {
                    "speaker": "A",
                    "zh": f"对于这个问题，你有什么想法？",
                    "pinyin": "",
                    "uz": "Bu masala bo'yicha qanday fikringiz bor?",
                    "ru": "Что вы думаете по этому вопросу?",
                    "tj": "Дар бораи ин масъала чӣ фикр доред?",
                },
                {
                    "speaker": "B",
                    "zh": f"我觉得最重要的是先观察生活，然后总结经验。",
                    "pinyin": "",
                    "uz": "Menimcha, eng muhimi avval hayotni kuzatish, keyin tajribadan xulosa chiqarish.",
                    "ru": "Думаю, важнее всего сначала наблюдать жизнь, а потом обобщать опыт.",
                    "tj": "Ба фикрам, муҳимтаринаш аввал зиндагиро мушоҳида кардан ва баъд таҷрибаро ҷамъбаст намудан аст.",
                },
                {
                    "speaker": "A",
                    "zh": f"对。这样我们才能把“{second_pattern}”用得更自然。",
                    "pinyin": "",
                    "uz": f"To'g'ri. Shunda “{second_pattern}”ni tabiiyroq ishlata olamiz.",
                    "ru": f"Верно. Так мы сможем естественнее использовать “{second_pattern}”.",
                    "tj": f"Дуруст. Ҳамин тавр “{second_pattern}”-ро табиитар истифода мебарем.",
                },
                {
                    "speaker": "B",
                    "zh": f"这就是《{title}》给我的启发。",
                    "pinyin": "",
                    "uz": f"«{title}» menga bergan asosiy xulosa shu.",
                    "ru": f"Вот главный вывод, который я получил из «{title}».",
                    "tj": f"Ин хулосаи асосии ман аз «{title}» аст.",
                },
            ],
            "grammar_notes": [_grammar_item(second_pattern, 2)],
        },
    ]


def _exercises(data: dict) -> list[dict]:
    patterns = data["grammar"]
    vocab = data["vocab"]
    return [
        {
            "no": 1,
            "type": "translation",
            "instruction_uz": "So'zlarning ma'nosini yozing:",
            "instruction_ru": "Напишите значения слов:",
            "instruction_tj": "Маънои калимаҳоро нависед:",
            "items": [
                {"prompt_uz": word[0], "prompt_ru": word[0], "prompt_tj": word[0], "answer": word[3], "pinyin": word[1]}
                for word in vocab[:5]
            ],
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction_uz": f"Mos qolipni tanlang ({'、'.join(patterns[:4])}):",
            "instruction_ru": f"Выберите подходящую конструкцию ({'、'.join(patterns[:4])}):",
            "instruction_tj": f"Қолаби мувофиқро интихоб кунед ({'、'.join(patterns[:4])}):",
            "items": [
                {
                    "prompt_uz": "______这个问题，我们还需要继续讨论。",
                    "prompt_ru": "______这个问题，我们还需要继续讨论。",
                    "prompt_tj": "______这个问题，我们还需要继续讨论。",
                    "answer": patterns[1] if len(patterns) > 1 else patterns[0],
                    "pinyin": "",
                },
                {
                    "prompt_uz": "他认真学习，______每天复习。",
                    "prompt_ru": "他认真学习，______每天复习。",
                    "prompt_tj": "他认真学习，______每天复习。",
                    "answer": patterns[0],
                    "pinyin": "",
                },
            ],
        },
    ]


def _answers(data: dict) -> list[dict]:
    return [
        {"no": 1, "answers": [word[3] for word in data["vocab"][:5]]},
        {"no": 2, "answers": [data["grammar"][1] if len(data["grammar"]) > 1 else data["grammar"][0], data["grammar"][0]]},
    ]


def _homework(data: dict) -> list[dict]:
    return [
        {
            "no": 1,
            "instruction_uz": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
            "instruction_ru": "Составьте 3 предложения, используя следующие слова:",
            "instruction_tj": "Бо истифодаи калимаҳои зерин 3 ҷумла тартиб диҳед:",
            "words": [word[0] for word in data["vocab"][:4]],
        },
        {
            "no": 2,
            "instruction_uz": f"'{data['grammar'][0]}' qolipi bilan 2 ta gap yozing.",
            "instruction_ru": f"Напишите 2 предложения с конструкцией '{data['grammar'][0]}'.",
            "instruction_tj": f"Бо қолаби '{data['grammar'][0]}' 2 ҷумла нависед.",
            "topic_uz": data["topic"]["uz"],
            "topic_ru": data["topic"]["ru"],
            "topic_tj": data["topic"]["tj"],
        },
        {
            "no": 3,
            "instruction_uz": "5-6 gapdan iborat kichik matn yozing:",
            "instruction_ru": "Напишите небольшой текст из 5-6 предложений:",
            "instruction_tj": "Матни кӯтоҳи 5-6 ҷумлагӣ нависед:",
            "topic_uz": data["topic"]["uz"],
            "topic_ru": data["topic"]["ru"],
            "topic_tj": data["topic"]["tj"],
        },
    ]


def build_lesson(order: int) -> dict:
    data = LESSON_DATA[order]
    return {
        "level": "hsk4",
        "lesson_order": order,
        "lesson_code": f"HSK4-L{order:02d}",
        "title": data["title"],
        "goal": json.dumps(_goal(data), ensure_ascii=False),
        "intro_text": json.dumps(_intro(data), ensure_ascii=False),
        "vocabulary_json": json.dumps(
            [
                {"no": i, "zh": zh, "pinyin": pinyin, "pos": pos, "uz": uz, "ru": ru, "tj": tj}
                for i, (zh, pinyin, pos, uz, ru, tj) in enumerate(data["vocab"], 1)
            ],
            ensure_ascii=False,
        ),
        "dialogue_json": json.dumps(_dialogue_blocks(order, data), ensure_ascii=False),
        "grammar_json": json.dumps([_grammar_item(pattern, i) for i, pattern in enumerate(data["grammar"], 1)], ensure_ascii=False),
        "exercise_json": json.dumps(_exercises(data), ensure_ascii=False),
        "answers_json": json.dumps(_answers(data), ensure_ascii=False),
        "homework_json": json.dumps(_homework(data), ensure_ascii=False),
        "review_json": "[]",
        "is_active": True,
    }


async def upsert_hsk4_lesson(order: int) -> None:
    lesson = build_lesson(order)
    async with SessionLocal() as session:
        result = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == lesson["lesson_code"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            for key, value in lesson.items():
                setattr(existing, key, value)
            print(f"updated: {lesson['lesson_code']}")
        else:
            session.add(CourseLesson(**lesson))
            print(f"inserted: {lesson['lesson_code']}")

        await session.commit()


def run_upsert(order: int):
    async def _upsert_lesson():
        await upsert_hsk4_lesson(order)

    return _upsert_lesson


if __name__ == "__main__":
    for lesson_order in range(12, 21):
        asyncio.run(upsert_hsk4_lesson(lesson_order))
