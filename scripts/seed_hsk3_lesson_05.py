import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 5,
    "lesson_code": "HSK3-L05",
    "title": "我最近越来越胖了",
    "goal": json.dumps({"uz": "Sog'liq o'zgarishlari va progressiv holatlarni ifodalashni o'rganish.", "ru": "Изучение выражения изменений здоровья и прогрессирующих состояний.", "tj": "Омӯзиши ифодаи тағйироти саломатӣ ва ҳолатҳои тадриҷӣ."}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu dars sog'liq o'zgarishlari va progressiv holatlarni ifodalashga bag'ishlangan. 5 ta asosiy so'z o'rganiladi va '了' (o'zgarishni bildiruvchi) hamda '越来越 + sifat/mental fe'l' grammatik shakllar o'zlashtiriladi.", "ru": "Этот урок посвящён выражению изменений здоровья и прогрессирующих состояний. Изучаются 5 ключевых слов и грамматические конструкции '了' (для обозначения изменения) и '越来越 + прилагательное/ментальный глагол'.", "tj": "Ин дарс ба ифодаи тағйироти саломатӣ ва ҳолатҳои тадриҷӣ бахшида шудааст. 5 калимаи асосӣ омӯхта мешавад ва сохторҳои грамматикии '了' (барои тағйирот) ва '越来越 + сифат/феъли зеҳнӣ' аз бар карда мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "最近", "pinyin": "zuìjìn", "pos": "adv.", "uz": "yaqinda, so'nggi paytda", "ru": "недавно, в последнее время", "tj": "охирон, дар вақтҳои охир"},
        {"no": 2, "zh": "发烧", "pinyin": "fāshāo", "pos": "v.", "uz": "isitma chiqmoq", "ru": "заболеть температурой, иметь жар", "tj": "таб омадан, табдор шудан"},
        {"no": 3, "zh": "感冒", "pinyin": "gǎnmào", "pos": "v./n.", "uz": "shamollamoq; shamollab qolish", "ru": "простудиться; простуда", "tj": "шамол хӯрдан; шамолхӯрӣ"},
        {"no": 4, "zh": "季节", "pinyin": "jìjié", "pos": "n.", "uz": "fasl, mavsum", "ru": "сезон, время года", "tj": "фасл, мавсим"},
        {"no": 5, "zh": "夏天", "pinyin": "xiàtiān", "pos": "n.", "uz": "yoz", "ru": "лето", "tj": "тобистон"}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_uz": "Sog'liq haqida suhbat",
            "scene_ru": "Разговор о здоровье",
            "scene_tj": "Сӯҳбат дар бораи саломатӣ",
            "dialogue": [
                {"speaker": "A", "zh": "你最近怎么了？", "pinyin": "Nǐ zuìjìn zěnme le?", "uz": "Siz so'nggi paytda qandaysiz?", "ru": "Как ты себя чувствуешь в последнее время?", "tj": "Шумо охирон чӣ хел ҳастед?"},
                {"speaker": "B", "zh": "我最近越来越胖了，而且还感冒了。", "pinyin": "Wǒ zuìjìn yuè lái yuè pàng le, érqiě hái gǎnmào le.", "uz": "So'nggi paytda tobora semirmoqdaman, ustiga ustak shamollab ham qoldim.", "ru": "В последнее время я становлюсь всё толще, и к тому же ещё простудился(ась).", "tj": "Дар вақтҳои охир ман рӯз аз рӯз чоқтар мешавам, ва боз шамол ҳам хӯрдам."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_uz": "Fasllar haqida",
            "scene_ru": "О временах года",
            "scene_tj": "Дар бораи фаслҳо",
            "dialogue": [
                {"speaker": "A", "zh": "夏天你容易发烧吗？", "pinyin": "Xiàtiān nǐ róngyì fāshāo ma?", "uz": "Yozda sizda tez-tez isitma chiqadimi?", "ru": "Часто ли у тебя бывает жар летом?", "tj": "Дар тобистон шумо зуд-зуд табдор мешавед?"},
                {"speaker": "B", "zh": "有时候，因为这个季节太热了。", "pinyin": "Yǒu shíhou, yīnwèi zhège jìjié tài rè le.", "uz": "Ba'zan, chunki bu fasl juda issiq.", "ru": "Иногда, потому что в этот сезон очень жарко.", "tj": "Баъзан, чунки ин мавсум хеле гарм аст."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "“了”表示变化",
            "title_uz": "'Le' o'zgarishni bildiradi",
            "title_ru": "'了' обозначает изменение",
            "title_tj": "'了' тағйиротро ифода мекунад",
            "rule_uz": "Gap oxiridagi '了' yangi holatning yuzaga kelganligini yoki holatning o'zgarganligini bildiradi. Bu '完成' (tugatilgan harakat) '了' emas, balki '变化' (o'zgarish) '了' dir. Masalan: 我胖了 (semirdim — avval bunday emasdi).",
            "rule_ru": "Частица '了' в конце предложения указывает на возникновение нового состояния или изменение ситуации. Это не '了' завершённого действия, а '了' изменения. Например: 我胖了 (я растолстел(а) — раньше так не было).",
            "rule_tj": "Зарраи '了' дар охири ҷумла пайдо шудани ҳолати нав ё тағйири вазъиятро нишон медиҳад. Ин '了'-и амали тамомшуда нест, балки '了'-и тағйирот аст. Масалан: 我胖了 (ман чоқ шудам — пеш чунин набудам).",
            "examples": [
                {"zh": "我最近越来越胖了。", "pinyin": "Wǒ zuìjìn yuè lái yuè pàng le.", "uz": "So'nggi paytda tobora semirmoqdaman.", "ru": "В последнее время я становлюсь всё толще.", "tj": "Дар вақтҳои охир ман рӯз аз рӯз чоқтар мешавам."},
                {"zh": "天气热了。", "pinyin": "Tiānqì rè le.", "uz": "Havo isindi.", "ru": "Погода потеплела.", "tj": "Ҳаво гарм шуд."}
            ]
        },
        {
            "no": 2,
            "title_zh": "越来越 + Adj/Mental V",
            "title_uz": "'Yuè lái yuè' + sifat/holat fe'li",
            "title_ru": "'越来越' + прилагательное/ментальный глагол",
            "title_tj": "'越来越' + сифат/феъли зеҳнӣ",
            "rule_uz": "Bu konstruktsiya holatning asta-sekin kuchayishini yoki ortishini bildiradi: 'tobora…, kundan-kunga…'. Sifat yoki holat fe'li bilan ishlatiladi. Masalan: 越来越好 (tobora yaxshilanmoqda), 越来越喜欢 (tobora yoqib ketmoqda).",
            "rule_ru": "Эта конструкция указывает на постепенное усиление или нарастание состояния: 'всё более…, с каждым днём…'. Используется с прилагательными или ментальными глаголами. Например: 越来越好 (становится лучше), 越来越喜欢 (нравится всё больше).",
            "rule_tj": "Ин конструксия тадриҷан афзоиш ёфтан ё шиддати ҳолатро нишон медиҳад: 'рӯз аз рӯз…, ҳар чӣ бештар…'. Бо сифат ё феълҳои зеҳнӣ истифода мешавад. Масалан: 越来越好 (рӯз аз рӯз беҳтар мешавад), 越来越喜欢 (рӯз аз рӯз бештар маъқул мешавад).",
            "examples": [
                {"zh": "我最近越来越胖了。", "pinyin": "Wǒ zuìjìn yuè lái yuè pàng le.", "uz": "So'nggi paytda tobora semirmoqdaman.", "ru": "В последнее время я становлюсь всё толще.", "tj": "Дар вақтҳои охир ман рӯз аз рӯз чоқтар мешавам."},
                {"zh": "他的汉语越来越好了。", "pinyin": "Tā de Hànyǔ yuè lái yuè hǎo le.", "uz": "Uning xitoy tili tobora yaxshilanmoqda.", "ru": "Его китайский становится всё лучше.", "tj": "Забони чинии ӯ рӯз аз рӯз беҳтар мешавад."}
            ]
        }
    ], ensure_ascii=False),
    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction_uz": "Quyidagi so'zlarning xitoychasini yozing:",
            "instruction_ru": "Напишите китайские эквиваленты следующих слов:",
            "instruction_tj": "Тарҷумаи чинии калимаҳои зеринро нависед:",
            "items": [
                {"prompt_uz": "yaqinda, so'nggi paytda", "prompt_ru": "недавно, в последнее время", "prompt_tj": "охирон, дар вақтҳои охир", "answer": "最近", "pinyin": "zuìjìn"},
                {"prompt_uz": "isitma chiqmoq", "prompt_ru": "иметь жар", "prompt_tj": "табдор шудан", "answer": "发烧", "pinyin": "fāshāo"},
                {"prompt_uz": "shamollamoq", "prompt_ru": "простудиться", "prompt_tj": "шамол хӯрдан", "answer": "感冒", "pinyin": "gǎnmào"},
                {"prompt_uz": "fasl, mavsum", "prompt_ru": "сезон", "prompt_tj": "фасл, мавсим", "answer": "季节", "pinyin": "jìjié"}
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction_uz": "Bo'sh joyni to'ldiring:",
            "instruction_ru": "Заполните пропуск:",
            "instruction_tj": "Ҷойи холиро пур кунед:",
            "items": [
                {"prompt_uz": "Men ___ semirmoqdaman. (越来越)", "prompt_ru": "Я ___ толстею. (越来越)", "prompt_tj": "Ман ___ чоқ мешавам. (越来越)", "answer": "越来越", "pinyin": "yuè lái yuè"},
                {"prompt_uz": "Havo ___ issiq bo'lib ketdi. (了)", "prompt_ru": "Погода стала ___ жаркой. (了)", "prompt_tj": "Ҳаво ___ гарм шуд. (了)", "answer": "了", "pinyin": "le"},
                {"prompt_uz": "U yozda ___ chiqadi. (发烧)", "prompt_ru": "У него летом ___ бывает. (发烧)", "prompt_tj": "Вай дар тобистон ___ мегирад. (发烧)", "answer": "发烧", "pinyin": "fāshāo"},
                {"prompt_uz": "Bu ___ juda issiq. (季节)", "prompt_ru": "В этот ___ очень жарко. (季节)", "prompt_tj": "Дар ин ___ хеле гарм аст. (季节)", "answer": "季节", "pinyin": "jìjié"}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "answers": ["最近", "发烧", "感冒", "季节"]},
        {"no": 2, "answers": ["越来越", "了", "发烧", "季节"]}
    ], ensure_ascii=False),
    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction_uz": "Quyidagi so'zlardan foydalanib 3 ta jumla tuzing:",
            "instruction_ru": "Составьте 3 предложения, используя следующие слова:",
            "instruction_tj": "Бо истифодаи калимаҳои зерин 3 ҷумла созед:",
            "words": ["最近", "发烧", "感冒"],
            "example": "我最近感冒了，一直发烧。",
            "topic_uz": "So'nggi paytdagi sog'liq holati",
            "topic_ru": "Состояние здоровья в последнее время",
            "topic_tj": "Ҳолати саломатӣ дар вақтҳои охир"
        },
        {
            "no": 2,
            "instruction_uz": "Dars mavzusi bo'yicha 4-5 jumladan iborat qisqa matn yozing:",
            "instruction_ru": "Напишите короткий абзац из 4-5 предложений по теме урока:",
            "instruction_tj": "Дар бораи мавзӯи дарс 4-5 ҷумлаи кӯтоҳ нависед:",
            "words": ["越来越", "最近", "感冒"],
            "example": "最近我越来越忙了，还感冒了。",
            "topic_uz": "我最近越来越胖了",
            "topic_ru": "我最近越来越胖了",
            "topic_tj": "我最近越来越胖了"
        }
    ], ensure_ascii=False),
    "review_json": "[]",
    "is_active": True
}


async def upsert_lesson():
    async with SessionLocal() as session:
        result = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])
        )
        existing = result.scalar_one_or_none()
        if existing:
            for key, value in LESSON.items():
                setattr(existing, key, value)
            print(f"updated: {LESSON['lesson_code']}")
        else:
            session.add(CourseLesson(**LESSON))
            print(f"inserted: {LESSON['lesson_code']}")
        await session.commit()


if __name__ == "__main__":
    asyncio.run(upsert_lesson())
