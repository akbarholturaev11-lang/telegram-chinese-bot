from typing import Optional

from aiogram import Bot

from app.repositories.user_repo import UserRepository
from app.repositories.message_repo import MessageRepository
from app.services.ai_service import AIService
from app.services.referral_service import ReferralService
from app.services.access_service import AccessService


class QAService:
    def __init__(self, session):
        self.session = session
        self.user_repo = UserRepository(session)
        self.message_repo = MessageRepository(session)
        self.ai_service = AIService()
        self.referral_service = ReferralService(session)
        self.access_service = AccessService(session)

    async def handle_user_message(
        self,
        bot: Bot,
        telegram_id: int,
        text: str,
        telegram_message_id: Optional[int] = None,
    ) -> str:
        can_use, message_key = await self.access_service.can_use_text_ai(telegram_id)
        if not can_use:
            return message_key

        user = await self.user_repo.get_by_telegram_id(telegram_id)
        if not user:
            return "access_start_first"

        cleaned_text = text.strip()
        if not cleaned_text:
            return "access_start_first"

        recent_messages = await self.message_repo.get_recent_by_user(
            user_id=user.id,
            limit=5,
        )

        history = [
            {
                "role": msg.role,
                "content": msg.content,
            }
            for msg in recent_messages
            if msg.role in ("user", "assistant") and msg.content_type != "image_context"
        ]

        latest_image_context = await self.message_repo.get_latest_image_context_by_user(
            user_id=user.id,
        )
        if latest_image_context:
            history.insert(
                0,
                {
                    "role": "system",
                    "content": latest_image_context.content,
                },
            )

        await self.message_repo.create(
            user_id=user.id,
            role="user",
            content=cleaned_text,
            content_type="text",
            telegram_message_id=telegram_message_id,
        )

        assistant_reply = await self.ai_service.generate_reply(
            text=cleaned_text,
            user_language=user.language,
            user_level=user.level,
            history=history,
        )

        await self.message_repo.create(
            user_id=user.id,
            role="assistant",
            content=assistant_reply,
            content_type="text",
        )

        await self.access_service.consume_one_question(telegram_id)

        await self.referral_service.activate_referral_if_eligible(
            bot=bot,
            invited_user_telegram_id=telegram_id,
        )

        await self.session.commit()
        return assistant_reply
