import base64
from pathlib import Path
from typing import List, Dict, Optional

from openai import AsyncOpenAI

from app.config import settings


class AIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.prompt_path = Path("app/prompts/qa_system.txt")

    def _build_system_prompt(self, user_language: str, user_level: str) -> str:
        template = self.prompt_path.read_text(encoding="utf-8")
        return template.format(
            user_language=user_language,
            user_level=user_level,
        )

    async def generate_reply(
        self,
        text: str,
        user_language: str,
        user_level: str,
        history: Optional[List[Dict[str, str]]] = None,
        model_override: str = None,
        max_completion_tokens: int | None = None,
    ) -> str:
        system_prompt = self._build_system_prompt(
            user_language=user_language,
            user_level=user_level,
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]

        if history:
            for msg in history:
                if msg.get("role") in ("user", "assistant"):
                    messages.append(msg)

        messages.append(
            {
                "role": "user",
                "content": text,
            }
        )

        request = {
            "model": model_override or "o4-mini",
            "messages": messages,
        }
        if max_completion_tokens is not None:
            request["max_completion_tokens"] = max_completion_tokens

        response = await self.client.chat.completions.create(**request)

        return response.choices[0].message.content or ""

    async def generate_vision_reply(
        self,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> str:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:{mime_type};base64,{image_b64}"

        response = await self.client.chat.completions.create(
            model="o4-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": data_url,
                            },
                        },
                    ],
                }
            ],
        )

        return response.choices[0].message.content or ""

    async def transcribe_voice(
        self,
        audio_bytes: bytes,
        filename: str,
        user_language: str,
        user_level: str,
    ) -> str:
        lang_labels = {
            "tj": "Tajik",
            "uz": "Uzbek",
            "ru": "Russian",
        }
        primary_lang = lang_labels.get(user_language, "Russian")
        prompt = (
            "Transcribe this Telegram voice message. Do not translate it. "
            f"The user's interface language is {primary_lang}, and their Chinese level is {user_level}. "
            "The audio is likely in the user's interface language or Chinese. "
            "Preserve Chinese characters, pinyin, names, numbers, and short mixed-language phrases carefully. "
            "If speech is unclear, transcribe only what you can hear."
        )

        response = await self.client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            chunking_strategy="auto",
            file=(filename, audio_bytes, "audio/ogg"),
            prompt=prompt,
            temperature=0,
        )

        if isinstance(response, str):
            return response.strip()
        return (getattr(response, "text", "") or "").strip()
