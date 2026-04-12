import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 3,
    "lesson_code": "HSK2-L03",
    "title": "左边那个红色的是我的",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "手表", "pinyin": "shǒubiǎo", "pos": "n."},
        {"no": 2, "zh": "千", "pinyin": "qiān", "pos": "num."},
        {"no": 3, "zh": "报纸", "pinyin": "bàozhǐ", "pos": "n."},
        {"no": 4, "zh": "送", "pinyin": "sòng", "pos": "v."},
        {"no": 5, "zh": "一下", "pinyin": "yíxià", "pos": ""},
        {"no": 6, "zh": "牛奶", "pinyin": "niúnǎi", "pos": "n."},
        {"no": 7, "zh": "房间", "pinyin": "fángjiān", "pos": "n."},
        {"no": 8, "zh": "丈夫", "pinyin": "zhàngfu", "pos": "n."},
        {"no": 9, "zh": "旁边", "pinyin": "pángbiān", "pos": "n."},
        {"no": 10, "zh": "真", "pinyin": "zhēn", "pos": "adv."},
        {"no": 11, "zh": "粉色", "pinyin": "fěnsè", "pos": "n."},
        {"no": 12, "zh": "粉", "pinyin": "fěn", "pos": "adj."},
        {"no": 13, "zh": "颜色", "pinyin": "yánsè", "pos": "n."},
        {"no": 14, "zh": "左边", "pinyin": "zuǒbian", "pos": "n."},
        {"no": 15, "zh": "红色", "pinyin": "hóngsè", "pos": "n."},
        {"no": 16, "zh": "红", "pinyin": "hóng", "pos": "adj."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在房间",
            "dialogue": [
                {"speaker": "A", "zh": "这块手表是你的吗？", "pinyin": "Zhè kuài shǒubiǎo shì nǐ de ma?"},
                {"speaker": "B", "zh": "不是我的。是我爸爸的。", "pinyin": "Bú shì wǒ de. Shì wǒ bàba de."},
                {"speaker": "A", "zh": "多少钱买的？", "pinyin": "Duōshao qián mǎi de?"},
                {"speaker": "B", "zh": "三千多块。", "pinyin": "Sānqiān duō kuài."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在家里 2",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "这是今天早上的报纸吗？", "pinyin": "Zhè shì jīntiān zǎoshang de bàozhǐ ma?"},
                {"speaker": "B", "zh": "不是，是昨天的。", "pinyin": "Bú shì, shì zuótiān de."},
                {"speaker": "A", "zh": "你听，是不是送报纸的来了？", "pinyin": "Nǐ tīng, shì bú shì sòng bàozhǐ de lái le?"},
                {"speaker": "B", "zh": "我看一下。不是，是送牛奶的。", "pinyin": "Wǒ kàn yíxià. Bú shì, shì sòng niúnǎi de."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在家里 3",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "这是谁的房间？", "pinyin": "Zhè shì shéi de fángjiān?"},
                {"speaker": "B", "zh": "这是我和我丈夫的，旁边那个小的房间是我女儿的。", "pinyin": "Zhè shì wǒ hé wǒ zhàngfu de, pángbiān nàge xiǎo de fángjiān shì wǒ nǚ'ér de."},
                {"speaker": "A", "zh": "你女儿的房间真漂亮啊！都是粉色的。", "pinyin": "Nǐ nǚ'ér de fángjiān zhēn piàoliang a! Dōu shì fěnsè de."},
                {"speaker": "B", "zh": "是啊，粉色是我女儿最喜欢的颜色。", "pinyin": "Shì a, fěnsè shì wǒ nǚ'ér zuì xǐhuan de yánsè."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在办公室 4",
            "scene_label_zh": "在办公室",
            "dialogue": [
                {"speaker": "A", "zh": "你看见我的杯子了吗？", "pinyin": "Nǐ kànjian wǒ de bēizi le ma?"},
                {"speaker": "B", "zh": "这里有几个杯子，哪个是你的？", "pinyin": "Zhèlǐ yǒu jǐ ge bēizi, nǎge shì nǐ de?"},
                {"speaker": "A", "zh": "左边那个红色的是我的。", "pinyin": "Zuǒbian nàge hóngsè de shì wǒ de."},
                {"speaker": "B", "zh": "给你。", "pinyin": "Gěi nǐ."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "“的”字短语"},
        {"no": 2, "title_zh": "量词“一下”"},
        {"no": 3, "title_zh": "语气副词“真”"}
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
