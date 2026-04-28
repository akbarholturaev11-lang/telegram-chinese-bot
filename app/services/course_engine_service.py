import json
from typing import Optional

from app.repositories.user_repo import UserRepository
from app.repositories.course_lesson_repo import CourseLessonRepository
from app.repositories.course_progress_repo import CourseProgressRepository
from app.repositories.course_attempt_repo import CourseAttemptRepository
from app.services.course_tutor_service import CourseTutorService


COURSE_STEP_ORDER = [
    "intro",
    "vocab",
    "dialogue",
    "grammar",
    "exercise",
    "quiz",
    "satisfaction_check",
    "homework",
    "completed",
]


class CourseEngineService:
    def __init__(self, session):
        self.session = session
        self.user_repo = UserRepository(session)
        self.lesson_repo = CourseLessonRepository(session)
        self.progress_repo = CourseProgressRepository(session)
        self.attempt_repo = CourseAttemptRepository(session)
        self.tutor = CourseTutorService()

    def _allowed_level_candidates(self, level: str | None) -> tuple[str, ...]:
        normalized = (level or "").strip().lower()
        fallback_map = {
            "beginner": ("hsk1",),
            "hsk1": ("hsk1",),
            "hsk2": ("hsk2", "hsk1"),
            "hsk3": ("hsk3", "hsk2", "hsk1"),
            "hsk4": ("hsk4", "hsk3", "hsk2", "hsk1"),
        }
        return fallback_map.get(normalized, ("hsk1",))

    async def get_or_create_progress(self, telegram_id: int):
        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return None, None, "access_start_first"

        progress = await self.progress_repo.get_by_user_id(user.id)
        if progress:
            return user, progress, ""

        progress = await self.progress_repo.create(
            user_id=user.id,
            level=user.level,
            current_lesson_id=None,
            current_step="intro",
            waiting_for="none",
        )
        await self.session.commit()
        return user, progress, ""

    async def get_current_lesson(self, telegram_id: int):
        user, progress, error_key = await self.get_or_create_progress(telegram_id)
        if error_key:
            return None, None, None, error_key

        if not progress or not progress.current_lesson_id:
            return user, progress, None, "course_no_lesson_found"

        lesson = await self.lesson_repo.get_by_id(progress.current_lesson_id)
        if not lesson:
            return user, progress, None, "course_no_lesson_found"

        return user, progress, lesson, ""

    async def continue_course(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return user, progress, lesson, error_key

        if not progress or not lesson:
            return user, progress, lesson, "course_no_lesson_selected"

        waiting_for = getattr(progress, "waiting_for", None) or "none"
        homework_status = getattr(progress, "homework_status", None) or "none"
        current_step = getattr(progress, "current_step", None) or "intro"

        if waiting_for in {
            "satisfaction_answer",
            "satisfaction_reason",
            "homework_submission",
            "next_study_time",
            "review_choice",
        }:
            return user, progress, lesson, ""

        if current_step == "completed" and homework_status == "completed":
            return user, progress, lesson, ""

        return user, progress, lesson, ""

    async def pick_lesson(self, telegram_id: int, lesson_id: int):
        user, progress, error_key = await self.get_or_create_progress(telegram_id)
        if error_key:
            return None, None, None, error_key

        lesson = await self.lesson_repo.get_by_id(lesson_id)
        if not lesson:
            return user, progress, None, "course_no_lesson_found"

        if lesson.level not in self._allowed_level_candidates(user.level):
            return user, progress, None, "course_lesson_not_unlocked"

        unlocked_order = max(1, (getattr(progress, "completed_lessons_count", 0) or 0) + 1)
        if lesson.lesson_order > unlocked_order:
            return user, progress, None, "course_lesson_not_unlocked"

        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=lesson.id,
            step="intro",
            waiting_for="none",
        )
        await self.session.commit()

        return user, progress, lesson, ""

    def get_next_step_name(self, current_step: str) -> str:
        if current_step not in COURSE_STEP_ORDER:
            return "intro"

        idx = COURSE_STEP_ORDER.index(current_step)
        if idx >= len(COURSE_STEP_ORDER) - 1:
            return "completed"

        return COURSE_STEP_ORDER[idx + 1]

    def get_prev_step_name(self, current_step: str) -> str:
        if current_step not in COURSE_STEP_ORDER:
            return "intro"

        idx = COURSE_STEP_ORDER.index(current_step)
        if idx <= 0:
            return "intro"

        return COURSE_STEP_ORDER[idx - 1]

    async def go_to_next_step(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, error_key

        next_step = self.get_next_step_name(progress.current_step)
        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=progress.current_lesson_id,
            step=next_step,
            waiting_for="none",
        )
        await self.session.commit()

        return user, progress, lesson, ""

    async def go_to_prev_step(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, error_key

        prev_step = self.get_prev_step_name(progress.current_step)
        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=progress.current_lesson_id,
            step=prev_step,
            waiting_for="none",
        )
        await self.session.commit()

        return user, progress, lesson, ""

    async def mark_quiz_passed_and_go_to_satisfaction(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, error_key

        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=progress.current_lesson_id,
            step="satisfaction_check",
            waiting_for="satisfaction_answer",
        )
        await self.session.commit()

        return user, progress, lesson, ""

    async def mark_satisfied_and_go_to_homework(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, error_key

        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=lesson.id,
            step="homework",
            waiting_for="homework_submission",
        )
        await self.progress_repo.set_homework_status(progress, "assigned")
        await self.session.commit()

        return user, progress, lesson, ""

    async def mark_not_satisfied_and_stay(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, error_key

        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=progress.current_lesson_id,
            step="satisfaction_check",
            waiting_for="satisfaction_reason",
        )
        await self.session.commit()

        return user, progress, lesson, ""

    async def mark_homework_submitted(self, telegram_id: int, submission_text: str):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return {"error_key": error_key}

        submission_text = (submission_text or "").strip()
        if not submission_text:
            return {"error_key": "course_homework_empty"}

        user_lang = user.language if getattr(user, "language", None) else "ru"
        user_level = user.level if getattr(user, "level", None) else "hsk1"

        evaluation = await self.tutor.evaluate_homework(
            user_language=user_lang,
            user_level=user_level,
            lesson=lesson,
            submission_text=submission_text,
        )

        score = evaluation.get("score", 0)
        passed = evaluation.get("passed", False)
        feedback_text = evaluation.get("feedback_text", "")

        await self.attempt_repo.create(
            user_id=user.id,
            lesson_id=lesson.id,
            attempt_type="homework",
            step_name="homework",
            score=score,
            passed=passed,
            answers_json=json.dumps({"submission_text": submission_text}, ensure_ascii=False),
            ai_feedback=feedback_text,
        )

        await self.progress_repo.set_homework_status(progress, "completed")
        await self.progress_repo.set_waiting_for(progress, "next_study_time")

        await self.session.commit()

        return {
            "error_key": None,
            "feedback_text": feedback_text,
            "ask_next_study_time": True,
            "score": score,
            "passed": passed,
        }

    async def set_next_study_at(self, telegram_id: int, next_study_at):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, error_key

        next_lesson = await self.lesson_repo.get_next_lesson(
            level=lesson.level,
            lesson_order=lesson.lesson_order,
        )

        await self.progress_repo.set_next_study_at(progress, next_study_at)
        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=lesson.id,
            step="completed",
            waiting_for="review_choice" if next_lesson else "none",
        )
        await self.session.commit()

        return user, progress, lesson, ""

    async def activate_next_lesson(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, error_key

        next_lesson = await self.lesson_repo.get_next_lesson(
            level=lesson.level,
            lesson_order=lesson.lesson_order,
        )
        if not next_lesson:
            return user, progress, None, "course_no_next_lesson"

        await self.progress_repo.mark_lesson_completed(progress)
        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=next_lesson.id,
            step="intro",
            waiting_for="none",
        )
        await self.progress_repo.set_homework_status(progress, "none")
        await self.session.commit()

        return user, progress, next_lesson, ""

    async def clear_review_prompt(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, error_key

        await self.progress_repo.set_review_prompt(
            progress=progress,
            needs_review_prompt=False,
        )
        await self.session.commit()

        return user, progress, lesson, ""

    async def complete_lesson_and_unlock_next(self, telegram_id: int):
        user, progress, lesson, error_key = await self.get_current_lesson(telegram_id)
        if error_key:
            return None, None, None, None, error_key

        current_order = lesson.lesson_order
        next_lesson = await self.lesson_repo.get_next_lesson(
            level=lesson.level,
            lesson_order=current_order,
        )

        await self.progress_repo.mark_lesson_completed(progress)

        await self.progress_repo.set_current_lesson_and_step(
            progress=progress,
            lesson_id=next_lesson.id if next_lesson else progress.current_lesson_id,
            step="intro" if next_lesson else "completed",
            waiting_for="none",
        )

        if next_lesson:
            await self.progress_repo.set_homework_status(progress, "none")

        await self.session.commit()

        return user, progress, lesson, next_lesson, ""
