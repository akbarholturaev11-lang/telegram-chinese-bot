#!/usr/bin/env python3
"""Update existing HSK1 lessons in DB with multilingual data from seed files.

Run once after translating seed files:
    python scripts/update_hsk1_lessons.py
"""

import asyncio
import json
from pathlib import Path

from sqlalchemy import select

from app.db.session import async_session_maker as SessionLocal
from app.db.models.course_lessons import CourseLesson

SCRIPTS_DIR = Path(__file__).parent


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


async def update_all():
    seed_files = sorted(SCRIPTS_DIR.glob("seed_hsk1_lesson_*.py"))
    print(f"Found {len(seed_files)} seed files.\n")

    async with SessionLocal() as session:
        for fp in seed_files:
            lesson_data = extract_lesson(fp)
            lesson_code = lesson_data["lesson_code"]

            # Ensure goal/intro_text are stored as JSON strings, not Python dicts
            for field in ("goal", "intro_text"):
                val = lesson_data.get(field)
                if isinstance(val, dict):
                    lesson_data[field] = json.dumps(val, ensure_ascii=False)

            existing = await session.execute(
                select(CourseLesson).where(CourseLesson.lesson_code == lesson_code)
            )
            row = existing.scalar_one_or_none()

            if row:
                for field, val in lesson_data.items():
                    setattr(row, field, val)
                print(f"✅ Updated  {lesson_code}")
            else:
                row = CourseLesson(**lesson_data)
                session.add(row)
                print(f"➕ Inserted {lesson_code}")

        await session.commit()

    print("\nDone! All lessons updated.")


if __name__ == "__main__":
    asyncio.run(update_all())
