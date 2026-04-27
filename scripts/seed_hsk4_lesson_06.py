import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk4",
    "lesson_order": 6,
    "lesson_code": "HSK4-L06",
    "title": "一分钱一分货",
    "goal": "narx va sifat munosabati, bozorda savdo haqida gapirish; 竟然, 倍, 值得, 其中, (在)...下 grammatik qoliplarini o'zlashtirish",
    "intro_text": "Bu dars 'Narx sifatga mos' mavzusiga bag'ishlangan. Unda do'konda narx savdolashish, mahsulot sifatini baholash va iste'molchi huquqlari haqida gaplashish o'rganiladi. Asosiy grammatik qoliplar: 竟然, 倍, 值得, 其中, （在）...下.",
    "vocabulary_json": json.dumps(
        [
            {"no": 1, "zh": "果汁", "pinyin": "guǒzhī", "pos": "n.", "meaning": "meva sharbati"},
            {"no": 2, "zh": "售货员", "pinyin": "shòuhuòyuán", "pos": "n.", "meaning": "sotuvchi, do'kon xodimi"},
            {"no": 3, "zh": "袜子", "pinyin": "wàzi", "pos": "n.", "meaning": "paypoq"},
            {"no": 4, "zh": "打扰", "pinyin": "dǎrǎo", "pos": "v.", "meaning": "bezovta qilmoq, halaqit bermoq"},
            {"no": 5, "zh": "竟然", "pinyin": "jìngrán", "pos": "adv.", "meaning": "kutilmaganda, ajablanish bilan"},
            {"no": 6, "zh": "西红柿", "pinyin": "xīhóngshì", "pos": "n.", "meaning": "pomidor"},
            {"no": 7, "zh": "百分之", "pinyin": "bǎi fēn zhī", "pos": "phrase", "meaning": "foiz"},
            {"no": 8, "zh": "倍", "pinyin": "bèi", "pos": "m.", "meaning": "marta, barobar (ko'paytma)"},
            {"no": 9, "zh": "皮肤", "pinyin": "pífū", "pos": "n.", "meaning": "teri, tana terisi"},
            {"no": 10, "zh": "好处", "pinyin": "hǎochu", "pos": "n.", "meaning": "foyda, manfaat"},
            {"no": 11, "zh": "尝", "pinyin": "cháng", "pos": "v.", "meaning": "tatib ko'rmoq, sinab ko'rmoq"},
            {"no": 12, "zh": "值得", "pinyin": "zhíde", "pos": "v.", "meaning": "arziydi, qimmatga arziydi"},
            {"no": 13, "zh": "其中", "pinyin": "qízhōng", "pos": "pron.", "meaning": "ularning ichida, shular orasida"},
            {"no": 14, "zh": "活动", "pinyin": "huódòng", "pos": "n./v.", "meaning": "tadbir, aksiya; harakatlanmoq"},
            {"no": 15, "zh": "免费", "pinyin": "miǎnfèi", "pos": "v./adj.", "meaning": "bepul bermoq; bepul"},
            {"no": 16, "zh": "修理", "pinyin": "xiūlǐ", "pos": "v.", "meaning": "ta'mirlash, tuzatish"},
            {"no": 17, "zh": "退换", "pinyin": "tuìhuàn", "pos": "v.", "meaning": "qaytarib almashmoq"},
            {"no": 18, "zh": "便宜", "pinyin": "piányí", "pos": "adj.", "meaning": "arzon"},
            {"no": 19, "zh": "贵", "pinyin": "guì", "pos": "adj.", "meaning": "qimmat, baholi"},
            {"no": 20, "zh": "比较", "pinyin": "bǐjiào", "pos": "adv.", "meaning": "nisbatan, ancha"},
        ],
        ensure_ascii=False,
    ),
    "dialogue_json": json.dumps(
        [
            {
                "block_no": 1,
                "section_label": "课文 1",
                "scene_label_zh": "张远和李谦谈上周去超市的经历",
                "dialogue": [
                    {"speaker": "张远", "zh": "昨天晚上我找给你打电话一直没人接，你在做什么呢？", "pinyin": "", "translation": "Kecha kechqurun senga qo'ng'iroq qildim, hech kim ko'tarmadi, nima qilyapding?"},
                    {"speaker": "李谦", "zh": "我妻子让我陪她去超市买果汁，我把手机忘在家里了。", "pinyin": "", "translation": "Xotinim meni supermarketda meva sharbati sotib olishga olib borgandi, telefonimy uyda qolgan edi."},
                    {"speaker": "张远", "zh": "那里从来不让我们进去，售货员说那地方我们偌大，拿了一条领带、两双袜子，然后我们就高高兴兴地回来了。", "pinyin": "", "translation": "Avval u yerga kirishimizga ruxsat bermadilar, sotuvchi aytdiki... Keyin bir bo'yin bog'ich va ikki juft paypoq oldik, so'ng xursandchilik bilan qaytdik."},
                    {"speaker": "李谦", "zh": "买东西时我自己选、自己买，自己决定，从来不希望别人帮我选。", "pinyin": "", "translation": "Men o'zim tanlayman, o'zim sotib olaman, o'zim qaror qilaman, hech qachon boshqaning yordam berishini xohlamayman."},
                ],
            },
            {
                "block_no": 2,
                "section_label": "课文 2",
                "scene_label_zh": "王静在商店买西红柿",
                "dialogue": [
                    {"speaker": "王静", "zh": "西红柿新鲜吗？怎么卖？", "pinyin": "", "translation": "Pomidor yangi chiqibdimi? Qancha turadi?"},
                    {"speaker": "售货员", "zh": "七块钱一斤，您放心，保证百分之百新鲜。", "pinyin": "", "translation": "Bir jin etti yuan, xotirjam bo'ling, yuz foiz yangi."},
                    {"speaker": "王静", "zh": "怎么这么贵呀！我昨天天在另一个超市，才五块五，今天的价格是昨天的两倍！", "pinyin": "", "translation": "Bu qadar qimmatmi! Men kecha boshqa supermarketda besh yuan besh fen topgan edim, bugungi narx kechagidan ikki barobar qimmat!"},
                    {"speaker": "售货员", "zh": "您看我们的西红柿是'绿色'的，一分钱一分货，每天吃两个这种特别的西红柿，对皮肤好处很多。", "pinyin": "", "translation": "Ko'ring, bizning pomidorimiz 'ekologik' toza, narx sifatga mos, har kuni bunday maxsus pomidordan ikkita yesangiz, teringizga juda foydali."},
                    {"speaker": "王静", "zh": "好，那我先买先尝尝。", "pinyin": "", "translation": "Yaxshi, unda avval sotib olib tatib ko'raman."},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "grammar_json": json.dumps(
        [
            {
                "no": 1,
                "title_zh": "竟然",
                "explanation": "'Kutilmaganda, ajablanib' ma'nosini beradi. Kutilmagan yoki hayratlanarli hodisani ifodalaydi.",
                "examples": [
                    {"zh": "他竟然一个人吃了两个西瓜！", "pinyin": "", "meaning": "U kutilmaganda bir o'zi ikkita tarvuz yedi!"},
                    {"zh": "这道题竟然这么简单。", "pinyin": "", "meaning": "Bu masala hayratlanarli darajada oddiy ekan."},
                ],
            },
            {
                "no": 2,
                "title_zh": "倍",
                "explanation": "'Marta, barobar' ma'nosini beradi. Miqdorning necha marta ko'payganini bildiradi.",
                "examples": [
                    {"zh": "今天的价格是昨天的两倍。", "pinyin": "", "meaning": "Bugungi narx kechagidan ikki barobar."},
                    {"zh": "我的速度是他的三倍。", "pinyin": "", "meaning": "Mening tezligim undan uch barobar ko'p."},
                ],
            },
            {
                "no": 3,
                "title_zh": "值得",
                "explanation": "'Arziydi, qimmatga arziydi' ma'nosini beradi. Biror narsa qilinishga arzirligini bildiradi.",
                "examples": [
                    {"zh": "这本书值得一读。", "pinyin": "", "meaning": "Bu kitob o'qishga arziydi."},
                    {"zh": "健康是最值得投资的事情。", "pinyin": "", "meaning": "Sog'liq — investitsiyaga eng ko'p arzigulik narsa."},
                ],
            },
            {
                "no": 4,
                "title_zh": "其中",
                "explanation": "'Ularning ichida, shular orasida' ma'nosini beradi. Bir guruh ichidan ma'lum bir qismni ajratadi.",
                "examples": [
                    {"zh": "他买了很多水果，其中有苹果和西红柿。", "pinyin": "", "meaning": "U ko'p meva-sabzavot sotib oldi, ular orasida olma va pomidor bor."},
                    {"zh": "班里有三十个同学，其中五个是外国人。", "pinyin": "", "meaning": "Sinfda o'ttiz talaba bor, ulardan beshta chet ellik."},
                ],
            },
            {
                "no": 5,
                "title_zh": "（在）……下",
                "explanation": "'...sharoitida, ...ostida' ma'nosini beradi. Biror shart yoki holat ostida narsa sodir bo'lishini bildiradi.",
                "examples": [
                    {"zh": "在父母的支持下，他完成了学业。", "pinyin": "", "meaning": "Ota-onasining qo'llab-quvvatlashi ostida u o'qishini tugatdi."},
                    {"zh": "在这种情况下，我们应该怎么做？", "pinyin": "", "meaning": "Bunday sharoitda biz nima qilishimiz kerak?"},
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
                    {"prompt": "meva sharbati", "answer": "果汁", "pinyin": "guǒzhī"},
                    {"prompt": "foiz", "answer": "百分之", "pinyin": "bǎi fēn zhī"},
                    {"prompt": "foyda, manfaat", "answer": "好处", "pinyin": "hǎochu"},
                    {"prompt": "arziydi", "answer": "值得", "pinyin": "zhíde"},
                    {"prompt": "bepul", "answer": "免费", "pinyin": "miǎnfèi"},
                ],
            },
            {
                "no": 2,
                "type": "translate_to_uzbek",
                "instruction": "Quyidagi so'zlarning o'zbekchasini yozing:",
                "items": [
                    {"prompt": "竟然", "answer": "kutilmaganda, ajablanib", "pinyin": "jìngrán"},
                    {"prompt": "倍", "answer": "marta, barobar", "pinyin": "bèi"},
                    {"prompt": "其中", "answer": "ularning ichida, shular orasida", "pinyin": "qízhōng"},
                    {"prompt": "打扰", "answer": "bezovta qilmoq", "pinyin": "dǎrǎo"},
                ],
            },
            {
                "no": 3,
                "type": "fill_blank",
                "instruction": "Mos so'zni tanlang (竟然、倍、值得、其中、在...下):",
                "items": [
                    {"prompt": "他______一个人喝了三瓶果汁！", "answer": "竟然", "pinyin": "jìngrán"},
                    {"prompt": "这里的苹果是那里的两______。", "answer": "倍", "pinyin": "bèi"},
                    {"prompt": "______老师的帮助______，他进步很快。", "answer": "在 / 下", "pinyin": "zài / xià"},
                ],
            },
        ],
        ensure_ascii=False,
    ),
    "answers_json": json.dumps(
        [
            {"no": 1, "answers": ["果汁", "百分之", "好处", "值得", "免费"]},
            {"no": 2, "answers": ["kutilmaganda, ajablanib", "marta, barobar", "ularning ichida, shular orasida", "bezovta qilmoq"]},
            {"no": 3, "answers": ["竟然", "倍", "在 / 下"]},
        ],
        ensure_ascii=False,
    ),
    "homework_json": json.dumps(
        [
            {
                "no": 1,
                "instruction": "Quyidagi so'zlardan foydalanib 3 ta gap tuzing:",
                "words": ["竟然", "值得", "其中", "好处"],
                "example": "这种水果对皮肤好处很多，其中维生素C尤其丰富，值得每天吃。",
            },
            {
                "no": 2,
                "instruction": "'倍' va '（在）...下' qoliplaridan foydalanib har biridan 2 ta gap tuzing.",
                "topic": "narx, xarid, iqtisodiyot mavzusida",
            },
            {
                "no": 3,
                "instruction": "5-6 gapdan iborat kichik matn yozing:",
                "topic": "Siz narx bilan sifatning qaysi biriga ko'proq e'tibor berasiz? 你认为一分钱一分货有道理吗？",
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
