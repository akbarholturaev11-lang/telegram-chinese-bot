from datetime import datetime, timedelta, timezone
from typing import Optional

from aiogram import Bot
from sqlalchemy import select

from app.bot.keyboards.feedback import feedback_dislike_keyboard, feedback_like_keyboard
from app.bot.utils.i18n import t
from app.db.models.bot_feedback import BotFeedback
from app.db.models.user import User
from app.repositories.bot_feedback_repo import BotFeedbackRepository
from app.repositories.user_repo import UserRepository


FEEDBACK_PERIOD_DAYS = 30
FEEDBACK_JOIN_DELAY = timedelta(days=1)
FEEDBACK_RETRY_AFTER = timedelta(hours=24)
FEEDBACK_REWARD_DAYS = 1


class BotFeedbackService:
    def __init__(self, session):
        self.session = session
        self.feedback_repo = BotFeedbackRepository(session)
        self.user_repo = UserRepository(session)

    def _aware(self, value: Optional[datetime]) -> Optional[datetime]:
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    def _is_prompt_due(self, feedback: BotFeedback, now: datetime) -> bool:
        prompted_at = self._aware(feedback.prompted_at)
        return prompted_at is None or now - prompted_at >= FEEDBACK_RETRY_AFTER

    async def _get_or_create_due_feedback(
        self,
        user: User,
        now: datetime,
    ) -> Optional[BotFeedback]:
        pending = await self.feedback_repo.get_latest_pending_by_user(user.id)
        if pending:
            return pending

        recent_since = now - timedelta(days=FEEDBACK_PERIOD_DAYS)
        if await self.feedback_repo.has_completed_since(user.id, recent_since):
            return None

        return await self.feedback_repo.create_pending(user)

    async def send_due_feedback_requests(self, bot: Bot) -> int:
        now = datetime.now(timezone.utc)
        oldest_join_time = now - FEEDBACK_JOIN_DELAY

        result = await self.session.execute(
            select(User)
            .where(User.created_at <= oldest_join_time)
            .where(User.status != "blocked")
            .order_by(User.created_at.asc())
        )
        users = list(result.scalars().all())

        sent_count = 0
        for user in users:
            feedback = await self._get_or_create_due_feedback(user, now)
            if not feedback or not self._is_prompt_due(feedback, now):
                continue

            lang = user.language if user.language else "ru"
            if feedback.liked_code and not feedback.disliked_code:
                text = t("feedback_dislike_question", lang)
                keyboard = feedback_dislike_keyboard(feedback.id, lang)
            else:
                text = t("feedback_like_question", lang)
                keyboard = feedback_like_keyboard(feedback.id, lang)

            message_id = None
            try:
                msg = await bot.send_message(
                    chat_id=user.telegram_id,
                    text=text,
                    reply_markup=keyboard,
                )
                message_id = msg.message_id
                sent_count += 1
            except Exception:
                pass

            await self.feedback_repo.mark_prompt_sent(feedback, message_id)

        await self.session.commit()
        return sent_count

    async def grant_feedback_reward(
        self,
        user: User,
        feedback: BotFeedback,
    ) -> None:
        if feedback.reward_granted_at:
            return

        now = datetime.now(timezone.utc)
        current_end = self._aware(user.end_date)
        base_end = current_end if user.status == "active" and current_end and current_end > now else now

        if user.status != "active" or not current_end or current_end <= now:
            user.start_date = now

        user.status = "active"
        user.end_date = base_end + timedelta(days=FEEDBACK_REWARD_DAYS)
        user.questions_used = 0
        user.bonus_questions_used = 0
        user.last_limit_reset_at = now
        user.expiry_reminder_sent_at = None
        user.selected_plan_type = None
        user.pending_checkout_msg_id = None

        await self.feedback_repo.mark_reward_granted(feedback)
        await self.session.flush()

    async def finish_feedback(
        self,
        feedback: BotFeedback,
        user: User,
    ) -> None:
        await self.feedback_repo.complete(feedback)
        await self.grant_feedback_reward(user, feedback)
