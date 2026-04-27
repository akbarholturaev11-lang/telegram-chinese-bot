import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 10,
    "lesson_code": "HSK4-L10",
    "title": "幸福的标准",
    "goal": "baxt va hayot maqsadlari haqida gapirish; 不过, 确实, 在...看来, 由于, 比如 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Baxt mezoni' mavzusiga bag'ishlangan. Unda baxtning ta'rifi, hayot maqsadlari va shaxsiy qadriyatlar haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 不过, 确实, 在...看来, 由于, 比如.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "礼拜天", "pinyin": "lǐbàitiān", "pos": "n.", "meaning": "yakshanba kuni"},
            {"no": 2, "zh": "空儿", "pinyin": "kòngr", "pos": "n.", "meaning": "bo'sh vaqt, fursat"},
            {"no": 3, "zh": "母亲", "pinyin": "mǔqīn", "pos": "n.", "meaning": "ona (rasmiy)"},
            {"no": 4, "zh": "不过", "pinyin": "búguò", "pos": "conj.", "meaning": "lekin, biroq, ammo"},
            {"no": 5, "zh": "永远", "pinyin": "yǒngyuǎn", "pos": "adv.", "meaning": "abadiy, doim, hamisha"},
            {"no": 6, "zh": "方向", "pinyin": "fāngxiàng", "pos": "n.", "meaning": "yo'nalish, toraf"},
            {"no": 7, "zh": "优秀", "pinyin": "yōuxiù", "pos": "adj.", "meaning": "a'lo, ajoyib, yuqori darajali"},
            {"no": 8, "zh": "硕士", "pinyin": "shuòshì", "pos": "n.", "meaning": "magistr, magistratura bitiruvchisi"},
            {"no": 9, "zh": "翻译", "pinyin": "fānyì", "pos": "n./v.", "meaning": "tarjimon; tarjima qilmoq"},
            {"no": 10, "zh": "确实", "pinyin": "quèshí", "pos": "adv.", "meaning": "haqiqatan ham, chindan"},
            {"no": 11, "zh": "兴奋", "pinyin": "xīngfèn", "pos": "adj.", "meaning": "hayajonlangan, shodon"},
            {"no": 12, "zh": "拉", "pinyin": "lā", "pos": "v.", "meaning": "tortmoq, sudramoq; torta bermoq"},
            {"no": 13, "zh": "由于", "pinyin": "yóuyú", "pos": "conj.", "meaning": "chunki, ...sababli"},
            {"no": 14, "zh": "比如", "pinyin": "bǐrú", "pos": "conj.", "meaning": "masalan, misol uchun"},
            {"no": 15, "zh": "标准", "pinyin": "biāozhǔn", "pos": "n./adj.", "meaning": "mezon, standart; standart darajadagi"},
            {"no": 16, "zh": "幸运", "pinyin": "xìngyùn", "pos": "adj./n.", "meaning": "omadli; omad, baxt"},
            {"no": 17, "zh": "满足", "pinyin": "mǎnzú", "pos": "v./adj.", "meaning": "qondirilmoq, qanoat qilmoq; mamnun"},
            {"no": 18, "zh": "生命", "pinyin": "shēngmìng", "pos": "n.", "meaning": "hayot, umr"},
            {"no": 19, "zh": "态度", "pinyin": "tàidu", "pos": "n.", "meaning": "munosabat, pozitsiya"},
            {"no": 20, "zh": "实现", "pinyin": "shíxiàn", "pos": "v.", "meaning": "amalga oshirmoq, ro'yobga chiqarmoq"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "孙月和王静聊王静礼拜天的生活情况",
                "dialogue": [
                    {"speaker": "孙月", "zh": "礼拜天有空儿吗？你在忙什么呢？", "pinyin": "", "translation": "Yakshanba kuni bo'sh vaqting bormi? Nima bilan shug'ullanayapsan?"},
                    {"speaker": "王静", "zh": "我可能去买东西，顺便把衣服送去干洗，最近家里事儿太多了。", "pinyin": "", "translation": "Ehtimol xarid qilgani boraman, yo'l-yo'lakay kiyimlarni kimyoviy tozalashga topshiraman, so'nggi paytlarda uy ishi juda ko'paydi."},
                    {"speaker": "孙月", "zh": "你现在在上班，还有孩子和老母亲要照顾，确实挺忙的。", "pinyin": "", "translation": "Sen hozir ishda ham ishlaysan, farzand va qarigan onangni ham boqasan, chindan ham juda band."},
                    {"speaker": "王静", "zh": "不过，虽然忙，但我感觉很幸福。因为我有一个好的家庭，家人永远是我最重要的方向。", "pinyin": "", "translation": "Biroq, garchi band bo'lsam ham, o'zimni baxtli his qilaman. Chunki yaxshi oilam bor, oila hamisha uchun eng muhim yo'nalishim."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "高老师和李老师聊在谈论幸福",
                "dialogue": [
                    {"speaker": "高老师", "zh": "你有没有人说你家儿子你也是老师，现在还有个好妻子，真让人羡慕。", "pinyin": "", "translation": "Kimdir dedi, sizning o'g'lingiz ham o'qituvchi, hozir yaxshi xotiningiz ham bor, rostdan hasad qilinadi."},
                    {"speaker": "李老师", "zh": "是呀，你说的没错，我确实是幸福的人。只是，幸福的标准对每个人来说是不一样的。", "pinyin": "", "translation": "Ha, to'g'ri aytasiz, men chindan ham baxtli odamman. Faqat baxtning mezoni har bir kishi uchun har xil."},
                    {"speaker": "高老师", "zh": "你觉得幸福的标准是什么？", "pinyin": "", "translation": "Sizningcha baxtning mezoni nima?"},
                    {"speaker": "李老师", "zh": "在我看来，幸福就是做自己喜欢做的事，由于每个人不同，比如有人觉得有钱就是幸福，有人觉得家庭和睦才是幸福。不过，我觉得最重要的是心里满足。", "pinyin": "", "translation": "Mening nazmimda, baxt — o'zingiz yaxshi ko'rgan narsani qilishdir. Har bir kishi boshqacha bo'lgani uchun, masalan, ba'zilar puli bo'lsa baxtli, ba'zilar oila baxtli bo'lsa baxtli. Biroq, menimcha eng muhimi — qalbdagi qanoat."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "不过",
                "explanation": "'Lekin, biroq, ammo' ma'nosini beradi. Oldingi fikrga yumshoq ziddiyat bildiradi (但是 dan kamroq kuchli).",
                "examples": [
                    {"zh": "虽然很忙，不过感觉很幸福。", "pinyin": "", "meaning": "Garchi juda band bo'lsam ham, biroq o'zimni baxtli his qilaman."},
                    {"zh": "这道菜好吃，不过有点儿辣。", "pinyin": "", "meaning": "Bu taom mazali, lekin biroz achchiq."},
                ],
            },
            {
                "no": 2,
                "title_zh": "确实",
                "explanation": "'Haqiqatan ham, chindan' ma'nosini beradi. Biror narsa to'g'riligini qat'iy tasdiqlaydi.",
                "examples": [
                    {"zh": "我确实是幸福的人。", "pinyin": "", "meaning": "Men chindan ham baxtli odamman."},
                    {"zh": "这里的天气确实很好。", "pinyin": "", "meaning": "Bu yerdagi havo haqiqatan ham yaxshi."},
                ],
            },
            {
                "no": 3,
                "title_zh": "在……看来",
                "explanation": "'...ning nazmida, ...ning nuqtayi nazaridan' ma'nosini beradi. Biror kishining shaxsiy fikri yoki qarashini bildiradi.",
                "examples": [
                    {"zh": "在我看来，幸福就是做自己喜欢做的事。", "pinyin": "", "meaning": "Mening nazmimda, baxt — o'zingiz yaxshi ko'rgan narsani qilishdir."},
                    {"zh": "在他看来，钱不是最重要的。", "pinyin": "", "meaning": "Uning nazmida, pul eng muhim narsa emas."},
                ],
            },
            {
                "no": 4,
                "title_zh": "由于",
                "explanation": "'...sababli, chunki' ma'nosini beradi. Sabab-natija munosabatida sabab qismini bildiradi (因为 dan rasmiyroq).",
                "examples": [
                    {"zh": "由于每个人不同，幸福的标准也不一样。", "pinyin": "", "meaning": "Har bir kishi boshqacha bo'lgani sababli, baxtning mezoni ham har xil."},
                    {"zh": "由于下雨，比赛推迟了。", "pinyin": "", "meaning": "Yomg'ir yog'gani sababli, musobaqa kechiktirildi."},
                ],
            },
            {
                "no": 5,
                "title_zh": "比如",
                "explanation": "'Masalan, misol uchun' ma'nosini beradi. Umumiy fikrni aniqlashtirish uchun misol keltiradi.",
                "examples": [
                    {"zh": "比如有人觉得有钱就是幸福。", "pinyin": "", "meaning": "Masalan, ba'zilar puli bo'lsa baxtli deb o'ylaydi."},
                    {"zh": "我喜欢运动，比如跑步和游泳。", "pinyin": "", "meaning": "Men sportni yaxshi ko'raman, masalan yugurish va suzish."},
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
                    {"prompt": "abadiy, doim", "answer": "永远", "pinyin": "yǒngyuǎn"},
                    {"prompt": "mezon, standart", "answer": "标准", "pinyin": "biāozhǔn"},
                    {"prompt": "amalga oshirmoq", "answer": "实现", "pinyin": "shíxiàn"},
                    {"prompt": "mamnun, qanoat qilmoq", "answer": "满足", "pinyin": "mǎnzú"},
                    {"prompt": "munosabat, pozitsiya", "answer": "态度", "pinyin": "tàidu"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "不过", "answer": "lekin, biroq", "pinyin": "búguò"},
                    {"prompt": "确实", "answer": "haqiqatan ham, chindan", "pinyin": "quèshí"},
                    {"prompt": "由于", "answer": "...sababli, chunki", "pinyin": "yóuyú"},
                    {"prompt": "比如", "answer": "masalan, misol uchun", "pinyin": "bǐrú"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (不过、确实、在...看来、由于、比如):",
                "items": [
                    {"prompt": "______我______，家庭是最重要的。", "answer": "在 / 看来", "pinyin": "zài / kànlái"},
                    {"prompt": "______天气不好，我们只好待在家里。", "answer": "由于", "pinyin": "yóuyú"},
                    {"prompt": "我喜欢中国文化，______书法和京剧。", "answer": "比如", "pinyin": "bǐrú"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["永远", "标准", "实现", "满足", "态度"]},
            {"no": 2, "answers": ["lekin, biroq", "haqiqatan ham, chindan", "...sababli, chunki", "masalan, misol uchun"]},
            {"no": 3, "answers": ["在 / 看来", "由于", "比如"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["幸福", "标准", "确实", "永远"],
                "example": "在我看来，幸福的标准确实因人而异，家人永远是最重要的。",
            },
            {
                "no": 2,
                "instruction": "'在...看来' va '由于...所以...' qoliplaridan foydalanib har biridan 2 ta gap tuzing.",
                "topic": "baxt va hayot maqsadlari mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Siz uchun baxtning mezoni nima? 你幸福的标准是什么？",
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
