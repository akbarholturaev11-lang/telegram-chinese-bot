from aiogram import Router, F
from aiogram.dispatcher.event.bases import SkipHandler
from aiogram.types import Message

from app.repositories.user_repo import UserRepository
from app.services.payment_service import PaymentService
from app.services.admin_notify_service import AdminNotifyService
from app.bot.utils.i18n import t


router = Router()


@router.message(F.photo)
async def payment_screenshot_handler(message: Message, session):
    user_repo = UserRepository(session)
    payment_service = PaymentService(session)
    admin_notify_service = AdminNotifyService()

    user = await user_repo.get_by_telegram_id(message.from_user.id)
    if not user:
        raise SkipHandler()

    lang = user.language if user.language else "ru"
    photo = message.photo[-1]
    screenshot_file_id = photo.file_id

    plan_type = user.selected_plan_type
    if not plan_type:
        latest_pending = await payment_service.get_latest_pending_payment(message.from_user.id)
        if latest_pending:
            plan_type = latest_pending.plan_type

    # Agar bu checkout/payment holati bo'lmasa, image handlerga o'tkazamiz
    if not plan_type:
        raise SkipHandler()

    payment, status_or_error = await payment_service.attach_or_create_payment_screenshot(
        telegram_id=message.from_user.id,
        plan_type=plan_type,
        screenshot_file_id=screenshot_file_id,
    )

    if not payment:
        await message.answer(t(status_or_error, lang))
        return

    await user_repo.set_selected_plan_type(user, None)
    await session.commit()

    await admin_notify_service.notify_payment_review(
        bot=message.bot,
        payment=payment,
        user=user,
    )

    await message.answer(t("payment_screenshot_received", lang))
