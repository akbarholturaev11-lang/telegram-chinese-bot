from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from app.db.models.discount_campaign import DiscountCampaign
from app.repositories.discount_campaign_repo import DiscountCampaignRepository


@dataclass
class DiscountChoice:
    source: str = "none"
    percent: int = 0
    campaign_id: Optional[int] = None
    title: Optional[str] = None
    details: Optional[str] = None


class DiscountService:
    def __init__(self, session):
        self.repo = DiscountCampaignRepository(session)

    async def get_best_discount(
        self,
        *,
        user,
        plan_type: str,
        payment_method: Optional[str],
    ) -> DiscountChoice:
        choices: list[DiscountChoice] = []

        if user.discount_eligible and not user.discount_used:
            choices.append(
                DiscountChoice(
                    source="referral",
                    percent=20,
                    title="Referral 3/3",
                    details="3 ta do'st taklif qilgani uchun referral chegirma.",
                )
            )

        now = datetime.now(timezone.utc)
        for campaign in await self.repo.list_current(now):
            if not self._matches_campaign(campaign, user, plan_type, payment_method):
                continue
            choice = await self._campaign_choice(campaign, user, now)
            if choice:
                choices.append(choice)

        if not choices:
            return DiscountChoice()

        return max(
            choices,
            key=lambda item: (item.percent, 1 if item.source == "admin_campaign" else 0),
        )

    def _matches_campaign(
        self,
        campaign: DiscountCampaign,
        user,
        plan_type: str,
        payment_method: Optional[str],
    ) -> bool:
        checks = [
            (campaign.audience_status, getattr(user, "status", None)),
            (campaign.audience_language, getattr(user, "language", None)),
            (campaign.audience_level, getattr(user, "level", None)),
            (campaign.payment_method, payment_method),
            (campaign.plan_type, plan_type),
        ]
        return all(expected is None or expected == actual for expected, actual in checks)

    async def _campaign_choice(
        self,
        campaign: DiscountCampaign,
        user,
        now: datetime,
    ) -> Optional[DiscountChoice]:
        last_usage = await self.repo.get_user_last_usage(campaign.id, user.telegram_id)
        if campaign.repeat_interval_days:
            if last_usage and last_usage.submitted_at:
                next_allowed = last_usage.submitted_at.timestamp() + campaign.repeat_interval_days * 86400
                if now.timestamp() < next_allowed:
                    return None
            usage_rule = f"har {campaign.repeat_interval_days} kunda qayta olish mumkin"
        else:
            if last_usage:
                return None
            usage_rule = "bir userga 1 marta"

        used = await self.repo.count_used(
            campaign.id,
            now=now,
            exclude_user_telegram_id=user.telegram_id,
        )
        if campaign.quota_total and used >= campaign.quota_total:
            return None

        quota_text = "limitsiz"
        if campaign.quota_total:
            quota_text = f"{used + 1}/{campaign.quota_total}"

        details = (
            f"Admin kampaniya #{campaign.id}: {campaign.title}; "
            f"limit: {quota_text}; qoida: {usage_rule}; "
            f"amal qiladi: {campaign.starts_at:%Y-%m-%d %H:%M} - {campaign.ends_at:%Y-%m-%d %H:%M} UTC."
        )
        return DiscountChoice(
            source="admin_campaign",
            percent=campaign.percent,
            campaign_id=campaign.id,
            title=campaign.title,
            details=details,
        )
