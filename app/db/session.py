from sqlalchemy import inspect, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Backward-compatible alias for older middleware and seed scripts.
SessionLocal = async_session_maker

from app.db.base import Base

_BOOTSTRAP_COLUMNS: dict[str, dict[str, str]] = {
    "users": {
        "pending_checkout_msg_id": "INTEGER",
    },
    "payments": {
        "checkout_msg_id": "INTEGER",
        "screenshot_msg_id": "INTEGER",
        "waiting_msg_id": "INTEGER",
        "payment_method": "VARCHAR(16)",
        "base_amount": "INTEGER",
        "discount_source": "VARCHAR(32) DEFAULT 'none' NOT NULL",
        "discount_percent": "INTEGER DEFAULT 0 NOT NULL",
        "discount_campaign_id": "INTEGER",
        "discount_title": "VARCHAR(120)",
        "discount_details": "TEXT",
    },
    "discount_campaigns": {
        "title_tj": "VARCHAR(180)",
        "title_ru": "VARCHAR(180)",
        "title_uz": "VARCHAR(180)",
    },
}


async def _ensure_bootstrap_columns(conn) -> None:
    # `create_all()` creates missing tables but does not add new columns to
    # existing tables, so we patch legacy Railway databases here.
    for table_name, columns in _BOOTSTRAP_COLUMNS.items():
        existing_columns = await conn.run_sync(
            lambda sync_conn, table_name=table_name: {
                column["name"]
                for column in inspect(sync_conn).get_columns(table_name)
            }
        )
        for column_name, column_type in columns.items():
            if column_name in existing_columns:
                continue
            try:
                await conn.execute(
                    text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                )
            except ProgrammingError as exc:
                if "already exists" not in str(exc).lower():
                    raise


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _ensure_bootstrap_columns(conn)
