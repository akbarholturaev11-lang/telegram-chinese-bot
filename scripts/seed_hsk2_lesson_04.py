import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 4,
    "lesson_code": "HSK2-L04",
    "title": "这个工作是他帮我介绍的",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "生日", "pinyin": "shēngrì", "pos": "n."},
        {"no": 2, "zh": "快乐", "pinyin": "kuàilè", "pos": "adj."},
        {"no": 3, "zh": "给", "pinyin": "gěi", "pos": "prep."},
        {"no": 4, "zh": "接", "pinyin": "jiē", "pos": "v."},
        {"no": 5, "zh": "晚上", "pinyin": "wǎnshang", "pos": "n."},
        {"no": 6, "zh": "问", "pinyin": "wèn", "pos": "v."},
        {"no": 7, "zh": "非常", "pinyin": "fēicháng", "pos": "adv."},
        {"no": 8, "zh": "开始", "pinyin": "kāishǐ", "pos": "v."},
        {"no": 9, "zh": "已经", "pinyin": "yǐjīng", "pos": "adv."},
        {"no": 10, "zh": "长", "pinyin": "cháng", "pos": "adj."},
        {"no": 11, "zh": "两", "pinyin": "liǎng", "pos": "num."},
        {"no": 12, "zh": "帮", "pinyin": "bāng", "pos": "v."},
        {"no": 13, "zh": "介绍", "pinyin": "jièshào", "pos": "v."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在教室",
            "dialogue": [
                {"speaker": "A", "zh": "生日快乐！这是送给你的！", "pinyin": "Shēngrì kuàilè! Zhè shì sòng gěi nǐ de!"},
                {"speaker": "B", "zh": "是什么？是一本书吗？", "pinyin": "Shì shénme? Shì yì běn shū ma?"},
                {"speaker": "A", "zh": "对，这本书是我写给你的。", "pinyin": "Duì, zhè běn shū shì wǒ xiě gěi nǐ de."},
                {"speaker": "B", "zh": "太谢谢你了！", "pinyin": "Tài xièxie nǐ le!"}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在家里 2",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "早上有你一个电话。", "pinyin": "Zǎoshang yǒu nǐ yí ge diànhuà."},
                {"speaker": "B", "zh": "电话是谁打的？", "pinyin": "Diànhuà shì shéi dǎ de?"},
                {"speaker": "A", "zh": "不知道，是儿子接的。", "pinyin": "Bù zhīdào, shì érzi jiē de."},
                {"speaker": "B", "zh": "好，晚上我问一下儿子。", "pinyin": "Hǎo, wǎnshang wǒ wèn yíxià érzi."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在运动场 3",
            "scene_label_zh": "在运动场",
            "dialogue": [
                {"speaker": "A", "zh": "你喜欢踢足球吗？", "pinyin": "Nǐ xǐhuan tī zúqiú ma?"},
                {"speaker": "B", "zh": "非常喜欢。", "pinyin": "Fēicháng xǐhuan."},
                {"speaker": "A", "zh": "你是什么时候开始踢足球的？", "pinyin": "Nǐ shì shénme shíhou kāishǐ tī zúqiú de?"},
                {"speaker": "B", "zh": "我十一岁的时候开始踢足球，已经踢了十年了。", "pinyin": "Wǒ shíyī suì de shíhou kāishǐ tī zúqiú, yǐjīng tī le shí nián le."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在公司 4",
            "scene_label_zh": "在公司",
            "dialogue": [
                {"speaker": "A", "zh": "你在这儿工作多长时间了？", "pinyin": "Nǐ zài zhèr gōngzuò duō cháng shíjiān le?"},
                {"speaker": "B", "zh": "已经两年多了，我是2011年来的。", "pinyin": "Yǐjīng liǎng nián duō le, wǒ shì èr líng yī yī nián lái de."},
                {"speaker": "A", "zh": "你认识谢先生吗？", "pinyin": "Nǐ rènshi Xiè xiānsheng ma?"},
                {"speaker": "B", "zh": "认识，我们是大学同学，这个工作是他帮我介绍的。", "pinyin": "Rènshi, wǒmen shì dàxué tóngxué, zhège gōngzuò shì tā bāng wǒ jièshào de."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "“是……的”句：强调施事"},
        {"no": 2, "title_zh": "表示时间：……的时候"},
        {"no": 3, "title_zh": "时间副词“已经”"}
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
