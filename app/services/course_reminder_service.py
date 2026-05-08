from datetime import datetime, timezone, timedelta

from aiogram import Bot
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.course_progress import CourseProgress
from app.db.models.user import User
from app.bot.utils.i18n import t


class CourseReminderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def send_due_reminders(self, bot: Bot) -> None:
        now_utc = datetime.now(timezone.utc)

        result = await self.session.execute(
            select(CourseProgress, User)
            .join(User, CourseProgress.user_id == User.id)
            .where(CourseProgress.reminder_enabled.is_(True))
            .where(CourseProgress.reminder_time.isnot(None))
        )
        rows = result.all()

        for progress, user in rows:
            if not progress.reminder_time:
                continue

            tz_offset = getattr(progress, "reminder_tz_offset", 5) or 5
            local_now = now_utc + timedelta(hours=tz_offset)

            if local_now.hour != progress.reminder_time.hour:
                continue

            if progress.last_reminder_sent_at:
                last_local = progress.last_reminder_sent_at + timedelta(hours=tz_offset)
                if last_local.date() == local_now.date():
                    continue

            lang = user.language if user.language else "ru"
            try:
                await bot.send_message(
                    user.telegram_id,
                    t("course_reminder_text", lang),
                )
                progress.last_reminder_sent_at = now_utc
            except Exception as e:
                print(f"CourseReminderService: failed to notify {user.telegram_id}: {e}")

        await self.session.commit()
