from typing import Optional

from app.repositories.payment_repo import PaymentRepository
from app.repositories.user_repo import UserRepository


PLAN_PRICES = {
    "10_days": 29,
    "1_month": 89,
}

DISCOUNT_PERCENT = 20


class PaymentService:
    def __init__(self, session):
        self.session = session
        self.payment_repo = PaymentRepository(session)
        self.user_repo = UserRepository(session)

    def get_plan_price(self, plan_type: str) -> Optional[int]:
        return PLAN_PRICES.get(plan_type)

    def calculate_discounted_price(self, amount: int) -> int:
        discounted = amount * (100 - DISCOUNT_PERCENT) / 100
        return int(round(discounted))

    async def get_checkout_info(
        self,
        user,
        plan_type: str,
    ):
        base_amount = self.get_plan_price(plan_type)
        if base_amount is None:
            return None

        discount_applied = bool(user.discount_eligible and not user.discount_used)

        if user.payment_method in ["alipay", "wechat"]:
            if plan_type == "10_days":
                base_amount = 29
            elif plan_type == "1_month":
                base_amount = 66

            currency = "¥"
        else:
            if plan_type == "10_days":
                base_amount = 29
            elif plan_type == "1_month":
                base_amount = 89

            currency = "somoni"

        final_amount = (
            self.calculate_discounted_price(base_amount)
            if discount_applied
            else base_amount
        )

        return {
            "plan_type": plan_type,
            "base_amount": base_amount,
            "final_amount": final_amount,
            "currency": currency,
            "discount_applied": discount_applied,
        }

    async def create_pending_payment(
        self,
        telegram_id: int,
        plan_type: str,
        screenshot_file_id: Optional[str] = None,
    ):
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return None, "access_start_first"

        checkout_info = await self.get_checkout_info(
            user=user,
            plan_type=plan_type,
        )
        if not checkout_info:
            return None, "payment_invalid_plan"

        payment = await self.payment_repo.create(
            user_telegram_id=telegram_id,
            plan_type=plan_type,
            amount=checkout_info["final_amount"],
            currency=checkout_info["currency"],
            screenshot_file_id=screenshot_file_id,
        )
        await self.session.commit()
        return payment, ""

    async def get_latest_pending_payment(
        self,
        telegram_id: int,
    ):
        return await self.payment_repo.get_latest_pending_by_user(telegram_id)

    async def attach_or_create_payment_screenshot(
        self,
        telegram_id: int,
        plan_type: str,
        screenshot_file_id: str,
    ):
        pending_payment = await self.payment_repo.get_latest_pending_by_user(telegram_id)

        if pending_payment:
            await self.payment_repo.update_screenshot(pending_payment, screenshot_file_id)
            await self.session.commit()
            return pending_payment, "updated"

        payment, error_key = await self.create_pending_payment(
            telegram_id=telegram_id,
            plan_type=plan_type,
            screenshot_file_id=screenshot_file_id,
        )
        if error_key:
            return None, error_key

        return payment, "created"
