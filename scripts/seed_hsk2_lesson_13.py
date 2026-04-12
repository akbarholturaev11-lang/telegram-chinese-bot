import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 13,
    "lesson_code": "HSK2-L13",
    "title": "门开着呢",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "着", "pinyin": "zhe", "pos": "part."},
        {"no": 2, "zh": "手", "pinyin": "shǒu", "pos": "n."},
        {"no": 3, "zh": "拿", "pinyin": "ná", "pos": "v."},
        {"no": 4, "zh": "铅笔", "pinyin": "qiānbǐ", "pos": "n."},
        {"no": 5, "zh": "班", "pinyin": "bān", "pos": "n."},
        {"no": 6, "zh": "长", "pinyin": "zhǎng", "pos": "v./adj."},
        {"no": 7, "zh": "笑", "pinyin": "xiào", "pos": "v."},
        {"no": 8, "zh": "宾馆", "pinyin": "bīnguǎn", "pos": "n."},
        {"no": 9, "zh": "一直", "pinyin": "yìzhí", "pos": "adv."},
        {"no": 10, "zh": "往", "pinyin": "wǎng", "pos": "prep."},
        {"no": 11, "zh": "路口", "pinyin": "lùkǒu", "pos": "n."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在办公室",
            "dialogue": [
                {"speaker": "A", "zh": "门开着呢，请进。", "pinyin": "Mén kāi zhe ne, qǐng jìn."},
                {"speaker": "B", "zh": "请问，张先生在吗？", "pinyin": "Qǐngwèn, Zhāng xiānsheng zài ma?"},
                {"speaker": "A", "zh": "他出去了。你下午再来吧。", "pinyin": "Tā chūqù le. Nǐ xiàwǔ zài lái ba."},
                {"speaker": "B", "zh": "好的，谢谢！", "pinyin": "Hǎo de, xièxie!"}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在办公室 2",
            "scene_label_zh": "在办公室",
            "dialogue": [
                {"speaker": "A", "zh": "那个正在说话的女孩子是谁？", "pinyin": "Nàge zhèngzài shuōhuà de nǚ háizi shì shéi?"},
                {"speaker": "B", "zh": "我知道她的名字，她姓杨，叫杨笑笑。她姐姐是我同学。", "pinyin": "Wǒ zhīdào tā de míngzi, tā xìng Yáng, jiào Yáng Xiàoxiào. Tā jiějie shì wǒ tóngxué."},
                {"speaker": "A", "zh": "那个手里拿着铅笔的呢？", "pinyin": "Nàge shǒu lǐ ná zhe qiānbǐ de ne?"},
                {"speaker": "B", "zh": "我不认识。", "pinyin": "Wǒ bù rènshi."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在运动场 3",
            "scene_label_zh": "在运动场",
            "dialogue": [
                {"speaker": "A", "zh": "听说你有女朋友了？我认识她吗？", "pinyin": "Tīngshuō nǐ yǒu nǚpéngyou le? Wǒ rènshi tā ma?"},
                {"speaker": "B", "zh": "就是我们班那个长着两个大眼睛，非常爱笑的女孩子。", "pinyin": "Jiù shì wǒmen bān nàge zhǎng zhe liǎng ge dà yǎnjing, fēicháng ài xiào de nǚ háizi."},
                {"speaker": "A", "zh": "她不是有男朋友了吗？", "pinyin": "Tā bú shì yǒu nánpéngyou le ma?"},
                {"speaker": "B", "zh": "那个已经是她的前男友了。", "pinyin": "Nàge yǐjīng shì tā de qián nányǒu le."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在路上 4",
            "scene_label_zh": "在路上",
            "dialogue": [
                {"speaker": "A", "zh": "请问，这儿离新京宾馆远吗？", "pinyin": "Qǐngwèn, zhèr lí Xīnjīng Bīnguǎn yuǎn ma?"},
                {"speaker": "B", "zh": "不远，走二十分钟就到了。", "pinyin": "Bù yuǎn, zǒu èrshí fēnzhōng jiù dào le."},
                {"speaker": "A", "zh": "你能告诉我怎么走吗？", "pinyin": "Nǐ néng gàosu wǒ zěnme zǒu ma?"},
                {"speaker": "B", "zh": "从这儿一直往前走，到了前面的路口再往右走。", "pinyin": "Cóng zhèr yìzhí wǎng qián zǒu, dào le qiánmian de lùkǒu zài wǎng yòu zǒu."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "动态助词“着”"},
        {"no": 2, "title_zh": "反问句“不是……吗”"},
        {"no": 3, "title_zh": "介词“往”"}
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
                {"no": 1, "zh": "张先生去哪儿了？", "pinyin": "Zhāng xiānsheng qù nǎr le?"},
                {"no": 2, "zh": "杨笑笑是谁？", "pinyin": "Yáng Xiàoxiào shì shéi?"},
                {"no": 3, "zh": "他的女朋友是谁？", "pinyin": "Tā de nǚpéngyou shì shéi?"},
                {"no": 4, "zh": "“前男友”是什么意思？", "pinyin": "“Qián nányǒu” shì shénme yìsi?"},
                {"no": 5, "zh": "去新京宾馆怎么走？", "pinyin": "Qù Xīnjīng Bīnguǎn zěnme zǒu?"}
            ]
        },
        {
            "order": 3,
            "type": "describe_picture",
            "title_zh": "用本课新学的语言点和词语描述图片",
            "items": [
                {"no": 1, "zh": "他________。（拿）", "pinyin": "Tā ________ . (ná)"},
                {"no": 2, "zh": "他________。（穿）", "pinyin": "Tā ________ . (chuān)"},
                {"no": 3, "zh": "电视________。（开）", "pinyin": "Diànshì ________ . (kāi)"},
                {"no": 4, "zh": "他________呢。（开）", "pinyin": "Tā ________ ne. (kāi)"}
            ]
        },
        {
            "order": 4,
            "type": "pair_work",
            "title_zh": "用“往……”练习说句子",
            "items": [
                {"no": 1, "zh": "往前走。", "pinyin": "Wǎng qián zǒu."},
                {"no": 2, "zh": "往后跑。", "pinyin": "Wǎng hòu pǎo."},
                {"no": 3, "zh": "往左看。", "pinyin": "Wǎng zuǒ kàn."},
                {"no": 4, "zh": "往右走。", "pinyin": "Wǎng yòu zǒu."}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "zh": "他出去了。", "pinyin": "Tā chūqù le."},
        {"no": 2, "zh": "她是他同学的妹妹。", "pinyin": "Tā shì tā tóngxué de mèimei."},
        {"no": 3, "zh": "是他们班那个长着两个大眼睛、非常爱笑的女孩子。", "pinyin": "Shì tāmen bān nàge zhǎng zhe liǎng ge dà yǎnjing, fēicháng ài xiào de nǚ háizi."},
        {"no": 4, "zh": "就是以前的男朋友。", "pinyin": "Jiù shì yǐqián de nánpéngyou."},
        {"no": 5, "zh": "从这儿一直往前走，到了前面的路口再往右走。", "pinyin": "Cóng zhèr yìzhí wǎng qián zǒu, dào le qiánmian de lùkǒu zài wǎng yòu zǒu."}
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
