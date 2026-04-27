import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 5,
    "lesson_code": "HSK4-L05",
    "title": "只买对的，不买贵的",
    "goal": "xarid qilish, narx va sifat haqida gapirish; 的确, 再说, 实际上, 对...来说, 尤其 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'To'g'risini sotib ol, qimmatini emas' mavzusiga bag'ishlangan. Unda do'konda xarid qilish, narx solishtirish va onlayn xarid haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 的确, 再说, 实际上, 对...来说, 尤其.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "家具", "pinyin": "jiājù", "pos": "n.", "meaning": "mebel"},
            {"no": 2, "zh": "沙发", "pinyin": "shāfā", "pos": "n.", "meaning": "divan, sofa"},
            {"no": 3, "zh": "打折", "pinyin": "dǎzhé", "pos": "v.", "meaning": "chegirma qilmoq, narx tushirmoq"},
            {"no": 4, "zh": "价格", "pinyin": "jiàgé", "pos": "n.", "meaning": "narx, baho"},
            {"no": 5, "zh": "质量", "pinyin": "zhìliàng", "pos": "n.", "meaning": "sifat"},
            {"no": 6, "zh": "肯定", "pinyin": "kěndìng", "pos": "adv.", "meaning": "albatta, shubhasiz"},
            {"no": 7, "zh": "流行", "pinyin": "liúxíng", "pos": "v./adj.", "meaning": "mashhur bo'lmoq, tarqalmoq; modali"},
            {"no": 8, "zh": "顺便", "pinyin": "shùnbiàn", "pos": "adv.", "meaning": "yo'l-yo'lakay, bir zumda"},
            {"no": 9, "zh": "台", "pinyin": "tái", "pos": "m.", "meaning": "dona (mashina, televizor uchun)"},
            {"no": 10, "zh": "光", "pinyin": "guāng", "pos": "adv.", "meaning": "faqat, shunchaki"},
            {"no": 11, "zh": "实在", "pinyin": "shízài", "pos": "adv.", "meaning": "haqiqatan, chindan ham"},
            {"no": 12, "zh": "冷冻", "pinyin": "lěngdòng", "pos": "v.", "meaning": "muzlatmoq, sovutmoq"},
            {"no": 13, "zh": "效果", "pinyin": "xiàoguǒ", "pos": "n.", "meaning": "natija, samara"},
            {"no": 14, "zh": "现金", "pinyin": "xiànjīn", "pos": "n.", "meaning": "naqd pul"},
            {"no": 15, "zh": "的确", "pinyin": "díquè", "pos": "adv.", "meaning": "haqiqatan ham, rostdan"},
            {"no": 16, "zh": "再说", "pinyin": "zàishuō", "pos": "conj.", "meaning": "bundan tashqari, yana ham"},
            {"no": 17, "zh": "实际上", "pinyin": "shíjì shàng", "pos": "adv.", "meaning": "aslida, haqiqatda"},
            {"no": 18, "zh": "尤其", "pinyin": "yóuqí", "pos": "adv.", "meaning": "ayniqsa, xususan"},
            {"no": 19, "zh": "信用卡", "pinyin": "xìnyòngkǎ", "pos": "n.", "meaning": "kredit karta"},
            {"no": 20, "zh": "比较", "pinyin": "bǐjiào", "pos": "adv./v.", "meaning": "nisbatan, ancha; solishtirmoq"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "王静和售货员在家具店买沙发",
                "dialogue": [
                    {"speaker": "售货员", "zh": "小姐，您好！您想看什么家具？需要我为您介绍一下吗？", "pinyin": "", "translation": "Xonim, salom! Qanday mebel qidiryapsiz? Taqdim etishim kerakmi?"},
                    {"speaker": "王静", "zh": "谢谢，我想买沙发。", "pinyin": "", "translation": "Rahmat, divan sotib olmoqchi edim."},
                    {"speaker": "售货员", "zh": "您看这款怎么样？现在正在打折，比平时便宜一些，就是今年最流行的款式。", "pinyin": "", "translation": "Bu modelga qarang. Hozir chegirma, odatdagidan arzonroq, bu yilning eng mashhur modeli."},
                    {"speaker": "王静", "zh": "价格还可以，就是不知道质量怎么样？", "pinyin": "", "translation": "Narxi yomon emas, faqat sifati qanday ekanini bilmadim."},
                    {"speaker": "售货员", "zh": "质量肯定没问题！实在不满意，一周内可以退换。", "pinyin": "", "translation": "Sifatiga shubha yo'q! Chindan ham mamnun bo'lmasangiz, bir hafta ichida qaytarib almashtirishingiz mumkin."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "王静和李进在商场买东西",
                "dialogue": [
                    {"speaker": "王静", "zh": "喝家里的冰箱买太旧了，再说冷冻效果也不太好，还是买个新的吧。", "pinyin": "", "translation": "Uyimizdagi muzlatgich juda eski bo'lib qoldi, bundan tashqari muzlatish samarasi ham yaxshi emas, yangi sotib olgan ma'qul."},
                    {"speaker": "李进", "zh": "这么多钱，你带够现金了吗？", "pinyin": "", "translation": "Bu qadar pul, naqd pul etarlimi?"},
                    {"speaker": "王静", "zh": "光带现金不够，我用信用卡吧。对了，顺便再看看那台洗衣机。", "pinyin": "", "translation": "Faqat naqd pul bilan yetmaydi, kredit karta ishlataman. Aytganday, yo'l-yo'lakay kir yuvgich ham ko'rib o'tay."},
                    {"speaker": "李进", "zh": "好，不过买东西的确要货比三家，尤其是买家具这样的大件。", "pinyin": "", "translation": "Yaxshi, lekin xarid qilishda haqiqatan ham bozorni o'rganish kerak, ayniqsa mebel kabi katta narsalarni."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "的确",
                "explanation": "'Haqiqatan ham, rostdan' ma'nosini beradi. Biror narsa to'g'riligini ta'kidlash uchun ishlatiladi.",
                "examples": [
                    {"zh": "买东西的确要货比三家。", "pinyin": "", "meaning": "Xarid qilishda haqiqatan ham narx solishtirilishi kerak."},
                    {"zh": "这件事的确很难。", "pinyin": "", "meaning": "Bu ish haqiqatan ham qiyin."},
                ],
            },
            {
                "no": 2,
                "title_zh": "再说",
                "explanation": "'Bundan tashqari, qolaverson' ma'nosini beradi. Birinchi sababdan keyin ikkinchi sabab yoki mulohaza qo'shiladi.",
                "examples": [
                    {"zh": "冰箱太旧了，再说冷冻效果也不好。", "pinyin": "", "meaning": "Muzlatgich juda eski, bundan tashqari muzlatish samarasi ham yaxshi emas."},
                    {"zh": "现在太晚了，再说我也累了。", "pinyin": "", "meaning": "Hozir juda kech, bundan tashqari men ham charchadim."},
                ],
            },
            {
                "no": 3,
                "title_zh": "实际上",
                "explanation": "'Aslida, haqiqatda' ma'nosini beradi. Ko'rinish bilan haqiqat o'rtasidagi farqni bildiradi.",
                "examples": [
                    {"zh": "看起来便宜，实际上质量不好。", "pinyin": "", "meaning": "Ko'rinishda arzon, aslida sifati yaxshi emas."},
                    {"zh": "实际上这件事没那么难。", "pinyin": "", "meaning": "Aslida bu ish o'ylaganchalik qiyin emas."},
                ],
            },
            {
                "no": 4,
                "title_zh": "对……来说",
                "explanation": "'...uchun, ...nuqtayi nazaridan' ma'nosini beradi. Biror kishi yoki guruh nuqtayi nazarini bildiradi.",
                "examples": [
                    {"zh": "对我来说，质量比价格更重要。", "pinyin": "", "meaning": "Men uchun sifat narxdan muhimroq."},
                    {"zh": "对学生来说，时间很宝贵。", "pinyin": "", "meaning": "Talabalar uchun vaqt juda qimmatli."},
                ],
            },
            {
                "no": 5,
                "title_zh": "尤其",
                "explanation": "'Ayniqsa, xususan' ma'nosini beradi. Biror narsani alohida ajratib ko'rsatish uchun ishlatiladi.",
                "examples": [
                    {"zh": "买大件尤其要注意质量。", "pinyin": "", "meaning": "Katta narsa sotib olishda ayniqsa sifatga e'tibor berish kerak."},
                    {"zh": "她喜欢运动，尤其喜欢游泳。", "pinyin": "", "meaning": "U sport qilishni yaxshi ko'radi, ayniqsa suzishni."},
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
                    {"prompt": "narx, baho", "answer": "价格", "pinyin": "jiàgé"},
                    {"prompt": "sifat", "answer": "质量", "pinyin": "zhìliàng"},
                    {"prompt": "chegirma qilmoq", "answer": "打折", "pinyin": "dǎzhé"},
                    {"prompt": "natija, samara", "answer": "效果", "pinyin": "xiàoguǒ"},
                    {"prompt": "naqd pul", "answer": "现金", "pinyin": "xiànjīn"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "的确", "answer": "haqiqatan ham, rostdan", "pinyin": "díquè"},
                    {"prompt": "尤其", "answer": "ayniqsa, xususan", "pinyin": "yóuqí"},
                    {"prompt": "实际上", "answer": "aslida, haqiqatda", "pinyin": "shíjì shàng"},
                    {"prompt": "再说", "answer": "bundan tashqari", "pinyin": "zàishuō"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (的确、再说、实际上、对...来说、尤其):",
                "items": [
                    {"prompt": "______我来______，质量比价格更重要。", "answer": "对 / 来说", "pinyin": "duì / lái shuō"},
                    {"prompt": "这件衣服______很贵，______质量也不怎么样。", "answer": "的确 / 再说", "pinyin": "díquè / zàishuō"},
                    {"prompt": "她喜欢吃甜食，______喜欢巧克力。", "answer": "尤其", "pinyin": "yóuqí"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["价格", "质量", "打折", "效果", "现金"]},
            {"no": 2, "answers": ["haqiqatan ham, rostdan", "ayniqsa, xususan", "aslida, haqiqatda", "bundan tashqari"]},
            {"no": 3, "answers": ["对 / 来说", "的确 / 再说", "尤其"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["价格", "质量", "的确", "尤其"],
                "example": "对我来说，的确质量比价格更重要，尤其是买家具的时候。",
            },
            {
                "no": 2,
                "instruction": "'对...来说' va '尤其' qoliplaridan foydalanib har biridan 2 ta gap tuzing.",
                "topic": "xarid qilish va pul sarflash mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Siz xarid qilishda nimalarga e'tibor berasiz? 你买东西时最注重什么？",
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
