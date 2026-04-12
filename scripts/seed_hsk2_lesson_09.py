import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 9,
    "lesson_code": "HSK2-L09",
    "title": "题太多，我没做完",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "错", "pinyin": "cuò", "pos": "adj."},
        {"no": 2, "zh": "从", "pinyin": "cóng", "pos": "prep."},
        {"no": 3, "zh": "跳舞", "pinyin": "tiàowǔ", "pos": "v."},
        {"no": 4, "zh": "第一", "pinyin": "dìyī", "pos": "num."},
        {"no": 5, "zh": "希望", "pinyin": "xīwàng", "pos": "v."},
        {"no": 6, "zh": "问题", "pinyin": "wèntí", "pos": "n."},
        {"no": 7, "zh": "欢迎", "pinyin": "huānyíng", "pos": "v."},
        {"no": 8, "zh": "上班", "pinyin": "shàngbān", "pos": "v."},
        {"no": 9, "zh": "懂", "pinyin": "dǒng", "pos": "v."},
        {"no": 10, "zh": "完", "pinyin": "wán", "pos": "v."},
        {"no": 11, "zh": "题", "pinyin": "tí", "pos": "n."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "打电话",
            "dialogue": [
                {"speaker": "A", "zh": "你好！请问张欢在吗？", "pinyin": "Nǐ hǎo! Qǐngwèn Zhāng Huān zài ma?"},
                {"speaker": "B", "zh": "你打错了，我们这儿没有叫张欢的。", "pinyin": "Nǐ dǎ cuò le, wǒmen zhèr méiyǒu jiào Zhāng Huān de."},
                {"speaker": "A", "zh": "对不起。", "pinyin": "Duìbuqǐ."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在学校 2",
            "scene_label_zh": "在学校",
            "dialogue": [
                {"speaker": "A", "zh": "您从几岁开始学跳舞？", "pinyin": "Nín cóng jǐ suì kāishǐ xué tiàowǔ?"},
                {"speaker": "B", "zh": "我第一次跳舞是在七岁的时候。", "pinyin": "Wǒ dì yī cì tiàowǔ shì zài qī suì de shíhou."},
                {"speaker": "A", "zh": "我女儿今年七岁了。我希望她能跟您学跳舞，可以吗？", "pinyin": "Wǒ nǚ'ér jīnnián qī suì le. Wǒ xīwàng tā néng gēn nín xué tiàowǔ, kěyǐ ma?"},
                {"speaker": "B", "zh": "没问题，非常欢迎。", "pinyin": "Méi wèntí, fēicháng huānyíng."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在家里 3",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "你知道吗？大卫找到工作了。", "pinyin": "Nǐ zhīdào ma? Dàwèi zhǎodào gōngzuò le."},
                {"speaker": "B", "zh": "太好了！他从什么时候开始上班？", "pinyin": "Tài hǎo le! Tā cóng shénme shíhou kāishǐ shàngbān?"},
                {"speaker": "A", "zh": "从下个星期一开始。", "pinyin": "Cóng xià ge xīngqīyī kāishǐ."},
                {"speaker": "B", "zh": "这是他的第一个工作，希望他能喜欢。", "pinyin": "Zhè shì tā de dì yī ge gōngzuò, xīwàng tā néng xǐhuan."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在教室 4",
            "scene_label_zh": "在教室",
            "dialogue": [
                {"speaker": "A", "zh": "昨天的考试怎么样？你都听懂了吗？", "pinyin": "Zuótiān de kǎoshì zěnmeyàng? Nǐ dōu tīngdǒng le ma?"},
                {"speaker": "B", "zh": "听懂了。", "pinyin": "Tīngdǒng le."},
                {"speaker": "A", "zh": "你都做完了没有？", "pinyin": "Nǐ dōu zuòwán le méiyǒu?"},
                {"speaker": "B", "zh": "题太多，我没做完。", "pinyin": "Tí tài duō, wǒ méi zuòwán."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "结果补语"},
        {"no": 2, "title_zh": "介词“从”"},
        {"no": 3, "title_zh": "“第”表示顺序"}
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
                {"no": 1, "zh": "老师从几岁开始学跳舞？", "pinyin": "Lǎoshī cóng jǐ suì kāishǐ xué tiàowǔ?"},
                {"no": 2, "zh": "老师想教她的女儿跳舞吗？", "pinyin": "Lǎoshī xiǎng jiāo tā de nǚ'ér tiàowǔ ma?"},
                {"no": 3, "zh": "大卫什么时候去工作？", "pinyin": "Dàwèi shénme shíhou qù gōngzuò?"},
                {"no": 4, "zh": "这次考试她都听懂了吗？", "pinyin": "Zhè cì kǎoshì tā dōu tīngdǒng le ma?"},
                {"no": 5, "zh": "她考试为什么没做完？", "pinyin": "Tā kǎoshì wèishénme méi zuòwán?"}
            ]
        },
        {
            "order": 3,
            "type": "describe_picture",
            "title_zh": "用本课新学的语言点和词语描述图片",
            "items": [
                {"no": 1, "zh": "衣服你洗了没有？", "pinyin": "Yīfu nǐ xǐ le méiyǒu?"},
                {"no": 2, "zh": "作业太多了，我还没做完。", "pinyin": "Zuòyè tài duō le, wǒ hái méi zuòwán."},
                {"no": 3, "zh": "从八点到十二点，她们都在上班。", "pinyin": "Cóng bā diǎn dào shí'èr diǎn, tāmen dōu zài shàngbān."},
                {"no": 4, "zh": "我第一次去北京。", "pinyin": "Wǒ dì yī cì qù Běijīng."}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "zh": "老师从七岁开始学跳舞。", "pinyin": "Lǎoshī cóng qī suì kāishǐ xué tiàowǔ."},
        {"no": 2, "zh": "想。", "pinyin": "Xiǎng."},
        {"no": 3, "zh": "从下个星期一开始。", "pinyin": "Cóng xià ge xīngqīyī kāishǐ."},
        {"no": 4, "zh": "都听懂了。", "pinyin": "Dōu tīngdǒng le."},
        {"no": 5, "zh": "因为题太多。", "pinyin": "Yīnwèi tí tài duō."}
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
