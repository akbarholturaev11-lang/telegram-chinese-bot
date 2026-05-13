from datetime import datetime, timezone, timedelta
from typing import Optional

from app.repositories.user_repo import UserRepository


PLAN_DURATIONS = {
    "10_days": 10,
    "1_month": 30,
}


class SubscriptionService:
    def __init__(self, session):
        self.session = session
        self.user_repo = UserRepository(session)

    async def activate_plan(
        self,
        telegram_id: int,
        plan_type: str,
        discount_source: Optional[str] = None,
    ) -> bool:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False

        duration_days = PLAN_DURATIONS.get(plan_type)
        if not duration_days:
            return False

        now = datetime.now(timezone.utc)

        user.status = "active"
        user.payment_status = "approved"
        user.start_date = now
        user.end_date = now + timedelta(days=duration_days)
        user.selected_plan_type = None
        user.expiry_reminder_sent_at = None

        if discount_source == "referral" and user.discount_eligible and not user.discount_used:
            user.discount_used = True
            user.discount_eligible = False

        await self.session.flush()
        return True
