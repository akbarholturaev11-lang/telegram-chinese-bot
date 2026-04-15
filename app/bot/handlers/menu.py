from aiogram import Router, F
from aiogram.types import Message

from app.repositories.user_repo import UserRepository
from app.bot.keyboards.subscription import payment_method_keyboard
from app.bot.utils.i18n import t


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
        t("payment_method_choose", lang),
        reply_markup=payment_method_keyboard(lang),
        parse_mode="HTML",
    )
