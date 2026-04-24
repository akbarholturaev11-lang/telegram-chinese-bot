from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.payment import Payment


class PaymentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_telegram_id: int,
        plan_type: str,
        amount: int,
        currency: str = "somoni",
        screenshot_file_id: Optional[str] = None,
    ) -> Payment:
        payment = Payment(
            user_telegram_id=user_telegram_id,
            plan_type=plan_type,
            amount=amount,
            currency=currency,
            payment_status="pending",
            screenshot_file_id=screenshot_file_id,
            submitted_at=datetime.now(timezone.utc),
        )
        self.session.add(payment)
        await self.session.flush()
        return payment

    async def get_by_id(self, payment_id: int) -> Optional[Payment]:
        result = await self.session.execute(
            select(Payment).where(Payment.id == payment_id)
        )
        return result.scalar_one_or_none()

    async def get_latest_pending_by_user(
        self,
        user_telegram_id: int,
    ) -> Optional[Payment]:
        result = await self.session.execute(
            select(Payment)
            .where(Payment.user_telegram_id == user_telegram_id)
            .where(Payment.payment_status == "pending")
            .order_by(Payment.submitted_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def has_pending_by_user(
        self,
        user_telegram_id: int,
    ) -> bool:
        result = await self.session.execute(
            select(Payment.id)
            .where(Payment.user_telegram_id == user_telegram_id)
            .where(Payment.payment_status == "pending")
            .limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def list_by_user(
        self,
        user_telegram_id: int,
        limit: int = 20,
    ) -> List[Payment]:
        result = await self.session.execute(
            select(Payment)
            .where(Payment.user_telegram_id == user_telegram_id)
            .order_by(Payment.submitted_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update_screenshot(
        self,
        payment: Payment,
        screenshot_file_id: str,
    ) -> None:
        payment.screenshot_file_id = screenshot_file_id
        payment.submitted_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def approve(
        self,
        payment: Payment,
        admin_comment: Optional[str] = None,
    ) -> None:
        payment.payment_status = "approved"
        payment.admin_comment = admin_comment
        payment.reviewed_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def reject(
        self,
        payment: Payment,
        admin_comment: Optional[str] = None,
    ) -> None:
        payment.payment_status = "rejected"
        payment.admin_comment = admin_comment
        payment.reviewed_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def count_pending(self) -> int:
        from sqlalchemy import func
        result = await self.session.execute(
            select(func.count()).where(Payment.payment_status == "pending")
        )
        return result.scalar() or 0
