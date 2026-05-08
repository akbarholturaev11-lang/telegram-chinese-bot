import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 7,
    "lesson_code": "HSK3-L07",
    "title": "我跟她都认识五年了",
    "goal": json.dumps({"uz": "Muddatni ifodalash va tanishlik haqida gapirishni o'rganish.", "ru": "Изучение выражения продолжительности и знакомства.", "tj": "Омӯзиши ифодаи муддат ва шиносоӣ."}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu dars muddatni ifodalash va tanishlik haqida gapirishga bag'ishlangan. 5 ta asosiy so'z o'rganiladi va 'vaqt davri ifodalash' hamda '半', '刻', '差' orqali vaqtni bildirish grammatik shakllar o'zlashtiriladi.", "ru": "Этот урок посвящён выражению продолжительности и знакомства. Изучаются 5 ключевых слов и грамматические конструкции для выражения временного периода, а также использование '半', '刻', '差' для выражения времени.", "tj": "Ин дарс ба ифодаи муддат ва шиносоӣ бахшида шудааст. 5 калимаи асосӣ омӯхта мешавад ва сохторҳои грамматикӣ барои ифодаи давраи вақт, инчунин истифодаи '半', '刻', '差' барои ифодаи вақт аз бар карда мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "同事", "pinyin": "tóngshì", "pos": "n.", "uz": "hamkasb, ishchi", "ru": "коллега, сослуживец", "tj": "ҳамкор, ҳамхизмат"},
        {"no": 2, "zh": "银行", "pinyin": "yínháng", "pos": "n.", "uz": "bank", "ru": "банк", "tj": "бонк"},
        {"no": 3, "zh": "结婚", "pinyin": "jiéhūn", "pos": "v.", "uz": "uylanmoq, turmush qurmoq", "ru": "жениться, выйти замуж", "tj": "издивоҷ кардан, хонадор шудан"},
        {"no": 4, "zh": "迟到", "pinyin": "chídào", "pos": "v.", "uz": "kechikmoq", "ru": "опоздать, прийти с опозданием", "tj": "дер омадан, кеч мондан"},
        {"no": 5, "zh": "半", "pinyin": "bàn", "pos": "num.", "uz": "yarim", "ru": "половина", "tj": "ним, нисф"}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_uz": "Eski do'stlar",
            "scene_ru": "Старые друзья",
            "scene_tj": "Дӯстони қадимӣ",
            "dialogue": [
                {"speaker": "A", "zh": "你跟她认识多久了？", "pinyin": "Nǐ gēn tā rènshi duō jiǔ le?", "uz": "Siz u bilan qancha vaqtdan beri tanishsiz?", "ru": "Как давно ты с ней знаком(а)?", "tj": "Шумо бо вай чанд вақт боз шинос ҳастед?"},
                {"speaker": "B", "zh": "我跟她都认识五年了。", "pinyin": "Wǒ gēn tā dōu rènshi wǔ nián le.", "uz": "Men u bilan besh yildan beri tanishman.", "ru": "Мы с ней знакомы уже пять лет.", "tj": "Ман бо вай панҷ сол боз шинос ҳастам."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_uz": "Bankda",
            "scene_ru": "В банке",
            "scene_tj": "Дар бонк",
            "dialogue": [
                {"speaker": "A", "zh": "你们以前是同事吗？", "pinyin": "Nǐmen yǐqián shì tóngshì ma?", "uz": "Siz oldin hamkasb edingizmi?", "ru": "Вы раньше были коллегами?", "tj": "Шумо пеш ҳамкор будед?"},
                {"speaker": "B", "zh": "对，我们在银行一起工作过。", "pinyin": "Duì, wǒmen zài yínháng yìqǐ gōngzuò guo.", "uz": "Ha, biz bankda birga ishlaganmiz.", "ru": "Да, мы вместе работали в банке.", "tj": "Бале, мо дар бонк якҷоя кор карда будем."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "时段的表达",
            "title_uz": "Vaqt davomiyligini ifodalash",
            "title_ru": "Выражение продолжительности времени",
            "title_tj": "Ифодаи давомнокии вақт",
            "rule_uz": "Harakat muddatini ifodalash uchun vaqt birligini fe'ldan keyin yozamiz. Tuzilish: Mavzu + fe'l + vaqt davomiyligi + 了. Masalan: 认识五年了 (besh yildan beri tanishman). Savol: 多久？ (qancha vaqt?). Davom etayotgan holat uchun 了 qo'yiladi.",
            "rule_ru": "Для выражения продолжительности действия единица времени ставится после глагола. Структура: Подлежащее + глагол + продолжительность + 了. Например: 认识五年了 (знакомы уже пять лет). Вопрос: 多久？ (как долго?). Для обозначения продолжающегося состояния добавляется 了.",
            "rule_tj": "Барои ифодаи муддати амал воҳиди вақт баъд аз феъл гузошта мешавад. Сохтор: Мубтадо + феъл + давомнокии вақт + 了. Масалан: 认识五年了 (панҷ сол боз шинос ҳастам). Пурсиш: 多久？ (чанд вақт?). Барои нишон додани ҳолати давомдор 了 зиёд мешавад.",
            "examples": [
                {"zh": "我跟她都认识五年了。", "pinyin": "Wǒ gēn tā dōu rènshi wǔ nián le.", "uz": "Men u bilan besh yildan beri tanishman.", "ru": "Мы с ней знакомы уже пять лет.", "tj": "Ман бо вай панҷ сол боз шинос ҳастам."},
                {"zh": "他学汉语学了三年了。", "pinyin": "Tā xué Hànyǔ xué le sān nián le.", "uz": "U uch yildan beri xitoy tilini o'rganmoqda.", "ru": "Он уже три года изучает китайский.", "tj": "Вай се сол боз забони чинӣ меомӯзад."}
            ]
        },
        {
            "no": 2,
            "title_zh": "用“半”“刻”“差”表示时间",
            "title_uz": "'Bàn', 'kè', 'chā' bilan vaqtni ifodalash",
            "title_ru": "Выражение времени с помощью '半', '刻', '差'",
            "title_tj": "Ифодаи вақт бо '半', '刻', '差'",
            "rule_uz": "Vaqtni aniq ifodalash uchun: 半 (yarim — 30 daqiqa), 刻 (chorak — 15 daqiqa), 差 (… ga yetmay — minus). Masalan: 两点半 (ikki yarim — 2:30), 两点一刻 (ikki va chorak — 2:15), 差五分两点 (ikki ga besh daqiqa qoldi — 1:55).",
            "rule_ru": "Для точного выражения времени: 半 (половина — 30 минут), 刻 (четверть — 15 минут), 差 (без … — минус). Например: 两点半 (половина третьего — 2:30), 两点一刻 (четверть третьего — 2:15), 差五分两点 (без пяти два — 1:55).",
            "rule_tj": "Барои ифодаи дақиқи вақт: 半 (ним — 30 дақиқа), 刻 (чоряк — 15 дақиқа), 差 (бе… — манфӣ). Масалан: 两点半 (соати ду ва ним — 2:30), 两点一刻 (соати ду ва чоряк — 2:15), 差五分两点 (панҷ дақиқа то соати ду — 1:55).",
            "examples": [
                {"zh": "他们结婚已经三年半了。", "pinyin": "Tāmen jiéhūn yǐjīng sān nián bàn le.", "uz": "Ular uch yarim yildan beri turmush qurishgan.", "ru": "Они женаты уже три с половиной года.", "tj": "Онҳо се сол ва ним боз оилавӣ ҳастанд."},
                {"zh": "差五分他就迟到了。", "pinyin": "Chā wǔ fēn tā jiù chídào le.", "uz": "Besh daqiqa qolsa u kechikardi.", "ru": "Пять минут — и он опоздал бы.", "tj": "Панҷ дақиқа монда буд ки дер монд."}
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
                {"prompt_uz": "hamkasb", "prompt_ru": "коллега", "prompt_tj": "ҳамкор", "answer": "同事", "pinyin": "tóngshì"},
                {"prompt_uz": "bank", "prompt_ru": "банк", "prompt_tj": "бонк", "answer": "银行", "pinyin": "yínháng"},
                {"prompt_uz": "turmush qurmoq", "prompt_ru": "жениться", "prompt_tj": "хонадор шудан", "answer": "结婚", "pinyin": "jiéhūn"},
                {"prompt_uz": "kechikmoq", "prompt_ru": "опоздать", "prompt_tj": "кеч мондан", "answer": "迟到", "pinyin": "chídào"}
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction_uz": "Bo'sh joyni to'ldiring:",
            "instruction_ru": "Заполните пропуск:",
            "instruction_tj": "Ҷойи холиро пур кунед:",
            "items": [
                {"prompt_uz": "Men u bilan ___ yildan beri tanishman. (五)", "prompt_ru": "Я с ней знаком(а) уже ___ лет. (五)", "prompt_tj": "Ман бо вай ___ сол боз шинос ҳастам. (五)", "answer": "五", "pinyin": "wǔ"},
                {"prompt_uz": "Ular bankda birga ___ ganlar. (工作)", "prompt_ru": "Они ___ вместе в банке. (工作)", "prompt_tj": "Онҳо дар бонк якҷоя ___ буданд. (工作)", "answer": "工作", "pinyin": "gōngzuò"},
                {"prompt_uz": "U ___ ikki yarim yildan beri. (结婚)", "prompt_ru": "Они ___ уже два с половиной года. (结婚)", "prompt_tj": "Онҳо ду сол ва ним боз ___. (结婚)", "answer": "结婚", "pinyin": "jiéhūn"},
                {"prompt_uz": "Besh daqiqa kechiksa ___ bo'ladi. (迟到)", "prompt_ru": "Пять минут — и ___ будет. (迟到)", "prompt_tj": "Панҷ дақиқа монда буд ки ___ мемонд. (迟到)", "answer": "迟到", "pinyin": "chídào"}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "answers": ["同事", "银行", "结婚", "迟到"]},
        {"no": 2, "answers": ["五", "工作", "结婚", "迟到"]}
    ], ensure_ascii=False),
    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction_uz": "Quyidagi so'zlardan foydalanib 3 ta jumla tuzing:",
            "instruction_ru": "Составьте 3 предложения, используя следующие слова:",
            "instruction_tj": "Бо истифодаи калимаҳои зерин 3 ҷумла созед:",
            "words": ["同事", "银行", "结婚"],
            "example": "我跟同事在银行认识，他们结婚了。",
            "topic_uz": "Muddatni ifodalash",
            "topic_ru": "Выражение продолжительности",
            "topic_tj": "Ифодаи муддат"
        },
        {
            "no": 2,
            "instruction_uz": "Dars mavzusi bo'yicha 4-5 jumladan iborat qisqa matn yozing:",
            "instruction_ru": "Напишите короткий абзац из 4-5 предложений по теме урока:",
            "instruction_tj": "Дар бораи мавзӯи дарс 4-5 ҷумлаи кӯтоҳ нависед:",
            "words": ["认识", "年了", "同事"],
            "example": "我跟同事认识三年了，我们在银行工作。",
            "topic_uz": "我跟她都认识五年了",
            "topic_ru": "我跟她都认识五年了",
            "topic_tj": "我跟她都认识五年了"
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
