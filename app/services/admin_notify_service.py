from aiogram import Bot

from app.config import settings
from app.bot.keyboards.admin_review import admin_payment_review_keyboard
from app.bot.utils.i18n import t


class AdminNotifyService:
    def __init__(self):
        self.admin_ids = self._parse_admin_ids(settings.ADMIN_IDS)

    def _parse_admin_ids(self, raw_value: str):
        if not raw_value:
            return []

        result = []
        for item in raw_value.split(","):
            item = item.strip()
            if not item:
                continue
            try:
                result.append(int(item))
            except ValueError:
                continue
        return result

    def build_payment_review_text(
        self,
        lang: str,
        telegram_id: int,
        full_name: str,
        plan_type: str,
        amount: int,
        currency: str,
        payment_id: int,
    ) -> str:
        return (
            f"{t('admin_payment_new_request', lang)}\n\n"
            f"{t('admin_payment_id', lang)}: {payment_id}\n"
            f"{t('admin_payment_user_id', lang)}: {telegram_id}\n"
            f"{t('admin_payment_full_name', lang)}: {full_name}\n"
            f"{t('admin_payment_plan', lang)}: {plan_type}\n"
            f"{t('admin_payment_amount', lang)}: {amount} {currency}"
        )

    async def notify_payment_review(
        self,
        bot: Bot,
        payment,
        user,
    ) -> None:
        if not self.admin_ids:
            return

        admin_lang = "uz"

        text = self.build_payment_review_text(
            lang=admin_lang,
            telegram_id=user.telegram_id,
            full_name=user.full_name or "-",
            plan_type=payment.plan_type,
            amount=payment.amount,
            currency=payment.currency,
            payment_id=payment.id,
        )

        keyboard = admin_payment_review_keyboard(payment.id, admin_lang)

        for admin_id in self.admin_ids:
            try:
                if payment.screenshot_file_id:
                    await bot.send_photo(
                        chat_id=admin_id,
                        photo=payment.screenshot_file_id,
                        caption=text,
                        reply_markup=keyboard,
                    )
                else:
                    await bot.send_message(
                        chat_id=admin_id,
                        text=text,
                        reply_markup=keyboard,
                    )
            except Exception:
                pass
