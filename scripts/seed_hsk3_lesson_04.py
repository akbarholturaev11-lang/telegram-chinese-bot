import asyncio
import json

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson


LESSON = {
    "level": "hsk3",
    "lesson_order": 4,
    "lesson_code": "HSK3-L04",
    "title": "她总是笑着跟客人说话",
    "goal": json.dumps({"uz": "Odatiy harakatlar va birga bajarilgan harakatlarni ifodalashni o'rganish.", "ru": "Изучение выражения привычных и сопутствующих действий.", "tj": "Омӯзиши ифодаи амалҳои одатӣ ва амалҳои ҳамзамон."}, ensure_ascii=False),
    "intro_text": json.dumps({"uz": "Bu dars odatiy harakatlar va birga bajarilgan harakatlarni ifodalashga bag'ishlangan. 5 ta asosiy so'z o'rganiladi va '又……又……' hamda 'V1着(O1)+V2(O2)' grammatik shakllar o'zlashtiriladi.", "ru": "Этот урок посвящён выражению привычных и сопутствующих действий. Изучаются 5 ключевых слов и грамматические конструкции '又……又……' и 'V1着(O1)+V2(O2)'.", "tj": "Ин дарс ба ифодаи амалҳои одатӣ ва амалҳои ҳамзамон бахшида шудааст. 5 калимаи асосӣ омӯхта мешавад ва сохторҳои грамматикии '又……又……' ва 'V1着(O1)+V2(O2)' аз бар карда мешаванд."}, ensure_ascii=False),
    "vocabulary_json": json.dumps([
        {"no": 1, "zh": "总是", "pinyin": "zǒngshì", "pos": "adv.", "uz": "har doim, doimo", "ru": "всегда, постоянно", "tj": "ҳамеша, доимо"},
        {"no": 2, "zh": "客人", "pinyin": "kèrén", "pos": "n.", "uz": "mehmon, mijoz", "ru": "гость, клиент", "tj": "меҳмон, мизоҷ"},
        {"no": 3, "zh": "照片", "pinyin": "zhàopiàn", "pos": "n.", "uz": "rasm, surat", "ru": "фотография, снимок", "tj": "акс, сурат"},
        {"no": 4, "zh": "认真", "pinyin": "rènzhēn", "pos": "adj.", "uz": "jiddiy, mas'uliyatli", "ru": "серьёзный, добросовестный", "tj": "ҷиддӣ, масъулиятшинос"},
        {"no": 5, "zh": "蛋糕", "pinyin": "dàngāo", "pos": "n.", "uz": "tort, keks", "ru": "торт, кекс", "tj": "торт, кулча"}
    ], ensure_ascii=False),
    "dialogue_json": json.dumps([
        {
            "block_no": 1,
            "section_label": "课文 1",
            "scene_uz": "Do'konda",
            "scene_ru": "В магазине",
            "scene_tj": "Дар мағоза",
            "dialogue": [
                {"speaker": "A", "zh": "她总是笑着跟客人说话。", "pinyin": "Tā zǒngshì xiào zhe gēn kèrén shuōhuà.", "uz": "U har doim mijozlar bilan gaplashayotganda kulib turadi.", "ru": "Она всегда разговаривает с клиентами с улыбкой.", "tj": "Вай ҳамеша бо мизоҷон хандон гап мезанад."},
                {"speaker": "B", "zh": "对，她服务很认真。", "pinyin": "Duì, tā fúwù hěn rènzhēn.", "uz": "Ha, u xizmat ko'rsatishda juda mas'uliyatli.", "ru": "Да, она очень добросовестно обслуживает.", "tj": "Бале, вай хизматрасониашро хеле ҷиддӣ мекунад."}
            ]
        },
        {
            "block_no": 2,
            "section_label": "课文 2",
            "scene_uz": "Ziyofatda",
            "scene_ru": "На вечеринке",
            "scene_tj": "Дар зиёфат",
            "dialogue": [
                {"speaker": "A", "zh": "桌子上又有蛋糕又有水果。", "pinyin": "Zhuōzi shàng yòu yǒu dàngāo yòu yǒu shuǐguǒ.", "uz": "Stolda ham tort, ham meva bor.", "ru": "На столе и торт, и фрукты.", "tj": "Дар рӯи мизи ҳам торт ҳам мева мавҷуд аст."},
                {"speaker": "B", "zh": "我们先拍照片吧。", "pinyin": "Wǒmen xiān pāi zhàopiàn ba.", "uz": "Avval rasm olaylik.", "ru": "Давай сначала сфотографируемся.", "tj": "Биёед аввал акс гирем."}
            ]
        }
    ], ensure_ascii=False),
    "grammar_json": json.dumps([
        {
            "no": 1,
            "title_zh": "又……又……",
            "title_uz": "'Yòu……yòu……' konstruktsiyasi",
            "title_ru": "Конструкция '又……又……'",
            "title_tj": "Конструксияи '又……又……'",
            "rule_uz": "Bu konstruktsiya bir vaqtda ikki xususiyat yoki holatni ta'kidlash uchun ishlatiladi: 'ham… ham…'. Ikkala qism ham sifat yoki holat bo'lishi kerak.",
            "rule_ru": "Эта конструкция используется для одновременного акцентирования двух качеств или состояний: 'и… и…'. Обе части должны быть прилагательными или состояниями.",
            "rule_tj": "Ин конструксия барои таъкиди якзамонаи ду хусусият ё ҳолат истифода мешавад: 'ҳам… ҳам…'. Ҳар ду қисм бояд сифат ё ҳолат бошанд.",
            "examples": [
                {"zh": "这个蛋糕又甜又新鲜。", "pinyin": "Zhège dàngāo yòu tián yòu xīnxiān.", "uz": "Bu tort ham shirin, ham yangi.", "ru": "Этот торт и сладкий, и свежий.", "tj": "Ин торт ҳам ширин ҳам тоза аст."},
                {"zh": "她又认真又热情。", "pinyin": "Tā yòu rènzhēn yòu rèqíng.", "uz": "U ham jiddiy, ham mehribon.", "ru": "Она и серьёзная, и тёплая.", "tj": "Вай ҳам ҷиддӣ ҳам меҳрубон аст."}
            ]
        },
        {
            "no": 2,
            "title_zh": "动作的伴随：V1着(O1)+V2(O2)",
            "title_uz": "Birga bajariladigan harakatlar: V1着(O1)+V2(O2)",
            "title_ru": "Сопутствующие действия: V1着(O1)+V2(O2)",
            "title_tj": "Амалҳои ҳамзамон: V1着(O1)+V2(O2)",
            "rule_uz": "'Zhe' yuklamasi birinchi fe'ldan keyin kelib, ikkinchi asosiy harakat bajarilayotgan paytdagi holatni (birga bajariladigan harakatni) bildiradi. Tuzilish: V1 + 着 + (O1) + V2 + (O2). Masalan: 笑着说话 (kulib gapirmoq).",
            "rule_ru": "Частица '着' после первого глагола выражает состояние, сопровождающее второе основное действие. Структура: V1 + 着 + (O1) + V2 + (O2). Например: 笑着说话 (говорить с улыбкой).",
            "rule_tj": "Зарраи '着' баъд аз феъли аввал ҳолатеро ифода мекунад ки амали асосии дуввумро ҳамроҳӣ мекунад. Сохтор: V1 + 着 + (O1) + V2 + (O2). Масалан: 笑着说话 (хандон гап задан).",
            "examples": [
                {"zh": "她总是笑着跟客人说话。", "pinyin": "Tā zǒngshì xiào zhe gēn kèrén shuōhuà.", "uz": "U har doim mijozlar bilan gaplashayotganda kulib turadi.", "ru": "Она всегда разговаривает с клиентами с улыбкой.", "tj": "Вай ҳамеша бо мизоҷон хандон гап мезанад."},
                {"zh": "他站着吃饭。", "pinyin": "Tā zhàn zhe chīfàn.", "uz": "U tik turib ovqatlanadi.", "ru": "Он ест стоя.", "tj": "Вай истода хӯрок мехӯрад."}
            ]
        }
    ], ensure_ascii=False),
    "exercise_json": json.dumps([
        {
            "no": 1,
            "type": "translate_to_chinese",
            "instruction_uz": "Quyidagi so'zlarning xitoychasini yozing:",
            "instruction_ru": "Напишите китайские эквиваленты следующих слов:",
            "instruction_tj": "Тарҷумаи чинии калимаҳои зеринро нависед:",
            "items": [
                {"prompt_uz": "har doim", "prompt_ru": "всегда", "prompt_tj": "ҳамеша", "answer": "总是", "pinyin": "zǒngshì"},
                {"prompt_uz": "mehmon, mijoz", "prompt_ru": "гость, клиент", "prompt_tj": "меҳмон, мизоҷ", "answer": "客人", "pinyin": "kèrén"},
                {"prompt_uz": "rasm, surat", "prompt_ru": "фотография", "prompt_tj": "акс, сурат", "answer": "照片", "pinyin": "zhàopiàn"},
                {"prompt_uz": "jiddiy, mas'uliyatli", "prompt_ru": "серьёзный, добросовестный", "prompt_tj": "ҷиддӣ, масъулиятшинос", "answer": "认真", "pinyin": "rènzhēn"}
            ]
        },
        {
            "no": 2,
            "type": "fill_blank",
            "instruction_uz": "Bo'sh joyni to'ldiring:",
            "instruction_ru": "Заполните пропуск:",
            "instruction_tj": "Ҷойи холиро пур кунед:",
            "items": [
                {"prompt_uz": "U har doim ___ mijozlar bilan gapiradi. (笑着)", "prompt_ru": "Она всегда ___ разговаривает с клиентами. (笑着)", "prompt_tj": "Вай ҳамеша ___ бо мизоҷон гап мезанад. (笑着)", "answer": "笑着", "pinyin": "xiào zhe"},
                {"prompt_uz": "Stolda ham tort ___ ham meva bor. (又)", "prompt_ru": "На столе ___ торт ___ фрукты. (又……又……)", "prompt_tj": "Дар мизи ҳам торт ___ ҳам мева ҳаст. (又)", "answer": "又", "pinyin": "yòu"},
                {"prompt_uz": "U xizmat ko'rsatishda juda ___. (认真)", "prompt_ru": "Она очень ___ в обслуживании. (认真)", "prompt_tj": "Вай дар хизматрасонӣ хеле ___. (认真)", "answer": "认真", "pinyin": "rènzhēn"},
                {"prompt_uz": "Avval ___ olaylik. (照片)", "prompt_ru": "Сначала сделаем ___. (照片)", "prompt_tj": "Аввал ___ гирем. (照片)", "answer": "照片", "pinyin": "zhàopiàn"}
            ]
        }
    ], ensure_ascii=False),
    "answers_json": json.dumps([
        {"no": 1, "answers": ["总是", "客人", "照片", "认真"]},
        {"no": 2, "answers": ["笑着", "又", "认真", "照片"]}
    ], ensure_ascii=False),
    "homework_json": json.dumps([
        {
            "no": 1,
            "instruction_uz": "Quyidagi so'zlardan foydalanib 3 ta jumla tuzing:",
            "instruction_ru": "Составьте 3 предложения, используя следующие слова:",
            "instruction_tj": "Бо истифодаи калимаҳои зерин 3 ҷумла созед:",
            "words": ["总是", "客人", "照片"],
            "example": "她总是笑着跟客人说话。",
            "topic_uz": "Odatiy harakatlar tavsifi",
            "topic_ru": "Описание привычных действий",
            "topic_tj": "Тавсифи амалҳои одатӣ"
        },
        {
            "no": 2,
            "instruction_uz": "Dars mavzusi bo'yicha 4-5 jumladan iborat qisqa matn yozing:",
            "instruction_ru": "Напишите короткий абзац из 4-5 предложений по теме урока:",
            "instruction_tj": "Дар бораи мавзӯи дарс 4-5 ҷумлаи кӯтоҳ нависед:",
            "words": ["总是", "笑着", "又……又……"],
            "example": "她总是笑着工作，又认真又热情。",
            "topic_uz": "她总是笑着跟客人说话",
            "topic_ru": "她总是笑着跟客人说话",
            "topic_tj": "她总是笑着跟客人说话"
        }
    ], ensure_ascii=False),
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
            for key, value in LESSON.items():
                setattr(existing, key, value)
            print(f"updated: {LESSON['lesson_code']}")
        else:
            session.add(CourseLesson(**LESSON))
            print(f"inserted: {LESSON['lesson_code']}")
        await session.commit()


if __name__ == "__main__":
    asyncio.run(upsert_lesson())
