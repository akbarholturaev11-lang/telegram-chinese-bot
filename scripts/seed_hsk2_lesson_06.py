import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 6,
    "lesson_code": "HSK2-L06",
    "title": "你怎么不吃了",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "门", "pinyin": "mén", "pos": "n."},
        {"no": 2, "zh": "外", "pinyin": "wài", "pos": "n."},
        {"no": 3, "zh": "自行车", "pinyin": "zìxíngchē", "pos": "n."},
        {"no": 4, "zh": "羊肉", "pinyin": "yángròu", "pos": "n."},
        {"no": 5, "zh": "好吃", "pinyin": "hǎochī", "pos": "adj."},
        {"no": 6, "zh": "面条", "pinyin": "miàntiáo", "pos": "n."},
        {"no": 7, "zh": "打篮球", "pinyin": "dǎ lánqiú", "pos": "v."},
        {"no": 8, "zh": "因为", "pinyin": "yīnwèi", "pos": "conj."},
        {"no": 9, "zh": "所以", "pinyin": "suǒyǐ", "pos": "conj."},
        {"no": 10, "zh": "游泳", "pinyin": "yóuyǒng", "pos": "v."},
        {"no": 11, "zh": "经常", "pinyin": "jīngcháng", "pos": "adv."},
        {"no": 12, "zh": "公斤", "pinyin": "gōngjīn", "pos": "m."},
        {"no": 13, "zh": "姐姐", "pinyin": "jiějie", "pos": "n."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在学校",
            "dialogue": [
                {"speaker": "A", "zh": "你知道小王今天什么时候来学校吗？", "pinyin": "Nǐ zhīdào Xiǎo Wáng jīntiān shénme shíhou lái xuéxiào ma?"},
                {"speaker": "B", "zh": "他已经来了。", "pinyin": "Tā yǐjīng lái le."},
                {"speaker": "A", "zh": "你怎么知道他来了？", "pinyin": "Nǐ zěnme zhīdào tā lái le?"},
                {"speaker": "B", "zh": "我在门外看见他的自行车了。", "pinyin": "Wǒ zài mén wài kànjian tā de zìxíngchē le."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在饭馆 2",
            "scene_label_zh": "在饭馆",
            "dialogue": [
                {"speaker": "A", "zh": "今天的羊肉很好吃，你怎么不吃了？", "pinyin": "Jīntiān de yángròu hěn hǎochī, nǐ zěnme bù chī le?"},
                {"speaker": "B", "zh": "这个星期我天天都吃羊肉，不想吃了。", "pinyin": "Zhège xīngqī wǒ tiāntiān dōu chī yángròu, bù xiǎng chī le."},
                {"speaker": "A", "zh": "那你想吃什么？", "pinyin": "Nà nǐ xiǎng chī shénme?"},
                {"speaker": "B", "zh": "来一点儿面条吧。", "pinyin": "Lái yìdiǎnr miàntiáo ba."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在健身房 3",
            "scene_label_zh": "在健身房",
            "dialogue": [
                {"speaker": "A", "zh": "昨天你们怎么都没去打篮球？", "pinyin": "Zuótiān nǐmen zěnme dōu méi qù dǎ lánqiú?"},
                {"speaker": "B", "zh": "因为昨天下雨，所以我们都没去。我去游泳了。", "pinyin": "Yīnwèi zuótiān xiàyǔ, suǒyǐ wǒmen dōu méi qù. Wǒ qù yóuyǒng le."},
                {"speaker": "A", "zh": "你经常游泳吗？", "pinyin": "Nǐ jīngcháng yóuyǒng ma?"},
                {"speaker": "B", "zh": "这个月我天天都游泳，我现在七十公斤了。", "pinyin": "Zhège yuè wǒ tiāntiān dōu yóuyǒng, wǒ xiànzài qīshí gōngjīn le."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在办公室 4",
            "scene_label_zh": "在办公室",
            "dialogue": [
                {"speaker": "A", "zh": "这两天怎么没看见小张？", "pinyin": "Zhè liǎng tiān zěnme méi kànjian Xiǎo Zhāng?"},
                {"speaker": "B", "zh": "他去北京了。", "pinyin": "Tā qù Běijīng le."},
                {"speaker": "A", "zh": "去北京了？是去旅游吗？", "pinyin": "Qù Běijīng le? Shì qù lǚyóu ma?"},
                {"speaker": "B", "zh": "不是，听说是去看他姐姐。", "pinyin": "Bú shì, tīngshuō shì qù kàn tā jiějie."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "疑问代词“怎么”"},
        {"no": 2, "title_zh": "量词的重叠"},
        {"no": 3, "title_zh": "关联词“因为……，所以……”"}
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
