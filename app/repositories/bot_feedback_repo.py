from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.bot_feedback import BotFeedback
from app.db.models.user import User


class BotFeedbackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, feedback_id: int) -> Optional[BotFeedback]:
        result = await self.session.execute(
            select(BotFeedback).where(BotFeedback.id == feedback_id)
        )
        return result.scalar_one_or_none()

    async def get_latest_pending_by_user(self, user_id: int) -> Optional[BotFeedback]:
        result = await self.session.execute(
            select(BotFeedback)
            .where(BotFeedback.user_id == user_id)
            .where(BotFeedback.status == "pending")
            .order_by(BotFeedback.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def has_completed_since(self, user_id: int, since: datetime) -> bool:
        result = await self.session.execute(
            select(BotFeedback.id)
            .where(BotFeedback.user_id == user_id)
            .where(BotFeedback.status == "completed")
            .where(BotFeedback.completed_at >= since)
            .limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def create_pending(self, user: User) -> BotFeedback:
        now = datetime.now(timezone.utc)
        feedback = BotFeedback(
            user_id=user.id,
            telegram_id=user.telegram_id,
            language=user.language or "ru",
            status="pending",
            created_at=now,
            updated_at=now,
        )
        self.session.add(feedback)
        await self.session.flush()
        return feedback

    async def mark_prompt_sent(
        self,
        feedback: BotFeedback,
        message_id: Optional[int],
    ) -> None:
        now = datetime.now(timezone.utc)
        feedback.prompt_message_id = message_id
        feedback.prompted_at = now
        feedback.updated_at = now
        await self.session.flush()

    async def save_liked(
        self,
        feedback: BotFeedback,
        code: str,
        text: str,
    ) -> None:
        feedback.liked_code = code
        feedback.liked_text = text
        feedback.updated_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def save_disliked(
        self,
        feedback: BotFeedback,
        code: str,
        text: str,
    ) -> None:
        feedback.disliked_code = code
        feedback.disliked_text = text
        feedback.updated_at = datetime.now(timezone.utc)
        await self.session.flush()

    async def complete(self, feedback: BotFeedback) -> None:
        now = datetime.now(timezone.utc)
        feedback.status = "completed"
        feedback.completed_at = now
        feedback.updated_at = now
        await self.session.flush()

    async def mark_reward_granted(self, feedback: BotFeedback) -> None:
        now = datetime.now(timezone.utc)
        feedback.reward_granted_at = now
        feedback.updated_at = now
        await self.session.flush()
