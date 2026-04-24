from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bot.utils.i18n import t


def _retry_keyboard(lang: str) -> InlineKeyboardMarkup:
    label = {
        "uz": "🔄 Qayta yuborish",
        "tj": "🔄 Аз нав фиристодан",
        "ru": "🔄 Отправить снова",
    }.get(lang, "🔄 Qayta yuborish")

    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=label,
                callback_data="payment:retry",
            )
        ]]
    )


class PaymentNotifyService:
    async def notify_payment_approved(self, bot: Bot, user) -> None:
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
        reason: str = None,
        plan_type: str = None,
    ) -> None:
        if not user:
            return
        lang = user.language if user.language else "ru"

        base_text = t("user_payment_rejected", lang)

        if reason:
            reason_prefix = {
                "uz": f"\n\nSabab: {reason}",
                "tj": f"\n\nСабаб: {reason}",
                "ru": f"\n\nПричина: {reason}",
            }.get(lang, f"\n\nSabab: {reason}")
            text = base_text + reason_prefix
        else:
            text = base_text

        try:
            await bot.send_message(
                chat_id=user.telegram_id,
                text=text,
                reply_markup=_retry_keyboard(lang),
            )
        except Exception:
            pass
