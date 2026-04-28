from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json

from app.repositories.user_repo import UserRepository
from app.services.course_engine_service import CourseEngineService
from app.services.course_tutor_service import CourseTutorService
from app.bot.utils.i18n import t
from app.bot.keyboards.course import (
    lesson_selection_keyboard, review_choice_keyboard,
    course_intro_keyboard, course_vocab_keyboard, course_dialogue_keyboard,
    course_grammar_keyboard, course_exercise_keyboard, course_homework_keyboard,
)
from app.bot.keyboards.subscription import payment_method_keyboard
from app.bot.keyboards.course_context import (
    course_understood_keyboard,
    course_review_offer_keyboard,
    course_satisfaction_keyboard,
    course_homework_keyboard as _ctx_homework_keyboard,
    course_next_lesson_keyboard,
)

from app.config import COURSE_MODE_ENABLED
from app.bot.utils.course_formatter import (
    format_intro, format_vocab, format_dialogue,
    format_grammar, format_exercise,
)
from app.bot.keyboards.main_menu import course_menu_keyboard, main_menu_keyboard



async def _block_if_course_disabled(callback, session):
    if not COURSE_MODE_ENABLED:
        lang = "ru"
        try:
            user_repo = UserRepository(session)
            user = await user_repo.get_by_telegram_id(callback.from_user.id)
            if user and user.language:
                lang = user.language
        except:
            pass

        msg_map = {
            "uz": "🚧 Kurs rejimi hozircha ishlab chiqilmoqda. Tez orada mavjud bo‘ladi.",
            "ru": "🚧 Режим курса сейчас в разработке. Скоро будет доступен.",
            "tj": "🚧 Реҷаи курс ҳоло дар навсози аст. Ба зудӣ дастрас мешавад.",
        }

        await callback.answer()
        await callback.message.answer(msg_map.get(lang, msg_map["ru"]))
        return True
    return False


router = Router()


def _course_level_candidates(level: str | None) -> tuple[str, ...]:
    normalized = (level or "").strip().lower()
    fallback_map = {
        "beginner": ("hsk1",),
        "hsk1": ("hsk1",),
        "hsk2": ("hsk2", "hsk1"),
        "hsk3": ("hsk3", "hsk2", "hsk1"),
        "hsk4": ("hsk4", "hsk3", "hsk2", "hsk1"),
    }
    return fallback_map.get(normalized, ("hsk1",))


async def _resolve_lessons_for_user_level(engine: CourseEngineService, level: str | None):
    candidates = _course_level_candidates(level)
    for candidate in candidates:
        lessons = await engine.lesson_repo.list_by_level(candidate)
        if lessons:
            return lessons, candidate
    return [], candidates[0]


def filter_unlocked_lessons(lessons: list, progress) -> list:
    unlocked_order = max(1, (getattr(progress, "completed_lessons_count", 0) or 0) + 1)
    return [lesson for lesson in lessons if lesson.lesson_order <= unlocked_order]


async def send_course_completion_prompt(*, respond, engine: CourseEngineService, lesson, lang: str) -> None:
    next_lesson = await engine.lesson_repo.get_next_lesson(
        level=lesson.level,
        lesson_order=lesson.lesson_order,
    )
    if next_lesson:
        await respond(
            t("course_next_lesson_unlocked", lang),
            reply_markup=course_next_lesson_keyboard(lang),
        )
    else:
        await respond(t("course_completed_title", lang))


def _format_homework_text(lang: str, homework_raw) -> str:
    title = t("course_homework_title", lang)

    if not homework_raw:
        return title

    try:
        data = json.loads(homework_raw) if isinstance(homework_raw, str) else homework_raw
    except Exception:
        return f"{title}\n\n{homework_raw}"

    if isinstance(data, list):
        lines = [title, ""]
        for i, item in enumerate(data, 1):
            lines.append(f"{i}. {item}")
        return "\n".join(lines)

    if isinstance(data, dict):
        lines = [title, ""]
        for key, value in data.items():
            if isinstance(value, list):
                lines.append(f"{key}:")
                for i, item in enumerate(value, 1):
                    lines.append(f"{i}. {item}")
            else:
                lines.append(f"{key}: {value}")
        return "\n".join(lines)

    return f"{title}\n\n{data}"





