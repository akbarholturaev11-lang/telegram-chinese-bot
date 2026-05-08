import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 6,
    "lesson_code": "HSK3-L06",
    "title": "怎么突然找不到了",
    "goal": json.dumps({"uz": "Yo'qolgan narsalarni qidirish va joylashuv so'rashni o'rganish.", "ru": "Изучение поиска потерянных вещей и уточнения местонахождения.", "tj": "Омӯзиши ҷустуҷӯи ашёҳои гумшуда ва пурсидан дар бораи ҷойгиршавӣ."}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu dars yo'qolgan narsalarni qidirish va joylashuv so'rashga bag'ishlangan. 5 ta asosiy so'z o'rganiladi va 'V得/不 + to'ldiruvchi' (imkoniyat to'ldiruvchisi) hamda '呢' (joylashuv so'rash uchun) grammatik shakllar o'zlashtiriladi.", "ru": "Этот урок посвящён поиску потерянных вещей и уточнению местонахождения. Изучаются 5 ключевых слов и грамматические конструкции 'V得/不 + дополнение' (дополнение возможности) и '呢' (для мягкого уточнения местонахождения).", "tj": "Ин дарс ба ҷустуҷӯи ашёҳои гумшуда ва пурсидан дар бораи ҷойгиршавӣ бахшида шудааст. 5 калимаи асосӣ омӯхта мешавад ва сохторҳои грамматикии 'V得/不 + иловаи имконпазирӣ' ва '呢' (барои пурсидан дар бораи ҷой) аз бар карда мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "眼镜", "pinyin": "yǎnjìng", "pos": "n.", "uz": "ko'zoynak", "ru": "очки", "tj": "айnak"},
        {"no": 2, "zh": "突然", "pinyin": "tūrán", "pos": "adv.", "uz": "to'satdan, birdan", "ru": "вдруг, внезапно", "tj": "якбора, ногаҳон"},
        {"no": 3, "zh": "离开", "pinyin": "líkāi", "pos": "v.", "uz": "ketmoq, tark etmoq", "ru": "уходить, покидать", "tj": "рафтан, тарк кардан"},
        {"no": 4, "zh": "公园", "pinyin": "gōngyuán", "pos": "n.", "uz": "bog', park", "ru": "парк, сад", "tj": "боғи истироҳатӣ"},
        {"no": 5, "zh": "明白", "pinyin": "míngbai", "pos": "v./adj.", "uz": "tushunmoq; aniq, ravshan", "ru": "понимать; ясный, понятный", "tj": "фаҳмидан; равшан, возеҳ"}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_uz": "Ko'zoynak qidirish",
            "scene_ru": "Поиск очков",
            "scene_tj": "Ҷустуҷӯи айnak",
            "dialogue": [
                {"speaker": "A", "zh": "我的眼镜怎么突然找不到了？", "pinyin": "Wǒ de yǎnjìng zěnme tūrán zhǎo bú dào le?", "uz": "Ko'zoynaklarim qayga ketdi, to'satdan topolmayapman?", "ru": "Куда вдруг пропали мои очки, никак не могу найти?", "tj": "Айнакҳои ман куҷо рафт, ногаҳон ёфта наметавонам?"},
                {"speaker": "B", "zh": "你刚才是不是离开教室了？", "pinyin": "Nǐ gāngcái shì bú shì líkāi jiàoshì le?", "uz": "Siz hozirgina sinfxonani tark etmadingizmi?", "ru": "Ты же только что уходил(а) из класса?", "tj": "Магар ту ҳозир синфхонаро тарк накардӣ?"}
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_uz": "Joylashuv so'rash",
            "scene_ru": "Уточнение местонахождения",
            "scene_tj": "Пурсидан дар бораи ҷой",
            "dialogue": [
                {"speaker": "A", "zh": "小王呢？", "pinyin": "Xiǎo Wáng ne?", "uz": "Xiao Van qani?", "ru": "А где Сяо Ван?", "tj": "Сяо Ван куҷост?"},
                {"speaker": "B", "zh": "他在公园那边，等会儿回来。", "pinyin": "Tā zài gōngyuán nàbiān, děng huìr huí lái.", "uz": "U park tarafda, bir ozdan qaytib keladi.", "ru": "Он там у парка, скоро вернётся.", "tj": "Ӯ он тарафи боғ аст, зуд бармегардад."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "可能补语：V得/不 + Complements",
            "title_uz": "Imkoniyat to'ldiruvchisi: V得/不 + to'ldiruvchi",
            "title_ru": "Дополнение возможности: V得/不 + дополнение",
            "title_tj": "Иловаи имконпазирӣ: V得/不 + иловакунанда",
            "rule_uz": "Imkoniyat to'ldiruvchisi fe'l va to'ldiruvchi orasiga '得' (imkon bor) yoki '不' (imkon yo'q) qo'shib hosil qilinadi. Masalan: 找得到 (topish mumkin), 找不到 (topolmayman). Bu imkon-imkonsizlikni bildiradi.",
            "rule_ru": "Дополнение возможности образуется вставкой '得' (возможно) или '不' (невозможно) между глаголом и дополнением. Например: 找得到 (можно найти), 找不到 (не могу найти). Выражает возможность или невозможность.",
            "rule_tj": "Иловаи имконпазирӣ бо гузоштани '得' (мумкин аст) ё '不' (мумкин нест) байни феъл ва иловакунанда ҳосил мешавад. Масалан: 找得到 (ёфтан мумкин аст), 找不到 (ёфта наметавонам). Имконпазирӣ ё имконнопазирӣ ро ифода мекунад.",
            "examples": [
                {"zh": "我怎么突然找不到了？", "pinyin": "Wǒ zěnme tūrán zhǎo bú dào le?", "uz": "Nima uchun to'satdan topolmayapman?", "ru": "Почему я вдруг не могу найти?", "tj": "Чаро ман ногаҳон ёфта наметавонам?"},
                {"zh": "这道题太难了，我做不出来。", "pinyin": "Zhè dào tí tài nán le, wǒ zuò bù chūlái.", "uz": "Bu masala juda qiyin, yecha olmayman.", "ru": "Эта задача слишком сложная, я не могу её решить.", "tj": "Ин масала хеле душвор аст, ман ҳал карда наметавонам."}
            ]
        },
        {
            "no": 2,
            "title_zh": "“呢”问处所",
            "title_uz": "'Ne' joylashuv so'rovi",
            "title_ru": "'呢' для мягкого уточнения местонахождения",
            "title_tj": "'呢' барои пурсидан дар бораи ҷой",
            "rule_uz": "'Ne' yuklamasi gap oxiriga qo'shilib, joylashuv, holat yoki davom etayotgan vaziyat haqida yumshoq savol hosil qiladi. Bu to'liq savol gapidan ko'ra qisqaroq va norasmiyroq. Masalan: 小王呢？ (Xiao Van qani?), 你的书呢？ (Sening kitobingchi?).",
            "rule_ru": "Частица '呢' в конце предложения образует мягкий вопрос о местонахождении, состоянии или продолжающейся ситуации. Это короче и менее формально, чем полный вопрос. Например: 小王呢？ (А где Сяо Ван?), 你的书呢？ (А где твоя книга?).",
            "rule_tj": "Зарраи '呢' дар охири ҷумла пурсиши нармро дар бораи ҷойгиршавӣ, ҳолат ё вазъияти давомдор ҳосил мекунад. Ин аз ҷумлаи пурсишии комил кӯтоҳтар ва ғайрирасмитар аст. Масалан: 小王呢？ (Сяо Ван куҷост?), 你的书呢？ (Китобат куҷост?).",
            "examples": [
                {"zh": "小王呢？", "pinyin": "Xiǎo Wáng ne?", "uz": "Xiao Van qani?", "ru": "А где Сяо Ван?", "tj": "Сяо Ван куҷост?"},
                {"zh": "你的眼镜呢？", "pinyin": "Nǐ de yǎnjìng ne?", "uz": "Sening ko'zoynakching qani?", "ru": "А где твои очки?", "tj": "Айнакат куҷост?"}
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
                {"prompt_uz": "ko'zoynak", "prompt_ru": "очки", "prompt_tj": "айnak", "answer": "眼镜", "pinyin": "yǎnjìng"},
                {"prompt_uz": "to'satdan", "prompt_ru": "вдруг", "prompt_tj": "ногаҳон", "answer": "突然", "pinyin": "tūrán"},
                {"prompt_uz": "ketmoq, tark etmoq", "prompt_ru": "уходить", "prompt_tj": "рафтан, тарк кардан", "answer": "离开", "pinyin": "líkāi"},
                {"prompt_uz": "park, bog'", "prompt_ru": "парк", "prompt_tj": "боғи истироҳатӣ", "answer": "公园", "pinyin": "gōngyuán"}
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction_uz": "Bo'sh joyni to'ldiring:",
            "instruction_ru": "Заполните пропуск:",
            "instruction_tj": "Ҷойи холиро пур кунед:",
            "items": [
                {"prompt_uz": "Ko'zoynaklarimni ___yolmayapman. (找不到)", "prompt_ru": "Никак не ___ очки. (找不到)", "prompt_tj": "Айнакҳоямро ___ наметавонам. (找不到)", "answer": "找不到", "pinyin": "zhǎo bú dào"},
                {"prompt_uz": "Xiao Van ___? (呢)", "prompt_ru": "А Сяо Ван ___? (呢)", "prompt_tj": "Сяо Ван ___? (呢)", "answer": "呢", "pinyin": "ne"},
                {"prompt_uz": "U ___ sinfxonani tark etdi. (突然)", "prompt_ru": "Он ___ вышел из класса. (突然)", "prompt_tj": "Вай ___ синфхонаро тарк кард. (突然)", "answer": "突然", "pinyin": "tūrán"},
                {"prompt_uz": "U ___ tarafda. (公园)", "prompt_ru": "Он у ___. (公园)", "prompt_tj": "Вай он тарафи ___ аст. (公园)", "answer": "公园", "pinyin": "gōngyuán"}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "answers": ["眼镜", "突然", "离开", "公园"]},
        {"no": 2, "answers": ["找不到", "呢", "突然", "公园"]}
    ], ensure_ascii=False),
    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction_uz": "Quyidagi so'zlardan foydalanib 3 ta jumla tuzing:",
            "instruction_ru": "Составьте 3 предложения, используя следующие слова:",
            "instruction_tj": "Бо истифодаи калимаҳои зерин 3 ҷумла созед:",
            "words": ["眼镜", "突然", "离开"],
            "example": "我的眼镜突然找不到了，刚才我还没离开。",
            "topic_uz": "Yo'qolgan narsa qidirish",
            "topic_ru": "Поиск потерянной вещи",
            "topic_tj": "Ҷустуҷӯи чизи гумшуда"
        },
        {
            "no": 2,
            "instruction_uz": "Dars mavzusi bo'yicha 4-5 jumladan iborat qisqa matn yozing:",
            "instruction_ru": "Напишите короткий абзац из 4-5 предложений по теме урока:",
            "instruction_tj": "Дар бораи мавзӯи дарс 4-5 ҷумлаи кӯтоҳ нависед:",
            "words": ["眼镜", "找不到", "突然"],
            "example": "我突然找不到眼镜了，很着急。",
            "topic_uz": "怎么突然找不到了",
            "topic_ru": "怎么突然找不到了",
            "topic_tj": "怎么突然找不到了"
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
