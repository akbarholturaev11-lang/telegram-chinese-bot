from aiogram import Bot

from app.bot.utils.i18n import t


class PaymentNotifyService:
    async def notify_payment_approved(
        self,
        bot: Bot,
        user,
    ) -> None:
        if not user:
            return

        lang = user.language if user.language else "ru"

        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text=t("user_payment_approved", lang),
            )
        except Exception:
            pass

    async def notify_payment_rejected(
        self,
        bot: Bot,
        user,
    ) -> None:
        if not user:
            return

        lang = user.language if user.language else "ru"

        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text=t("user_payment_rejected", lang),
            )
        except Exception:
            pass
