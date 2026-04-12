import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 2,
    "lesson_code": "HSK2-L02",
    "title": "我每天六点起床",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "生病", "pinyin": "shēngbìng", "pos": "v."},
        {"no": 2, "zh": "每", "pinyin": "měi", "pos": "pron."},
        {"no": 3, "zh": "早上", "pinyin": "zǎoshang", "pos": "n."},
        {"no": 4, "zh": "跑步", "pinyin": "pǎobù", "pos": "v."},
        {"no": 5, "zh": "起床", "pinyin": "qǐchuáng", "pos": "v."},
        {"no": 6, "zh": "药", "pinyin": "yào", "pos": "n."},
        {"no": 7, "zh": "身体", "pinyin": "shēntǐ", "pos": "n."},
        {"no": 8, "zh": "出院", "pinyin": "chūyuàn", "pos": "v."},
        {"no": 9, "zh": "出", "pinyin": "chū", "pos": "v."},
        {"no": 10, "zh": "高", "pinyin": "gāo", "pos": "adj."},
        {"no": 11, "zh": "米", "pinyin": "mǐ", "pos": "m."},
        {"no": 12, "zh": "知道", "pinyin": "zhīdào", "pos": "v."},
        {"no": 13, "zh": "休息", "pinyin": "xiūxi", "pos": "v."},
        {"no": 14, "zh": "忙", "pinyin": "máng", "pos": "adj."},
        {"no": 15, "zh": "时间", "pinyin": "shíjiān", "pos": "n."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在运动场",
            "dialogue": [
                {"speaker": "A", "zh": "你很少生病，是不是喜欢运动？", "pinyin": "Nǐ hěn shǎo shēngbìng, shì bú shì xǐhuan yùndòng?"},
                {"speaker": "B", "zh": "是啊，我每天早上都要出去跑步。", "pinyin": "Shì a, wǒ měitiān zǎoshang dōu yào chūqù pǎobù."},
                {"speaker": "A", "zh": "你每天几点起床？", "pinyin": "Nǐ měitiān jǐ diǎn qǐchuáng?"},
                {"speaker": "B", "zh": "我每天六点起床。", "pinyin": "Wǒ měitiān liù diǎn qǐchuáng."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在医院 2",
            "scene_label_zh": "在医院",
            "dialogue": [
                {"speaker": "A", "zh": "吃药了吗？现在身体怎么样？", "pinyin": "Chī yào le ma? Xiànzài shēntǐ zěnmeyàng?"},
                {"speaker": "B", "zh": "吃了。现在好多了。", "pinyin": "Chī le. Xiànzài hǎo duō le."},
                {"speaker": "A", "zh": "什么时候能出院？", "pinyin": "Shénme shíhou néng chūyuàn?"},
                {"speaker": "B", "zh": "医生说下个星期。", "pinyin": "Yīshēng shuō xià ge xīngqī."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在操场 3",
            "scene_label_zh": "在操场",
            "dialogue": [
                {"speaker": "A", "zh": "大卫今年多大？", "pinyin": "Dàwèi jīnnián duō dà?"},
                {"speaker": "B", "zh": "二十多岁。", "pinyin": "Èrshí duō suì."},
                {"speaker": "A", "zh": "他多高？", "pinyin": "Tā duō gāo?"},
                {"speaker": "B", "zh": "一米八几。", "pinyin": "Yì mǐ bā jǐ."},
                {"speaker": "A", "zh": "你怎么知道这么多啊？", "pinyin": "Nǐ zěnme zhīdào zhème duō a?"},
                {"speaker": "B", "zh": "他是我同学。", "pinyin": "Tā shì wǒ tóngxué."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在房间 4",
            "scene_label_zh": "在房间",
            "dialogue": [
                {"speaker": "A", "zh": "张老师星期六也不休息啊？", "pinyin": "Zhāng lǎoshī xīngqīliù yě bù xiūxi a?"},
                {"speaker": "B", "zh": "是啊，他这几天很忙，没有时间休息。", "pinyin": "Shì a, tā zhè jǐ tiān hěn máng, méiyǒu shíjiān xiūxi."},
                {"speaker": "A", "zh": "那会很累吧？", "pinyin": "Nà huì hěn lèi ba?"},
                {"speaker": "B", "zh": "他每天回来都很累。", "pinyin": "Tā měitiān huílái dōu hěn lèi."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "用“是不是”的问句"},
        {"no": 2, "title_zh": "代词“每”"},
        {"no": 3, "title_zh": "疑问代词“多”"}
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
