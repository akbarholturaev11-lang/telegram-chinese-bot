import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 14,
    "lesson_code": "HSK2-L14",
    "title": "你看过那个电影吗",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "有意思", "pinyin": "yǒu yìsi", "pos": "adj."},
        {"no": 2, "zh": "但是", "pinyin": "dànshì", "pos": "conj."},
        {"no": 3, "zh": "虽然", "pinyin": "suīrán", "pos": "conj."},
        {"no": 4, "zh": "次", "pinyin": "cì", "pos": "m."},
        {"no": 5, "zh": "玩儿", "pinyin": "wánr", "pos": "v."},
        {"no": 6, "zh": "晴", "pinyin": "qíng", "pos": "adj."},
        {"no": 7, "zh": "百", "pinyin": "bǎi", "pos": "num."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在教室",
            "dialogue": [
                {"speaker": "A", "zh": "你看过那个电影没有？", "pinyin": "Nǐ kànguo nàge diànyǐng méiyǒu?"},
                {"speaker": "B", "zh": "没看过，听说很有意思。", "pinyin": "Méi kànguo, tīngshuō hěn yǒu yìsi."},
                {"speaker": "A", "zh": "那我们下个星期一一起去看吧？", "pinyin": "Nà wǒmen xià ge xīngqīyī yìqǐ qù kàn ba?"},
                {"speaker": "B", "zh": "可以，但是我女朋友也想去。", "pinyin": "Kěyǐ, dànshì wǒ nǚpéngyou yě xiǎng qù."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在办公室 2",
            "scene_label_zh": "在办公室",
            "dialogue": [
                {"speaker": "A", "zh": "听说你去过中国，还想去吗？", "pinyin": "Tīngshuō nǐ qùguo Zhōngguó, hái xiǎng qù ma?"},
                {"speaker": "B", "zh": "我虽然去过好几次，但是还想再去中国玩儿。", "pinyin": "Wǒ suīrán qùguo hǎo jǐ cì, dànshì hái xiǎng zài qù Zhōngguó wánr."},
                {"speaker": "A", "zh": "那我们一起去吧。", "pinyin": "Nà wǒmen yìqǐ qù ba."},
                {"speaker": "B", "zh": "好啊，到时候我给你打电话。", "pinyin": "Hǎo a, dào shíhou wǒ gěi nǐ dǎ diànhuà."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在房间 3",
            "scene_label_zh": "在房间",
            "dialogue": [
                {"speaker": "A", "zh": "明天天气怎么样？", "pinyin": "Míngtiān tiānqì zěnmeyàng?"},
                {"speaker": "B", "zh": "虽然是晴天，但是很冷。", "pinyin": "Suīrán shì qíngtiān, dànshì hěn lěng."},
                {"speaker": "A", "zh": "那还能够跑步吗？", "pinyin": "Nà hái nénggòu pǎobù ma?"},
                {"speaker": "B", "zh": "可以，但是你自己去吧，我还有很多事情要做。", "pinyin": "Kěyǐ, dànshì nǐ zìjǐ qù ba, wǒ hái yǒu hěn duō shìqing yào zuò."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在商店 4",
            "scene_label_zh": "在商店",
            "dialogue": [
                {"speaker": "A", "zh": "你在这个商店买过东西没有？", "pinyin": "Nǐ zài zhège shāngdiàn mǎiguo dōngxi méiyǒu?"},
                {"speaker": "B", "zh": "买过一次，这儿的东西还可以，就是有点儿便宜。", "pinyin": "Mǎiguo yí cì, zhèr de dōngxi hái kěyǐ, jiùshì bù piányi."},
                {"speaker": "A", "zh": "我喜欢这件衣服，但是觉得有点儿贵。", "pinyin": "Wǒ xǐhuan zhè jiàn yīfu, dànshì juéde yǒudiǎnr guì."},
                {"speaker": "B", "zh": "两百块还可以，喜欢就买吧。", "pinyin": "Liǎng bǎi kuài hái kěyǐ, xǐhuan jiù mǎi ba."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "动态助词“过”"},
        {"no": 2, "title_zh": "关联词“虽然……，但是……”"},
        {"no": 3, "title_zh": "动量补语“次”"}
    ], ensure_ascii=False),
    "exercise_json": json.dumps([
        {
            "order": 1,
            "type": "role_play",
            "title_zh": "分角色朗读课文",
            "prompt_zh": "分角色朗读课文。"
        },
        {
            "order": 2,
            "type": "qa_from_dialog",
            "title_zh": "根据课文内容回答问题",
            "questions": [
                {"no": 1, "zh": "他们看过那个电影吗？", "pinyin": "Tāmen kànguo nàge diànyǐng ma?"},
                {"no": 2, "zh": "他们想几个人去看电影？", "pinyin": "Tāmen xiǎng jǐ ge rén qù kàn diànyǐng?"},
                {"no": 3, "zh": "他们想去中国做什么？", "pinyin": "Tāmen xiǎng qù Zhōngguó zuò shénme?"},
                {"no": 4, "zh": "为什么她明天不能去跑步？", "pinyin": "Wèishénme tā míngtiān bù néng qù pǎobù?"},
                {"no": 5, "zh": "女的觉得这个商店的东西怎么样？", "pinyin": "Nǚ de juéde zhège shāngdiàn de dōngxi zěnmeyàng?"}
            ]
        },
        {
            "order": 3,
            "type": "describe_picture",
            "title_zh": "用本课新学的语言点和词语描述图片",
            "items": [
                {"no": 1, "zh": "你以前____过这种水果吗？", "pinyin": "Nǐ yǐqián ____ guo zhè zhǒng shuǐguǒ ma?"},
                {"no": 2, "zh": "我去年____你姐姐一次。", "pinyin": "Wǒ qùnián ____ nǐ jiějie yí cì."},
                {"no": 3, "zh": "虽然天气很冷，但是他____。", "pinyin": "Suīrán tiānqì hěn lěng, dànshì tā ____."},
                {"no": 4, "zh": "虽然英语很难，但是她____。", "pinyin": "Suīrán Yīngyǔ hěn nán, dànshì tā ____."}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "zh": "没有，一个没看过，一个也没看过。", "pinyin": "Méiyǒu, yí ge méi kànguo, yí ge yě méi kànguo."},
        {"no": 2, "zh": "三个人。", "pinyin": "Sān ge rén."},
        {"no": 3, "zh": "去中国玩儿。", "pinyin": "Qù Zhōngguó wánr."},
        {"no": 4, "zh": "因为她还有很多事情要做。", "pinyin": "Yīnwèi tā hái yǒu hěn duō shìqing yào zuò."},
        {"no": 5, "zh": "还可以，但是有点儿贵。", "pinyin": "Hái kěyǐ, dànshì yǒudiǎnr guì."}
    ], ensure_ascii=False),
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
