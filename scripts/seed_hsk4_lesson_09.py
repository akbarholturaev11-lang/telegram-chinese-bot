import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 9,
    "lesson_code": "HSK4-L09",
    "title": "阳光总在风雨后",
    "goal": "sport, qiyinchiliklar va muvaffaqiyat haqida gapirish; 渐渐, 通过, 结果, 坚持 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Quyosh yomg'irdan keyin chiqadi' mavzusiga bag'ishlangan. Unda sport musobaqalari, qiyinchiliklarga bardosh berish va muvaffaqiyat sari harakat haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 渐渐, 通过, 可是, 结果, 上.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "饼干", "pinyin": "bǐnggān", "pos": "n.", "meaning": "pechenye, biskvit"},
            {"no": 2, "zh": "难道", "pinyin": "nándào", "pos": "adv.", "meaning": "masa, axir (ritorik savol uchun)"},
            {"no": 3, "zh": "得", "pinyin": "děi", "pos": "modal", "meaning": "kerak, shart (majburiyat)"},
            {"no": 4, "zh": "坚持", "pinyin": "jiānchí", "pos": "v.", "meaning": "davom ettirmoq, chidamoq, qat'iy turmoq"},
            {"no": 5, "zh": "放弃", "pinyin": "fàngqì", "pos": "v.", "meaning": "voz kechmoq, tashlab ketmoq"},
            {"no": 6, "zh": "主意", "pinyin": "zhǔyì", "pos": "n.", "meaning": "fikr, g'oya, qaror"},
            {"no": 7, "zh": "网球", "pinyin": "wǎngqiú", "pos": "n.", "meaning": "tennis"},
            {"no": 8, "zh": "国际", "pinyin": "guójì", "pos": "adj.", "meaning": "xalqaro"},
            {"no": 9, "zh": "轻松", "pinyin": "qīngsōng", "pos": "adj.", "meaning": "yengil, oson, erkin"},
            {"no": 10, "zh": "赢", "pinyin": "yíng", "pos": "v.", "meaning": "g'alaba qozonmoq, yutmoq"},
            {"no": 11, "zh": "随便", "pinyin": "suíbiàn", "pos": "adj./adv.", "meaning": "befarq, ixtiyoriy; istalgan vaqt"},
            {"no": 12, "zh": "汗", "pinyin": "hàn", "pos": "n.", "meaning": "ter"},
            {"no": 13, "zh": "通过", "pinyin": "tōngguò", "pos": "prep./v.", "meaning": "orqali, vositasida; o'tmoq"},
            {"no": 14, "zh": "渐渐", "pinyin": "jiànjiàn", "pos": "adv.", "meaning": "asta-sekin, sekin-asta"},
            {"no": 15, "zh": "结果", "pinyin": "jiéguǒ", "pos": "n./conj.", "meaning": "natija; natijada, oxir-oqibat"},
            {"no": 16, "zh": "加油", "pinyin": "jiā yóu", "pos": "v.", "meaning": "kuch qo'shmoq, rag'batlantirmoq"},
            {"no": 17, "zh": "比赛", "pinyin": "bǐsài", "pos": "n./v.", "meaning": "musobaqa; musobaqalashmoq"},
            {"no": 18, "zh": "失败", "pinyin": "shībài", "pos": "v./n.", "meaning": "mag'lub bo'lmoq; mag'lubiyat"},
            {"no": 19, "zh": "成绩", "pinyin": "chéngjì", "pos": "n.", "meaning": "natija, ball, ko'rsatkich"},
            {"no": 20, "zh": "相信", "pinyin": "xiāngxìn", "pos": "v.", "meaning": "ishonmoq"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "小李和小林聊关于放弃网球的主意",
                "dialogue": [
                    {"speaker": "小李", "zh": "这里的饼干好吃吗？你不要太随便，一分钱一分货嘛。", "pinyin": "", "translation": "Bu yerdagi pechenye mazalimi? Siz juda befarq bo'lmang, narx sifatga mos-da."},
                    {"speaker": "小林", "zh": "难道你不相信我的眼光？我觉得打网球得坚持，不能放弃。", "pinyin": "", "translation": "Masa, menga ishonmaysizmi? Menimcha tennis o'ynash davom ettirilishi kerak, voz kechmaslik lozim."},
                    {"speaker": "小李", "zh": "你练了多长时间了？成绩怎么样？", "pinyin": "", "translation": "Qancha vaqtdan beri mashq qilyapsiz? Natijalaringiz qanday?"},
                    {"speaker": "小林", "zh": "练了一年多了，可是成绩还不是很好，有时候我都想放弃这个主意了。", "pinyin": "", "translation": "Bir yildan ko'proq mashq qildim, lekin natijam hali yaxshi emas, ba'zan bu fikrdan voz kechmoqchiman."},
                    {"speaker": "小李", "zh": "不能放弃！通过努力，成绩渐渐会好起来的，阳光总在风雨后嘛！", "pinyin": "", "translation": "Voz kechmaslik kerak! Harakat orqali natijalar asta-sekin yaxshilanadi, quyosh yomg'irdan keyin chiqadi-da!"},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "小夏和小雨聊关于上次足球比赛的感受",
                "dialogue": [
                    {"speaker": "小夏", "zh": "上次比赛你们赢了吗？", "pinyin": "", "translation": "O'tgan gal musobaqada g'alaba qozonganmisiz?"},
                    {"speaker": "小雨", "zh": "没有，我们输了，但这次比赛让我们学到了很多，失败了不要紧，重要的是继续坚持。", "pinyin": "", "translation": "Yo'q, mag'lub bo'ldik, lekin bu musobaqa bizga ko'p narsa o'rgatdi, mag'lubiyat muhim emas, muhimi davom ettirishdir."},
                    {"speaker": "小夏", "zh": "说得对！通过这次比赛，大家渐渐明白了团队合作的重要性，结果对大家都有好处。", "pinyin": "", "translation": "To'g'ri aytdingiz! Bu musobaqa orqali hammamiz asta-sekin jamoa ishining muhimligini tushundik, natija hammamizga foydali bo'ldi."},
                    {"speaker": "小雨", "zh": "国际比赛真的很不轻松，每次都出很多汗，但这种感觉很好，加油吧！", "pinyin": "", "translation": "Xalqaro musobaqa haqiqatan ham oson emas, har safar ko'p ter to'kiladi, lekin bu his juda yaxshi, rag'batlantiraylik!"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "渐渐",
                "explanation": "'Asta-sekin, sekin-asta' ma'nosini beradi. Biror o'zgarish yoki jarayon sekin-asta sodir bo'lishini bildiradi.",
                "examples": [
                    {"zh": "通过努力，成绩渐渐会好起来的。", "pinyin": "", "meaning": "Harakat orqali natijalar asta-sekin yaxshilanadi."},
                    {"zh": "来中国以后，他的汉语渐渐进步了。", "pinyin": "", "meaning": "Xitoyga kelgandan so'ng, uning xitoy tili asta-sekin rivojlandi."},
                ],
            },
            {
                "no": 2,
                "title_zh": "通过",
                "explanation": "'Orqali, vositasida' ma'nosini beradi. Biror usul yoki vosita yordamida maqsadga erishishni bildiradi.",
                "examples": [
                    {"zh": "通过这次比赛，大家学到了很多。", "pinyin": "", "meaning": "Bu musobaqa orqali hammamiz ko'p narsa o'rgandik."},
                    {"zh": "通过学习，他的成绩提高了。", "pinyin": "", "meaning": "O'qish orqali uning natijalari ko'tarildi."},
                ],
            },
            {
                "no": 3,
                "title_zh": "可是",
                "explanation": "'Lekin, ammo' ma'nosini beradi. Oldingi gapga zid ma'noni bildiradi.",
                "examples": [
                    {"zh": "我练了一年多，可是成绩还不太好。", "pinyin": "", "meaning": "Men bir yildan ko'proq mashq qildim, lekin natijam hali yaxshi emas."},
                    {"zh": "他很努力，可是没有时间休息。", "pinyin": "", "meaning": "U juda tirishqoq, lekin dam olishga vaqti yo'q."},
                ],
            },
            {
                "no": 4,
                "title_zh": "结果",
                "explanation": "'Natija; natijada, oxir-oqibat' ma'nosida ishlatiladi. Bir holat yoki harakatning natijasini bildiradi.",
                "examples": [
                    {"zh": "他努力练习，结果赢了比赛。", "pinyin": "", "meaning": "U qattiq mashq qildi, natijada musobaqada g'alaba qozondi."},
                    {"zh": "比赛的结果对大家都有好处。", "pinyin": "", "meaning": "Musobaqaning natijasi hammamizga foydali bo'ldi."},
                ],
            },
            {
                "no": 5,
                "title_zh": "动词 + 上（趋向补语）",
                "explanation": "Ba'zi fe'llarga 上 qo'shilganda 'boshlash, o'rganish, yaxshi ko'rib qolish' ma'nosini beradi.",
                "examples": [
                    {"zh": "他慢慢爱上了打网球。", "pinyin": "", "meaning": "U asta-sekin tennis o'ynashni yaxshi ko'rib qoldi."},
                    {"zh": "成绩好起来了。", "pinyin": "", "meaning": "Natijalar yaxshilana boshladi."},
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
                    {"prompt": "davom ettirmoq, chidamoq", "answer": "坚持", "pinyin": "jiānchí"},
                    {"prompt": "voz kechmoq", "answer": "放弃", "pinyin": "fàngqì"},
                    {"prompt": "g'alaba qozonmoq", "answer": "赢", "pinyin": "yíng"},
                    {"prompt": "natija", "answer": "结果", "pinyin": "jiéguǒ"},
                    {"prompt": "xalqaro", "answer": "国际", "pinyin": "guójì"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "渐渐", "answer": "asta-sekin, sekin-asta", "pinyin": "jiànjiàn"},
                    {"prompt": "通过", "answer": "orqali, vositasida", "pinyin": "tōngguò"},
                    {"prompt": "难道", "answer": "masa, axir (ritorik savol)", "pinyin": "nándào"},
                    {"prompt": "相信", "answer": "ishonmoq", "pinyin": "xiāngxìn"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (渐渐、通过、可是、结果、坚持):",
                "items": [
                    {"prompt": "他练了很久，______还是没赢。", "answer": "可是", "pinyin": "kěshì"},
                    {"prompt": "______努力学习，他______进步了很多。", "answer": "通过 / 渐渐", "pinyin": "tōngguò / jiànjiàn"},
                    {"prompt": "不管多难，都要______下去。", "answer": "坚持", "pinyin": "jiānchí"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["坚持", "放弃", "赢", "结果", "国际"]},
            {"no": 2, "answers": ["asta-sekin, sekin-asta", "orqali, vositasida", "masa, axir (ritorik savol)", "ishonmoq"]},
            {"no": 3, "answers": ["可是", "通过 / 渐渐", "坚持"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["坚持", "通过", "渐渐", "结果"],
                "example": "通过每天坚持练习，他的网球水平渐渐提高了，结果赢得了比赛。",
            },
            {
                "no": 2,
                "instruction": "'通过...就...' va '渐渐' qoliplaridan foydalanib har biridan 2 ta gap tuzing.",
                "topic": "sport, muvaffaqiyat va qiyinchiliklar mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Siz qachondir qiyinchilikdan o'tib muvaffaqiyat qozonganmisiz? 你有过坚持并取得成功的经历吗？",
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
