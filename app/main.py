import asyncio
import contextlib
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.bot.create_bot import create_bot
from app.bot.middlewares.db_session import DbSessionMiddleware


bot, dp = create_bot(settings)
dp.update.middleware(DbSessionMiddleware())


@asynccontextmanager
async def lifespan(app: FastAPI):
    polling_task = asyncio.create_task(dp.start_polling(bot))
    try:
        yield
    finally:
        polling_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await polling_task
        await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}
