import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 7,
    "lesson_code": "HSK4-L07",
    "title": "最好的医生是自己",
    "goal": "sog'liq, kasallik va sport haqida gapirish; 估计, 再也不, 合适, 帅 va 来不及 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Eng yaxshi shifokor o'zingiz' mavzusiga bag'ishlangan. Unda sog'lom hayot kechirish, kasallikdan saqlanish va sport haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 估计, 再也不, 合适, 出现, 来不及.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "流血", "pinyin": "liú xiě", "pos": "v.", "meaning": "qon ketmoq, qon oqmoq"},
            {"no": 2, "zh": "擦", "pinyin": "cā", "pos": "v.", "meaning": "artmoq, tozalamoq"},
            {"no": 3, "zh": "气候", "pinyin": "qìhòu", "pos": "n.", "meaning": "iqlim, ob-havo"},
            {"no": 4, "zh": "估计", "pinyin": "gūjì", "pos": "v.", "meaning": "taxmin qilmoq, hisoblash"},
            {"no": 5, "zh": "咳嗽", "pinyin": "késou", "pos": "v.", "meaning": "yo'talmoq"},
            {"no": 6, "zh": "严重", "pinyin": "yánzhòng", "pos": "adj.", "meaning": "jiddiy, og'ir (holat)"},
            {"no": 7, "zh": "窗户", "pinyin": "chuānghù", "pos": "n.", "meaning": "deraza"},
            {"no": 8, "zh": "空气", "pinyin": "kōngqì", "pos": "n.", "meaning": "havo"},
            {"no": 9, "zh": "抽烟", "pinyin": "chōu yān", "pos": "v.", "meaning": "chekmoq (sigaret)"},
            {"no": 10, "zh": "动作", "pinyin": "dòngzuò", "pos": "n.", "meaning": "harakat, imo-ishora"},
            {"no": 11, "zh": "帅", "pinyin": "shuài", "pos": "adj.", "meaning": "kelishgan, chiroyli (erkak)"},
            {"no": 12, "zh": "出现", "pinyin": "chūxiàn", "pos": "v.", "meaning": "paydo bo'lmoq, namoyon bo'lmoq"},
            {"no": 13, "zh": "后悔", "pinyin": "hòuhuǐ", "pos": "v.", "meaning": "pushaymon bo'lmoq, afsuslanmoq"},
            {"no": 14, "zh": "来不及", "pinyin": "láibují", "pos": "v.", "meaning": "vaqt yetmaydi, kech qolmoq"},
            {"no": 15, "zh": "反对", "pinyin": "fǎnduì", "pos": "v.", "meaning": "qarshi bo'lmoq, e'tiroz bildirmoq"},
            {"no": 16, "zh": "健康", "pinyin": "jiànkāng", "pos": "adj./n.", "meaning": "sog'lom; sog'liq"},
            {"no": 17, "zh": "锻炼", "pinyin": "duànliàn", "pos": "v.", "meaning": "mashq qilmoq, sport bilan shug'ullanmoq"},
            {"no": 18, "zh": "休息", "pinyin": "xiūxi", "pos": "v.", "meaning": "dam olmoq"},
            {"no": 19, "zh": "医生", "pinyin": "yīshēng", "pos": "n.", "meaning": "shifokor, doktor"},
            {"no": 20, "zh": "合适", "pinyin": "héshì", "pos": "adj.", "meaning": "mos, to'g'ri keladigan"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "小李和小林聊天气和身体情况",
                "dialogue": [
                    {"speaker": "小李", "zh": "你的鼻子怎么流血了？使用纸巾擦擦。", "pinyin": "", "translation": "Burnig'iz nima uchun qon ketmoqda? Doka bilan arting."},
                    {"speaker": "小林", "zh": "我还不习惯北方的气候，估计是天气不是很干，你怎么这么多？", "pinyin": "", "translation": "Men hali shimoliy iqlimga ko'nikmaganman, taxminan havo quruq bo'lgani uchun, siz nega bu qadar ko'p?"},
                    {"speaker": "小李", "zh": "那说明你要多喝水，这种天气容易咳嗽，要注意身体啊。", "pinyin": "", "translation": "Demak ko'p suv ichishingiz kerak, bunday havoda yo'tal osonlikcha bo'ladi, sog'lig'ingizga e'tibor bering."},
                    {"speaker": "小林", "zh": "没有，我只是有点儿咳嗽，不严重，多喝点儿水就好了，另外要经常开窗户，让空气流通。", "pinyin": "", "translation": "Yo'q, biroz yo'talim bor, jiddiy emas, ko'p suv ichsam bo'ladi, bundan tashqari tez-tez deraza ochib, havo almashtirib turish kerak."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "小夏和小雨聊小雨戒烟的事情",
                "dialogue": [
                    {"speaker": "小夏", "zh": "你不是说不抽烟了吗？", "pinyin": "", "translation": "Sigaret chekmaydi demaganmidingiz?"},
                    {"speaker": "小雨", "zh": "是老毛病了，就让我抽完这一根以后不再抽了。", "pinyin": "", "translation": "Bu eski odat, mana shuni tugatib, keyin boshqa chekmayman."},
                    {"speaker": "小夏", "zh": "你的身体出现了一些问题，如果再不改变的话，后来就来不及了。", "pinyin": "", "translation": "Sizning sog'lig'ingizda ba'zi muammolar paydo bo'ldi, agar o'zgartirmasangiz, keyinroq kech bo'lib qoladi."},
                    {"speaker": "小雨", "zh": "我自己也知道，再不见的话对身体不好，我家人也一直反对我抽烟，拉我去健身房，时时刻刻提醒我。", "pinyin": "", "translation": "Men o'zim ham bilaman, davom etsam sog'lig'im yomonlashadi, oilam ham chekishimga doim qarshi, meni sport zaliga olib boradi, har doim eslatib turadi."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "估计",
                "explanation": "'Taxmin qilmoq, hisoblash' ma'nosini beradi. Aniq ma'lumot bo'lmagan holda taxminan qanday ekanligi haqida fikr bildiradi.",
                "examples": [
                    {"zh": "估计是天气太干了。", "pinyin": "", "meaning": "Taxminan havo juda quruq bo'lgani uchun."},
                    {"zh": "我估计他今天不会来了。", "pinyin": "", "meaning": "Men taxmin qilaman, u bugun kelmaydi."},
                ],
            },
            {
                "no": 2,
                "title_zh": "再也不……了",
                "explanation": "'Boshqa hech qachon...emas' ma'nosini beradi. Biror narsa endi qilinmaydi yoki sodir bo'lmaydi degan qat'iy qarorni bildiradi.",
                "examples": [
                    {"zh": "我再也不抽烟了！", "pinyin": "", "meaning": "Men boshqa hech qachon chekmayman!"},
                    {"zh": "他说再也不迟到了。", "pinyin": "", "meaning": "U boshqa hech qachon kech qolmasligini aytdi."},
                ],
            },
            {
                "no": 3,
                "title_zh": "合适",
                "explanation": "'Mos, to'g'ri keladigan' ma'nosini beradi. Biror narsa biror holat yoki kishiga mos ekanligini bildiradi.",
                "examples": [
                    {"zh": "每天跑步对健康很合适。", "pinyin": "", "meaning": "Har kuni yugurish sog'liq uchun juda mos."},
                    {"zh": "这种药对你的情况合适吗？", "pinyin": "", "meaning": "Bu dori sizning holatingizga mos keladimi?"},
                ],
            },
            {
                "no": 4,
                "title_zh": "出现",
                "explanation": "'Paydo bo'lmoq, namoyon bo'lmoq' ma'nosini beradi. Oldin bo'lmagan narsa endi bo'ladigan bo'lishini bildiradi.",
                "examples": [
                    {"zh": "身体出现了一些问题。", "pinyin": "", "meaning": "Tanada ba'zi muammolar paydo bo'ldi."},
                    {"zh": "他突然出现在我面前。", "pinyin": "", "meaning": "U to'satdan ro'paramda paydo bo'ldi."},
                ],
            },
            {
                "no": 5,
                "title_zh": "来不及",
                "explanation": "'Vaqt yetmaydi, kech qolmoq' ma'nosini beradi. Biror narsa uchun vaqt qolmaganligini bildiradi.",
                "examples": [
                    {"zh": "如果再不改变，后来就来不及了。", "pinyin": "", "meaning": "Agar o'zgartirmasang, keyinroq kech bo'lib qoladi."},
                    {"zh": "我来不及吃早饭就出发了。", "pinyin": "", "meaning": "Nonushta qilishga vaqtim bo'lmay yo'lga chiqdim."},
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
                    {"prompt": "iqlim, ob-havo", "answer": "气候", "pinyin": "qìhòu"},
                    {"prompt": "yo'talmoq", "answer": "咳嗽", "pinyin": "késou"},
                    {"prompt": "deraza", "answer": "窗户", "pinyin": "chuānghù"},
                    {"prompt": "pushaymon bo'lmoq", "answer": "后悔", "pinyin": "hòuhuǐ"},
                    {"prompt": "mashq qilmoq", "answer": "锻炼", "pinyin": "duànliàn"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "估计", "answer": "taxmin qilmoq", "pinyin": "gūjì"},
                    {"prompt": "严重", "answer": "jiddiy, og'ir", "pinyin": "yánzhòng"},
                    {"prompt": "反对", "answer": "qarshi bo'lmoq", "pinyin": "fǎnduì"},
                    {"prompt": "来不及", "answer": "vaqt yetmaydi, kech qolmoq", "pinyin": "láibují"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (估计、再也不、出现、合适、来不及):",
                "items": [
                    {"prompt": "他说这次以后______喝酒了。", "answer": "再也不", "pinyin": "zài yě bù"},
                    {"prompt": "最近他身体______了一些问题。", "answer": "出现", "pinyin": "chūxiàn"},
                    {"prompt": "______他现在在图书馆。", "answer": "估计", "pinyin": "gūjì"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["气候", "咳嗽", "窗户", "后悔", "锻炼"]},
            {"no": 2, "answers": ["taxmin qilmoq", "jiddiy, og'ir", "qarshi bo'lmoq", "vaqt yetmaydi, kech qolmoq"]},
            {"no": 3, "answers": ["再也不", "出现", "估计"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["健康", "锻炼", "估计", "严重"],
                "example": "估计每天锻炼对健康很有好处，不要等问题严重才去医院。",
            },
            {
                "no": 2,
                "instruction": "'再也不...了' va '来不及' qoliplaridan foydalanib har biridan 2 ta gap tuzing.",
                "topic": "sog'liq va yomon odatlardan xalos bo'lish mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Sog'lom yashash uchun nima qilish kerak? 怎么样才能保持健康的生活？",
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
