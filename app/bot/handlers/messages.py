import json
from datetime import datetime, timezone, time

from aiogram import F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from app.bot.utils.response_effect import ResponseEffect
from app.bot.handlers.course import (
    get_course_keyboard_for_step,
    _keyboard_for_step,
    run_course_entry_flow,
    _resolve_lessons_for_user_level,
    filter_unlocked_lessons,
    send_course_completion_prompt,
)
from app.bot.keyboards.course_context import course_tushundim_keyboard
from app.bot.keyboards.course import (
    lesson_selection_keyboard,
    review_choice_keyboard,
    course_reminder_timezone_keyboard,
    reminder_time_keyboard,
)
from app.bot.keyboards.course import course_intro_keyboard
from app.bot.keyboards.checkout import checkout_keyboard
from app.bot.keyboards.main_menu import main_menu_keyboard, course_menu_keyboard
from app.bot.keyboards.referral import photo_limit_subscription_keyboard
from app.bot.keyboards.referral import referral_daily_limit_keyboard
from app.bot.utils.course_formatter import format_intro
from app.repositories.message_repo import MessageRepository
from app.repositories.user_repo import UserRepository
from app.services.access_service import AccessService
from app.services.course_engine_service import CourseEngineService
from app.services.course_tutor_service import CourseTutorService
from app.services.image_input_service import ImageInputService
from app.services.image_qa_service import ImageQAService
from app.services.qa_service import QAService
from app.bot.utils.i18n import t


router = Router()


def _next_study_time_keyboard(user_lang: str) -> ReplyKeyboardMarkup:
    skip_map = {
        "uz": "O‘tkazib yuborish",
        "ru": "Пропустить",
        "tj": "Гузаронидан",
    }

    skip_text = skip_map.get(user_lang, "Пропустить")

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="09:00"), KeyboardButton(text="14:00")],
            [KeyboardButton(text="19:00"), KeyboardButton(text="21:00")],
            [KeyboardButton(text=skip_text)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )



def _parse_reminder_time(text: str):
    text = (text or "").strip()
    try:
        parts = text.split(":")
        if len(parts) == 2:
            h, m = int(parts[0].strip()), int(parts[1].strip())
            if 0 <= h < 24 and 0 <= m < 60:
                return time(h, m)
    except (ValueError, AttributeError):
        pass
    return None


def _parse_next_study_at(raw_text: str):
    raw_text = (raw_text or "").strip()
    if not raw_text:
        return None

    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%H:%M",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(raw_text, fmt)
            if fmt == "%H:%M":
                now = datetime.now()
                parsed = parsed.replace(year=now.year, month=now.month, day=now.day)
            return parsed
        except ValueError:
            continue

    return None


