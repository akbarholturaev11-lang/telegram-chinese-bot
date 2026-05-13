from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def _mark(active: bool) -> str:
    return "✅ " if active else ""


def broadcast_panel_keyboard(
    lang_filter: Optional[str],
    status_filter: Optional[str],
    level_filter: Optional[str],
    mode_filter: Optional[str] = None,
    payment_status_filter: Optional[str] = None,
    payment_method_filter: Optional[str] = None,
    plan_filter: Optional[str] = None,
    discount_filter: Optional[str] = None,
    course_promo_filter: Optional[str] = None,
    activity_filter: Optional[str] = None,
) -> InlineKeyboardMarkup:
    def lang_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(lang_filter == val)}{label}",
            callback_data=f"bc:lang:{val or 'all'}",
        )

    def status_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(status_filter == val)}{label}",
            callback_data=f"bc:status:{val or 'all'}",
        )

    def level_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(level_filter == val)}{label}",
            callback_data=f"bc:level:{val or 'all'}",
        )

    def mode_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(mode_filter == val)}{label}",
            callback_data=f"bc:mode:{val or 'all'}",
        )

    def pay_status_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(payment_status_filter == val)}{label}",
            callback_data=f"bc:paystatus:{val or 'all'}",
        )

    def pay_method_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(payment_method_filter == val)}{label}",
            callback_data=f"bc:paymethod:{val or 'all'}",
        )

    def plan_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(plan_filter == val)}{label}",
            callback_data=f"bc:plan:{val or 'all'}",
        )

    def discount_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(discount_filter == val)}{label}",
            callback_data=f"bc:discount:{val or 'all'}",
        )

    def promo_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(course_promo_filter == val)}{label}",
            callback_data=f"bc:promo:{val or 'all'}",
        )

    def activity_btn(val: Optional[str], label: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(
            text=f"{_mark(activity_filter == val)}{label}",
            callback_data=f"bc:activity:{val or 'all'}",
        )

    return InlineKeyboardMarkup(inline_keyboard=[
        [
            lang_btn(None, "Hammasi"),
            lang_btn("uz", "UZ"),
            lang_btn("ru", "RU"),
            lang_btn("tj", "TJ"),
        ],
        [
            status_btn(None, "Hammasi"),
            status_btn("active", "Active"),
            status_btn("trial", "Trial"),
        ],
        [
            status_btn("free", "Free"),
            status_btn("expired", "Expired"),
            status_btn("blocked", "Blocked"),
        ],
        [
            level_btn(None, "Hammasi"),
            level_btn("beginner", "Beginner"),
            level_btn("hsk1", "HSK1"),
            level_btn("hsk2", "HSK2"),
        ],
        [
            level_btn("hsk3", "HSK3"),
            level_btn("hsk4", "HSK4"),
        ],
        [
            mode_btn(None, "Mode: All"),
            mode_btn("qa", "QA"),
            mode_btn("course", "Course"),
        ],
        [
            pay_status_btn(None, "Pay: All"),
            pay_status_btn("none", "None"),
            pay_status_btn("pending", "Pending"),
        ],
        [
            pay_status_btn("approved", "Approved"),
            pay_status_btn("rejected", "Rejected"),
        ],
        [
            pay_method_btn(None, "Method: All"),
            pay_method_btn("visa", "Visa"),
            pay_method_btn("alipay", "Alipay"),
            pay_method_btn("wechat", "WeChat"),
        ],
        [
            plan_btn(None, "Plan: All"),
            plan_btn("10_days", "10d"),
            plan_btn("1_month", "1m"),
        ],
        [
            discount_btn(None, "Discount: All"),
            discount_btn("eligible", "Eligible"),
            discount_btn("used", "Used"),
        ],
        [
            discount_btn("none", "No discount"),
        ],
        [
            promo_btn(None, "Promo: All"),
            promo_btn("sent", "Promo sent"),
            promo_btn("not_sent", "Promo no"),
        ],
        [
            activity_btn(None, "Activity: All"),
            activity_btn("active_7d", "Active 7d"),
            activity_btn("inactive_7d", "Cold 7d"),
        ],
        [
            activity_btn("new_7d", "New 7d"),
        ],
        [InlineKeyboardButton(text="✏️ Matn kiritish", callback_data="bc:enter_text")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="bc:cancel")],
    ])


def broadcast_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yuborish", callback_data="bc:confirm"),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data="bc:cancel"),
        ],
    ])
