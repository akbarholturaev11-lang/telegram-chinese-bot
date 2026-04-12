import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 12,
    "lesson_code": "HSK2-L12",
    "title": "你穿得太少了",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "得", "pinyin": "de", "pos": "part."},
        {"no": 2, "zh": "妻子", "pinyin": "qīzi", "pos": "n."},
        {"no": 3, "zh": "雪", "pinyin": "xuě", "pos": "n."},
        {"no": 4, "zh": "零", "pinyin": "líng", "pos": "num."},
        {"no": 5, "zh": "度", "pinyin": "dù", "pos": "n./m."},
        {"no": 6, "zh": "穿", "pinyin": "chuān", "pos": "v."},
        {"no": 7, "zh": "进", "pinyin": "jìn", "pos": "v."},
        {"no": 8, "zh": "弟弟", "pinyin": "dìdi", "pos": "n."},
        {"no": 9, "zh": "近", "pinyin": "jìn", "pos": "adj."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在教室",
            "dialogue": [
                {"speaker": "A", "zh": "你每天早上几点起床？", "pinyin": "Nǐ měitiān zǎoshang jǐ diǎn qǐchuáng?"},
                {"speaker": "B", "zh": "六点多。", "pinyin": "Liù diǎn duō."},
                {"speaker": "A", "zh": "你比我早起一个小时。", "pinyin": "Nǐ bǐ wǒ zǎo qǐ yí ge xiǎoshí."},
                {"speaker": "B", "zh": "我睡得也早，我每天晚上十点就睡觉。早睡早起对身体好。", "pinyin": "Wǒ shuì de yě zǎo, wǒ měitiān wǎnshang shí diǎn jiù shuìjiào. Zǎo shuì zǎo qǐ duì shēntǐ hǎo."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在朋友家 2",
            "scene_label_zh": "在朋友家",
            "dialogue": [
                {"speaker": "A", "zh": "再来点儿米饭吧，你吃得太少了。", "pinyin": "Zài lái diǎnr mǐfàn ba, nǐ chī de tài shǎo le."},
                {"speaker": "B", "zh": "不心了，今天吃得很好，太谢谢你了。", "pinyin": "Bù xīn le, jīntiān chī de hěn hǎo, tài xièxie nǐ le."},
                {"speaker": "A", "zh": "你饭做得怎么样？", "pinyin": "Nǐ fàn zuò de zěnmeyàng?"},
                {"speaker": "B", "zh": "不怎么样，我妻子比我饭做得好。", "pinyin": "Bù zěnmeyàng, wǒ qīzi bǐ wǒ zuò fàn zuò de hǎo."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在家门口 3",
            "scene_label_zh": "在家门口",
            "dialogue": [
                {"speaker": "A", "zh": "下雪了，今天真冷。", "pinyin": "Xià xuě le, jīntiān zhēn lěng."},
                {"speaker": "B", "zh": "有零下10度吧？", "pinyin": "Yǒu líng xià shí dù ba?"},
                {"speaker": "A", "zh": "是啊，你穿得太少了，我们进房间吧。", "pinyin": "Shì a, nǐ chuān de tài shǎo le, wǒmen jìn fángjiān ba."},
                {"speaker": "B", "zh": "好吧。", "pinyin": "Hǎo ba."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在家里 4",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "你在忙什么呢？", "pinyin": "Nǐ zài máng shénme ne?"},
                {"speaker": "B", "zh": "我弟弟让我帮他找个房子，现在他离公司有点儿远。", "pinyin": "Wǒ dìdi ràng wǒ bāng tā zhǎo ge fángzi, xiànzài tā lí gōngsī yǒudiǎnr yuǎn."},
                {"speaker": "A", "zh": "住得远真的很累！", "pinyin": "Zhù de yuǎn zhēn de hěn lèi!"},
                {"speaker": "B", "zh": "是啊，他也希望能住得近一点儿。", "pinyin": "Shì a, tā yě xīwàng néng zhù de jìn yìdiǎnr."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "状态补语"},
        {"no": 2, "title_zh": "“比”字句（2）"}
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
                {"no": 1, "zh": "她为什么每天晚上十点就睡觉？", "pinyin": "Tā wèishénme měitiān wǎnshang shí diǎn jiù shuìjiào?"},
                {"no": 2, "zh": "他们家谁做饭做得好？", "pinyin": "Tāmen jiā shéi zuò fàn zuò de hǎo?"},
                {"no": 3, "zh": "今天天气怎么样？", "pinyin": "Jīntiān tiānqì zěnmeyàng?"},
                {"no": 4, "zh": "她这两天在忙什么呢？", "pinyin": "Tā zhè liǎng tiān zài máng shénme ne?"},
                {"no": 5, "zh": "她弟弟为什么要找新的房子？", "pinyin": "Tā dìdi wèishénme yào zhǎo xīn de fángzi?"}
            ]
        },
        {
            "order": 3,
            "type": "describe_picture",
            "title_zh": "用本课新学的语言点和词语描述图片",
            "items": [
                {"no": 1, "zh": "她唱得________。", "pinyin": "Tā chàng de ________."},
                {"no": 2, "zh": "爸爸开车开得________。", "pinyin": "Bàba kāichē kāi de ________."},
                {"no": 3, "zh": "哥哥比我吃得________。", "pinyin": "Gēge bǐ wǒ chī de ________."},
                {"no": 4, "zh": "爸爸比妈妈做饭做得________。", "pinyin": "Bàba bǐ māma zuò fàn zuò de ________."}
            ]
        },
        {
            "order": 4,
            "type": "pair_work",
            "title_zh": "用状态补语练习说句子",
            "items": [
                {"no": 1, "zh": "他跑得很快。", "pinyin": "Tā pǎo de hěn kuài."},
                {"no": 2, "zh": "我跑得不快。", "pinyin": "Wǒ pǎo de bù kuài."}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "zh": "因为早睡早起对身体好。", "pinyin": "Yīnwèi zǎo shuì zǎo qǐ duì shēntǐ hǎo."},
        {"no": 2, "zh": "他妻子做饭做得好。", "pinyin": "Tā qīzi zuò fàn zuò de hǎo."},
        {"no": 3, "zh": "今天很冷，下雪了。", "pinyin": "Jīntiān hěn lěng, xià xuě le."},
        {"no": 4, "zh": "她在帮弟弟找房子。", "pinyin": "Tā zài bāng dìdi zhǎo fángzi."},
        {"no": 5, "zh": "因为他现在离公司有点儿远。", "pinyin": "Yīnwèi tā xiànzài lí gōngsī yǒudiǎnr yuǎn."}
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
