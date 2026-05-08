#!/usr/bin/env python3
"""
Translate HSK1 seed files to uz/tj/ru trilingual format using Google Translate.

Fields transformed:
  goal, intro_text         → {"uz": ..., "tj": ..., "ru": ...}
  meaning (vocab/examples) → {"uz": ..., "tj": ..., "ru": ...}
  translation (dialogue)   → {"uz": ..., "tj": ..., "ru": ...}
  explanation (grammar)    → {"rule_uz":..., "rule_tj":..., "rule_ru":...}
  instruction (exercises)  → {"uz": ..., "tj": ..., "ru": ...}
  scene_label_zh (Uzbek)   → {"uz": ..., "tj": ..., "ru": ...}
  prompt (English only)    → {"uz": ..., "tj": ..., "ru": ...}
"""

import json
import re
import sys
import time
from pathlib import Path

from deep_translator import GoogleTranslator

# ── Config ────────────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent
DELAY = 0.25          # seconds between individual translation requests
RETRY_DELAY = 3.0     # seconds to wait after a rate-limit error
MAX_RETRIES = 4

JSON_FIELDS = [
    "vocabulary_json", "dialogue_json", "grammar_json",
    "exercise_json", "answers_json", "homework_json",
]

# ── Translation cache  ────────────────────────────────────────────────────────
# key: (source_lang, target_lang, text)  →  translated string
_tr_cache: dict[tuple, str] = {}


def _translate_one(text: str, src: str, tgt: str) -> str:
    """Translate a single text with retry logic."""
    if not text.strip():
        return text
    key = (src, tgt, text)
    if key in _tr_cache:
        return _tr_cache[key]
    for attempt in range(MAX_RETRIES):
        try:
            result = GoogleTranslator(source=src, target=tgt).translate(text)
            time.sleep(DELAY)
            _tr_cache[key] = result or text
            return _tr_cache[key]
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_DELAY * (attempt + 1)
                print(f"    [retry {attempt+1}] {e!s:.60} — waiting {wait:.0f}s …")
                time.sleep(wait)
            else:
                print(f"    [FAILED] {text[:40]!r}: {e}")
                _tr_cache[key] = text
                return text
    return text


def translate_en(text: str) -> dict:
    """Translate English text → {"uz": ..., "tj": ..., "ru": ...}."""
    return {
        "uz": _translate_one(text, "en", "uz"),
        "tj": _translate_one(text, "en", "tg"),
        "ru": _translate_one(text, "en", "ru"),
    }


def translate_uz(text: str) -> dict:
    """Translate Uzbek text (scene labels) → {"uz": orig, "tj": ..., "ru": ...}."""
    return {
        "uz": text,
        "tj": _translate_one(text, "uz", "tg"),
        "ru": _translate_one(text, "uz", "ru"),
    }


def translate_explanation_en(text: str) -> dict:
    """Translate English grammar explanation → {"rule_uz":..., "rule_tj":..., "rule_ru":...}."""
    return {
        "rule_uz": _translate_one(text, "en", "uz"),
        "rule_tj": _translate_one(text, "en", "tg"),
        "rule_ru": _translate_one(text, "en", "ru"),
    }


# ── Chinese detection ─────────────────────────────────────────────────────────
_CJK = re.compile(r"[一-鿿㐀-䶿]")


def has_chinese(text: str) -> bool:
    return bool(_CJK.search(text))


# ── Extract LESSON dict from seed file ────────────────────────────────────────
def extract_lesson(filepath: Path) -> dict:
    content = filepath.read_text(encoding="utf-8")
    lines = []
    skip = False
    for line in content.splitlines():
        if line.startswith(("import ", "from ")):
            continue
        if line.startswith("async def seed") or line.startswith("if __name__"):
            skip = True
        if not skip:
            lines.append(line)
    ns: dict = {"json": json}
    exec("\n".join(lines), ns)  # noqa: S102
    return ns["LESSON"]


