from datetime import datetime, timezone, timedelta

from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.course_progress import CourseProgress
from app.db.models.user import User
from app.bot.utils.i18n import t


def _reminder_keyboard(lang: str):
    labels = {
        "uz": "📖 Darsni davom ettirish",
        "ru": "📖 Продолжить урок",
        "tj": "📖 Идома додани дарс",
    }
    builder = InlineKeyboardBuilder()
    builder.button(text=labels.get(lang, labels["ru"]), callback_data="course:continue")
    return builder.as_markup()


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

            # Soatni moslashtirish
            if local_now.hour != progress.reminder_time.hour:
                continue

            # Bugun allaqachon yuborilganmi?
            if progress.last_reminder_sent_at:
                last_local = progress.last_reminder_sent_at + timedelta(hours=tz_offset)
                if last_local.date() == local_now.date():
                    continue

            lang = user.language if user.language else "ru"
            try:
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=t("course_reminder_text", lang),
                    reply_markup=_reminder_keyboard(lang),
                    parse_mode="HTML",
                )
                progress.last_reminder_sent_at = now_utc
                print(f"CourseReminderService: sent reminder to {user.telegram_id}")
            except Exception as e:
                print(f"CourseReminderService: failed to notify {user.telegram_id}: {e}")

        await self.session.commit()