def get_course_keyboard_for_step(lang: str, step: str):
    if step == "satisfaction_check":
        return course_satisfaction_keyboard(lang)
    if step == "homework":
        return _ctx_homework_keyboard(lang)
    if step == "completed":
        return course_next_lesson_keyboard(lang)
    return course_understood_keyboard(lang, step)

@router.callback_query(F.data.startswith("course:lessons_page:"))
async def course_lessons_page_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"

    if user.status != "active":
        await callback.answer()
        await callback.message.answer(
            t("course_only_active_users", lang),
            reply_markup=payment_method_keyboard(lang),
            parse_mode="HTML",
        )
        return

    try:
        page = int(callback.data.split(":")[-1])
    except Exception:
        page = 0

    progress = await engine.progress_repo.get_by_user_id(user.id)
    lessons, _ = await _resolve_lessons_for_user_level(engine, user.level)
    lessons = filter_unlocked_lessons(lessons, progress)

    await callback.answer()
    await callback.message.edit_reply_markup(
        reply_markup=lesson_selection_keyboard(lessons, page=page, lang=lang)
    )


@router.callback_query(F.data.startswith("course:pick_lesson:"))
async def course_pick_lesson_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    engine = CourseEngineService(session)

    lang = callback.from_user.language_code if callback.from_user.language_code in ["ru", "uz", "tj"] else "ru"

    try:
        lesson_id = int(callback.data.split(":")[-1])
    except Exception:
        await callback.answer()
        return

    _, _, _, error_key = await engine.pick_lesson(callback.from_user.id, lesson_id)
    if error_key:
        if error_key == "course_lesson_not_unlocked":
            await callback.answer(t(error_key, lang), show_alert=True)
        else:
            await callback.answer()
            await callback.message.answer(t(error_key, lang))
        return

    await callback.answer()
    try:
        await callback.message.delete()
    except Exception:
        pass
    await run_course_entry_flow(
        session=session,
        telegram_id=callback.from_user.id,
        respond=callback.message.answer,
    )



@router.callback_query(F.data == "mode:qa")
async def mode_qa_handler(callback: CallbackQuery, session):

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(callback.from_user.id)

    lang = callback.from_user.language_code if callback.from_user.language_code in ["ru", "uz", "tj"] else "ru"

    if not user:
        await callback.answer()
        await callback.message.answer(t("user_not_found", lang))
        return

    lang = user.language if user.language else "ru"
    user.learning_mode = "qa"
    await session.commit()

    await callback.answer()
    await callback.message.answer(t("trial_started_info", lang))
    await callback.message.answer(t("send_first_message", lang), reply_markup=main_menu_keyboard(lang))

@router.callback_query(F.data == "mode:course")
async def course_mode_open_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    await callback.answer()
    await run_course_entry_flow(
        session=session,
        telegram_id=callback.from_user.id,
        respond=callback.message.answer,
    )




