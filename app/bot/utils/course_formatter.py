import ast
import json
from typing import Any


def _parse(value: Any, default: Any = None):
    if value is None:
        return default
    if isinstance(value, (list, dict)):
        return value
    try:
        return json.loads(value)
    except Exception:
        return default


def _ml(value: Any, lang: str, fallback_lang: str = "uz") -> str:
    """Extract a language string from either a plain string or a multilingual dict."""
    if isinstance(value, dict):
        return value.get(lang) or value.get(fallback_lang) or next(iter(value.values()), "") or ""
    return value or ""


def _ml_rule(value: Any, lang: str) -> str:
    """Extract grammar rule from either a plain string or a {rule_uz, rule_tj, rule_ru} dict."""
    if isinstance(value, dict):
        return value.get(f"rule_{lang}") or value.get("rule_uz") or next(iter(value.values()), "") or ""
    return value or ""


def _parse_text_field(raw: Any) -> Any:
    """Parse a DB text field that may be JSON, Python repr dict, or plain string."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except Exception:
            pass
        try:
            return ast.literal_eval(raw)
        except Exception:
            pass
    return raw


def format_vocab(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    vocab = _parse(lesson.vocabulary_json, [])
    title = lesson.title or ""

    label = {"uz": "Yangi so'zlar 🇨🇳", "tj": "Калимаҳои нав 🇨🇳", "ru": "Новые слова 🇨🇳"}
    lines = [f"【1/{lesson_total_steps}】 {title} · {label.get(lang, label['ru'])}", ""]

    hint = {
        "uz": f"✨ Bugun {len(vocab)} ta so'z — darsni tugatgach ishlatishni bilasiz!",
        "tj": f"✨ Имрӯз {len(vocab)} калима — пас аз дарс истифода карда метавонед!",
        "ru": f"✨ Сегодня {len(vocab)} слов — после урока сможете их использовать!",
    }
    lines.append(hint.get(lang, hint["ru"]))
    lines.append("")

    nums = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for i, word in enumerate(vocab):
        if not isinstance(word, dict):
            continue
        zh = word.get("zh", "")
        pinyin = word.get("pinyin", "")
        meaning = _ml(word.get("meaning") or word.get(lang), lang)
        example_zh = word.get("example_zh", "")
        example_pinyin = word.get("example_pinyin", "")
        example_lang = _ml(word.get("example") or word.get(f"example_{lang}"), lang)

        num = nums[i] if i < len(nums) else f"{i+1}."

        lines.append("━━━━━━━━━━━━━━")
        lines.append(f"{num}  {zh}")
        lines.append(f"     {pinyin}")
        lines.append(f"     👉 {meaning}")

        if example_zh:
            lines.append("")
            lines.append(f"     💬 {example_zh}")
            if example_pinyin:
                lines.append(f"        {example_pinyin}")
            if example_lang:
                lines.append(f"        {example_lang}")

        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    return "\n".join(lines)


def format_dialogue(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    dialogues = _parse(lesson.dialogue_json, [])
    title = lesson.title or ""

    step_label = {"uz": "Jonli dialog 🎭", "tj": "Муколамаи зинда 🎭", "ru": "Живой диалог 🎭"}
    lines = [f"【2/{lesson_total_steps}】 {title} · {step_label.get(lang, step_label['ru'])}", ""]

    for block in dialogues:
        if not isinstance(block, dict):
            continue

        # section label (课文 1, 课文 2 ...)
        section = block.get("section_label", "")
        scene = _ml(
            block.get("scene_label_zh") or block.get(f"scene_{lang}") or block.get("scene_uz"),
            lang,
        )

        header = " · ".join(filter(None, [section, scene]))
        if header:
            lines.append(f"📍 {header}")
            lines.append("")

        lines.append("━━━━━━━━━━━━━━")

        # actual key is "dialogue", fallback to "lines"
        dialogue_lines = block.get("dialogue") or block.get("lines") or []
        for line in dialogue_lines:
            if not isinstance(line, dict):
                continue
            speaker = line.get("speaker", "")
            zh = line.get("zh", "")
            pinyin = line.get("pinyin", "")
            # actual key is "translation", fallback to lang key
            translation = _ml(
                line.get("translation") or line.get(lang) or line.get("uz"),
                lang,
            )

            icon = "👤" if speaker == "A" else "👥"
            lines.append(f"{icon} {speaker}:  {zh}")
            lines.append(f"       {pinyin}")
            lines.append(f"       {translation}")
            lines.append("")

        lines.append("━━━━━━━━━━━━━━")

        notes = block.get("notes", [])
        if notes:
            lines.append("")
            tip = {"uz": "💡 Bilasizmi?", "tj": "💡 Медонед?", "ru": "💡 Знаете ли вы?"}
            lines.append(tip.get(lang, tip["ru"]))
            for note in notes:
                note_text = note.get(lang) or note.get("uz") or ""
                if note_text:
                    lines.append(note_text)

        lines.append("")

    return "\n".join(lines).rstrip()


def format_grammar(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    grammar = _parse(lesson.grammar_json, [])
    title = lesson.title or ""

    step_label = {"uz": "Grammatika 📐", "tj": "Грамматика 📐", "ru": "Грамматика 📐"}
    lines = [f"【3/{lesson_total_steps}】 {title} · {step_label.get(lang, step_label['ru'])}", ""]

    for i, g in enumerate(grammar, 1):
        if not isinstance(g, dict):
            continue

        g_title = g.get(f"title_{lang}") or g.get("title_uz") or g.get("title_zh") or ""
        rule = _ml_rule(
            g.get("explanation") or g.get(f"rule_{lang}") or g.get("rule_uz") or g.get("rule"),
            lang,
        )

        lines.append("━━━━━━━━━━━━━━")
        lines.append(f"📌 {i}. {g_title}")
        lines.append("")
        if rule:
            for rule_line in rule.split("\n"):
                lines.append(f"   {rule_line}")
        lines.append("")

        examples = g.get("examples", [])
        if examples:
            eg_label = {"uz": "Misollar:", "tj": "Мисолҳо:", "ru": "Примеры:"}
            lines.append(f"   {eg_label.get(lang, eg_label['ru'])}")
            for ex in examples:
                zh = ex.get("zh", "")
                pinyin = ex.get("pinyin", "")
                meaning = _ml(ex.get("meaning") or ex.get(lang) or ex.get("uz"), lang)
                lines.append(f"   • {zh} ({pinyin}) — {meaning}")
        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    return "\n".join(lines)


def format_exercise(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    exercises = _parse(lesson.exercise_json, [])
    title = lesson.title or ""

    step_label = {"uz": "Test vaqti! 🧠", "tj": "Вақти санҷиш! 🧠", "ru": "Время теста! 🧠"}
    lines = [f"【5/{lesson_total_steps}】 {title} · {step_label.get(lang, step_label['ru'])}", ""]

    hint = {
        "uz": "Siz tayyor deb o'ylaymiz... Isbotlang! 😄",
        "tj": "Мо фикр мекунем шумо омодаед... Исбот кунед! 😄",
        "ru": "Думаем, вы готовы... Докажите! 😄",
    }
    lines.append(hint.get(lang, hint["ru"]))
    lines.append("")

    answer_hint = {
        "uz": "Javobingizni yozing ⬇️",
        "tj": "Посухатонро нависед ⬇️",
        "ru": "Напишите ответ ⬇️",
    }

    for ex in exercises:
        if not isinstance(ex, dict):
            continue

        instruction = _ml(ex.get("instruction", ""), lang)
        items = ex.get("items", [])

        lines.append("━━━━━━━━━━━━━━")
        if instruction:
            lines.append(f"📝 {instruction}")
            lines.append("")

        for i, item in enumerate(items, 1):
            if not isinstance(item, dict):
                continue
            prompt = _ml(item.get("prompt", ""), lang)
            if prompt:
                lines.append(f"  {i}. {prompt}")

        lines.append("")

    lines.append("━━━━━━━━━━━━━━")
    lines.append(answer_hint.get(lang, answer_hint["ru"]))

    return "\n".join(lines)


def format_intro(lesson, lang: str, lesson_total_steps: int = 6) -> str:
    title = lesson.title or ""
    intro_raw = lesson.intro_text or ""

    intro_data = _parse_text_field(intro_raw)
    if isinstance(intro_data, dict):
        intro = intro_data.get(lang) or intro_data.get("uz") or next(iter(intro_data.values()), "") or ""
    else:
        intro = str(intro_data) if intro_data else ""

    step_label = {"uz": "Darsga xush kelibsiz! 🎉", "tj": "Хуш омадед ба дарс! 🎉", "ru": "Добро пожаловать на урок! 🎉"}
    lines = [
        f"【Dars {lesson.lesson_order}】 {title}",
        "",
        step_label.get(lang, step_label["ru"]),
        "",
        "━━━━━━━━━━━━━━",
        intro,
        "━━━━━━━━━━━━━━",
    ]

    return "\n".join(lines)