@router.message(F.text & ~F.text.startswith("/"))
async def handle_text_message(message: Message, session):
    user_repo = UserRepository(session)
    access_service = AccessService(session)

    user = await user_repo.get_by_telegram_id(message.from_user.id)
    user_lang = user.language if user and user.language else "ru"

    if message.text and message.text.startswith("/"):
        return

    if user and user.selected_plan_type and user.payment_status != "approved":
        await message.answer(
            t("payment_send_screenshot_only", user_lang),
            reply_markup=checkout_keyboard(user_lang),
        )
        return

    if user and user.learning_mode == "course":
        engine = CourseEngineService(session)
        tutor = CourseTutorService()

        msg_text = (message.text or "").strip()

        if msg_text == t("course_settings_button", user_lang):
            settings_engine = CourseEngineService(session)
            progress = await settings_engine.progress_repo.get_by_user_id(user.id)
            lessons, resolved_level = await _resolve_lessons_for_user_level(settings_engine, user.level)
            if not lessons:
                await message.answer(t("course_no_lessons_available", user_lang))
                return
            level_label = resolved_level.upper() if resolved_level else "HSK"
            await message.answer(
                f"{level_label}. {t('course_settings_choose_lesson', user_lang)}",
                reply_markup=lesson_selection_keyboard(lessons, page=0, lang=user_lang),
            )
            return

        if msg_text == t("course_progress", user_lang):
            current_user, progress, lesson, error_key = await engine.get_current_lesson(message.from_user.id)
            if error_key:
                await message.answer(t(error_key, user_lang))
                return
            current_lesson_title = lesson.title if lesson else "—"
            completed_count = getattr(progress, "completed_lessons_count", 0) or 0
            vocab_count = 0
            if completed_count > 0:
                all_lessons = await engine.lesson_repo.list_by_level(user.level)
                for les in all_lessons:
                    if les.lesson_order <= completed_count and les.vocabulary_json:
                        try:
                            vdata = json.loads(les.vocabulary_json) if isinstance(les.vocabulary_json, str) else les.vocabulary_json
                            if isinstance(vdata, list):
                                vocab_count += len(vdata)
                        except Exception:
                            pass
            days_studying = 1
            if progress.created_at:
                created = progress.created_at
                if not created.tzinfo:
                    created = created.replace(tzinfo=timezone.utc)
                days_studying = max(1, (datetime.now(timezone.utc) - created).days)
            await message.answer(
                t("course_progress_full_text", user_lang,
                  lessons=completed_count,
                  vocab=vocab_count,
                  days=days_studying,
                  current=current_lesson_title),
                parse_mode="HTML",
            )
            return

        if msg_text == t("course_back_to_qa_button", user_lang):
            user.learning_mode = "qa"
            await session.commit()
            await message.answer(t("send_first_message", user_lang), reply_markup=main_menu_keyboard(user_lang))
            return

        if msg_text == t("course_reread_button", user_lang):
            _, progress_rr, lesson_rr, err_rr = await engine.get_current_lesson(message.from_user.id)
            if err_rr or not lesson_rr:
                await message.answer(t(err_rr or "course_no_lesson_found", user_lang))
                return
            await engine.progress_repo.set_current_lesson_and_step(
                progress=progress_rr,
                lesson_id=lesson_rr.id,
                step="intro",
                waiting_for="none",
            )
            await session.commit()
            text_rr = format_intro(lesson_rr, user_lang)
            await message.answer(t("course_reread_start_msg", user_lang))
            await message.answer(text_rr, reply_markup=course_intro_keyboard(user_lang), parse_mode="HTML")
            return

        if msg_text == t("course_reminder_set_button", user_lang):
            progress_rm = await engine.progress_repo.get_by_user_id(user.id)
            if not progress_rm:
                return
            await engine.progress_repo.set_waiting_for(progress_rm, "reminder_setup")
            await session.commit()
            await message.answer(
                t("course_reminder_setup_msg", user_lang),
                reply_markup=reminder_time_keyboard(user_lang),
                parse_mode="HTML",
            )
            return

        current_user, progress, lesson, error_key = await engine.get_current_lesson(message.from_user.id)
        if error_key:
            await message.answer(t(error_key, user_lang))
            return

        if progress.waiting_for == "reminder_setup":
            cancel_map = {"uz": "❌ Bekor qilish", "ru": "❌ Отмена", "tj": "❌ Бекор кардан"}
            if msg_text == cancel_map.get(user_lang, "❌ Отмена"):
                await engine.progress_repo.set_waiting_for(progress, "none")
                await session.commit()
                await message.answer(
                    t("course_reminder_cancelled", user_lang),
                    reply_markup=course_menu_keyboard(user_lang),
                )
                return
            parsed_reminder = _parse_reminder_time(msg_text)
            if not parsed_reminder:
                await message.answer(
                    t("course_invalid_time_format", user_lang),
                    reply_markup=reminder_time_keyboard(user_lang),
                )
                return
            await engine.progress_repo.set_reminder(progress, enabled=True, reminder_time=parsed_reminder)
            await engine.progress_repo.set_waiting_for(progress, "none")
            await session.commit()
            # Faqat bitta blok — timezone tanlash (yakuniy xabar timezone tanlanganida yuboriladi)
            await message.answer(
                t("course_reminder_tz_title", user_lang),
                reply_markup=course_reminder_timezone_keyboard(),
            )
            return

        if progress.waiting_for == "satisfaction_answer":
            await message.answer(
                t("course_wait_for_answer", user_lang),
                reply_markup=get_course_keyboard_for_step(user_lang, progress.current_step),
            )
            return

        if progress.current_step == "completed" and progress.homework_status == "completed":
            if progress.waiting_for == "review_choice":
                await message.answer(
                    t("course_review_choice", user_lang),
                    reply_markup=review_choice_keyboard(user_lang),
                )
                return

            await send_course_completion_prompt(
                respond=message.answer,
                engine=engine,
                lesson=lesson,
                lang=user_lang,
            )
            return

        if progress.waiting_for == "satisfaction_reason":
            tutor_text = await tutor.generate_step_response(
                user_language=current_user.language,
                user_level=current_user.level,
                lesson=lesson,
                step=progress.current_step,
                user_message=f"User did not understand this part: {message.text or ''}",
            )
            await engine.mark_not_satisfied_and_stay(message.from_user.id)
            refreshed_user, refreshed_progress, refreshed_lesson, refreshed_error = await engine.get_current_lesson(
                message.from_user.id
            )
            if refreshed_error:
                await message.answer(t(refreshed_error, user_lang))
                return

            await message.answer(
                tutor_text,
                reply_markup=_keyboard_for_step(user_lang, refreshed_progress.current_step, refreshed_lesson),
                parse_mode="HTML",
            )
            return

        if progress.waiting_for == "exercise_answer":
            _loading_ex = await message.answer("🔎")

            eval_text = await tutor.generate_step_response(
                user_language=current_user.language,
                user_level=current_user.level,
                lesson=lesson,
                step="exercise",
                user_message=message.text or "",
            )

            try:
                await _loading_ex.delete()
            except Exception:
                pass

            await engine.progress_repo.set_current_lesson_and_step(
                progress=progress,
                lesson_id=progress.current_lesson_id,
                step="satisfaction_check",
                waiting_for="satisfaction_answer",
            )
            await session.commit()

            satisfaction_text = await tutor.generate_step_response(
                user_language=current_user.language,
                user_level=current_user.level,
                lesson=lesson,
                step="satisfaction_check",
                user_message="",
            )

            await message.answer(eval_text, parse_mode="HTML")
            await message.answer(
                satisfaction_text,
                reply_markup=get_course_keyboard_for_step(user_lang, "satisfaction_check"),
                parse_mode="HTML",
            )
            return

        if progress.waiting_for == "homework_submission":
            result = await engine.mark_homework_submitted(
                message.from_user.id,
                message.text or "",
            )

            if isinstance(result, dict) and result.get("error_key"):
                await message.answer(t(result["error_key"], user_lang))
                return

            if isinstance(result, dict) and result.get("feedback_text"):
                await message.answer(result["feedback_text"])
            else:
                await message.answer(t("course_homework_received", user_lang))

            if isinstance(result, dict) and result.get("ask_next_study_time"):
                reminder_already_set = getattr(progress, "reminder_enabled", False)
                shown_count = getattr(progress, "reminder_prompt_count", 0) or 0

                if not reminder_already_set and shown_count < 2:
                    # Faqat eslatma o'rnatilmagan va 2 martadan kam ko'rsatilganda chiqar
                    progress.reminder_prompt_count = shown_count + 1
                    await session.commit()
                    await message.answer(
                        t("course_next_study_time_optional", user_lang),
                        reply_markup=_next_study_time_keyboard(user_lang),
                    )
                else:
                    # Eslatma allaqachon o'rnatilgan yoki 2 marta ko'rsatilgan — o'tkazib yuborish
                    await engine.set_next_study_at(message.from_user.id, None)
                    _, rp, rl, re_err = await engine.get_current_lesson(message.from_user.id)
                    if not re_err:
                        if rp.waiting_for == "review_choice":
                            await message.answer(
                                t("course_review_choice", user_lang),
                                reply_markup=review_choice_keyboard(user_lang),
                            )
                        else:
                            await send_course_completion_prompt(
                                respond=message.answer,
                                engine=engine,
                                lesson=rl,
                                lang=user_lang,
                            )

            return

        if progress.waiting_for == "next_study_time":
            skip_map = {
                "uz": "O‘tkazib yuborish",
                "ru": "Пропустить",
                "tj": "Гузаронидан",
            }

            if (message.text or "").strip() == skip_map.get(user_lang, "Пропустить"):
                await engine.set_next_study_at(message.from_user.id, None)
                await message.answer(
                    t("course_next_study_time_skipped", user_lang),
                    reply_markup=course_menu_keyboard(user_lang),
                )
                _, refreshed_progress, refreshed_lesson, refreshed_error = await engine.get_current_lesson(message.from_user.id)
                if refreshed_error:
                    return
                if refreshed_progress.waiting_for == "review_choice":
                    await message.answer(
                        t("course_review_choice", user_lang),
                        reply_markup=review_choice_keyboard(user_lang),
                    )
                else:
                    await send_course_completion_prompt(
                        respond=message.answer,
                        engine=engine,
                        lesson=refreshed_lesson,
                        lang=user_lang,
                    )
                return

            next_study_at = _parse_next_study_at(message.text or "")
            if not next_study_at:
                await message.answer(
                    t("course_invalid_time_format", user_lang),
                    reply_markup=_next_study_time_keyboard(user_lang),
                )
                return

            await engine.set_next_study_at(message.from_user.id, next_study_at)
            await message.answer(
                t("course_next_study_time_saved", user_lang),
                reply_markup=course_menu_keyboard(user_lang),
            )
            _, refreshed_progress, refreshed_lesson, refreshed_error = await engine.get_current_lesson(message.from_user.id)
            if refreshed_error:
                return
            if refreshed_progress.waiting_for == "review_choice":
                await message.answer(
                    t("course_review_choice", user_lang),
                    reply_markup=review_choice_keyboard(user_lang),
                )
            else:
                await send_course_completion_prompt(
                    respond=message.answer,
                    engine=engine,
                    lesson=refreshed_lesson,
                    lang=user_lang,
                )
            return

        message_repo = MessageRepository(session)
        recent = await message_repo.get_recent_by_user(
            user_id=current_user.id,
            limit=10,
        )

        current_step = progress.current_step
        # For intro step, don't use history to avoid repetition
        if current_step == "intro":
            course_history = []
        else:
            course_history = [
                {"role": m.role, "content": m.content}
                for m in recent
                if m.content_type == "course" and m.role in ("user", "assistant")
            ][-4:]

        await message_repo.create(
            user_id=current_user.id,
            role="user",
            content=message.text or "",
            content_type="course",
        )

        import asyncio as _asyncio
        if current_step == "quiz":
            _anim_msg = await message.answer("🔎")
            _anim_task = None
        else:
            _emojis = ["🪄", "💫", "🪄", "💫", "🪄", "💫"]
            _anim_msg = await message.answer(_emojis[0])

            async def _animate():
                for _i in range(1, 30):
                    await _asyncio.sleep(1)
                    try:
                        await _anim_msg.edit_text(_emojis[_i % len(_emojis)])
                    except Exception:
                        break

            _anim_task = _asyncio.create_task(_animate())

        tutor_text = await tutor.generate_step_response(
            user_language=current_user.language,
            user_level=current_user.level,
            lesson=lesson,
            step=progress.current_step,
            user_message=message.text or "",
            history=course_history,
        )

        if _anim_task:
            _anim_task.cancel()
        try:
            await _anim_msg.delete()
        except Exception:
            pass

        await message_repo.create(
            user_id=current_user.id,
            role="assistant",
            content=tutor_text,
            content_type="course",
        )
        await session.commit()

        _content_steps = {
            "intro", "vocab", "vocabulary", "dialogue", "grammar",
            "vocab_1", "vocab_2",
            "dialogue_1", "dialogue_2", "dialogue_3", "dialogue_4",
        }
        if progress.current_step in _content_steps:
            ai_keyboard = course_tushundim_keyboard(user_lang)
        else:
            ai_keyboard = _keyboard_for_step(user_lang, progress.current_step, lesson)

        await message.answer(
            tutor_text,
            reply_markup=ai_keyboard,
            parse_mode="HTML",
        )
        return

    can_use, message_key = await access_service.can_use_text_ai(message.from_user.id)

    if not can_use:
        if message_key == "access_daily_limit_reached":
            if user and not await user_repo.was_daily_limit_offer_sent_today(user):
                await user_repo.mark_daily_limit_offer_sent(user)
                await session.commit()
                await message.answer(
                    t("referral_daily_limit_offer", user_lang),
                    reply_markup=referral_daily_limit_keyboard(user_lang),
                )
                return

            await message.answer(t("access_daily_limit_reached", user_lang))
            return

        await message.answer(t(message_key, user_lang))
        return

    effect = ResponseEffect(message)
    await effect.start()

    try:
        qa_service = QAService(session)
        reply = await qa_service.handle_user_message(
            bot=message.bot,
            telegram_id=message.from_user.id,
            text=message.text,
            telegram_message_id=message.message_id,
        )
    finally:
        await effect.stop()

    if reply.startswith("access_"):
        await message.answer(t(reply, user_lang))
        return

    await message.answer(reply)


