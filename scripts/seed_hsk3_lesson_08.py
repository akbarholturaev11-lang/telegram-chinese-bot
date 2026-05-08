import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 8,
    "lesson_code": "HSK3-L08",
    "title": "你去哪儿我就去哪儿",
    "goal": json.dumps({"uz": "So'roq olmoshlarini erkin ishlatish va yo'nalishni ifodalashni o'rganish.", "ru": "Изучение свободного использования вопросительных местоимений и выражения направления.", "tj": "Омӯзиши озодона истифодаи асмои пурсишӣ ва ифодаи самт."}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu dars so'roq olmoshlarini erkin ishlatish va yo'nalishni ifodalashga bag'ishlangan. 5 ta asosiy so'z o'rganiladi va '又' hamda '再' farqi hamda so'roq olmoshlarining umumiy ishlatilishi (疑问代词活用 1) grammatik shakllar o'zlashtiriladi.", "ru": "Этот урок посвящён свободному использованию вопросительных местоимений и выражению направления. Изучаются 5 ключевых слов и грамматические конструкции: разница между '又' и '再', а также обобщённое использование вопросительных местоимений (疑问代词活用 1).", "tj": "Ин дарс ба озодона истифода бурдани асмои пурсишӣ ва ифодаи самт бахшида шудааст. 5 калимаи асосӣ омӯхта мешавад ва сохторҳои грамматикӣ: фарқи '又' ва '再', инчунин истифодаи умумии асмои пурсишӣ (疑问代词活用 1) аз бар карда мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "熊猫", "pinyin": "xióngmāo", "pos": "n.", "uz": "panda", "ru": "панда", "tj": "панда"},
        {"no": 2, "zh": "电梯", "pinyin": "diàntī", "pos": "n.", "uz": "lift, eskalator", "ru": "лифт, подъёмник", "tj": "лифт"},
        {"no": 3, "zh": "洗手间", "pinyin": "xǐshǒujiān", "pos": "n.", "uz": "hojatxona, tualet", "ru": "туалет, санузел", "tj": "ҳоҷатхона, туалет"},
        {"no": 4, "zh": "马上", "pinyin": "mǎshàng", "pos": "adv.", "uz": "darhol, zudlik bilan", "ru": "сейчас же, немедленно", "tj": "дарҳол, фавран"},
        {"no": 5, "zh": "健康", "pinyin": "jiànkāng", "pos": "adj./n.", "uz": "sog'lom; sog'liq", "ru": "здоровый; здоровье", "tj": "солим; саломатӣ"}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_uz": "Birga borish",
            "scene_ru": "Идти вместе",
            "scene_tj": "Якҷоя рафтан",
            "dialogue": [
                {"speaker": "A", "zh": "你去哪儿我就去哪儿。", "pinyin": "Nǐ qù nǎr wǒ jiù qù nǎr.", "uz": "Siz qayerga borsangiz, men ham boraman.", "ru": "Куда ты пойдёшь, туда и я пойду.", "tj": "Ту ба куҷо равӣ, ман ҳам ба ҳамон ҷо мераваm."},
                {"speaker": "B", "zh": "那我们先去看熊猫吧。", "pinyin": "Nà wǒmen xiān qù kàn xióngmāo ba.", "uz": "Unda avval pandalarni ko'rish boraylik.", "ru": "Тогда давай сначала пойдём посмотрим на панд.", "tj": "Пас биёед аввал ба тамошои пандаҳо биравем."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_uz": "Binoda",
            "scene_ru": "В здании",
            "scene_tj": "Дар бино",
            "dialogue": [
                {"speaker": "A", "zh": "你害怕坐电梯吗？", "pinyin": "Nǐ hàipà zuò diàntī ma?", "uz": "Siz liftda yurishdan qo'rqasizmi?", "ru": "Ты боишься ездить на лифте?", "tj": "Шумо аз лифт тарс доред?"},
                {"speaker": "B", "zh": "不害怕，我马上就上去。", "pinyin": "Bù hàipà, wǒ mǎshàng jiù shàngqù.", "uz": "Yo'q, darhol chiqib ketaman.", "ru": "Нет, я сейчас же поднимусь.", "tj": "Не, ман дарҳол мебароям."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "“又”和“再”",
            "title_uz": "'Yòu' va 'zài' farqi",
            "title_ru": "Разница между '又' и '再'",
            "title_tj": "Фарқи '又' ва '再'",
            "rule_uz": "'Yòu' — allaqachon takrorlangan harakat uchun ishlatiladi (o'tmishda yoki hozirda): 他又来了 (u yana keldi). '再' — kelajakda takrorlanadigan harakat uchun: 明天再来 (ertaga yana keling). Qisqacha: 又 = takrorlandi (o'tgan/hozir), 再 = takrorlanadi (kelajak).",
            "rule_ru": "'又' используется для уже повторившегося действия (в прошлом или настоящем): 他又来了 (он снова пришёл). '再' — для действия, которое повторится в будущем: 明天再来 (приходи снова завтра). Кратко: 又 = снова (прошлое/настоящее), 再 = снова (будущее).",
            "rule_tj": "'又' барои амали аллакай такроршуда (дар гузашта ё ҳозир) истифода мешавад: 他又来了 (вай боз омад). '再' — барои амале ки дар оянда такрор мешавад: 明天再来 (фардо боз биё). Хулоса: 又 = боз (гузашта/ҳозир), 再 = боз (оянда).",
            "examples": [
                {"zh": "他又迟到了。", "pinyin": "Tā yòu chídào le.", "uz": "U yana kechikdi.", "ru": "Он снова опоздал.", "tj": "Вай боз дер монд."},
                {"zh": "你明天再来吧。", "pinyin": "Nǐ míngtiān zài lái ba.", "uz": "Siz ertaga yana keling.", "ru": "Приходи снова завтра.", "tj": "Ту фардо боз биё."}
            ]
        },
        {
            "no": 2,
            "title_zh": "疑问代词活用 1",
            "title_uz": "So'roq olmoshlarining umumiy ishlatilishi 1",
            "title_ru": "Обобщённое использование вопросительных местоимений 1",
            "title_tj": "Истифодаи умумии асмои пурсишӣ 1",
            "rule_uz": "Xitoy tilida so'roq olmoshlari (谁, 哪儿, 什么 va h.k.) savol bildirmasdan umumiy yoki noaniq ma'noda ham ishlatilishi mumkin. Bu 'kim bo'lsa ham', 'qayerda bo'lsa ham' ma'nolarini beradi. Masalan: 你去哪儿我就去哪儿 (Siz qayerga borsangiz, men ham boraman).",
            "rule_ru": "В китайском языке вопросительные местоимения (谁, 哪儿, 什么 и т.д.) могут использоваться не для вопроса, а в обобщённом или неопределённом значении. Это выражает 'кто бы ни', 'где бы ни'. Например: 你去哪儿我就去哪儿 (Куда ты пойдёшь, туда и я).",
            "rule_tj": "Дар забони чинӣ асмои пурсишӣ (谁, 哪儿, 什么 ва ғ.) метавонанд на барои пурсиш, балки дар маъноии умумӣ ё номуайян истифода шаванд. Ин 'ҳар кӣ бошад', 'ҳар куҷо бошад' маъноҳоро медиҳад. Масалан: 你去哪儿我就去哪儿 (Ту ба куҷо равӣ, ман ҳам ба ҳамон ҷо мераваm).",
            "examples": [
                {"zh": "你去哪儿我就去哪儿。", "pinyin": "Nǐ qù nǎr wǒ jiù qù nǎr.", "uz": "Siz qayerga borsangiz, men ham boraman.", "ru": "Куда ты пойдёшь, туда и я пойду.", "tj": "Ту ба куҷо равӣ, ман ҳам ба ҳамон ҷо мераваm."},
                {"zh": "谁都可以参加。", "pinyin": "Shéi dōu kěyǐ cānjiā.", "uz": "Hamma ishtirok etishi mumkin.", "ru": "Любой может участвовать.", "tj": "Ҳар кас метавонад иштирок кунад."}
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
                {"prompt_uz": "panda", "prompt_ru": "панда", "prompt_tj": "панда", "answer": "熊猫", "pinyin": "xióngmāo"},
                {"prompt_uz": "lift", "prompt_ru": "лифт", "prompt_tj": "лифт", "answer": "电梯", "pinyin": "diàntī"},
                {"prompt_uz": "hojatxona", "prompt_ru": "туалет", "prompt_tj": "ҳоҷатхона", "answer": "洗手间", "pinyin": "xǐshǒujiān"},
                {"prompt_uz": "darhol", "prompt_ru": "немедленно", "prompt_tj": "дарҳол", "answer": "马上", "pinyin": "mǎshàng"}
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction_uz": "Bo'sh joyni to'ldiring:",
            "instruction_ru": "Заполните пропуск:",
            "instruction_tj": "Ҷойи холиро пур кунед:",
            "items": [
                {"prompt_uz": "Siz qayerga borsangiz, men ___ boraman. (就)", "prompt_ru": "Куда ты пойдёшь, я ___ пойду. (就)", "prompt_tj": "Ту ба куҷо равӣ, ман ___ мераваm. (就)", "answer": "就", "pinyin": "jiù"},
                {"prompt_uz": "U ___ kechikdi. (又)", "prompt_ru": "Он ___ опоздал. (又)", "prompt_tj": "Вай ___ дер монд. (又)", "answer": "又", "pinyin": "yòu"},
                {"prompt_uz": "Ertaga ___ keling. (再)", "prompt_ru": "Приходите ___ завтра. (再)", "prompt_tj": "Фардо ___ биёед. (再)", "answer": "再", "pinyin": "zài"},
                {"prompt_uz": "Men ___ chiqib ketaman. (马上)", "prompt_ru": "Я ___ выйду. (马上)", "prompt_tj": "Ман ___ мебароям. (马上)", "answer": "马上", "pinyin": "mǎshàng"}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "answers": ["熊猫", "电梯", "洗手间", "马上"]},
        {"no": 2, "answers": ["就", "又", "再", "马上"]}
    ], ensure_ascii=False),
    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction_uz": "Quyidagi so'zlardan foydalanib 3 ta jumla tuzing:",
            "instruction_ru": "Напишите 3 предложения, используя следующие слова:",
            "instruction_tj": "Бо истифодаи калимаҳои зерин 3 ҷумла нависед:",
            "words": ["熊猫", "电梯", "洗手间"],
            "example": "我们坐电梯去看熊猫，洗手间在左边。",
            "topic_uz": "Yo'nalish va harakat",
            "topic_ru": "Направление и движение",
            "topic_tj": "Самт ва ҳаракат"
        },
        {
            "no": 2,
            "instruction_uz": "Dars mavzusi bo'yicha 4-5 jumladan iborat qisqa matn yozing:",
            "instruction_ru": "Напишите короткий абзац из 4-5 предложений по теме урока:",
            "instruction_tj": "Дар бораи мавзӯи дарс 4-5 ҷумлаи кӯтоҳ нависед:",
            "words": ["哪儿", "就", "又", "再"],
            "example": "你去哪儿我就去哪儿，我们一起去看熊猫吧。",
            "topic_uz": "你去哪儿我就去哪儿",
            "topic_ru": "你去哪儿我就去哪儿",
            "topic_tj": "你去哪儿我就去哪儿"
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
