import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 8,
    "lesson_code": "HSK4-L08",
    "title": "生活中不缺少美",
    "goal": "go'zallik, his-tuyg'u va tabiat haqida gapirish; 使, 因此, 往往, 可不是 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Hayotda go'zallik ko'p' mavzusiga bag'ishlangan. Unda tabiat go'zalligi, his-tuyg'ular, sport va psixologik holat haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 使, 因此, 往往, 可不是, 只要...就...",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "巧克力", "pinyin": "qiǎokèlì", "pos": "n.", "meaning": "shokolad"},
            {"no": 2, "zh": "亲戚", "pinyin": "qīnqì", "pos": "n.", "meaning": "qarindosh, yaqin"},
            {"no": 3, "zh": "伤心", "pinyin": "shāng xīn", "pos": "adj.", "meaning": "qayg'uli, xafa"},
            {"no": 4, "zh": "使", "pinyin": "shǐ", "pos": "v.", "meaning": "qilmoq, bo'lishiga sabab bo'lmoq"},
            {"no": 5, "zh": "心情", "pinyin": "xīnqíng", "pos": "n.", "meaning": "kayfiyat, ruhiy holat"},
            {"no": 6, "zh": "愉快", "pinyin": "yúkuài", "pos": "adj.", "meaning": "xursand, shod"},
            {"no": 7, "zh": "景色", "pinyin": "jǐngsè", "pos": "n.", "meaning": "manzara, ko'rinish"},
            {"no": 8, "zh": "放松", "pinyin": "fàngsōng", "pos": "v.", "meaning": "bo'shashmoq, dam olmoq (ruhiy)"},
            {"no": 9, "zh": "压力", "pinyin": "yālì", "pos": "n.", "meaning": "bosim, stres"},
            {"no": 10, "zh": "回忆", "pinyin": "huíyì", "pos": "v./n.", "meaning": "eslamoq; xotira, esdalik"},
            {"no": 11, "zh": "发生", "pinyin": "fāshēng", "pos": "v.", "meaning": "sodir bo'lmoq, yuz bermoq"},
            {"no": 12, "zh": "成为", "pinyin": "chéngwéi", "pos": "v.", "meaning": "bo'lmoq, aylanmoq"},
            {"no": 13, "zh": "只要", "pinyin": "zhǐyào", "pos": "conj.", "meaning": "faqat...bo'lsa, agar...bo'lsa kifoya"},
            {"no": 14, "zh": "师傅", "pinyin": "shīfu", "pos": "n.", "meaning": "usta, malakali mutaxassis"},
            {"no": 15, "zh": "大使馆", "pinyin": "dàshǐguǎn", "pos": "n.", "meaning": "elchixona"},
            {"no": 16, "zh": "堵车", "pinyin": "dǔ chē", "pos": "v.", "meaning": "tiqilinch, transport qotib qolmoq"},
            {"no": 17, "zh": "距离", "pinyin": "jùlí", "pos": "n.", "meaning": "masofa, uzoqlik"},
            {"no": 18, "zh": "耐心", "pinyin": "nàixīn", "pos": "n./adj.", "meaning": "sabr, toqat; sabr-toqatli"},
            {"no": 19, "zh": "因此", "pinyin": "yīncǐ", "pos": "conj.", "meaning": "shu sababli, shuning uchun"},
            {"no": 20, "zh": "往往", "pinyin": "wǎngwǎng", "pos": "adv.", "meaning": "ko'pincha, odatda"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "李老师和高老师聊关于巧克力的事情",
                "dialogue": [
                    {"speaker": "李老师", "zh": "这种巧克力不好找，你在哪儿买的？", "pinyin": "", "translation": "Bunday shokolad topish qiyin, siz uni qayerdan topdingiz?"},
                    {"speaker": "高老师", "zh": "不是我买的，是我女儿从国外常常买回来送给我的礼物。", "pinyin": "", "translation": "Men sotib olmadim, bu qizim chet eldan tez-tez olib keladigan sovg'a."},
                    {"speaker": "李老师", "zh": "不是说吃巧克力以后常常会有很多亲戚来？", "pinyin": "", "translation": "Shokolad yegandan keyin ko'p qarindosh keladi deyishmaydimi?"},
                    {"speaker": "高老师", "zh": "是呀！而且很多人伤心的时候都会吃巧克力，因为它能使人的心情变得愉快。", "pinyin": "", "translation": "Ha! Ko'p odamlar xafa bo'lganida shokolad yeydi, chunki u kishining kayfiyatini yaxshilaydi."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "小夏和马克聊关于上次足球比赛的事情",
                "dialogue": [
                    {"speaker": "小夏", "zh": "这里的景色真美，空气也好，心情放松多了。", "pinyin": "", "translation": "Bu yerdagi manzara juda chiroyli, havosi ham yaxshi, kayfiyat ancha yaxshilandi."},
                    {"speaker": "马克", "zh": "你不要有压力，好好儿把这次比赛当做一次学习机会。", "pinyin": "", "translation": "Xavotir olmang, bu musobaqani yaxshilab o'rganish imkoniyati deb biling."},
                    {"speaker": "小夏", "zh": "这段时间我总是回忆以前发生的事，一个人空着的时间里往往会这样。", "pinyin": "", "translation": "Bu vaqt ichida men doim oldin bo'lgan voqealarni eslab yuraman, bo'sh vaqt bo'lganda ko'pincha shunday bo'ladi."},
                    {"speaker": "马克", "zh": "只要你保持好的心情，一切都会成为美好的回忆。生活中不缺少美，因此要用心去发现。", "pinyin": "", "translation": "Faqat yaxshi kayfiyatni saqlasang, hammasi yaxshi xotiraga aylanadi. Hayotda go'zallik ko'p, shuning uchun uni yurak bilan topish kerak."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "使",
                "explanation": "'Qilmoq, bo'lishiga sabab bo'lmoq' ma'nosini beradi. Birov yoki biror narsa boshqa bir holatga olib kelishini bildiradi.",
                "examples": [
                    {"zh": "巧克力能使人的心情变得愉快。", "pinyin": "", "meaning": "Shokolad kishining kayfiyatini yaxshilaydi."},
                    {"zh": "这件事使我很感动。", "pinyin": "", "meaning": "Bu narsa meni juda ta'sirlantirdi."},
                ],
            },
            {
                "no": 2,
                "title_zh": "因此",
                "explanation": "'Shu sababli, shuning uchun' ma'nosini beradi. Sabab-natija munosabatini bildiradi.",
                "examples": [
                    {"zh": "生活中不缺少美，因此要用心去发现。", "pinyin": "", "meaning": "Hayotda go'zallik ko'p, shuning uchun uni topishga harakat qilish kerak."},
                    {"zh": "他努力工作，因此取得了好成绩。", "pinyin": "", "meaning": "U qattiq ishladi, shuning uchun yaxshi natijaga erishdi."},
                ],
            },
            {
                "no": 3,
                "title_zh": "往往",
                "explanation": "'Ko'pincha, odatda' ma'nosini beradi. Biror holat ko'p marta yoki odatda shunday bo'lishini bildiradi.",
                "examples": [
                    {"zh": "一个人的时候往往会想很多。", "pinyin": "", "meaning": "Yolg'iz qolganda ko'pincha ko'p narsalar o'ylanadi."},
                    {"zh": "下雨天往往让人心情不好。", "pinyin": "", "meaning": "Yomg'irli kunda ko'pincha kayfiyat yaxshi bo'lmaydi."},
                ],
            },
            {
                "no": 4,
                "title_zh": "可不是",
                "explanation": "'Albatta, to'g'ri, ha-da' ma'nosini beradi. Boshqa kishining gapiga qo'shilish yoki tasdiqlash uchun ishlatiladi (og'zaki nutqda).",
                "examples": [
                    {"zh": "A: 今天天气真好！B: 可不是！", "pinyin": "", "meaning": "A: Bugun havo juda yaxshi! B: Ha, albatta!"},
                    {"zh": "A: 这里的景色太美了。B: 可不是，我也这么觉得。", "pinyin": "", "meaning": "A: Bu yerdagi manzara juda chiroyli. B: Ha, ha, men ham shunday deb o'ylayman."},
                ],
            },
            {
                "no": 5,
                "title_zh": "只要……就……",
                "explanation": "'Faqat...bo'lsa, ...bo'ladi' ma'nosini beradi. Minimal shart bajarilsa natija yuz berishini bildiradi.",
                "examples": [
                    {"zh": "只要你保持好心情，一切都会好的。", "pinyin": "", "meaning": "Faqat yaxshi kayfiyatni saqlasang, hammasi yaxshi bo'ladi."},
                    {"zh": "只要努力，就能成功。", "pinyin": "", "meaning": "Faqat harakat qilsang, muvaffaqiyat qozonasan."},
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
                    {"prompt": "kayfiyat", "answer": "心情", "pinyin": "xīnqíng"},
                    {"prompt": "manzara, ko'rinish", "answer": "景色", "pinyin": "jǐngsè"},
                    {"prompt": "bosim, stres", "answer": "压力", "pinyin": "yālì"},
                    {"prompt": "eslamoq; xotira", "answer": "回忆", "pinyin": "huíyì"},
                    {"prompt": "sabr, toqat", "answer": "耐心", "pinyin": "nàixīn"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "使", "answer": "qilmoq, sabab bo'lmoq", "pinyin": "shǐ"},
                    {"prompt": "因此", "answer": "shu sababli, shuning uchun", "pinyin": "yīncǐ"},
                    {"prompt": "往往", "answer": "ko'pincha, odatda", "pinyin": "wǎngwǎng"},
                    {"prompt": "成为", "answer": "bo'lmoq, aylanmoq", "pinyin": "chéngwéi"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (使、因此、往往、只要、成为):",
                "items": [
                    {"prompt": "这首歌______我想起了很多过去的事。", "answer": "使", "pinyin": "shǐ"},
                    {"prompt": "他很努力，______取得了很好的成绩。", "answer": "因此", "pinyin": "yīncǐ"},
                    {"prompt": "______你坚持，就一定能______优秀的人。", "answer": "只要 / 成为", "pinyin": "zhǐyào / chéngwéi"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["心情", "景色", "压力", "回忆", "耐心"]},
            {"no": 2, "answers": ["qilmoq, sabab bo'lmoq", "shu sababli, shuning uchun", "ko'pincha, odatda", "bo'lmoq, aylanmoq"]},
            {"no": 3, "answers": ["使", "因此", "只要 / 成为"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["心情", "景色", "使", "往往"],
                "example": "美丽的景色使我心情愉快，压力往往在大自然中消失了。",
            },
            {
                "no": 2,
                "instruction": "'使' va '只要...就...' qoliplaridan foydalanib har biridan 2 ta gap tuzing.",
                "topic": "his-tuyg'u, tabiat va go'zallik mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Siz hayotda go'zallikni qayerdan topasiz? 生活中你在哪里发现美？",
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
