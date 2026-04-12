import asyncio
import json

from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk2",
    "lesson_order": 10,
    "lesson_code": "HSK2-L10",
    "title": "别找了，手机在桌子上呢",
    "goal": "",
    "intro_text": "",
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "课", "pinyin": "kè", "pos": "n."},
        {"no": 2, "zh": "帮助", "pinyin": "bāngzhù", "pos": "v."},
        {"no": 3, "zh": "别", "pinyin": "bié", "pos": "adv."},
        {"no": 4, "zh": "哥哥", "pinyin": "gēge", "pos": "n."},
        {"no": 5, "zh": "鸡蛋", "pinyin": "jīdàn", "pos": "n."},
        {"no": 6, "zh": "西瓜", "pinyin": "xīguā", "pos": "n."},
        {"no": 7, "zh": "正在", "pinyin": "zhèngzài", "pos": "adv."},
        {"no": 8, "zh": "手机", "pinyin": "shǒujī", "pos": "n."},
        {"no": 9, "zh": "洗", "pinyin": "xǐ", "pos": "v."}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "别看电视了，明天上午还有汉语课呢。", "pinyin": "Bié kàn diànshì le，míngtiān shàngwǔ hái yǒu Hànyǔ kè ne."},
                {"speaker": "B", "zh": "看电视对学汉语有帮助。", "pinyin": "Kàn diànshì duì xué Hànyǔ yǒu bāngzhù."},
                {"speaker": "A", "zh": "明天的课你都准备好了吗？", "pinyin": "Míngtiān de kè nǐ dōu zhǔnbèi hǎo le ma?"},
                {"speaker": "B", "zh": "都准备好了。", "pinyin": "Dōu zhǔnbèi hǎo le."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "在医院 2",
            "scene_label_zh": "在医院",
            "dialogue": [
                {"speaker": "A", "zh": "别看报纸了，医生说你要多休息。", "pinyin": "Bié kàn bàozhǐ le，yīshēng shuō nǐ yào duō xiūxi."},
                {"speaker": "B", "zh": "好，不看了。给我一杯茶吧。", "pinyin": "Hǎo，bù kàn le. Gěi wǒ yì bēi chá ba."},
                {"speaker": "A", "zh": "医生说吃药后的两个小时不要喝茶。", "pinyin": "Yīshēng shuō chī yàohòu de liǎng ge xiǎoshí búyào hē chá."},
                {"speaker": "B", "zh": "医生还说什么了？", "pinyin": "Yīshēng hái shuō shénme le?"},
                {"speaker": "A", "zh": "医生让你听我的。", "pinyin": "Yīshēng ràng nǐ tīng wǒ de."}
            ]
        },
        {
            "block_no": 3,
            "section_label": "在家里 3",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "你怎么买了这么多东西啊？", "pinyin": "Nǐ zěnme mǎi le zhème duō dōngxi a?"},
                {"speaker": "B", "zh": "哥哥今天中午回来吃饭。", "pinyin": "Gēge jīntiān zhōngwǔ huílái chīfàn."},
                {"speaker": "A", "zh": "我看看买什么了。羊肉，鸡蛋，面条，西瓜……真不少！妈妈呢？", "pinyin": "Wǒ kànkan mǎi shénme le. Yángròu，jīdàn，miàntiáo，xīguā…… zhēn bù shǎo! Māma ne?"},
                {"speaker": "B", "zh": "正在准备午饭呢！", "pinyin": "Zhèngzài zhǔnbèi wǔfàn ne!"}
            ]
        },
        {
            "block_no": 4,
            "section_label": "在家里 4",
            "scene_label_zh": "在家里",
            "dialogue": [
                {"speaker": "A", "zh": "你在找什么？", "pinyin": "Nǐ zài zhǎo shénme?"},
                {"speaker": "B", "zh": "你看见我的手机了吗？白色的。", "pinyin": "Nǐ kànjian wǒ de shǒujī le ma? Báisè de."},
                {"speaker": "A", "zh": "别找了，手机在桌子上呢，电脑旁边。", "pinyin": "Bié zhǎo le，shǒujī zài zhuōzi shang ne，diànnǎo pángbiān."},
                {"speaker": "B", "zh": "你看见我的衣服了吗？红色的那件。", "pinyin": "Nǐ kànjian wǒ de yīfu le ma? Hóngsè de nà jiàn."},
                {"speaker": "A", "zh": "那件衣服我帮你洗了，在外边呢。", "pinyin": "Nà jiàn yīfu wǒ bāng nǐ xǐ le，zài wàibian ne."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {"no": 1, "title_zh": "祈使句：不要……了；别……了"},
        {"no": 2, "title_zh": "介词“对”"}
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
                {"no": 1, "zh": "孩子们正在做什么？", "pinyin": "Háizimen zhèngzài zuò shénme?"},
                {"no": 2, "zh": "妈妈为什么不让他们看电视了？", "pinyin": "Māma wèishénme bù ràng tāmen kàn diànshì le?"},
                {"no": 3, "zh": "吃药以后可以喝茶吗？", "pinyin": "Chī yào yǐhòu kěyǐ hē chá ma?"},
                {"no": 4, "zh": "他今天都买了什么东西？为什么要买这么多？", "pinyin": "Tā jīntiān dōu mǎi le shénme dōngxi? Wèishénme yào mǎi zhème duō?"},
                {"no": 5, "zh": "你知道男的正在找什么吗？", "pinyin": "Nǐ zhīdào nán de zhèngzài zhǎo shénme ma?"}
            ]
        },
        {
            "order": 3,
            "type": "describe_picture",
            "title_zh": "用本课新学的语言点和词语描述图片",
            "items": [
                {"no": 1, "zh": "你的病已经好了，别____了。", "pinyin": "Nǐ de bìng yǐjīng hǎo le，bié ____ le."},
                {"no": 2, "zh": "别____了，明天上午还要上汉语课呢。", "pinyin": "Bié ____ le，míngtiān shàngwǔ hái yào shàng Hànyǔ kè ne."},
                {"no": 3, "zh": "____对身体很好。", "pinyin": "____ duì shēntǐ hěn hǎo."},
                {"no": 4, "zh": "____对学习英语有帮助。", "pinyin": "____ duì xuéxí Yīngyǔ yǒu bāngzhù."}
            ]
        },
        {
            "order": 4,
            "type": "pair_work",
            "title_zh": "用“不要……了”/“别……了”练习说句子",
            "items": [
                {"no": 1, "zh": "不要玩电脑了。", "pinyin": "Búyào wán diànnǎo le."},
                {"no": 2, "zh": "别看电视了。", "pinyin": "Bié kàn diànshì le."},
                {"no": 3, "zh": "不要喝咖啡了。", "pinyin": "Búyào hē kāfēi le."},
                {"no": 4, "zh": "别吃药了。", "pinyin": "Bié chī yào le."}
            ]
        },
        {
            "order": 5,
            "type": "group_work",
            "title_zh": "用介词“对”练习说句子",
            "items": [
                {"no": 1, "zh": "看电视对眼睛不好。", "pinyin": "Kàn diànshì duì yǎnjing bù hǎo."}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "zh": "孩子们正在看电视。", "pinyin": "Háizimen zhèngzài kàn diànshì."},
        {"no": 2, "zh": "因为明天上午还有汉语课。", "pinyin": "Yīnwèi míngtiān shàngwǔ hái yǒu Hànyǔ kè."},
        {"no": 3, "zh": "不可以。", "pinyin": "Bù kěyǐ."},
        {"no": 4, "zh": "买了羊肉、鸡蛋、面条和西瓜，因为他哥哥今天中午回来吃饭。", "pinyin": "Mǎi le yángròu、jīdàn、miàntiáo hé xīguā，yīnwèi tā gēge jīntiān zhōngwǔ huílái chīfàn."},
        {"no": 5, "zh": "他正在找手机。", "pinyin": "Tā zhèngzài zhǎo shǒujī."}
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
