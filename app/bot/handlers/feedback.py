from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.bot.fsm.feedback import FeedbackStates
from app.bot.keyboards.feedback import (
    feedback_cancel_keyboard,
    feedback_dislike_keyboard,
    feedback_dislike_label,
    feedback_like_keyboard,
    feedback_like_label,
)
from app.bot.utils.i18n import t
from app.repositories.bot_feedback_repo import BotFeedbackRepository
from app.repositories.user_repo import UserRepository
from app.services.admin_notify_service import AdminNotifyService
from app.services.bot_feedback_service import BotFeedbackService


router = Router()


def _parse_feedback_callback(data: str):
    parts = (data or "").split(":")
    if len(parts) < 3 or parts[0] != "fb":
        return None
    try:
        feedback_id = int(parts[1])
    except ValueError:
        return None
    action = parts[2]
    code = parts[3] if len(parts) > 3 else None
    return feedback_id, action, code


async def _load_feedback_context(session, telegram_id: int, feedback_id: int):
    feedback_repo = BotFeedbackRepository(session)
    user_repo = UserRepository(session)
    feedback = await feedback_repo.get_by_id(feedback_id)
    user = await user_repo.get_by_telegram_id(telegram_id)
    if not feedback or not user or feedback.telegram_id != telegram_id:
        return feedback_repo, None, None
    return feedback_repo, feedback, user


async def _edit_message(target, text: str, reply_markup=None) -> None:
    try:
        await target.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception:
        await target.answer(text, reply_markup=reply_markup, parse_mode="HTML")


async def _edit_stored_message(message: Message, message_id: int, text: str, reply_markup=None) -> None:
    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode="HTML",
        )
    except Exception:
        sent = await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
        message_id = sent.message_id

    try:
        await message.delete()
    except Exception:
        pass


@router.callback_query(F.data.startswith("fb:"))
async def feedback_callback_handler(callback: CallbackQuery, state: FSMContext, session):
    parsed = _parse_feedback_callback(callback.data or "")
    if not parsed:
        await callback.answer()
        return

    feedback_id, action, code = parsed
    feedback_repo, feedback, user = await _load_feedback_context(
        session,
        callback.from_user.id,
        feedback_id,
    )
    lang = user.language if user and user.language else "ru"

    if not feedback or not user:
        await callback.answer(t("feedback_not_found", lang), show_alert=True)
        return

    if feedback.status == "completed":
        await callback.answer(t("feedback_already_completed", lang), show_alert=True)
        return

    if action == "cancel_other":
        data = await state.get_data()
        field = data.get("field")
        await state.clear()
        if field == "disliked":
            await _edit_message(
                callback.message,
                t("feedback_dislike_question", lang),
                feedback_dislike_keyboard(feedback.id, lang),
            )
        else:
            await _edit_message(
                callback.message,
                t("feedback_like_question", lang),
                feedback_like_keyboard(feedback.id, lang),
            )
        await callback.answer()
        return

    if action == "like" and code:
        if code == "other":
            await state.set_state(FeedbackStates.waiting_other_text)
            await state.update_data(
                feedback_id=feedback.id,
                field="liked",
                message_id=callback.message.message_id,
            )
            await _edit_message(
                callback.message,
                t("feedback_other_like_prompt", lang),
                feedback_cancel_keyboard(feedback.id, lang),
            )
            await callback.answer()
            return

        await feedback_repo.save_liked(feedback, code, feedback_like_label(code, lang))
        await _edit_message(
            callback.message,
            t("feedback_dislike_question", lang),
            feedback_dislike_keyboard(feedback.id, lang),
        )
        await session.commit()
        await callback.answer()
        return

    if action == "dislike" and code:
        if code == "other":
            await state.set_state(FeedbackStates.waiting_other_text)
            await state.update_data(
                feedback_id=feedback.id,
                field="disliked",
                message_id=callback.message.message_id,
            )
            await _edit_message(
                callback.message,
                t("feedback_other_dislike_prompt", lang),
                feedback_cancel_keyboard(feedback.id, lang),
            )
            await callback.answer()
            return

        await feedback_repo.save_disliked(feedback, code, feedback_dislike_label(code, lang))
        await BotFeedbackService(session).finish_feedback(feedback, user)
        await session.commit()
        await _edit_message(callback.message, t("feedback_thanks", lang))
        await AdminNotifyService().notify_bot_feedback(
            bot=callback.bot,
            feedback=feedback,
            user=user,
        )
        await callback.answer()
        return

    await callback.answer()


@router.message(StateFilter(FeedbackStates.waiting_other_text), F.text)
async def feedback_other_text_handler(message: Message, state: FSMContext, session):
    data = await state.get_data()
    feedback_id = data.get("feedback_id")
    field = data.get("field")
    message_id = data.get("message_id")

    feedback_repo, feedback, user = await _load_feedback_context(
        session,
        message.from_user.id,
        int(feedback_id or 0),
    )
    lang = user.language if user and user.language else "ru"

    if not feedback or not user or feedback.status == "completed":
        await state.clear()
        await message.answer(t("feedback_not_found", lang))
        return

    text = (message.text or "").strip()
    if not text:
        await message.answer(t("feedback_other_empty", lang))
        return

    if field == "liked":
        await feedback_repo.save_liked(feedback, "other", text[:1000])
        await state.clear()
        await session.commit()
        await _edit_stored_message(
            message,
            int(message_id or feedback.prompt_message_id or message.message_id),
            t("feedback_dislike_question", lang),
            feedback_dislike_keyboard(feedback.id, lang),
        )
        return

    if field == "disliked":
        await feedback_repo.save_disliked(feedback, "other", text[:1000])
        await BotFeedbackService(session).finish_feedback(feedback, user)
        await state.clear()
        await session.commit()
        await _edit_stored_message(
            message,
            int(message_id or feedback.prompt_message_id or message.message_id),
            t("feedback_thanks", lang),
        )
        await AdminNotifyService().notify_bot_feedback(
            bot=message.bot,
            feedback=feedback,
            user=user,
        )
        return

    await state.clear()
    await message.answer(t("feedback_not_found", lang))


@router.message(StateFilter(FeedbackStates.waiting_other_text))
async def feedback_other_non_text_handler(message: Message, state: FSMContext, session):
    user = await UserRepository(session).get_by_telegram_id(message.from_user.id)
    lang = user.language if user and user.language else "ru"
    await message.answer(t("feedback_other_text_only", lang))
