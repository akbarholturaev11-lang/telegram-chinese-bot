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
            if item:
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
        ai_result: dict = None,
        pending_count: int = 0,
    ) -> str:
        plan_label = "10 kunlik" if plan_type == "10_days" else "1 oylik"

        lines = [
            f"💳 Yangi to'lov so'rovi",
            f"",
            f"👤 {full_name} ({telegram_id})",
            f"📦 Tarif: {plan_label} — {amount} {currency}",
            f"🆔 To'lov ID: #{payment_id}",
        ]

        if pending_count > 1:
            lines.append(f"⏳ Navbatda: {pending_count} ta to'lov")

        if ai_result:
            verdict = ai_result.get("verdict", "unknown")
            ai_amount = ai_result.get("amount")
            ai_currency = ai_result.get("currency", "")
            date_str = ai_result.get("date", "unknown")
            pay_sys = ai_result.get("payment_system", "unknown")
            amount_match = ai_result.get("amount_match", False)
            reason = ai_result.get("reason", "")

            if verdict == "trusted":
                verdict_icon = "✅"
            elif verdict == "suspicious":
                verdict_icon = "⚠️"
            else:
                verdict_icon = "❌"

            lines.append(f"")
            lines.append(f"🤖 AI tekshiruvi: {verdict_icon} {verdict.upper()}")

            if ai_amount is not None:
                match_icon = "✅" if amount_match else "❌"
                lines.append(f"  Summa: {ai_amount} {ai_currency} {match_icon}")
            else:
                lines.append(f"  Summa: aniqlanmadi ❌")

            lines.append(f"  Sana: {date_str}")
            lines.append(f"  To'lov tizimi: {pay_sys}")

            if reason and verdict != "trusted":
                lines.append(f"  Sabab: {reason}")

        return "\n".join(lines)

    async def notify_payment_review(
        self,
        bot: Bot,
        payment,
        user,
        ai_result: dict = None,
        pending_count: int = 1,
    ) -> None:
        if not self.admin_ids:
            return

        text = self.build_payment_review_text(
            lang="uz",
            telegram_id=user.telegram_id,
            full_name=user.full_name or "-",
            plan_type=payment.plan_type,
            amount=payment.amount,
            currency=payment.currency,
            payment_id=payment.id,
            ai_result=ai_result,
            pending_count=pending_count,
        )

        keyboard = admin_payment_review_keyboard(payment.id, "uz")

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
