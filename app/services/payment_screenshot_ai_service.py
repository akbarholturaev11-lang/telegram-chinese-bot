from app.services.ai_service import AIService

PAYMENT_VERIFY_PROMPT = """
You are a payment screenshot verifier for a Telegram bot.

Analyze the payment screenshot and extract the following information.

Respond ONLY in this exact JSON format, nothing else:
{
  "amount": <number or null>,
  "currency": <"somoni" or "CNY" or "USD" or "unknown">,
  "date": <"today" or "recent" or "old" or "unknown">,
  "payment_system": <"Alipay" or "WeChat" or "Visa" or "bank_transfer" or "unknown">,
  "verdict": <"trusted" or "suspicious" or "rejected">,
  "reason": <short reason string in Russian, max 10 words>
}

Rules:
- "trusted": amount is visible, date looks recent (today or yesterday), screenshot looks real
- "suspicious": amount found but date unclear or something looks off
- "rejected": no amount found, clearly fake, or unrelated image
- If you cannot determine something, use null or "unknown"
- Do not add any text outside the JSON
"""


class PaymentScreenshotAIService:
    def __init__(self):
        self.ai_service = AIService()

    async def verify_screenshot(
        self,
        image_bytes: bytes,
        mime_type: str,
        expected_amount: int,
        currency: str,
    ) -> dict:
        """
        Returns dict:
        {
            "amount": int or None,
            "currency": str,
            "date": str,
            "payment_system": str,
            "verdict": "trusted" | "suspicious" | "rejected",
            "reason": str,
            "amount_match": bool,
        }
        """
        import json

        raw = await self.ai_service.generate_vision_reply(
            image_bytes=image_bytes,
            mime_type=mime_type,
            prompt=PAYMENT_VERIFY_PROMPT,
        )

        try:
            cleaned = raw.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            result = json.loads(cleaned.strip())
        except Exception:
            result = {
                "amount": None,
                "currency": "unknown",
                "date": "unknown",
                "payment_system": "unknown",
                "verdict": "suspicious",
                "reason": "Не удалось разобрать скриншот",
            }

        ai_amount = result.get("amount")
        result["amount_match"] = (
            ai_amount is not None and abs(int(ai_amount) - expected_amount) <= 2
        )

        return result
