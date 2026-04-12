import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 7,
    "lesson_code": "HSK2-L07",
    "title": "你家离公司远吗",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "教室", "pinyin": "jiàoshì", "pos": "n."},
        {"no": 2, "zh": "机场", "pinyin": "jīchǎng", "pos": "n."},
        {"no": 3, "zh": "路", "pinyin": "lù", "pos": "n."},
        {"no": 4, "zh": "离", "pinyin": "lí", "pos": "v."},
        {"no": 5, "zh": "公司", "pinyin": "gōngsī", "pos": "n."},
        {"no": 6, "zh": "远", "pinyin": "yuǎn", "pos": "adj."},
        {"no": 7, "zh": "公共汽车", "pinyin": "gōnggòng qìchē", "pos": "n."},
        {"no": 8, "zh": "小时", "pinyin": "xiǎoshí", "pos": "n."},
        {"no": 9, "zh": "慢", "pinyin": "màn", "pos": "adj."},
        {"no": 10, "zh": "快", "pinyin": "kuài", "pos": "adj."},
        {"no": 11, "zh": "过", "pinyin": "guò", "pos": "v."},
        {"no": 12, "zh": "走", "pinyin": "zǒu", "pos": "v."},
        {"no": 13, "zh": "到", "pinyin": "dào", "pos": "v."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "大卫回来了吗？", "pinyin": "Dàwèi huílái le ma?"},
                {"speaker": "B", "zh": "没有，他还在教室学习呢。", "pinyin": "Méiyǒu, tā hái zài jiàoshì xuéxí ne."},
                {"speaker": "A", "zh": "已经9点多了，他怎么还在学习？", "pinyin": "Yǐjīng jiǔ diǎn duō le, tā zěnme hái zài xuéxí?"},
                {"speaker": "B", "zh": "明天有考试，他说今天要好好准备。", "pinyin": "Míngtiān yǒu kǎoshì, tā shuō jīntiān yào hǎohǎo zhǔnbèi."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "去机场的路上 2",
            "scene_label_zh": "去机场的路上",
            "dialogue": [
                {"speaker": "A", "zh": "你现在在哪儿呢？", "pinyin": "Nǐ xiànzài zài nǎr ne?"},
                {"speaker": "B", "zh": "在去机场的路上。你已经到了吗？", "pinyin": "Zài qù jīchǎng de lùshang. Nǐ yǐjīng dào le ma?"},
                {"speaker": "A", "zh": "我下飞机了。你还有多长时间能到这儿？", "pinyin": "Wǒ xià fēijī le. Nǐ hái yǒu duō cháng shíjiān néng dào zhèr?"},
                {"speaker": "B", "zh": "二十分钟就到。", "pinyin": "Èrshí fēnzhōng jiù dào."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在健身房 3",
            "scene_label_zh": "在健身房",
            "dialogue": [
                {"speaker": "A", "zh": "你家离公司远吗？", "pinyin": "Nǐ jiā lí gōngsī yuǎn ma?"},
                {"speaker": "B", "zh": "很远，坐公共汽车要一个多小时呢！", "pinyin": "Hěn yuǎn, zuò gōnggòng qìchē yào yí ge duō xiǎoshí ne!"},
                {"speaker": "A", "zh": "坐公共汽车太慢了，你怎么不开车？", "pinyin": "Zuò gōnggòng qìchē tài màn le, nǐ zěnme bù kāi chē?"},
                {"speaker": "B", "zh": "开车也不快，路上车太多了！", "pinyin": "Kāi chē yě bù kuài, lùshang chē tài duō le!"}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在路上 4",
            "scene_label_zh": "在路上",
            "dialogue": [
                {"speaker": "A", "zh": "今天晚上我们一起吃饭吧，给你过生日。今天？", "pinyin": "Jīntiān wǎnshang wǒmen yìqǐ chīfàn ba, gěi nǐ guò shēngrì. Jīntiān?"},
                {"speaker": "B", "zh": "今天？离我的生日还有一个多星期呢！", "pinyin": "Jīntiān? Lí wǒ de shēngrì hái yǒu yí ge duō xīngqī ne!"},
                {"speaker": "A", "zh": "下个星期我要去北京，今天过吧。", "pinyin": "Xià ge xīngqī wǒ yào qù Běijīng, jīntiān guò ba."},
                {"speaker": "B", "zh": "好吧，离这儿不远有一个中国饭馆，走几分钟就到了。", "pinyin": "Hǎo ba, lí zhèr bù yuǎn yǒu yí ge Zhōngguó fànguǎn, zǒu jǐ fēnzhōng jiù dào le."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "语气副词“还”（2）"},
        {"no": 2, "title_zh": "时间副词“就”"},
        {"no": 3, "title_zh": "离"},
        {"no": 4, "title_zh": "语气助词“呢”"}
    ], ensure_ascii=False),
    "exercise_json": "[]",
    "answers_json": "[]",
    "homework_json": "[]",
    "review_json": "[]",
    "is_active": True
}


async def upsert_lesson():
    async with SessionLocal() as session:
        result = await session.execute(
            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.level = LESSON["level"]
            existing.lesson_order = LESSON["lesson_order"]
            existing.title = LESSON["title"]
            existing.goal = LESSON["goal"]
            existing.intro_text = LESSON["intro_text"]
            existing.vocabulary_json = LESSON["vocabulary_json"]
            existing.dialogue_json = LESSON["dialogue_json"]
            existing.grammar_json = LESSON["grammar_json"]
            existing.exercise_json = LESSON["exercise_json"]
            existing.answers_json = LESSON["answers_json"]
            existing.homework_json = LESSON["homework_json"]
            existing.review_json = LESSON["review_json"]
            existing.is_active = LESSON["is_active"]
            print(f"updated: {LESSON['lesson_code']}")
        else:
            session.add(CourseLesson(**LESSON))
            print(f"inserted: {LESSON['lesson_code']}")

        await session.commit()


if __name__ == "__main__":
    asyncio.run(upsert_lesson())