# ── Count texts for progress display ─────────────────────────────────────────
def count_translations(lesson: dict) -> int:
    count = 0
    for field in ("goal", "intro_text"):
        if isinstance(lesson.get(field), str):
            count += 3   # uz, tj, ru

    vocab = json.loads(lesson.get("vocabulary_json", "[]"))
    count += sum(3 for item in vocab if isinstance(item.get("meaning"), str))

    dialogues = json.loads(lesson.get("dialogue_json", "[]"))
    for block in dialogues:
        if isinstance(block.get("scene_label_zh"), str):
            count += 2   # only tj and ru (uz stays)
        count += sum(3 for line in block.get("dialogue", [])
                     if isinstance(line.get("translation"), str))

    grammar = json.loads(lesson.get("grammar_json", "[]"))
    for rule in grammar:
        if isinstance(rule.get("explanation"), str):
            count += 3
        count += sum(3 for ex in rule.get("examples", [])
                     if isinstance(ex.get("meaning"), str))

    exercises = json.loads(lesson.get("exercise_json", "[]"))
    for ex in exercises:
        if isinstance(ex.get("instruction"), str):
            count += 3
        count += sum(3 for item in ex.get("items", [])
                     if isinstance(item.get("prompt"), str) and not has_chinese(item["prompt"]))

    homework = json.loads(lesson.get("homework_json", "[]"))
    for hw in homework:
        if isinstance(hw.get("instruction"), str):
            count += 3
        if isinstance(hw.get("example"), str) and not has_chinese(hw["example"]):
            count += 3
        count += sum(3 for item in hw.get("items", [])
                     if isinstance(item.get("prompt"), str) and not has_chinese(item["prompt"]))

    return count


# ── Apply translations ────────────────────────────────────────────────────────
class Counter:
    def __init__(self, total: int):
        self.n = 0
        self.total = total

    def tick(self, label: str = ""):
        self.n += 1
        if label:
            pct = self.n * 100 // self.total
            sys.stdout.write(f"\r    [{pct:3d}%] {self.n}/{self.total}  {label[:55]:<55}")
            sys.stdout.flush()


def transform_lesson(lesson: dict, ctr: Counter) -> dict:
    result = dict(lesson)

    # Top-level string fields → multilingual dict
    for field in ("goal", "intro_text"):
        val = result.get(field)
        if isinstance(val, str) and val.strip():
            ctr.tick(f"{field}: {val[:40]}")
            result[field] = translate_en(val)

    # vocabulary_json
    vocab = json.loads(lesson["vocabulary_json"])
    for item in vocab:
        m = item.get("meaning")
        if isinstance(m, str) and m.strip():
            ctr.tick(f"meaning: {m[:40]}")
            item["meaning"] = translate_en(m)
    result["vocabulary_json"] = json.dumps(vocab, ensure_ascii=False)

    # dialogue_json
    dialogues = json.loads(lesson["dialogue_json"])
    for block in dialogues:
        scene = block.get("scene_label_zh")
        if isinstance(scene, str) and scene.strip():
            ctr.tick(f"scene: {scene[:40]}")
            block["scene_label_zh"] = translate_uz(scene)
        for line in block.get("dialogue", []):
            tr = line.get("translation")
            if isinstance(tr, str) and tr.strip():
                ctr.tick(f"translation: {tr[:40]}")
                line["translation"] = translate_en(tr)
    result["dialogue_json"] = json.dumps(dialogues, ensure_ascii=False)

    # grammar_json
    grammar = json.loads(lesson["grammar_json"])
    for rule in grammar:
        exp = rule.get("explanation")
        if isinstance(exp, str) and exp.strip():
            ctr.tick(f"explanation: {exp[:40]}")
            rule["explanation"] = translate_explanation_en(exp)
        for ex in rule.get("examples", []):
            m = ex.get("meaning")
            if isinstance(m, str) and m.strip():
                ctr.tick(f"meaning: {m[:40]}")
                ex["meaning"] = translate_en(m)
    result["grammar_json"] = json.dumps(grammar, ensure_ascii=False)

    # exercise_json
    exercises = json.loads(lesson["exercise_json"])
    for ex in exercises:
        ins = ex.get("instruction")
        if isinstance(ins, str) and ins.strip():
            ctr.tick(f"instruction: {ins[:40]}")
            ex["instruction"] = translate_en(ins)
        for item in ex.get("items", []):
            pr = item.get("prompt")
            if isinstance(pr, str) and pr.strip() and not has_chinese(pr):
                ctr.tick(f"prompt: {pr[:40]}")
                item["prompt"] = translate_en(pr)
    result["exercise_json"] = json.dumps(exercises, ensure_ascii=False)

    # homework_json
    homework = json.loads(lesson["homework_json"])
    for hw in homework:
        ins = hw.get("instruction")
        if isinstance(ins, str) and ins.strip():
            ctr.tick(f"hw instruction: {ins[:40]}")
            hw["instruction"] = translate_en(ins)
        example = hw.get("example")
        if isinstance(example, str) and example.strip() and not has_chinese(example):
            ctr.tick(f"hw example: {example[:40]}")
            hw["example"] = translate_en(example)
        for item in hw.get("items", []):
            pr = item.get("prompt")
            if isinstance(pr, str) and pr.strip() and not has_chinese(pr):
                ctr.tick(f"hw prompt: {pr[:40]}")
                item["prompt"] = translate_en(pr)
    result["homework_json"] = json.dumps(homework, ensure_ascii=False)

    return result


