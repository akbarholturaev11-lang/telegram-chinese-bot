from datetime import datetime, timezone
from typing import Tuple

from app.repositories.user_repo import UserRepository
from app.repositories.message_repo import MessageRepository
from app.repositories.payment_repo import PaymentRepository

class AccessService:
    def __init__(self, session):
        self.session = session
        self.user_repo = UserRepository(session)
        self.message_repo = MessageRepository(session)
        self.payment_repo = PaymentRepository(session)

    def _today_utc_date(self):
        return datetime.now(timezone.utc).date()

    def _is_date_expired(self, dt) -> bool:
        if not dt:
            return False
        if hasattr(dt, "date"):
            return dt.date() < self._today_utc_date()
        return dt < self._today_utc_date()

    async def can_use_text_ai(self, telegram_id: int) -> Tuple[bool, str]:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False, "access_start_first"

        if user.status == "blocked":
            return False, "access_blocked"

        if user.status != "active":
            has_pending_payment = await self.payment_repo.has_pending_by_user(telegram_id)
            if has_pending_payment:
                return False, "access_payment_pending_review"

        if user.status == "active":
            if self._is_date_expired(user.end_date):
                return False, "access_subscription_expired"
            return True, ""

        if user.status == "expired":
            return False, "access_subscription_expired"

        from datetime import datetime, timedelta, timezone    

        if user.status == "trial":
            now = datetime.now(timezone.utc)

            if user.last_limit_reset_at is None or now - user.last_limit_reset_at >= timedelta(days=1):
                user.questions_used = 0
                user.bonus_questions_used = 0
                user.last_limit_reset_at = now
                await self.user_repo.session.commit()

            if user.questions_used >= user.question_limit:
                bonus_balance = self.user_repo.get_bonus_balance(user)
                if bonus_balance <= 0:
                    return False, "access_daily_limit_reached"

            return True, ""

        return False, "access_start_first"

    async def can_use_image_ai(self, telegram_id: int) -> Tuple[bool, str]:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return False, "access_start_first"

        if user.status == "blocked":
            return False, "access_blocked"

        if user.status != "active":
            has_pending_payment = await self.payment_repo.has_pending_by_user(telegram_id)
            if has_pending_payment:
                return False, "access_payment_pending_review"

        if user.status == "active":
            if self._is_date_expired(user.end_date):
                return False, "access_subscription_expired"
            return True, ""

        if user.status == "expired":
            return False, "access_subscription_expired"

        if user.status == "trial":

            from datetime import datetime, timedelta, timezone
            now = datetime.now(timezone.utc)
        
            if not user.last_limit_reset_at:
                user.last_limit_reset_at = now
                user.questions_used = 0
            elif now - user.last_limit_reset_at >= timedelta(days=1):
                user.last_limit_reset_at = now
                user.questions_used = 0

            if self._is_date_expired(user.end_date):
                return False, "access_trial_expired"

            today_image_count = await self.message_repo.count_user_messages_today(
                user_id=user.id,
                content_type="image",
            )
            if today_image_count >= 1:
                return False, "access_daily_image_limit_reached"

            return True, ""

        return False, "access_start_first"

    async def consume_one_question(self, telegram_id: int) -> None:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return

        from datetime import datetime, timedelta, timezone

        if user.status == "trial":

            now = datetime.now(timezone.utc)

            if not user.last_limit_reset_at:
                user.last_limit_reset_at = now
                user.questions_used = 0
            elif now - user.last_limit_reset_at >= timedelta(days=1):
                user.last_limit_reset_at = now
                user.questions_used = 0

            if user.questions_used >= user.question_limit:
                bonus = self.user_repo.get_bonus_balance(user)
                if bonus > 0:
                    await self.user_repo.consume_bonus_question(user)
                else:
                    return
 
        user.questions_used += 1
        await self.session.flush()
