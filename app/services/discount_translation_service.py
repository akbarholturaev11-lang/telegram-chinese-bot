import json
from typing import Dict

from openai import AsyncOpenAI

from app.config import settings


class DiscountTranslationService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def translate_title(self, title: str) -> Dict[str, str]:
        fallback = {"tj": title, "ru": title, "uz": title}
        if not settings.OPENAI_API_KEY or not title.strip():
            return fallback

        try:
            response = await self.client.chat.completions.create(
                model="o4-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Translate a short Telegram discount campaign title into Tajik Cyrillic, "
                            "Russian, and Uzbek Latin. Return only valid JSON with keys tj, ru, uz. "
                            "Keep emojis, numbers, percentages, and brand names unchanged."
                        ),
                    },
                    {"role": "user", "content": title[:120]},
                ],
            )
            raw = response.choices[0].message.content or ""
            start = raw.find("{")
            end = raw.rfind("}")
            payload = json.loads(raw[start : end + 1] if start >= 0 and end >= 0 else raw)
        except Exception:
            return fallback

        return {
            "tj": str(payload.get("tj") or title)[:180],
            "ru": str(payload.get("ru") or title)[:180],
            "uz": str(payload.get("uz") or title)[:180],
        }
