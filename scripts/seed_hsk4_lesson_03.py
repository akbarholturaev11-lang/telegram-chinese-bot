import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 3,
    "lesson_code": "HSK4-L03",
    "title": "经理对我印象不错",
    "goal": "ish topish, suhbat va ish muhiti haqida gapirish; 越...越..., 本来, 另外, 首先...其次..., 不管 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Menejer men haqimda yaxshi fikrda' mavzusiga bag'ishlangan. Unda ish intervyusi, ish topish va yangi ish joyiga ko'nikish haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 越...越..., 本来, 另外, 首先...其次..., 不管.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "挺", "pinyin": "tǐng", "pos": "adv.", "meaning": "juda, ancha (og'zaki)"},
            {"no": 2, "zh": "紧张", "pinyin": "jǐnzhāng", "pos": "adj.", "meaning": "asabiy, ta'sirchan, hayajonlangan"},
            {"no": 3, "zh": "信心", "pinyin": "xìnxīn", "pos": "n.", "meaning": "ishonch, o'ziga ishonch"},
            {"no": 4, "zh": "能力", "pinyin": "nénglì", "pos": "n.", "meaning": "qobiliyat, mahorat"},
            {"no": 5, "zh": "招聘", "pinyin": "zhāopìn", "pos": "v.", "meaning": "ishchi yollash, xodim qidirish"},
            {"no": 6, "zh": "提供", "pinyin": "tígōng", "pos": "v.", "meaning": "ta'minlamoq, bermoq"},
            {"no": 7, "zh": "负责", "pinyin": "fùzé", "pos": "v.", "meaning": "mas'ul bo'lmoq, javobgarlikni o'z zimmasiga olmoq"},
            {"no": 8, "zh": "本来", "pinyin": "běnlái", "pos": "adv.", "meaning": "aslida, dastlab, oldindan"},
            {"no": 9, "zh": "应聘", "pinyin": "yìngpìn", "pos": "v.", "meaning": "ish uchun murojaat qilmoq, intervyuga bormoq"},
            {"no": 10, "zh": "材料", "pinyin": "cáiliào", "pos": "n.", "meaning": "material, hujjat, ma'lumot"},
            {"no": 11, "zh": "符合", "pinyin": "fúhé", "pos": "v.", "meaning": "mos kelmoq, muvofiq bo'lmoq"},
            {"no": 12, "zh": "通知", "pinyin": "tōngzhī", "pos": "v./n.", "meaning": "xabar bermoq; xabarnoma"},
            {"no": 13, "zh": "越", "pinyin": "yuè", "pos": "adv.", "meaning": "tobora, borgan sari"},
            {"no": 14, "zh": "另外", "pinyin": "lìngwài", "pos": "adv./conj.", "meaning": "bundan tashqari, boshqacha"},
            {"no": 15, "zh": "首先", "pinyin": "shǒuxiān", "pos": "adv.", "meaning": "avvalo, birinchi navbatda"},
            {"no": 16, "zh": "其次", "pinyin": "qícì", "pos": "adv.", "meaning": "ikkinchidan, so'ngra"},
            {"no": 17, "zh": "不管", "pinyin": "bùguǎn", "pos": "conj.", "meaning": "qanday bo'lmasin, nima bo'lsa ham"},
            {"no": 18, "zh": "面试", "pinyin": "miànshì", "pos": "v./n.", "meaning": "og'zaki suhbat o'tkazmoq; og'zaki suhbat"},
            {"no": 19, "zh": "经验", "pinyin": "jīngyàn", "pos": "n.", "meaning": "tajriba"},
            {"no": 20, "zh": "机会", "pinyin": "jīhuì", "pos": "n.", "meaning": "imkoniyat, fursat"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "小夏和小雨聊小夏面试的情况",
                "dialogue": [
                    {"speaker": "小夏", "zh": "你上午的面试怎么样？", "pinyin": "", "translation": "Ertalabki suhbating qanday o'tdi?"},
                    {"speaker": "小雨", "zh": "还可以，他们问的问题都挺容易的，就是我有点儿紧张。", "pinyin": "", "translation": "Yaxshi edi, berishgan savollar ancha oson edi, lekin men biroz asabiy bo'ldim."},
                    {"speaker": "小夏", "zh": "面试的时候，一定要表现出自己有能力、有信心。", "pinyin": "", "translation": "Suhbatda o'zingning qobiliyatli va ishonchli ekanligini ko'rsatish kerak."},
                    {"speaker": "小雨", "zh": "这次招聘对我来说是个好机会，我们一起去看看吧，越了解越有信心。", "pinyin": "", "translation": "Bu ishga yollash men uchun yaxshi imkoniyat, birga borib ko'ramiz, qancha ko'p bilsak, shuncha ko'p ishonch hosil qilamiz."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "马经理和小林聊招聘的事情",
                "dialogue": [
                    {"speaker": "马经理", "zh": "林，这次招聘不是小事，你觉得应该怎么做？", "pinyin": "", "translation": "Lin, bu safar ishga yollash kichik ish emas, qanday qilishimiz kerak deb o'ylaysiz?"},
                    {"speaker": "小林", "zh": "本来是小季员责任的，但他突然生病住院了，所以就委给我来做了。", "pinyin": "", "translation": "Bu aslida kichik Ji-ning mas'uliyati edi, lekin u to'satdan kasalxonaga yotdi, shuning uchun menga topshirildi."},
                    {"speaker": "马经理", "zh": "哦，这次应聘的人多吗？", "pinyin": "", "translation": "E, bu safar murojaat qilganlar ko'pmi?"},
                    {"speaker": "小林", "zh": "本次共有应聘者15人，经过笔试和面试，有两个人不错。这是他们提供的材料，都符合我们的要求。另外，我已经通知他们下周一来办公室。", "pinyin": "", "translation": "Bu safar jami 15 kishi murojaat qildi, yozma va og'zaki suhbatdan so'ng ikkita kishi yaxshi bo'ldi. Bu ularning hujjatlari, hammasi bizning talablarimizga mos keladi. Bundan tashqari, men ularni dushanba kuni ofisga kelishga chaqirdim."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "越……越……",
                "explanation": "'Qancha...shuncha...' ma'nosini beradi. Birinchi 越 dan keyingi holat ortishi bilan, ikkinchi 越 dan keyingi natija ham ortadi.",
                "examples": [
                    {"zh": "越了解越有信心。", "pinyin": "", "meaning": "Qancha ko'p bilsak, shuncha ko'proq ishonch hosil qilamiz."},
                    {"zh": "天气越来越冷了。", "pinyin": "", "meaning": "Havo tobora sovuq bo'lmoqda."},
                ],
            },
            {
                "no": 2,
                "title_zh": "本来",
                "explanation": "'Aslida, dastlab' ma'nosini beradi. Hozirgi holat aslida boshqacha bo'lishi kerak edi, degan ma'noni bildiradi.",
                "examples": [
                    {"zh": "本来是小季的责任，但他生病了。", "pinyin": "", "meaning": "Bu aslida kichik Ji-ning mas'uliyati edi, lekin u kasal bo'ldi."},
                    {"zh": "我本来想去，但没时间。", "pinyin": "", "meaning": "Men aslida bormoqchi edim, lekin vaqtim bo'lmadi."},
                ],
            },
            {
                "no": 3,
                "title_zh": "另外",
                "explanation": "'Bundan tashqari, yana' ma'nosini beradi. Avvalgi gapdagi ma'lumotga qo'shimcha ma'lumot qo'shadi.",
                "examples": [
                    {"zh": "另外，我已经通知他们了。", "pinyin": "", "meaning": "Bundan tashqari, men ularni allaqachon xabardor qildim."},
                    {"zh": "他会说英语，另外还会说法语。", "pinyin": "", "meaning": "U inglizcha gapiradi, bundan tashqari frantsuzcha ham biladi."},
                ],
            },
            {
                "no": 4,
                "title_zh": "首先……其次……",
                "explanation": "'Avvalo...ikkinchidan...' ma'nosini beradi. Bir nechta fikrni tartib bilan sanash uchun ishlatiladi.",
                "examples": [
                    {"zh": "首先要有能力，其次还要有经验。", "pinyin": "", "meaning": "Avvalo qobiliyat kerak, ikkinchidan tajriba ham zarur."},
                    {"zh": "首先感谢大家，其次介绍一下情况。", "pinyin": "", "meaning": "Avvalo hammaga rahmat, keyin vaziyatni tushuntiraman."},
                ],
            },
            {
                "no": 5,
                "title_zh": "不管……都/也……",
                "explanation": "'Qanday bo'lmasin, baribir...' ma'nosini beradi. Har qanday holatda ham natija o'zgarmasligini bildiradi.",
                "examples": [
                    {"zh": "不管多忙，他都会按时完成工作。", "pinyin": "", "meaning": "Qancha band bo'lmasin, u ishni o'z vaqtida tugatadi."},
                    {"zh": "不管天气怎么样，我们都要去。", "pinyin": "", "meaning": "Ob-havo qanday bo'lmasin, biz baribir boramiz."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "exercise_json": json.dumps(
        [
            {
                "no": 1,
                "type": "translate_to_chinese",
                "instruction": "Quyidagi so'zlarning xitoychasini yozing:",
                "items": [
                    {"prompt": "qobiliyat, mahorat", "answer": "能力", "pinyin": "nénglì"},
                    {"prompt": "ishonch", "answer": "信心", "pinyin": "xìnxīn"},
                    {"prompt": "mos kelmoq", "answer": "符合", "pinyin": "fúhé"},
                    {"prompt": "tajriba", "answer": "经验", "pinyin": "jīngyàn"},
                    {"prompt": "imkoniyat", "answer": "机会", "pinyin": "jīhuì"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "招聘", "answer": "ishchi yollash", "pinyin": "zhāopìn"},
                    {"prompt": "负责", "answer": "mas'ul bo'lmoq", "pinyin": "fùzé"},
                    {"prompt": "通知", "answer": "xabar bermoq", "pinyin": "tōngzhī"},
                    {"prompt": "另外", "answer": "bundan tashqari", "pinyin": "lìngwài"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (越、本来、另外、首先、不管):",
                "items": [
                    {"prompt": "______，要有能力，______还要有经验。", "answer": "首先 / 其次", "pinyin": "shǒuxiān / qícì"},
                    {"prompt": "天气______来______热了。", "answer": "越 / 越", "pinyin": "yuè / yuè"},
                    {"prompt": "______多忙，她也会按时来。", "answer": "不管", "pinyin": "bùguǎn"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["能力", "信心", "符合", "经验", "机会"]},
            {"no": 2, "answers": ["ishchi yollash", "mas'ul bo'lmoq", "xabar bermoq", "bundan tashqari"]},
            {"no": 3, "answers": ["首先 / 其次", "越 / 越", "不管"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["能力", "经验", "机会", "负责"],
                "example": "首先要有能力，其次还要有丰富的经验。",
            },
            {
                "no": 2,
                "instruction": "'越...越...' va '不管...都...' qoliplaridan foydalanib har biridan 2 ta gap tuzing.",
                "topic": "ish va o'qish mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Ish intervyusida o'zingizni qanday taqdim etasiz? 如果参加面试，你会怎么介绍自己？",
            },
        ],
        ensure_ascii=False,
    ),
    "review_json": "[]",
    "is_active": True,
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
