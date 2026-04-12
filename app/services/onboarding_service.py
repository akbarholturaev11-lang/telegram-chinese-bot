from typing import Optional, Tuple

from app.repositories.user_repo import UserRepository
from app.db.models.user import User
from app.services.referral_service import ReferralService


class OnboardingService:
    def __init__(self, session):
        self.user_repo = UserRepository(session)
        self.referral_service = ReferralService(session)

    async def get_or_create_user(
        self,
        telegram_id: int,
        full_name: Optional[str] = None,
        referral_code: Optional[str] = None,
    ) -> Tuple[User, bool]:
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if user:
            return user, False

        user = await self.user_repo.create(
            telegram_id=telegram_id,
            full_name=full_name,
            language="tj",
            level="beginner",
        )

        await self.referral_service.attach_referral_if_needed(
            invited_user_telegram_id=telegram_id,
            referral_code=referral_code,
        )

        user = await self.user_repo.get_by_telegram_id(telegram_id)
        return user, True
