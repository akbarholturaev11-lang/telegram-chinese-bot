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

        response = await self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )

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
            model="gpt-4o",
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
