import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 15,
    "lesson_code": "HSK2-L15",
    "title": "新年就要到了",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "日", "pinyin": "rì", "pos": "n."},
        {"no": 2, "zh": "新年", "pinyin": "xīnnián", "pos": "n."},
        {"no": 3, "zh": "票", "pinyin": "piào", "pos": "n."},
        {"no": 4, "zh": "火车站", "pinyin": "huǒchēzhàn", "pos": "n."},
        {"no": 5, "zh": "大家", "pinyin": "dàjiā", "pos": "pron."},
        {"no": 6, "zh": "更", "pinyin": "gèng", "pos": "adv."},
        {"no": 7, "zh": "妹妹", "pinyin": "mèimei", "pos": "n."},
        {"no": 8, "zh": "阴", "pinyin": "yīn", "pos": "adj."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在朋友家",
            "dialogue": [
                {"speaker": "A", "zh": "今天是12月20日，新年就要到了。", "pinyin": "Jīntiān shì shí'èr yuè èrshí rì, xīnnián jiù yào dào le."},
                {"speaker": "B", "zh": "新年你准备做什么？", "pinyin": "Xīnnián nǐ zhǔnbèi zuò shénme?"},
                {"speaker": "A", "zh": "我想去北京旅游，北京很不错，我去过一次。", "pinyin": "Wǒ xiǎng qù Běijīng lǚyóu, Běijīng hěn búcuò, wǒ qùguo yí cì."},
                {"speaker": "B", "zh": "你买票了吗？", "pinyin": "Nǐ mǎi piào le ma?"},
                {"speaker": "A", "zh": "还没有呢，明天就去火车站买票。", "pinyin": "Hái méiyǒu ne, míngtiān jiù qù huǒchēzhàn mǎi piào."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在公司 2",
            "scene_label_zh": "在公司",
            "dialogue": [
                {"speaker": "A", "zh": "时间过得真快，新的一年快要到了！", "pinyin": "Shíjiān guò de zhēn kuài, xīn de yì nián kuài yào dào le!"},
                {"speaker": "B", "zh": "是啊，谢谢大家这一年对我的帮助！", "pinyin": "Shì a, xièxie dàjiā zhè yì nián duì wǒ de bāngzhù!"},
                {"speaker": "C", "zh": "希望我们的公司明年更好！", "pinyin": "Xīwàng wǒmen de gōngsī míngnián gèng hǎo!"}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在车站 3",
            "scene_label_zh": "在车站",
            "dialogue": [
                {"speaker": "A", "zh": "你妹妹怎么还没来？都八点四十了！", "pinyin": "Nǐ mèimei zěnme hái méi lái? Dōu bā diǎn sìshí le!"},
                {"speaker": "B", "zh": "我们再等她几分钟吧。", "pinyin": "Wǒmen zài děng tā jǐ fēnzhōng ba."},
                {"speaker": "A", "zh": "都等她半个小时了！", "pinyin": "Dōu děng tā bàn ge xiǎoshí le!"},
                {"speaker": "B", "zh": "她来了，我听见她说话了。", "pinyin": "Tā lái le, wǒ tīngjiàn tā shuōhuà le."}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在咖啡馆门口 4",
            "scene_label_zh": "在咖啡馆门口",
            "dialogue": [
                {"speaker": "A", "zh": "天阴了，我要回去了。", "pinyin": "Tiān yīn le, wǒ yào huíqù le."},
                {"speaker": "B", "zh": "好的，快要下雨了，你路上慢点儿。", "pinyin": "Hǎo de, kuài yào xiàyǔ le, nǐ lùshang màn diǎnr."},
                {"speaker": "A", "zh": "没关系，我坐公共汽车。", "pinyin": "Méi guānxi, wǒ zuò gōnggòng qìchē."},
                {"speaker": "B", "zh": "好的，再见。", "pinyin": "Hǎo de, zàijiàn."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "动作的状态“要……了”"},
        {"no": 2, "title_zh": "“都……了”"}
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
                {"no": 1, "zh": "新年的时候他准备做什么？", "pinyin": "Xīnnián de shíhou tā zhǔnbèi zuò shénme?"},
                {"no": 2, "zh": "明天他有什么事要做？", "pinyin": "Míngtiān tā yǒu shénme shì yào zuò?"},
                {"no": 3, "zh": "他们两个人在等谁呢？", "pinyin": "Tāmen liǎng ge rén zài děng shéi ne?"},
                {"no": 4, "zh": "他们等的人来了没有？", "pinyin": "Tāmen děng de rén lái le méiyǒu?"},
                {"no": 5, "zh": "外面的天气怎么样？", "pinyin": "Wàimiàn de tiānqì zěnmeyàng?"}
            ]
        },
        {
            "order": 3,
            "type": "describe_picture",
            "title_zh": "用本课新学的语言点和词语描述图片",
            "items": [
                {"no": 1, "zh": "姐姐________就要回国了。", "pinyin": "Jiějie ________ jiù yào huíguó le."},
                {"no": 2, "zh": "7点50分了，我们________。", "pinyin": "Qī diǎn wǔshí fēn le, wǒmen ________."},
                {"no": 3, "zh": "弟弟都________了，可以自己吃饭了。", "pinyin": "Dìdi dōu ________ le, kěyǐ zìjǐ chīfàn le."},
                {"no": 4, "zh": "都十二点了，商店________了。", "pinyin": "Dōu shí'èr diǎn le, shāngdiàn ________ le."}
            ]
        },
        {
            "order": 4,
            "type": "pair_work",
            "title_zh": "询问对方今年新年的打算",
            "items": [
                {"no": 1, "zh": "新年你想在哪儿过？", "pinyin": "Xīnnián nǐ xiǎng zài nǎr guò?"},
                {"no": 2, "zh": "你想和谁一起过新年？", "pinyin": "Nǐ xiǎng hé shéi yìqǐ guò xīnnián?"},
                {"no": 3, "zh": "你想送给朋友什么新年礼物？", "pinyin": "Nǐ xiǎng sòng gěi péngyou shénme xīnnián lǐwù?"}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "zh": "他准备去北京旅游。", "pinyin": "Tā zhǔnbèi qù Běijīng lǚyóu."},
        {"no": 2, "zh": "明天他要去火车站买票。", "pinyin": "Míngtiān tā yào qù huǒchēzhàn mǎi piào."},
        {"no": 3, "zh": "他们在等妹妹。", "pinyin": "Tāmen zài děng mèimei."},
        {"no": 4, "zh": "来了。", "pinyin": "Lái le."},
        {"no": 5, "zh": "天阴了，快要下雨了。", "pinyin": "Tiān yīn le, kuài yào xiàyǔ le."}
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
