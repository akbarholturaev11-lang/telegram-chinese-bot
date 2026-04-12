import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 5,
    "lesson_code": "HSK2-L05",
    "title": "就买这件吧",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "外面", "pinyin": "wàimiàn", "pos": "n."},
        {"no": 2, "zh": "准备", "pinyin": "zhǔnbèi", "pos": "v."},
        {"no": 3, "zh": "就", "pinyin": "jiù", "pos": "adv."},
        {"no": 4, "zh": "鱼", "pinyin": "yú", "pos": "n."},
        {"no": 5, "zh": "吧", "pinyin": "ba", "pos": "part."},
        {"no": 6, "zh": "件", "pinyin": "jiàn", "pos": "m."},
        {"no": 7, "zh": "还", "pinyin": "hái", "pos": "adv."},
        {"no": 8, "zh": "可以", "pinyin": "kěyǐ", "pos": "adj."},
        {"no": 9, "zh": "不错", "pinyin": "búcuò", "pos": "adj."},
        {"no": 10, "zh": "考试", "pinyin": "kǎoshì", "pos": "n."},
        {"no": 11, "zh": "意思", "pinyin": "yìsi", "pos": "n."},
        {"no": 12, "zh": "咖啡", "pinyin": "kāfēi", "pos": "n."},
        {"no": 13, "zh": "对", "pinyin": "duì", "pos": "prep."},
        {"no": 14, "zh": "以后", "pinyin": "yǐhòu", "pos": "n."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "晚上我们去饭馆吃饭，怎么样？", "pinyin": "Wǎnshang wǒmen qù fànguǎn chīfàn, zěnmeyàng?"},
                {"speaker": "B", "zh": "我不想去外面吃，我想在家吃。", "pinyin": "Wǒ bù xiǎng qù wàimiàn chī, wǒ xiǎng zài jiā chī."},
                {"speaker": "A", "zh": "那你准备做什么呢？", "pinyin": "Nà nǐ zhǔnbèi zuò shénme ne?"},
                {"speaker": "B", "zh": "就做你爱吃的鱼吧。", "pinyin": "Jiù zuò nǐ ài chī de yú ba."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在商店 2",
            "scene_label_zh": "在商店",
            "dialogue": [
                {"speaker": "A", "zh": "帮我看一下这件衣服怎么样。", "pinyin": "Bāng wǒ kàn yíxià zhè jiàn yīfu zěnmeyàng."},
                {"speaker": "B", "zh": "颜色还可以，就是有点儿大。", "pinyin": "Yánsè hái kěyǐ, jiùshì yǒudiǎnr dà."},
                {"speaker": "A", "zh": "这件小的怎么样？", "pinyin": "Zhè jiàn xiǎo de zěnmeyàng?"},
                {"speaker": "B", "zh": "这件不错，就买这件吧。", "pinyin": "Zhè jiàn búcuò, jiù mǎi zhè jiàn ba."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在教室 3",
            "scene_label_zh": "在教室",
            "dialogue": [
                {"speaker": "A", "zh": "今天去不去打球？", "pinyin": "Jīntiān qù bú qù dǎ qiú?"},
                {"speaker": "B", "zh": "这两天有点儿累，不去打球了。", "pinyin": "Zhè liǎng tiān yǒudiǎnr lèi, bù qù dǎ qiú le."},
                {"speaker": "A", "zh": "你在做什么呢？是在想昨天的考试吗？", "pinyin": "Nǐ zài zuò shénme ne? Shì zài xiǎng zuótiān de kǎoshì ma?"},
                {"speaker": "B", "zh": "是啊，我觉得听和说还可以，读和写不好，很多字我都不知道是什么意思。", "pinyin": "Shì a, wǒ juéde tīng hé shuō hái kěyǐ, dú hé xiě bù hǎo, hěn duō zì wǒ dōu bù zhīdào shì shénme yìsi."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在公司 4",
            "scene_label_zh": "在公司",
            "dialogue": [
                {"speaker": "A", "zh": "休息一下吧，喝咖啡吗？", "pinyin": "Xiūxi yíxià ba, hē kāfēi ma?"},
                {"speaker": "B", "zh": "不喝了，我已经喝两杯了。", "pinyin": "Bù hē le, wǒ yǐjīng hē liǎng bēi le."},
                {"speaker": "A", "zh": "是啊，咖啡喝多了对身体不好。", "pinyin": "Shì a, kāfēi hē duō le duì shēntǐ bù hǎo."},
                {"speaker": "B", "zh": "以后我少喝一点儿，每天喝一杯。", "pinyin": "Yǐhòu wǒ shǎo hē yìdiǎnr, měitiān hē yì bēi."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "副词“就”"},
        {"no": 2, "title_zh": "语气副词“还”（1）"},
        {"no": 3, "title_zh": "程度副词“有点儿”"}
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