@router.message(F.photo)
async def handle_image_message(message: Message, session):
    user_repo = UserRepository(session)
    access_service = AccessService(session)
    image_input_service = ImageInputService()

    user = await user_repo.get_by_telegram_id(message.from_user.id)
    user_lang = user.language if user and user.language else "ru"

    can_use, message_key = await access_service.can_use_image_ai(message.from_user.id)
    if not can_use:
        if message_key == "access_daily_image_limit_reached":
            await message.answer(
                t("access_daily_image_limit_reached", user_lang),
                reply_markup=photo_limit_subscription_keyboard(user_lang),
            )
            return

        await message.answer(t(message_key, user_lang))
        return

    if not user:
        await message.answer(t("access_start_first", user_lang))
        return

    file_id = image_input_service.get_image_file_id(message)
    mime_type = image_input_service.get_image_mime_type(message)

    if not file_id:
        await message.answer(t("image_invalid_format", user_lang))
        return

    effect = ResponseEffect(message)
    await effect.start()

    try:
        image_qa_service = ImageQAService(session)
        reply = await image_qa_service.handle_user_image(
            bot=message.bot,
            telegram_id=message.from_user.id,
            file_id=file_id,
            mime_type=mime_type,
            telegram_message_id=message.message_id,
        )
    finally:
        await effect.stop()

    if reply.startswith("access_"):
        await message.answer(t(reply, user_lang))
        return

    await message.answer(reply)


@router.message(F.document)
async def handle_unsupported_document(message: Message, session):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(message.from_user.id)
    user_lang = user.language if user and user.language else "ru"

    if user and user.selected_plan_type:
        await message.answer(
            t("payment_send_screenshot_only", user_lang),
            reply_markup=checkout_keyboard(user_lang),
        )
        return

    await message.answer(t("image_invalid_format", user_lang))