async def run_course_entry_flow(
    *,
    session,
    telegram_id: int,
    respond,
):
    user_repo = UserRepository(session)
    engine = CourseEngineService(session)
    tutor = CourseTutorService()

    user = await user_repo.get_by_telegram_id(telegram_id)
    if not user:
        await respond(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    if user.status != "active":
        await respond(
            t("course_only_active_users", lang),
            reply_markup=payment_method_keyboard(lang),
            parse_mode="HTML",
        )
        return

    was_in_course = user.learning_mode == "course"
    user.learning_mode = "course"
    await session.commit()

    if not was_in_course:
        await respond(t("course_menu_title", lang), reply_markup=course_menu_keyboard(lang))
    else:
        await respond("📚", reply_markup=course_menu_keyboard(lang))

    progress = await engine.progress_repo.get_by_user_id(user.id)
    if not progress:
        progress = await engine.progress_repo.create(
            user_id=user.id,
            level=user.level,
            current_lesson_id=None,
            current_step="intro",
            waiting_for="none",
        )

    if not progress.current_lesson_id:
        lessons, resolved_level = await _resolve_lessons_for_user_level(engine, user.level)
        lessons = filter_unlocked_lessons(lessons, progress)

        if not lessons:
            await respond(t("course_no_lessons_available", lang))
            return

        level_label = resolved_level.upper() if resolved_level else "HSK"
        await respond(
            f"{level_label}. {t('course_choose_lesson', lang)}",
            reply_markup=lesson_selection_keyboard(lessons, page=0, lang=lang),
        )
        return

    if getattr(progress, "waiting_for", None) == "next_study_time":
        await respond(t("course_next_study_time_optional", lang))
        return

    if (
        getattr(progress, "current_step", None) == "completed"
        and getattr(progress, "homework_status", None) == "completed"
        and getattr(progress, "waiting_for", None) == "review_choice"
    ):
        await respond(
            t("course_review_choice", lang),
            reply_markup=review_choice_keyboard(lang),
        )
        return

    if getattr(progress, "current_step", None) == "completed" and getattr(progress, "homework_status", None) == "completed":
        lesson = await engine.lesson_repo.get_by_id(progress.current_lesson_id)
        if lesson:
            await send_course_completion_prompt(
                respond=respond,
                engine=engine,
                lesson=lesson,
                lang=lang,
            )
        else:
            await respond(t("course_completed_title", lang))
        return

    user, progress, lesson, error_key = await engine.continue_course(telegram_id)
    if error_key:
        await respond(t(error_key, lang))
        return

    step = progress.current_step
    formatter_map = {
        "intro":    lambda: format_intro(lesson, lang),
        "vocab":    lambda: format_vocab(lesson, lang),
        "dialogue": lambda: format_dialogue(lesson, lang),
        "grammar":  lambda: format_grammar(lesson, lang),
        "exercise": lambda: format_exercise(lesson, lang),
    }
    step_keyboards = {
        "intro":    lambda: course_intro_keyboard(lang),
        "vocab":    lambda: course_vocab_keyboard(lang),
        "dialogue": lambda: course_dialogue_keyboard(lang),
        "grammar":  lambda: course_grammar_keyboard(lang),
        "exercise": lambda: course_exercise_keyboard(lang),
    }
    if step in formatter_map:
        text = formatter_map[step]()
        keyboard = step_keyboards.get(step, lambda: None)()
    elif step == "homework":
        text = _format_homework_text(lang, lesson.homework_json)
        keyboard = None
    else:
        text = await tutor.generate_step_response(
            user_language=user.language,
            user_level=user.level,
            lesson=lesson,
            step=step,
            user_message="",
        )
        keyboard = get_course_keyboard_for_step(lang, step)
    await respond(text, reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "/course")
async def course_command_handler(message: Message, session):

    if not COURSE_MODE_ENABLED:
        lang = "ru"
        try:
            user_repo = UserRepository(session)
            user = await user_repo.get_by_telegram_id(message.from_user.id)
            if user and user.language:
                lang = user.language
        except:
            pass

        msg_map = {
            "uz": "🚧 Kurs rejimi hozircha ishlab chiqilmoqda. Tez orada mavjud bo‘ladi.",
            "ru": "🚧 Режим курса сейчас в разработке. Скоро будет доступен.",
            "tj": "🚧 Реҷаи курс ҳоло дар таҳия аст. Ба зудӣ дастрас мешавад.",
        }

        await message.answer(msg_map.get(lang, msg_map["ru"]))
        return

    await run_course_entry_flow(
        session=session,
        telegram_id=message.from_user.id,
        respond=message.answer,
    )


@router.callback_query(F.data == "course:back_to_qa")
async def course_back_to_qa_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    user.learning_mode = "qa"
    await session.commit()

    lang = user.language if user.language else "ru"

    await callback.answer()
    await callback.message.answer(t("send_first_message", lang), reply_markup=main_menu_keyboard(lang))




@router.callback_query(F.data == "course:continue")
async def course_continue_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    await callback.answer()
    await run_course_entry_flow(
        session=session,
        telegram_id=callback.from_user.id,
        respond=callback.message.answer,
    )




@router.callback_query(F.data == "course:review_yes")
async def course_review_yes_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)
    tutor = CourseTutorService()

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"
    progress = await engine.progress_repo.get_by_user_id(user.id)
    if not progress or progress.waiting_for != "review_choice":
        await callback.answer()
        return

    user, progress, lesson, error_key = await engine.get_current_lesson(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    review_text = await tutor.generate_step_response(
        user_language=user.language,
        user_level=user.level,
        lesson=lesson,
        step="review",
        user_message="",
    )

    if getattr(progress, "homework_status", None) == "completed":
        await engine.progress_repo.set_waiting_for(progress, "none")
        await session.commit()

        await callback.answer()
        await callback.message.answer(t("course_review", lang))
        await callback.message.answer(review_text)
        await send_course_completion_prompt(
            respond=callback.message.answer,
            engine=engine,
            lesson=lesson,
            lang=lang,
        )
        return

    await engine.progress_repo.set_waiting_for(progress, "homework_submission")
    await session.commit()

    if lesson.homework_json:
        homework_text = _format_homework_text(lang, lesson.homework_json)
    else:
        homework_text = await tutor.generate_step_response(
            user_language=user.language,
            user_level=user.level,
            lesson=lesson,
            step="homework",
            user_message="",
        )

    await callback.answer()
    await callback.message.answer(t("course_review_then_homework", lang))
    await callback.message.answer(review_text)
    await callback.message.answer(t("course_lesson_homework_intro", lang))
    await callback.message.answer(homework_text)


@router.callback_query(F.data == "course:review_no")
async def course_review_no_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"

    user, progress, lesson, current_error_key = await engine.get_current_lesson(callback.from_user.id)
    if current_error_key:
        await callback.answer()
        await callback.message.answer(t(current_error_key, lang))
        return

    if getattr(progress, "homework_status", None) != "completed":
        await callback.answer()
        await callback.message.answer(t("course_complete_homework_first", lang))
        return

    user, progress, lesson, next_lesson, error_key = await engine.complete_lesson_and_unlock_next(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    if not next_lesson:
        await callback.answer()
        await callback.message.answer(t("course_completed_title", lang))
        return

    text = format_intro(next_lesson, lang)

    await callback.answer()
    await callback.message.answer(t("course_skip_review_next_lesson", lang))
    await callback.message.answer(
        text,
        reply_markup=course_intro_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "course:progress")
async def course_progress_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    if user.status != "active":
        await callback.answer()
        await callback.message.answer(
            t("course_only_active_users", lang),
            reply_markup=payment_method_keyboard(lang),
            parse_mode="HTML",
        )
        return

    user, progress, lesson, error_key = await engine.get_current_lesson(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    current_lesson = lesson.title if lesson else "-"
    completed_count = getattr(progress, "completed_lessons_count", 0) or 0

    text = (
        f"📊 {t('course_progress', lang)}\n\n"
        f"{t('course_current_lesson', lang)}: {current_lesson}\n"
        f"{t('course_completed_lessons', lang)}: {completed_count}"
    )

    await callback.answer()
    await callback.message.answer(text)



@router.callback_query(F.data == "course:review_last")
async def course_review_last_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    if user.status != "active":
        await callback.answer()
        await callback.message.answer(
            t("course_only_active_users", lang),
            reply_markup=payment_method_keyboard(lang),
            parse_mode="HTML",
        )
        return

    user.learning_mode = "course"
    await session.commit()

    user, progress, lesson, error_key = await engine.get_current_lesson(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    step = progress.current_step
    formatter_map = {
        "intro":    lambda: format_intro(lesson, lang),
        "vocab":    lambda: format_vocab(lesson, lang),
        "dialogue": lambda: format_dialogue(lesson, lang),
        "grammar":  lambda: format_grammar(lesson, lang),
        "exercise": lambda: format_exercise(lesson, lang),
    }
    text = formatter_map[step]() if step in formatter_map else ""

    await callback.answer()
    await callback.message.answer(text)



@router.callback_query(F.data == "course:retry_test")
async def course_retry_test_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)
    tutor = CourseTutorService()

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    if user.status != "active":
        await callback.answer()
        await callback.message.answer(
            t("course_only_active_users", lang),
            reply_markup=payment_method_keyboard(lang),
            parse_mode="HTML",
        )
        return

    user.learning_mode = "course"
    await session.commit()

    user, progress, lesson, error_key = await engine.get_current_lesson(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    await engine.progress_repo.set_current_lesson_and_step(
        progress=progress,
        lesson_id=lesson.id,
        step="quiz",
    )
    await session.commit()

    text = await tutor.generate_step_response(
        user_language=user.language,
        user_level=user.level,
        lesson=lesson,
        step="quiz",
        user_message=t("course_start_quiz", lang),
    )

    await callback.answer()
    await callback.message.answer(
        text,
        reply_markup=get_course_keyboard_for_step(lang, "quiz"),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "course:satisfied_yes")
async def course_satisfied_yes_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    user, progress, lesson, error_key = await engine.mark_satisfied_and_go_to_homework(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    await engine.progress_repo.set_waiting_for(progress, "homework_submission")
    await session.commit()

    if lesson.homework_json:
        homework_text = _format_homework_text(lang, lesson.homework_json)
    else:
        homework_text = await CourseTutorService().generate_step_response(
            user_language=user.language,
            user_level=user.level,
            lesson=lesson,
            step="homework",
            user_message="",
        )

    await callback.answer()
    await callback.message.answer(t("course_lesson_homework_intro", lang))
    await callback.message.answer(homework_text)


@router.callback_query(F.data == "course:satisfied_no")
async def course_satisfied_no_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    user, progress, lesson, error_key = await engine.mark_not_satisfied_and_stay(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    await callback.answer()
    await callback.message.answer(
        t("course_lesson_what_unclear", lang)
    )


@router.callback_query(F.data == "course:show_homework")
async def course_show_homework_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    user, progress, lesson, error_key = await engine.get_current_lesson(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    if lesson.homework_json:
        homework_text = _format_homework_text(lang, lesson.homework_json)
    else:
        homework_text = await CourseTutorService().generate_step_response(
            user_language=user.language,
            user_level=user.level,
            lesson=lesson,
            step="homework",
            user_message="",
        )

    if progress.current_step == "homework" and progress.homework_status != "completed":
        await engine.progress_repo.set_waiting_for(progress, "homework_submission")
        await session.commit()

    await callback.answer()
    await callback.message.answer(homework_text)


@router.callback_query(F.data == "course:start_next_lesson")
async def course_start_next_lesson_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    user, progress, lesson, current_error_key = await engine.get_current_lesson(callback.from_user.id)
    if current_error_key:
        await callback.answer()
        await callback.message.answer(t(current_error_key, lang))
        return

    if progress.homework_status != "completed":
        await callback.answer()
        await callback.message.answer(t("course_complete_homework_first", lang))
        return

    user, progress, lesson, next_lesson, error_key = await engine.complete_lesson_and_unlock_next(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    if not next_lesson:
        await callback.answer()
        await callback.message.answer(t("course_completed_title", lang))
        return

    await callback.answer()
    await run_course_entry_flow(
        session=session,
        telegram_id=callback.from_user.id,
        respond=callback.message.answer,
    )


async def _go_to_step(callback, session, step: str):
    if await _block_if_course_disabled(callback, session):
        return

    from app.bot.keyboards.course import (
        course_intro_keyboard, course_vocab_keyboard, course_dialogue_keyboard,
        course_grammar_keyboard, course_exercise_keyboard,
    )

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"
    user, progress, lesson, error_key = await engine.get_current_lesson(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    await engine.progress_repo.set_current_lesson_and_step(
        progress=progress,
        lesson_id=lesson.id,
        step=step,
        waiting_for="none",
    )
    await session.commit()

    formatter_map = {
        "intro":    lambda: format_intro(lesson, lang),
        "vocab":    lambda: format_vocab(lesson, lang),
        "dialogue": lambda: format_dialogue(lesson, lang),
        "grammar":  lambda: format_grammar(lesson, lang),
        "exercise": lambda: format_exercise(lesson, lang),
    }
    step_keyboards = {
        "intro":    lambda: course_intro_keyboard(lang),
        "vocab":    lambda: course_vocab_keyboard(lang),
        "dialogue": lambda: course_dialogue_keyboard(lang),
        "grammar":  lambda: course_grammar_keyboard(lang),
        "exercise": lambda: course_exercise_keyboard(lang),
    }
    if step in formatter_map:
        text = formatter_map[step]()
        keyboard = step_keyboards.get(step, lambda: None)()
    else:
        tutor = CourseTutorService()
        text = await tutor.generate_step_response(
            user_language=user.language,
            user_level=user.level,
            lesson=lesson,
            step=step,
            user_message="",
        )
        keyboard = get_course_keyboard_for_step(lang, step)

    await callback.answer()
    await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data == "course:go_vocab")
async def course_go_vocab(callback: CallbackQuery, session):
    await _go_to_step(callback, session, "vocab")

@router.callback_query(F.data == "course:go_dialogue")
async def course_go_dialogue(callback: CallbackQuery, session):
    await _go_to_step(callback, session, "dialogue")

@router.callback_query(F.data == "course:go_grammar")
async def course_go_grammar(callback: CallbackQuery, session):
    await _go_to_step(callback, session, "grammar")

@router.callback_query(F.data == "course:go_exercise")
async def course_go_exercise(callback: CallbackQuery, session):
    await _go_to_step(callback, session, "exercise")

@router.callback_query(F.data == "course:go_quiz")
async def course_go_quiz(callback: CallbackQuery, session):
    await _go_to_step(callback, session, "quiz")


@router.callback_query(F.data == "course:finish_quiz")
async def course_finish_quiz(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)
    tutor = CourseTutorService()

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"
    user, progress, lesson, error_key = await engine.mark_quiz_passed_and_go_to_satisfaction(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    text = await tutor.generate_step_response(
        user_language=user.language,
        user_level=user.level,
        lesson=lesson,
        step="satisfaction_check",
        user_message="",
    )

    await callback.answer()
    await callback.message.answer(
        text,
        reply_markup=course_satisfaction_keyboard(lang),
        parse_mode="HTML",
    )

@router.callback_query(F.data == "course:repeat_step")
async def course_repeat_step(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    from app.bot.keyboards.course import (
        course_intro_keyboard, course_vocab_keyboard, course_dialogue_keyboard,
        course_grammar_keyboard, course_exercise_keyboard,
    )

    user_repo = UserRepository(session)
    engine = CourseEngineService(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        return

    lang = user.language if user.language else "ru"
    user, progress, lesson, error_key = await engine.get_current_lesson(callback.from_user.id)
    if error_key:
        await callback.answer()
        await callback.message.answer(t(error_key, lang))
        return

    step = progress.current_step

    formatter_map = {
        "intro":    lambda: format_intro(lesson, lang),
        "vocab":    lambda: format_vocab(lesson, lang),
        "dialogue": lambda: format_dialogue(lesson, lang),
        "grammar":  lambda: format_grammar(lesson, lang),
        "exercise": lambda: format_exercise(lesson, lang),
    }
    text = formatter_map[step]() if step in formatter_map else ""

    step_keyboards = {
        "intro":    lambda: course_intro_keyboard(lang),
        "vocab":    lambda: course_vocab_keyboard(lang),
        "dialogue": lambda: course_dialogue_keyboard(lang),
        "grammar":  lambda: course_grammar_keyboard(lang),
        "exercise": lambda: course_exercise_keyboard(lang),
    }

    keyboard = step_keyboards.get(step, lambda: None)()
    await callback.answer()
    await callback.message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data == "course:skip_next_study_time")
async def course_skip_next_study_time_handler(callback: CallbackQuery, session):
    if await _block_if_course_disabled(callback, session):
        return

    user_repo = UserRepository(session)

    user = await user_repo.get_by_telegram_id(callback.from_user.id)
    if not user:
        await callback.answer()
        await callback.message.answer(t("access_start_first", "ru"))
        return

    lang = user.language if user.language else "ru"

    await callback.answer()
    await callback.message.answer(
        t("course_next_study_time_skipped", lang)
    )
