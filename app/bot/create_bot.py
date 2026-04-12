from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.bot.handlers.start import router as start_router
from app.bot.handlers.commands import router as commands_router
from app.bot.handlers.referral import router as referral_router
from app.bot.handlers.subscription import router as subscription_router
from app.bot.handlers.menu import router as menu_router
from app.bot.handlers.payments import router as payments_router
from app.bot.handlers.admin_payments import router as admin_payments_router
from app.bot.handlers.messages import router as messages_router
from app.bot.handlers.course import router as course_router


def create_bot(settings):
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(commands_router)
    dp.include_router(referral_router)
    dp.include_router(subscription_router)
    dp.include_router(menu_router)
    dp.include_router(payments_router)
    dp.include_router(admin_payments_router)
    dp.include_router(course_router)
    dp.include_router(messages_router)

    return bot, dp

import asyncio
from app.config import settings


async def main():
    bot, dp = create_bot(settings)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
