from aiogram import Router, F
from aiogram.types import Message

from app.repositories.user_repo import UserRepository
from app.bot.handlers.subscription import build_subscription_main_text_for_user
from app.bot.keyboards.subscription import subscription_main_keyboard


router = Router()


@router.message(F.text.in_([
    "💳 Обуна",
    "💳 Подписка",
    "💳 Obuna",
]))
async def handle_subscription_button(message: Message, session):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(message.from_user.id)

    if not user:
        return

    lang = user.language if user.language else "ru"

    await message.answer(
        build_subscription_main_text_for_user(user, lang),
        reply_markup=subscription_main_keyboard(lang),
        disable_web_page_preview=True,
    )
