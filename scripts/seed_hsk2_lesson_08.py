import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 8,
    "lesson_code": "HSK2-L08",
    "title": "让我想想再告诉你",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "再", "pinyin": "zài", "pos": "adv."},
        {"no": 2, "zh": "让", "pinyin": "ràng", "pos": "v."},
        {"no": 3, "zh": "告诉", "pinyin": "gàosu", "pos": "v."},
        {"no": 4, "zh": "等", "pinyin": "děng", "pos": "v."},
        {"no": 5, "zh": "找", "pinyin": "zhǎo", "pos": "v."},
        {"no": 6, "zh": "事情", "pinyin": "shìqing", "pos": "n."},
        {"no": 7, "zh": "服务员", "pinyin": "fúwùyuán", "pos": "n."},
        {"no": 8, "zh": "白", "pinyin": "bái", "pos": "adj."},
        {"no": 9, "zh": "黑", "pinyin": "hēi", "pos": "adj."},
        {"no": 10, "zh": "贵", "pinyin": "guì", "pos": "adj."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在教室",
            "dialogue": [
                {"speaker": "A", "zh": "我们下午去看电影，好吗？", "pinyin": "Wǒmen xiàwǔ qù kàn diànyǐng, hǎo ma?"},
                {"speaker": "B", "zh": "今天下午我没有时间，明天下午再去吧。", "pinyin": "Jīntiān xiàwǔ wǒ méiyǒu shíjiān, míngtiān xiàwǔ zài qù ba."},
                {"speaker": "A", "zh": "你想看什么电影？", "pinyin": "Nǐ xiǎng kàn shénme diànyǐng?"},
                {"speaker": "B", "zh": "让我想想再告诉你。", "pinyin": "Ràng wǒ xiǎngxiang zài gàosu nǐ."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在宿舍 2",
            "scene_label_zh": "在宿舍",
            "dialogue": [
                {"speaker": "A", "zh": "外边天气很好，我们出去运动运动吧！", "pinyin": "Wàibian tiānqì hěn hǎo, wǒmen chūqù yùndòng yùndòng ba!"},
                {"speaker": "B", "zh": "你等等我，好吗？王老师让我给大卫打个电话。", "pinyin": "Nǐ děngdeng wǒ, hǎo ma? Wáng lǎoshī ràng wǒ gěi Dàwèi dǎ ge diànhuà."},
                {"speaker": "A", "zh": "回来再打吧。找大卫有什么事情吗？", "pinyin": "Huílái zài dǎ ba. Zhǎo Dàwèi yǒu shénme shìqing ma?"},
                {"speaker": "B", "zh": "听说大卫病了，我想找时间去看看他。", "pinyin": "Tīngshuō Dàwèi bìng le, wǒ xiǎng zhǎo shíjiān qù kànkan tā."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在宾馆的前台 3",
            "scene_label_zh": "在宾馆的前台",
            "dialogue": [
                {"speaker": "A", "zh": "服务员，我房间的门打不开了。", "pinyin": "Fúwùyuán, wǒ fángjiān de mén dǎ bù kāi le."},
                {"speaker": "B", "zh": "您住哪个房间？", "pinyin": "Nín zhù nǎ ge fángjiān?"},
                {"speaker": "A", "zh": "317。", "pinyin": "Sān yāo qī."},
                {"speaker": "B", "zh": "好的，我叫人去看看。", "pinyin": "Hǎo de, wǒ jiào rén qù kànkan."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在商店 4",
            "scene_label_zh": "在商店",
            "dialogue": [
                {"speaker": "A", "zh": "你看看这几件衣服怎么样。", "pinyin": "Nǐ kànkan zhè jǐ jiàn yīfu zěnmeyàng."},
                {"speaker": "B", "zh": "这件白的有点儿长，那件黑的有点儿贵。", "pinyin": "Zhè jiàn bái de yǒudiǎnr cháng, nà jiàn hēi de yǒudiǎnr guì."},
                {"speaker": "A", "zh": "这件红的呢？这是今天新来的。", "pinyin": "Zhè jiàn hóng de ne? Zhè shì jīntiān xīn lái de."},
                {"speaker": "B", "zh": "让我再看看。", "pinyin": "Ràng wǒ zài kànkan."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "疑问句“……，好吗”"},
        {"no": 2, "title_zh": "副词“再”"},
        {"no": 3, "title_zh": "兼语句"},
        {"no": 4, "title_zh": "动词的重叠"}
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
