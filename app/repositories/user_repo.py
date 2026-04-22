from datetime import datetime, timezone, timedelta, date
from typing import Optional
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_by_referral_code(self, referral_code: str) -> Optional[User]:
        result = await self.session.execute(
            select(User).where(User.referral_code == referral_code)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        telegram_id: int,
        full_name: Optional[str] = None,
        language: str = "tj",
        level: str = "beginner",
    ) -> User:
        now = datetime.now(timezone.utc)

        user = User(
            telegram_id=telegram_id,
            full_name=full_name,
            language=language,
            level=level,
            learning_mode="qa",
            status="trial",
            payment_status="none",
            question_limit=5,
            questions_used=0,
            bonus_questions=0,
            bonus_questions_used=0,
            referral_code=self._generate_referral_code(),
            start_date=now,
            end_date=now + timedelta(days=3),
            discount_referral_count=0,
            discount_eligible=False,
            discount_used=False,
            created_at=now,
            last_active_at=now,
        )
        self.session.add(user)
        await self.session.flush()
        return user

    async def update_last_active(self, user: User) -> None:
        user.last_active_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def set_referred_by(
        self,
        user: User,
        referrer_telegram_id: int,
    ) -> None:
        # already set → skip
        if user.referrer_id:
            return

        user.referred_by_telegram_id = referrer_telegram_id

        referrer = await self.get_by_telegram_id(referrer_telegram_id)
        if referrer:
            user.referrer_id = referrer.id

        await self.session.flush()

    async def add_bonus_questions(
        self,
        user: User,
        amount: int,
    ) -> None:
        user.bonus_questions += amount
        await self.session.flush()

    async def consume_bonus_question(
        self,
        user: User,
    ) -> None:
        user.bonus_questions_used += 1
        await self.session.flush()

    def get_bonus_balance(self, user: User) -> int:
        return max(user.bonus_questions - user.bonus_questions_used, 0)

    async def start_discount_offer(
        self,
        user: User,
    ) -> None:
        user.discount_offer_started_at = datetime.now(timezone.utc)
        user.discount_referral_count = 0
        user.discount_eligible = False
        await self.session.flush()

    async def increment_discount_referral_count(
        self,
        user: User,
        amount: int = 1,
    ) -> None:
        user.discount_referral_count += amount
        if user.discount_referral_count >= 3 and not user.discount_used:
            user.discount_eligible = True
        await self.session.flush()

    async def mark_discount_used(
        self,
        user: User,
    ) -> None:
        user.discount_used = True
        user.discount_eligible = False
        await self.session.flush()

    async def ensure_referral_code(self, user: User) -> None:
        if user.referral_code:
            return

        user.referral_code = self._generate_referral_code()
        await self.session.flush()

    async def was_daily_limit_offer_sent_today(self, user: User) -> bool:
        if not user.daily_limit_offer_sent_at:
            return False

        return user.daily_limit_offer_sent_at.date() == datetime.now(timezone.utc).date()

    async def mark_daily_limit_offer_sent(self, user: User) -> None:
        user.daily_limit_offer_sent_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def set_discount_progress_message(
        self,
        user: User,
        chat_id: int,
        message_id: int,
    ) -> None:
        user.discount_progress_chat_id = chat_id
        user.discount_progress_message_id = message_id
        await self.session.flush()

    async def clear_discount_progress_message(
        self,
        user: User,
    ) -> None:
        user.discount_progress_chat_id = None
        user.discount_progress_message_id = None
        await self.session.flush()

    async def set_selected_plan_type(
        self,
        user: User,
        plan_type: Optional[str],
    ) -> None:
        user.selected_plan_type = plan_type
        await self.session.flush()

    async def get_all_users(self) -> list[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    async def get_filtered_users(
        self,
        language: Optional[str] = None,
        status: Optional[str] = None,
        level: Optional[str] = None,
    ) -> list[User]:
        query = select(User)
        if language:
            query = query.where(User.language == language)
        if status:
            query = query.where(User.status == status)
        if level:
            query = query.where(User.level == level)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def list_active_users_expiring_on(
        self,
        target_date: date,
    ) -> list[User]:
        result = await self.session.execute(
            select(User).where(User.status == "active")
        )
        users = list(result.scalars().all())
        return [
            user for user in users
            if user.end_date and user.end_date.date() == target_date
        ]

    def _generate_referral_code(self) -> str:
        return secrets.token_hex(4)
