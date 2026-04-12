import asyncio
from app.db.session import SessionLocal
from sqlalchemy import text

async def clean():
    async with SessionLocal() as session:

        tables = [
            "course_attempts",
            "course_progress",
            "referrals",
            "messages",
            "payments",
            "users"
        ]

        for table in tables:
            try:
                await session.execute(text(f"DELETE FROM {table}"))
                print(f"cleared: {table}")
            except Exception as e:
                print(f"skip: {table} ({e})")

        await session.commit()
        print("🔥 FULL CLEAN DONE")

asyncio.run(clean())
