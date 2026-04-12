import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 11,
    "lesson_code": "HSK2-L11",
    "title": "他比我大三岁",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "唱歌", "pinyin": "chànggē", "pos": "v."},
        {"no": 2, "zh": "男", "pinyin": "nán", "pos": "adj."},
        {"no": 3, "zh": "女", "pinyin": "nǚ", "pos": "adj."},
        {"no": 4, "zh": "孩子", "pinyin": "háizi", "pos": "n."},
        {"no": 5, "zh": "右边", "pinyin": "yòubian", "pos": "n."},
        {"no": 6, "zh": "比", "pinyin": "bǐ", "pos": "prep."},
        {"no": 7, "zh": "便宜", "pinyin": "piányi", "pos": "adj."},
        {"no": 8, "zh": "说话", "pinyin": "shuōhuà", "pos": "v."},
        {"no": 9, "zh": "可能", "pinyin": "kěnéng", "pos": "aux."},
        {"no": 10, "zh": "去年", "pinyin": "qùnián", "pos": "n."},
        {"no": 11, "zh": "姓", "pinyin": "xìng", "pos": "v."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在歌厅",
            "dialogue": [
                {"speaker": "A", "zh": "王方，昨天和你一起唱歌的人是谁？", "pinyin": "Wáng Fāng, zuótiān hé nǐ yìqǐ chànggē de rén shì shéi?"},
                {"speaker": "B", "zh": "一个朋友。", "pinyin": "Yí ge péngyou."},
                {"speaker": "A", "zh": "什么朋友？是不是男朋友？", "pinyin": "Shénme péngyou? Shì bú shì nán péngyou?"},
                {"speaker": "B", "zh": "不是不是，我同学介绍的，昨天第一次见。", "pinyin": "Bú shì bú shì, wǒ tóngxué jièshào de, zuótiān dì yī cì jiàn."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在宿舍 2",
            "scene_label_zh": "在宿舍",
            "dialogue": [
                {"speaker": "A", "zh": "左边这个看报纸的女孩子是你姐姐吗？", "pinyin": "Zuǒbian zhège kàn bàozhǐ de nǚ háizi shì nǐ jiějie ma?"},
                {"speaker": "B", "zh": "是，右边写字的那个人是我哥哥。", "pinyin": "Shì, yòubian xiě zì de nà ge rén shì wǒ gēge."},
                {"speaker": "A", "zh": "你哥哥多大？", "pinyin": "Nǐ gēge duō dà?"},
                {"speaker": "B", "zh": "25岁，他比我大三岁。", "pinyin": "Èrshíwǔ suì, tā bǐ wǒ dà sān suì."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在商店 3",
            "scene_label_zh": "在商店",
            "dialogue": [
                {"speaker": "A", "zh": "今天的西瓜怎么卖？", "pinyin": "Jīntiān de xīguā zěnme mài?"},
                {"speaker": "B", "zh": "三块五一斤。", "pinyin": "Sān kuài wǔ yì jīn."},
                {"speaker": "A", "zh": "比昨天便宜。", "pinyin": "Bǐ zuótiān piányi."},
                {"speaker": "B", "zh": "是，苹果也比昨天便宜一些。您来点儿吧。", "pinyin": "Shì, píngguǒ yě bǐ zuótiān piányi yìxiē. Nín lái diǎnr ba."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在学校 4",
            "scene_label_zh": "在学校",
            "dialogue": [
                {"speaker": "A", "zh": "前边说话的那个人是不是我的汉语老师？你可能不认识她。", "pinyin": "Qiánbian shuōhuà de nà ge rén shì bú shì wǒ de Hànyǔ lǎoshī? Nǐ kěnéng bù rènshi tā."},
                {"speaker": "B", "zh": "是新来的汉语老师吗？", "pinyin": "Shì xīn lái de Hànyǔ lǎoshī ma?"},
                {"speaker": "A", "zh": "是去年来自的，她姓王，28岁。", "pinyin": "Shì qùnián lái de, tā xìng Wáng, èrshíbā suì."},
                {"speaker": "B", "zh": "她比我们老师小两岁。", "pinyin": "Tā bǐ wǒmen lǎoshī xiǎo liǎng suì."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "动词结构做定语"},
        {"no": 2, "title_zh": "“比”字句（1）"},
        {"no": 3, "title_zh": "助动词“可能”"}
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
                {"no": 1, "zh": "昨天和王方一起唱歌的人是谁？", "pinyin": "Zuótiān hé Wáng Fāng yìqǐ chànggē de rén shì shéi?"},
                {"no": 2, "zh": "左边看报纸的女孩子是谁？", "pinyin": "Zuǒbian kàn bàozhǐ de nǚ háizi shì shéi?"},
                {"no": 3, "zh": "她的哥哥25岁了，她多大了？", "pinyin": "Tā de gēge èrshíwǔ suì le, tā duō dà le?"},
                {"no": 4, "zh": "昨天的西瓜可能卖多少钱？", "pinyin": "Zuótiān de xīguā kěnéng mài duōshao qián?"},
                {"no": 5, "zh": "王老师是新老师吗？", "pinyin": "Wáng lǎoshī shì xīn lǎoshī ma?"}
            ]
        },
        {
            "order": 3,
            "type": "describe_picture",
            "title_zh": "用本课新学的语言点和词语描述图片",
            "items": [
                {"no": 1, "zh": "绿苹果比红苹果____。", "pinyin": "Lǜ píngguǒ bǐ hóng píngguǒ ____."},
                {"no": 2, "zh": "姐姐比我____。", "pinyin": "Jiějie bǐ wǒ ____."},
                {"no": 3, "zh": "昨天35°，今天没有____。", "pinyin": "Zuótiān sānshíwǔ dù, jīntiān méiyǒu ____."},
                {"no": 4, "zh": "哥哥学习很好，我没有____。", "pinyin": "Gēge xuéxí hěn hǎo, wǒ méiyǒu ____."}
            ]
        },
        {
            "order": 4,
            "type": "pair_work",
            "title_zh": "用“比”字句练习说句子",
            "items": [
                {"no": 1, "zh": "西瓜比苹果大。", "pinyin": "Xīguā bǐ píngguǒ dà."},
                {"no": 2, "zh": "苹果没有西瓜大。", "pinyin": "Píngguǒ méiyǒu xīguā dà."}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "zh": "一个朋友。", "pinyin": "Yí ge péngyou."},
        {"no": 2, "zh": "是她姐姐。", "pinyin": "Shì tā jiějie."},
        {"no": 3, "zh": "22岁。", "pinyin": "Èrshí'èr suì."},
        {"no": 4, "zh": "可能三块多。", "pinyin": "Kěnéng sān kuài duō."},
        {"no": 5, "zh": "是。", "pinyin": "Shì."}
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
