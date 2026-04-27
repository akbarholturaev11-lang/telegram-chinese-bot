import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 2,
    "lesson_code": "HSK4-L02",
    "title": "真正的朋友",
    "goal": "do'stlik va munosabatlar haqida gapirish; 正好, 差不多, 尽管 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Haqiqiy do'st' mavzusiga bag'ishlangan. Unda do'stlik qilish, aloqada bo'lish va yangi muhitga moslashish haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 正好, 差不多, 弄, 帮, 尽管.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "适应", "pinyin": "shìyìng", "pos": "v.", "meaning": "moslashmoq, ko'nikmoq"},
            {"no": 2, "zh": "交", "pinyin": "jiāo", "pos": "v.", "meaning": "do'st orttirmoq, tanishmoq"},
            {"no": 3, "zh": "平时", "pinyin": "píngshí", "pos": "n.", "meaning": "odatda, kundalik hayotda"},
            {"no": 4, "zh": "逛", "pinyin": "guàng", "pos": "v.", "meaning": "sayr qilmoq, ko'rinib chiqmoq"},
            {"no": 5, "zh": "短信", "pinyin": "duǎnxìn", "pos": "n.", "meaning": "qisqa xabar (SMS)"},
            {"no": 6, "zh": "正好", "pinyin": "zhènghǎo", "pos": "adv.", "meaning": "aynan, o'z vaqtida, to'g'ri keldi"},
            {"no": 7, "zh": "聚会", "pinyin": "jùhuì", "pos": "v./n.", "meaning": "yig'ilish o'tkazmoq; yig'ilish, ziyofat"},
            {"no": 8, "zh": "联系", "pinyin": "liánxì", "pos": "v.", "meaning": "aloqa qilmoq, bog'lanmoq"},
            {"no": 9, "zh": "差不多", "pinyin": "chàbuduō", "pos": "adv.", "meaning": "deyarli, taxminan, xuddi shunday"},
            {"no": 10, "zh": "专门", "pinyin": "zhuānmén", "pos": "adv.", "meaning": "maxsus, ataylab"},
            {"no": 11, "zh": "毕业", "pinyin": "bì yè", "pos": "v.", "meaning": "bitirmoq (maktab, universitet)"},
            {"no": 12, "zh": "麻烦", "pinyin": "máfan", "pos": "v./adj.", "meaning": "bezovta qilmoq; qiyin, muammoli"},
            {"no": 13, "zh": "好像", "pinyin": "hǎoxiàng", "pos": "adv.", "meaning": "xuddi, go'yo, shekilli"},
            {"no": 14, "zh": "重新", "pinyin": "chóngxīn", "pos": "adv.", "meaning": "qaytadan, yana"},
            {"no": 15, "zh": "尽管", "pinyin": "jǐnguǎn", "pos": "conj.", "meaning": "garchi...bo'lsa ham, qaramay"},
            {"no": 16, "zh": "真正", "pinyin": "zhēnzhèng", "pos": "adj.", "meaning": "haqiqiy, chin"},
            {"no": 17, "zh": "友谊", "pinyin": "yǒuyì", "pos": "n.", "meaning": "do'stlik"},
            {"no": 18, "zh": "了解", "pinyin": "liǎojiě", "pos": "v.", "meaning": "bilmoq, tanib olmoq"},
            {"no": 19, "zh": "帮助", "pinyin": "bāngzhù", "pos": "v./n.", "meaning": "yordam bermoq; yordam"},
            {"no": 20, "zh": "关心", "pinyin": "guānxīn", "pos": "v.", "meaning": "g'amxo'rlik qilmoq, qayg'urmoq"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "小夏和马克聊在中国的朋友",
                "dialogue": [
                    {"speaker": "小夏", "zh": "来中国快一年了，你适应这儿的生活了吗？", "pinyin": "", "translation": "Xitoyga kelganing bir yilga yaqin bo'ldi, bu yerdagi hayotga moslashdingmi?"},
                    {"speaker": "马克", "zh": "开始有点儿不习惯，后来慢慢就好了，我还交了一个中国朋友。", "pinyin": "", "translation": "Boshida biroz qiyin bo'ldi, keyin asta-sekin odatlandim, bir xitoylik do'stim ham bor."},
                    {"speaker": "小夏", "zh": "那挺好的！你们平时一起做什么？", "pinyin": "", "translation": "Bu juda yaxshi! Siz odatda birga nima qilasiz?"},
                    {"speaker": "马克", "zh": "我们在图书馆认识的，平时一起逛街、踢球，他还给我发短信教我汉语。", "pinyin": "", "translation": "Biz kutubxonada tanishdik, odatda birga ko'chada sayr qilamiz, futbol o'ynaymiz, u menga SMS bilan xitoy tilini o'rgatadi."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "小李和小林聊同学聚会的事情",
                "dialogue": [
                    {"speaker": "小李", "zh": "星期天同学聚会，你能来吗？", "pinyin": "", "translation": "Yakshanba kuni sinfdoshlar yig'ilishadi, kela olasanmi?"},
                    {"speaker": "小林", "zh": "是不是上次联系过我的那几位同学？大概多少人？", "pinyin": "", "translation": "O'sha safar men bilan aloqa qilgan sinfdoshlar emasmi? Taxminan necha kishi?"},
                    {"speaker": "小李", "zh": "差不多十五个人，好多都是专门从外地飞回来的。", "pinyin": "", "translation": "Taxminan o'n besh kishi, ko'plari maxsus boshqa shaharlardan uchib kelishdi."},
                    {"speaker": "小林", "zh": "太好了！毕业后大家联系少了，正好借这个机会重新聚一聚。", "pinyin": "", "translation": "Juda yaxshi! Bitiruvdan keyin hammaning aloqasi kamaydi, bu aynan qayta yig'ilish uchun yaxshi imkoniyat."},
                ],
            },
            {
                "block_no": 3,
                "section_label": "课文 3",
                "scene_label_zh": "关于真正友谊的短文",
                "dialogue": [
                    {"speaker": "旁白", "zh": "真正的朋友，不是见面次数多的人，而是了解你、关心你、在你需要帮助时出现的人。", "pinyin": "", "translation": "Haqiqiy do'st — ko'p uchrashuvchi kishi emas, balki seni tushunib, g'amxo'rlik qilib, muhtoj paytingda yonida bo'ladigan kishidir."},
                    {"speaker": "旁白", "zh": "尽管大家都很忙，但真正的友谊经得起时间和距离的考验。", "pinyin": "", "translation": "Garchi hammaning vaqti yo'q bo'lsa ham, haqiqiy do'stlik vaqt va masofaga bardosh beradi."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "正好",
                "explanation": "'Aynan, to'g'ri keldi, o'z vaqtida' ma'nosini beradi. Biror narsa kutilmaganda yoki mos holda sodir bo'lganini bildiradi.",
                "examples": [
                    {"zh": "我刚想找你，你正好来了。", "pinyin": "", "meaning": "Men seni izlamoqchi edim, sen aynan kelib qolding."},
                    {"zh": "这件衣服正好合适。", "pinyin": "", "meaning": "Bu kiyim aynan mos keldi."},
                ],
            },
            {
                "no": 2,
                "title_zh": "差不多",
                "explanation": "'Deyarli, taxminan, xuddi shunday' ma'nosini beradi. Miqdor yoki sifat jihatidan o'xshashlikni bildiradi.",
                "examples": [
                    {"zh": "差不多十五个人来了。", "pinyin": "", "meaning": "Taxminan o'n besh kishi keldi."},
                    {"zh": "我们俩的想法差不多。", "pinyin": "", "meaning": "Bizning ikkalamizning fikrimiz deyarli bir xil."},
                ],
            },
            {
                "no": 3,
                "title_zh": "弄 + 结果补语",
                "explanation": "'弄' fe'li + natija to'ldiruvchisi qo'shilib, biror natijaga erishishni bildiradi. Masalan: 弄坏 (buzdim), 弄脏 (kirdim), 弄好 (yakladim).",
                "examples": [
                    {"zh": "对不起，我把你的书弄坏了。", "pinyin": "", "meaning": "Kechirasiz, men sizning kitobingizni buzdim."},
                    {"zh": "这个问题我弄清楚了。", "pinyin": "", "meaning": "Bu masalani men aniqladim."},
                ],
            },
            {
                "no": 4,
                "title_zh": "帮",
                "explanation": "'帮' — 'yordam bermoq' ma'nosida ishlatiladi. 帮 + kishi + fe'l yoki 帮助 + kishi + fe'l shaklida qo'llanadi.",
                "examples": [
                    {"zh": "他帮我学汉语。", "pinyin": "", "meaning": "U menga xitoy tilini o'rgatadi (yordam beradi)."},
                    {"zh": "朋友帮助我解决了问题。", "pinyin": "", "meaning": "Do'st menga muammoni hal qilishda yordam berdi."},
                ],
            },
            {
                "no": 5,
                "title_zh": "尽管……但是/还是……",
                "explanation": "'Garchi...bo'lsa ham' ma'nosini beradi. Birinchi gapda 尽管, ikkinchi gapda 但是 yoki 还是 ishlatiladi.",
                "examples": [
                    {"zh": "尽管大家都很忙，但真正的友谊经得起考验。", "pinyin": "", "meaning": "Garchi hammaning vaqti yo'q bo'lsa ham, haqiqiy do'stlik bardosh beradi."},
                    {"zh": "尽管很远，他还是来了。", "pinyin": "", "meaning": "Garchi uzoq bo'lsa ham, u baribir keldi."},
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
                    {"prompt": "moslashmoq", "answer": "适应", "pinyin": "shìyìng"},
                    {"prompt": "do'st orttirmoq", "answer": "交朋友", "pinyin": "jiāo péngyou"},
                    {"prompt": "haqiqiy", "answer": "真正", "pinyin": "zhēnzhèng"},
                    {"prompt": "do'stlik", "answer": "友谊", "pinyin": "yǒuyì"},
                    {"prompt": "qaytadan", "answer": "重新", "pinyin": "chóngxīn"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "正好", "answer": "aynan, to'g'ri keldi", "pinyin": "zhènghǎo"},
                    {"prompt": "差不多", "answer": "deyarli, taxminan", "pinyin": "chàbuduō"},
                    {"prompt": "联系", "answer": "aloqa qilmoq", "pinyin": "liánxì"},
                    {"prompt": "尽管", "answer": "garchi...bo'lsa ham", "pinyin": "jǐnguǎn"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (正好、差不多、尽管、专门、重新):",
                "items": [
                    {"prompt": "他______从上海飞回来参加聚会。", "answer": "专门", "pinyin": "zhuānmén"},
                    {"prompt": "______很忙，他还是来帮我了。", "answer": "尽管", "pinyin": "jǐnguǎn"},
                    {"prompt": "我找你，你______来了。", "answer": "正好", "pinyin": "zhènghǎo"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["适应", "交朋友", "真正", "友谊", "重新"]},
            {"no": 2, "answers": ["aynan, to'g'ri keldi", "deyarli, taxminan", "aloqa qilmoq", "garchi...bo'lsa ham"]},
            {"no": 3, "answers": ["专门", "尽管", "正好"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["适应", "联系", "友谊", "了解"],
                "example": "来到新城市后，我慢慢地适应了这里的生活。",
            },
            {
                "no": 2,
                "instruction": "'尽管...但是...' qolipidan foydalanib 2 ta gap tuzing.",
                "topic": "do'stlik va munosabatlar mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Sizning eng yaqin do'stingiz haqida yozing. 你最好的朋友是什么样的人？",
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
