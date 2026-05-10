from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.db.models.course_audio import CourseAudio


class CourseAudioRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, level: str, lesson_order: int, audio_type: str) -> Optional[str]:
        """file_id ni qaytaradi, yo'q bo'lsa None."""
        result = await self.session.execute(
            select(CourseAudio.file_id).where(
                CourseAudio.level == level,
                CourseAudio.lesson_order == lesson_order,
                CourseAudio.audio_type == audio_type,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(self, level: str, lesson_order: int, audio_type: str, file_id: str) -> None:
        """file_id ni yangilaydi yoki yaratadi (upsert)."""
        stmt = (
            insert(CourseAudio)
            .values(level=level, lesson_order=lesson_order, audio_type=audio_type, file_id=file_id)
            .on_conflict_do_update(
                constraint="uq_course_audio",
                set_={"file_id": file_id},
            )
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def list_for_lesson(self, level: str, lesson_order: int) -> list[CourseAudio]:
        """Bir dars uchun barcha audio yozuvlarini qaytaradi."""
        result = await self.session.execute(
            select(CourseAudio).where(
                CourseAudio.level == level,
                CourseAudio.lesson_order == lesson_order,
            ).order_by(CourseAudio.audio_type)
        )
        return list(result.scalars().all())
