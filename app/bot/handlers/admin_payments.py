from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.repositories.payment_repo import PaymentRepository
from app.repositories.user_repo import UserRepository
from app.services.subscription_service import SubscriptionService
from app.services.payment_notify_service import PaymentNotifyService
from app.bot.utils.i18n import t


router = Router()


@router.callback_query(F.data.startswith("admin_payment:approve:"))
async def admin_payment_approve_handler(callback: CallbackQuery, session):
    payment_repo = PaymentRepository(session)
    user_repo = UserRepository(session)
    subscription_service = SubscriptionService(session)
    payment_notify_service = PaymentNotifyService()

    payment_id = int(callback.data.split(":")[2])
    payment = await payment_repo.get_by_id(payment_id)
    if not payment:
        await callback.answer(t("admin_payment_not_found", "uz"), show_alert=True)
        return

    if payment.payment_status != "pending":
        await callback.answer(t("admin_payment_already_reviewed", "uz"), show_alert=True)
        return

    await payment_repo.approve(payment, admin_comment="approved by admin")
    await subscription_service.activate_plan(
        telegram_id=payment.user_telegram_id,
        plan_type=payment.plan_type,
    )

    user = await user_repo.get_by_telegram_id(payment.user_telegram_id)
    await session.commit()

    await callback.answer(t("admin_payment_approved", "uz"), show_alert=True)
    await callback.message.edit_reply_markup(reply_markup=None)

    await payment_notify_service.notify_payment_approved(
        bot=callback.bot,
        user=user,
    )


@router.callback_query(F.data.startswith("admin_payment:reject:"))
async def admin_payment_reject_handler(callback: CallbackQuery, session):
    payment_repo = PaymentRepository(session)
    user_repo = UserRepository(session)
    payment_notify_service = PaymentNotifyService()

    payment_id = int(callback.data.split(":")[2])
    payment = await payment_repo.get_by_id(payment_id)
    if not payment:
        await callback.answer(t("admin_payment_not_found", "uz"), show_alert=True)
        return

    if payment.payment_status != "pending":
        await callback.answer(t("admin_payment_already_reviewed", "uz"), show_alert=True)
        return

    await payment_repo.reject(payment, admin_comment="rejected by admin")
    user = await user_repo.get_by_telegram_id(payment.user_telegram_id)
    if user:
        await user_repo.set_selected_plan_type(user, payment.plan_type)
    await session.commit()

    await callback.answer(t("admin_payment_rejected", "uz"), show_alert=True)
    await callback.message.edit_reply_markup(reply_markup=None)

    await payment_notify_service.notify_payment_rejected(
        bot=callback.bot,
        user=user,
    )
