import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 1,
    "lesson_code": "HSK4-L01",
    "title": "简单的爱情",
    "goal": "romantik munosabatlar va sevgi haqida gapirish; 不仅…也…, 从来, 刚, 即使…也… grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Oddiy sevgi' mavzusiga bag'ishlangan. Unda turmush o'rtoq tanlash, sevgi va munosabatlar haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 不仅...也/还/而且..., 从来, 刚, 即使...也..., (在)...上.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "法律", "pinyin": "fǎlǜ", "pos": "n.", "meaning": "huquq, qonun"},
            {"no": 2, "zh": "俩", "pinyin": "liǎ", "pos": "num.-m.", "meaning": "ikkalasi, ikki (kishi)"},
            {"no": 3, "zh": "印象", "pinyin": "yìnxiàng", "pos": "n.", "meaning": "taassurot"},
            {"no": 4, "zh": "深", "pinyin": "shēn", "pos": "adj.", "meaning": "chuqur"},
            {"no": 5, "zh": "熟悉", "pinyin": "shúxī", "pos": "v.", "meaning": "yaxshi bilmoq, tanish bo'lmoq"},
            {"no": 6, "zh": "不仅", "pinyin": "bùjǐn", "pos": "conj.", "meaning": "nafaqat, faqat emas"},
            {"no": 7, "zh": "性格", "pinyin": "xìnggé", "pos": "n.", "meaning": "xarakter, tabiat"},
            {"no": 8, "zh": "开玩笑", "pinyin": "kāi wánxiào", "pos": "v.", "meaning": "hazil qilmoq, kulgi qilmoq"},
            {"no": 9, "zh": "从来", "pinyin": "cónglái", "pos": "adv.", "meaning": "hech qachon (inkor bilan), doim"},
            {"no": 10, "zh": "最好", "pinyin": "zuìhǎo", "pos": "adv.", "meaning": "eng yaxshisi, ma'quli"},
            {"no": 11, "zh": "共同", "pinyin": "gòngtóng", "pos": "adj.", "meaning": "umumiy, birgalikdagi"},
            {"no": 12, "zh": "适合", "pinyin": "shìhé", "pos": "v.", "meaning": "mos kelmoq, to'g'ri kelmoq"},
            {"no": 13, "zh": "幸福", "pinyin": "xìngfú", "pos": "adj./n.", "meaning": "baxtli; baxt"},
            {"no": 14, "zh": "生活", "pinyin": "shēnghuó", "pos": "v./n.", "meaning": "yashash; hayot, turmush"},
            {"no": 15, "zh": "刚", "pinyin": "gāng", "pos": "adv.", "meaning": "hozir, yaqinda (nisbatan)"},
            {"no": 16, "zh": "浪漫", "pinyin": "làngmàn", "pos": "adj.", "meaning": "romantik"},
            {"no": 17, "zh": "够", "pinyin": "gòu", "pos": "v./adj.", "meaning": "yetarli bo'lmoq; yetarli"},
            {"no": 18, "zh": "缺点", "pinyin": "quēdiǎn", "pos": "n.", "meaning": "kamchilik, nuqson"},
            {"no": 19, "zh": "接受", "pinyin": "jiēshòu", "pos": "v.", "meaning": "qabul qilmoq"},
            {"no": 20, "zh": "羡慕", "pinyin": "xiànmù", "pos": "v.", "meaning": "hasad qilmoq, qiziqish bilan qarash"},
            {"no": 21, "zh": "爱情", "pinyin": "àiqíng", "pos": "n.", "meaning": "sevgi (romantik)"},
            {"no": 22, "zh": "星星", "pinyin": "xīngxīng", "pos": "n.", "meaning": "yulduz"},
            {"no": 23, "zh": "即使", "pinyin": "jíshǐ", "pos": "conj.", "meaning": "hatto agar...ham"},
            {"no": 24, "zh": "加班", "pinyin": "jiābān", "pos": "v.", "meaning": "qo'shimcha ish soatlarida ishlash"},
            {"no": 25, "zh": "照", "pinyin": "zhào", "pos": "v.", "meaning": "yoritmoq, nur sochmoq"},
            {"no": 26, "zh": "感动", "pinyin": "gǎndòng", "pos": "v.", "meaning": "ta'sir qilmoq, his qilmoq"},
            {"no": 27, "zh": "自然", "pinyin": "zìrán", "pos": "adv.", "meaning": "tabiiyki, o'z-o'zidan"},
            {"no": 28, "zh": "原因", "pinyin": "yuányīn", "pos": "n.", "meaning": "sabab"},
            {"no": 29, "zh": "互相", "pinyin": "hùxiāng", "pos": "adv.", "meaning": "bir-biriga, o'zaro"},
            {"no": 30, "zh": "吸引", "pinyin": "xīyǐn", "pos": "v.", "meaning": "jalb qilmoq, tortmoq"},
            {"no": 31, "zh": "脾气", "pinyin": "píqì", "pos": "n.", "meaning": "fe'l-atvor, kayfiyat"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "孙月和王静聊王静男朋友的事情",
                "dialogue": [
                    {"speaker": "孙月", "zh": "听说你哥哥最近要结婚了，他是你同学吗？", "pinyin": "", "translation": "Eshitdim, akang yaqinda uylanadi, u sening sinfdoshing ekanmi?"},
                    {"speaker": "王静", "zh": "不是，他学的是新闻，我学的是法律，我们不是一个班。", "pinyin": "", "translation": "Yo'q, u jurnalistika o'qiydi, men esa huquq, biz bir guruhda emasmiz."},
                    {"speaker": "孙月", "zh": "那你们俩是怎么认识的？", "pinyin": "", "translation": "Xo'sh, siz ikkalangiz qanday tanishib qoldingiz?"},
                    {"speaker": "王静", "zh": "我们是在足球比赛中认识的，我对他的印象很深，他不仅踢球踢得好，性格也不错。", "pinyin": "", "translation": "Biz futbol musobaqasida tanishdik, u menga katta taassurot qoldirdi — nafaqat yaxshi futbol o'ynaydi, xarakteri ham yaxshi."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "王静跟李老师聊她要结婚的事情",
                "dialogue": [
                    {"speaker": "王静", "zh": "李老师，我下周五就要结婚了。", "pinyin": "", "translation": "O'qituvchi Li, men kelasi juma kuni turmushga chiqaman."},
                    {"speaker": "李老师", "zh": "你是在开玩笑吧？你们不是才认识一个月？", "pinyin": "", "translation": "Hazil qilayapsanmi? Siz bir oy oldin tanishmagandingizmi?"},
                    {"speaker": "王静", "zh": "虽然我们认识的时间不长，但我从来没有这么快乐过。我们有共同的爱好，彼此很适合。", "pinyin": "", "translation": "Garchi biz uzoq vaqt tanish bo'lmasak-da, men hech qachon bunday baxtli bo'lmagan edim. Bizda umumiy qiziqishlar bor, bir-birimizga mos kelamiz."},
                    {"speaker": "李老师", "zh": "那太好了！祝你们幸福！", "pinyin": "", "translation": "Bu juda yaxshi! Sizlarga baxt tilayman!"},
                ],
            },
            {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": "高老师和李老师聊婚姻生活",
                "dialogue": [
                    {"speaker": "高老师", "zh": "听说您和丈夫结婚快二十年了？", "pinyin": "", "translation": "Eshitdim, siz eringiz bilan yigirma yilga yaqin turmush qurgan ekansiz?"},
                    {"speaker": "李老师", "zh": "是的。刚结婚那时候，每天都很浪漫，现在生活虽然不够浪漫，但是我们很幸福。", "pinyin": "", "translation": "Ha. Yangi turmush qurgan paytimizda hamma narsa romantik edi, hozir hayot unchalik romantik emas, lekin biz baxtlimiz."},
                    {"speaker": "高老师", "zh": "幸福的原因是什么？", "pinyin": "", "translation": "Baxtning sababi nima?"},
                    {"speaker": "李老师", "zh": "即使有缺点，也要互相接受、互相吸引。简单的生活就是最大的幸福。", "pinyin": "", "translation": "Hatto kamchiliklari bo'lsa ham, bir-birini qabul qilish, bir-biriga jalb bo'lish kerak. Oddiy hayot — eng katta baxt."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "不仅……也/还/而且……",
                "explanation": "'Nafaqat...balki...ham' ma'nosini beradi. Birinchi gapda 不仅, ikkinchi gapda 也, 还 yoki 而且 ishlatiladi.",
                "examples": [
                    {"zh": "他不仅足球踢得好，性格也不错。", "pinyin": "", "meaning": "U nafaqat futbolni yaxshi o'ynaydi, xarakteri ham yaxshi."},
                    {"zh": "这里不仅风景美，而且空气也很好。", "pinyin": "", "meaning": "Bu yerda nafaqat manzara chiroyli, balki havo ham yaxshi."},
                ],
            },
            {
                "no": 2,
                "title_zh": "从来",
                "explanation": "'Hech qachon' yoki 'doim' ma'nosini beradi. Ko'pincha inkor fe'llari (不/没) bilan birga ishlatiladi.",
                "examples": [
                    {"zh": "我从来没有这么快乐过。", "pinyin": "", "meaning": "Men hech qachon bunday baxtli bo'lmagan edim."},
                    {"zh": "他从来不迟到。", "pinyin": "", "meaning": "U hech qachon kech qolmaydi."},
                ],
            },
            {
                "no": 3,
                "title_zh": "刚",
                "explanation": "'Hozirgina, yaqinda' ma'nosini beradi. Biror narsa yaqin o'tmishda bo'lganini bildiradi.",
                "examples": [
                    {"zh": "刚结婚那时候，每天都很浪漫。", "pinyin": "", "meaning": "Yangi turmush qurgan paytimizda hamma kun romantik edi."},
                    {"zh": "我刚到家，你就来了。", "pinyin": "", "meaning": "Men uyga hozirgina kelgan edim, sen ham kelding."},
                ],
            },
            {
                "no": 4,
                "title_zh": "即使……也……",
                "explanation": "'Hatto agar...bo'lsa ham' ma'nosini beradi. Shart qanchalik og'ir bo'lmasin, natija o'zgarmaydi.",
                "examples": [
                    {"zh": "即使有缺点，也要互相接受。", "pinyin": "", "meaning": "Hatto kamchiliklari bo'lsa ham, bir-birini qabul qilish kerak."},
                    {"zh": "即使很忙，他也会打电话。", "pinyin": "", "meaning": "Hatto band bo'lsa ham, u qo'ng'iroq qiladi."},
                ],
            },
            {
                "no": 5,
                "title_zh": "（在）……上",
                "explanation": "'...jihatidan, ...sohasida' ma'nosini beradi. Biror sohani yoki aspektni bildiradi.",
                "examples": [
                    {"zh": "在性格上，他们两个很合适。", "pinyin": "", "meaning": "Xarakter jihatidan, ular ikkalasi juda mos keladi."},
                    {"zh": "在学习上，他很认真。", "pinyin": "", "meaning": "O'qish sohasida u juda tirishqoq."},
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
                    {"prompt": "taassurot", "answer": "印象", "pinyin": "yìnxiàng"},
                    {"prompt": "xarakter, tabiat", "answer": "性格", "pinyin": "xìnggé"},
                    {"prompt": "umumiy, birgalikdagi", "answer": "共同", "pinyin": "gòngtóng"},
                    {"prompt": "mos kelmoq", "answer": "适合", "pinyin": "shìhé"},
                    {"prompt": "kamchilik", "answer": "缺点", "pinyin": "quēdiǎn"},
                    {"prompt": "sevgi (romantik)", "answer": "爱情", "pinyin": "àiqíng"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "幸福", "answer": "baxtli; baxt", "pinyin": "xìngfú"},
                    {"prompt": "浪漫", "answer": "romantik", "pinyin": "làngmàn"},
                    {"prompt": "吸引", "answer": "jalb qilmoq", "pinyin": "xīyǐn"},
                    {"prompt": "接受", "answer": "qabul qilmoq", "pinyin": "jiēshòu"},
                    {"prompt": "脾气", "answer": "fe'l-atvor, kayfiyat", "pinyin": "píqì"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (不仅、从来、即使、适合、共同):",
                "items": [
                    {"prompt": "他______没有迟到过。", "answer": "从来", "pinyin": "cónglái"},
                    {"prompt": "______很忙，他也会陪家人。", "answer": "即使", "pinyin": "jíshǐ"},
                    {"prompt": "他们有______的爱好，很______在一起。", "answer": "共同 / 适合", "pinyin": "gòngtóng / shìhé"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["印象", "性格", "共同", "适合", "缺点", "爱情"]},
            {"no": 2, "answers": ["baxtli; baxt", "romantik", "jalb qilmoq", "qabul qilmoq", "fe'l-atvor, kayfiyat"]},
            {"no": 3, "answers": ["从来", "即使", "共同 / 适合"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["印象", "性格", "适合", "幸福"],
                "example": "他给我留下了很深的印象，因为他的性格很好。",
            },
            {
                "no": 2,
                "instruction": "'不仅...也...' qolipidan foydalanib 2 ta gap tuzing.",
                "topic": "sevgi va do'stlik mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Siz uchun ideal turmush o'rtoq qanday bo'lishi kerak? 幸福的爱情是什么样的？",
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
