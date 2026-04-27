import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 4,
    "lesson_code": "HSK4-L04",
    "title": "不要太着急赚钱",
    "goal": "pul ishlash, ish va hayot balansi haqida gapirish; 以为, 原来, 并, 起初, 甚至 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Pul topishga shoshilmang' mavzusiga bag'ishlangan. Unda yangi ish boshlash, moddiy va ma'naviy qadriyatlar haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 以为, 原来, 并, 起初, 甚至.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "提", "pinyin": "tí", "pos": "v.", "meaning": "eslatmoq, aytmoq, ko'tarmoq"},
            {"no": 2, "zh": "以为", "pinyin": "yǐwéi", "pos": "v.", "meaning": "o'ylash (noto'g'ri bo'lib chiqadigan), xayol qilmoq"},
            {"no": 3, "zh": "份", "pinyin": "fèn", "pos": "m.", "meaning": "dona (ish, gazeta, hujjat uchun)"},
            {"no": 4, "zh": "完全", "pinyin": "wánquán", "pos": "adv.", "meaning": "butunlay, to'liq"},
            {"no": 5, "zh": "赚", "pinyin": "zhuàn", "pos": "v.", "meaning": "pul ishlash, daromad qilish"},
            {"no": 6, "zh": "调查", "pinyin": "diàochá", "pos": "v./n.", "meaning": "o'rganmoq, tekshirmoq; tadqiqot"},
            {"no": 7, "zh": "原来", "pinyin": "yuánlái", "pos": "adv./adj.", "meaning": "aslida, demak; dastlabki"},
            {"no": 8, "zh": "计划", "pinyin": "jìhuà", "pos": "n./v.", "meaning": "reja; reja qilmoq"},
            {"no": 9, "zh": "提前", "pinyin": "tíqián", "pos": "v.", "meaning": "oldindan qilmoq, muddatidan oldin"},
            {"no": 10, "zh": "保证", "pinyin": "bǎozhèng", "pos": "v./n.", "meaning": "kafolat bermoq; kafolat"},
            {"no": 11, "zh": "提醒", "pinyin": "tíxǐng", "pos": "v.", "meaning": "eslatmoq, ogohlantirilmoq"},
            {"no": 12, "zh": "乱", "pinyin": "luàn", "pos": "adj.", "meaning": "tartibsiz, chalkash; shoshqaloq"},
            {"no": 13, "zh": "起初", "pinyin": "qǐchū", "pos": "adv.", "meaning": "dastlab, boshida"},
            {"no": 14, "zh": "甚至", "pinyin": "shènzhì", "pos": "adv.", "meaning": "hatto, shu qadar"},
            {"no": 15, "zh": "并", "pinyin": "bìng", "pos": "adv.", "meaning": "umuman (inkor bilan), aslida emas"},
            {"no": 16, "zh": "收入", "pinyin": "shōurù", "pos": "n.", "meaning": "daromad, maosh"},
            {"no": 17, "zh": "稳定", "pinyin": "wěndìng", "pos": "adj.", "meaning": "barqaror, beqiyos"},
            {"no": 18, "zh": "努力", "pinyin": "nǔlì", "pos": "v./adj.", "meaning": "harakat qilmoq; g'ayratli"},
            {"no": 19, "zh": "成功", "pinyin": "chénggōng", "pos": "v./n.", "meaning": "muvaffaqiyat qozonmoq; muvaffaqiyat"},
            {"no": 20, "zh": "经历", "pinyin": "jīnglì", "pos": "n./v.", "meaning": "tajriba; boshdan kechirmoq"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "小林和小李聊小李的工作",
                "dialogue": [
                    {"speaker": "小林", "zh": "听说你找到新工作了？今年已经换了三次工作了。", "pinyin": "", "translation": "Eshitdim, yangi ish topdingmi? Bu yil allaqachon uch marta ish almashtirding."},
                    {"speaker": "小李", "zh": "对了！我以前以为薪水高的工作才是好工作，现在完全改变了想法。", "pinyin": "", "translation": "Ha! Ilgari men maoshi yuqori ish — yaxshi ish deb o'ylardim, endi fikrim butunlay o'zgardi."},
                    {"speaker": "小林", "zh": "以前那份工作不是挺好的吗？收入高，工作稳定。", "pinyin": "", "translation": "Oldingi ishing yaxshi emasmi? Maoshi yuqori, ishi barqaror."},
                    {"speaker": "小李", "zh": "起初以为不错，但实际上每天加班，甚至周末也要上班，这样下去并不好，所以我决定换一份工作。", "pinyin": "", "translation": "Boshida yaxshi deb o'ylardim, lekin aslida har kuni qo'shimcha ishlayman, hatto dushanba kunlari ham ishga boraman, bu holat umuman yaxshi emas, shu sababli ish almashtirishga qaror qildim."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "王经理和小李谈工作计划",
                "dialogue": [
                    {"speaker": "王经理", "zh": "那份调查报告应该需要多长时间才能做完？", "pinyin": "", "translation": "U tadqiqot hisoboti qancha vaqt oladi?"},
                    {"speaker": "小李", "zh": "原来的计划是周末，但是我们可以提前完成，周末前能保证完成。", "pinyin": "", "translation": "Dastlabki reja shanba kuni edi, lekin biz ertaroq tugatishimiz mumkin, shanba kunidan oldin kafolat bera olaman."},
                    {"speaker": "王经理", "zh": "虽然我们公司在做这类工作上经验还没那么多，但认真努力的态度非常重要，提醒你不要太着急。", "pinyin": "", "translation": "Garchi bizning kompaniyamizda bunday ishda tajriba unchalik ko'p bo'lmasa ham, jiddiy va g'ayratli munosabat juda muhim, sizni shoshmaslik haqida ogohlantiraman."},
                    {"speaker": "小李", "zh": "谢谢您的提醒！我明白了，成功需要时间，不要太乱，要按计划来。", "pinyin": "", "translation": "Eslatganiz uchun rahmat! Tushundim, muvaffaqiyat vaqt talab qiladi, shoshqaloq bo'lmay, rejaga ko'ra ish qilish kerak."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "以为",
                "explanation": "'...deb o'ylash (lekin noto'g'ri)' ma'nosini beradi. Ko'pincha keyinroq noto'g'ri bo'lib chiqqan fikrni bildiradi.",
                "examples": [
                    {"zh": "我以为他不来了，原来他在等我们。", "pinyin": "", "meaning": "Men u kelmaydi deb o'ylardim, aslida u bizni kutayotgan ekan."},
                    {"zh": "起初以为这份工作很好。", "pinyin": "", "meaning": "Boshida bu ish yaxshi deb o'ylardim."},
                ],
            },
            {
                "no": 2,
                "title_zh": "原来",
                "explanation": "'Aslida, demak (ajablanishni bildiradi)' yoki 'dastlabki holat' ma'nosini beradi.",
                "examples": [
                    {"zh": "原来他在这儿！我找了半天。", "pinyin": "", "meaning": "Demak u bu yerda ekan! Men uni anchadan beri qidiryapman."},
                    {"zh": "原来的计划是周末完成。", "pinyin": "", "meaning": "Dastlabki reja shanba kuni tugatish edi."},
                ],
            },
            {
                "no": 3,
                "title_zh": "并（不/没）",
                "explanation": "'Umuman emas, aslida emas' ma'nosini beradi. Inkor gaplarda kutilganidek emas ekanligini ta'kidlaydi.",
                "examples": [
                    {"zh": "这样下去并不好。", "pinyin": "", "meaning": "Bunday davom etish umuman yaxshi emas."},
                    {"zh": "他并没有不高兴，只是有点儿累。", "pinyin": "", "meaning": "U umuman xafa emas edi, shunchaki biroz charchagan edi."},
                ],
            },
            {
                "no": 4,
                "title_zh": "起初",
                "explanation": "'Boshida, dastlab' ma'nosini beradi. Biror hodisaning boshlanish vaqtini bildiradi.",
                "examples": [
                    {"zh": "起初我觉得这个工作很难，后来慢慢就好了。", "pinyin": "", "meaning": "Boshida bu ish juda qiyin deb o'ylardim, keyin asta-sekin yaxshi bo'ldi."},
                    {"zh": "起初他并不同意，后来改变了主意。", "pinyin": "", "meaning": "Boshida u rozi bo'lmadi, keyin fikrini o'zgartirdi."},
                ],
            },
            {
                "no": 5,
                "title_zh": "甚至",
                "explanation": "'Hatto, shu qadar' ma'nosini beradi. Kutilmagan yoki juda yuqori darajani bildiradi.",
                "examples": [
                    {"zh": "他每天加班，甚至周末也要上班。", "pinyin": "", "meaning": "U har kuni qo'shimcha ishlaydi, hatto shanba-yakshanba kunlari ham."},
                    {"zh": "她汉语说得很好，甚至比中国人还好。", "pinyin": "", "meaning": "U xitoycha juda yaxshi gapiradi, hatto xitoyliklardan ham yaxshiroq."},
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
                    {"prompt": "pul ishlash", "answer": "赚钱", "pinyin": "zhuàn qián"},
                    {"prompt": "kafolat bermoq", "answer": "保证", "pinyin": "bǎozhèng"},
                    {"prompt": "eslatmoq", "answer": "提醒", "pinyin": "tíxǐng"},
                    {"prompt": "daromad", "answer": "收入", "pinyin": "shōurù"},
                    {"prompt": "muvaffaqiyat", "answer": "成功", "pinyin": "chénggōng"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "以为", "answer": "o'ylash (noto'g'ri bo'lib chiqadigan)", "pinyin": "yǐwéi"},
                    {"prompt": "原来", "answer": "aslida, demak", "pinyin": "yuánlái"},
                    {"prompt": "甚至", "answer": "hatto, shu qadar", "pinyin": "shènzhì"},
                    {"prompt": "起初", "answer": "boshida, dastlab", "pinyin": "qǐchū"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (以为、原来、并、起初、甚至):",
                "items": [
                    {"prompt": "我______他已经回国了，______他还在这儿。", "answer": "以为 / 原来", "pinyin": "yǐwéi / yuánlái"},
                    {"prompt": "他______没有生气，只是有点累。", "answer": "并", "pinyin": "bìng"},
                    {"prompt": "______，我不喜欢吃辣的，现在______爱上了四川菜。", "answer": "起初 / 甚至", "pinyin": "qǐchū / shènzhì"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["赚钱", "保证", "提醒", "收入", "成功"]},
            {"no": 2, "answers": ["o'ylash (noto'g'ri bo'lib chiqadigan)", "aslida, demak", "hatto, shu qadar", "boshida, dastlab"]},
            {"no": 3, "answers": ["以为 / 原来", "并", "起初 / 甚至"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["以为", "原来", "甚至", "努力"],
                "example": "起初我以为这份工作很好，原来需要甚至周末也工作。",
            },
            {
                "no": 2,
                "instruction": "'并不/并没...' va '甚至...' qoliplaridan foydalanib har biridan 2 ta gap tuzing.",
                "topic": "ish va pul topish mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Sizning karyera va hayot maqsadlaringiz qanday? 你的职业理想是什么？",
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