# ── Code generation ───────────────────────────────────────────────────────────
def _py_str(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _fmt_val(val, depth: int = 1) -> str:
    pad = "    " * depth
    inner = "    " * (depth + 1)
    if isinstance(val, bool):
        return "True" if val else "False"
    if isinstance(val, int):
        return str(val)
    if val is None:
        return "None"
    if isinstance(val, str):
        return f'"{_py_str(val)}"'
    if isinstance(val, dict):
        if not val:
            return "{}"
        rows = [f'{inner}"{k}": {_fmt_val(v, depth + 1)}' for k, v in val.items()]
        return "{\n" + ",\n".join(rows) + f"\n{pad}" + "}"
    if isinstance(val, list):
        if not val:
            return "[]"
        rows = [f"{inner}{_fmt_val(v, depth + 1)}" for v in val]
        return "[\n" + ",\n".join(rows) + f"\n{pad}" + "]"
    return repr(val)


def generate_file(lesson: dict) -> str:
    lines: list[str] = [
        "import asyncio",
        "import json",
        "",
        "from sqlalchemy import select",
        "",
        "from app.db.session import async_session_maker as SessionLocal",
        "from app.db.models.course_lessons import CourseLesson",
        "",
        "",
        "LESSON = {",
    ]

    for key in ("level", "lesson_order", "lesson_code", "title"):
        if key not in lesson:
            continue
        val = lesson[key]
        if isinstance(val, str):
            lines.append(f'    "{key}": "{_py_str(val)}",')
        else:
            lines.append(f'    "{key}": {_fmt_val(val)},')

    for key in ("goal", "intro_text"):
        if key not in lesson:
            continue
        lines.append(f'    "{key}": {_fmt_val(lesson[key])},')

    for field in JSON_FIELDS:
        if field not in lesson:
            continue
        raw = lesson[field]
        data = json.loads(raw) if isinstance(raw, str) else raw
        inner_json = json.dumps(data, ensure_ascii=False, indent=8)
        lines.append("")
        lines.append(f'    "{field}": json.dumps({inner_json}, ensure_ascii=False),')

    if "is_active" in lesson:
        lines.append("")
        lines.append(f'    "is_active": {_fmt_val(lesson["is_active"])},')

    lines += [
        "}",
        "",
        "",
        "async def seed():",
        "    async with SessionLocal() as session:",
        "        existing = await session.execute(",
        '            select(CourseLesson).where(CourseLesson.lesson_code == LESSON["lesson_code"])',
        "        )",
        "        if existing.scalar_one_or_none():",
        "            print(f\"Lesson {LESSON['lesson_code']} already exists, skipping.\")",
        "            return",
        "",
        "        lesson = CourseLesson(**LESSON)",
        "        session.add(lesson)",
        "        await session.commit()",
        "        print(f\"\\u2705 Lesson {LESSON['lesson_code']} \\u2014 {LESSON['title']} created.\")",
        "",
        "",
        'if __name__ == "__main__":',
        "    asyncio.run(seed())",
        "",
    ]
    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    seed_files = sorted(SCRIPTS_DIR.glob("seed_hsk1_lesson_*.py"))
    if not seed_files:
        print("No seed files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(seed_files)} seed files.\n")

    for idx, fp in enumerate(seed_files, 1):
        print(f"[{idx:2d}/{len(seed_files)}] {fp.name}")
        lesson = extract_lesson(fp)
        total = count_translations(lesson)
        print(f"         {total} translation calls needed")

        ctr = Counter(total)
        transformed = transform_lesson(lesson, ctr)
        print()   # newline after progress bar

        code = generate_file(transformed)
        fp.write_text(code, encoding="utf-8")
        print(f"         ✅ written\n")

    print(f"Done! All {len(seed_files)} files updated.")


if __name__ == "__main__":
    main()
