from aiogram import Router
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.services.onboarding_service import OnboardingService
from app.bot.utils.i18n import t
from app.bot.keyboards.onboarding import language_keyboard, level_keyboard
from app.bot.fsm.onboarding import OnboardingStates


router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: Message,
    state: FSMContext,
    session,
    command: CommandObject,
):
    service = OnboardingService(session)
    first_name = message.from_user.first_name if message.from_user and message.from_user.first_name else "Friend"

    referral_code = command.args if command and command.args else None

    user, created = await service.get_or_create_user(
        telegram_id=message.from_user.id,
        full_name=message.from_user.full_name if message.from_user else None,
        referral_code=referral_code,
    )

    await state.clear()

    if not created and user.language and user.level:
        await message.answer(
            t("welcome_back", user.language, name=first_name)
        )
        return

    onboarding_msg = await message.answer(
        f"{t('welcome', user.language, name=first_name)}\n\n{t('choose_language', user.language)}",
        reply_markup=language_keyboard(),
    )

    await state.update_data(
        onboarding_message_id=onboarding_msg.message_id,
        first_name=first_name,
    )
    await state.set_state(OnboardingStates.choosing_language)


@router.callback_query(OnboardingStates.choosing_language)
async def process_language(callback: CallbackQuery, state: FSMContext, session):
    lang = callback.data.split(":")[1]

    service = OnboardingService(session)

    user, _ = await service.get_or_create_user(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name if callback.from_user else None,
    )
    user.language = lang
    await session.commit()

    await callback.answer()

    data = await state.get_data()
    onboarding_message_id = data.get("onboarding_message_id")
    first_name = data.get("first_name", "Friend")

    try:
        if onboarding_message_id:
            await callback.bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=onboarding_message_id,
                text=f"{t('welcome', lang, name=first_name)}\n\n{t('choose_level', lang)}",
                reply_markup=level_keyboard(lang),
            )
    except Exception:
        pass

    await state.update_data(lang=lang)
    await state.set_state(OnboardingStates.choosing_level)


@router.callback_query(OnboardingStates.choosing_level)
async def process_level(callback: CallbackQuery, state: FSMContext, session):
    level = callback.data.split(":")[1]

    service = OnboardingService(session)

    user, _ = await service.get_or_create_user(
        telegram_id=callback.from_user.id,
        full_name=callback.from_user.full_name if callback.from_user else None,
    )
    user.level = level
    user.learning_mode = "qa"
    await session.commit()

    await callback.answer()

    data = await state.get_data()
    onboarding_message_id = data.get("onboarding_message_id")

    try:
        if onboarding_message_id:
            await callback.bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=onboarding_message_id,
                text=t("level_saved_explained", user.language),
            )
    except Exception:
        pass

    await callback.message.answer(t("trial_started_info", user.language))
    await callback.message.answer(t("send_first_message", user.language))
    await state.clear()
