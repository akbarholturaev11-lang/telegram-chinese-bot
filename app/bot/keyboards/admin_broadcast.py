from typing import Optional

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def _mark(active: bool) -> str:
    return "✅ " if active else ""


def broadcast_panel_keyboard(
    lang_filter: Optional[str],
    status_filter: Optional[str],
    level_filter: Optional[str],
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
            status_btn("free", "Expired"),
        ],
        [
            level_btn(None, "Hammasi"),
            level_btn("hsk1", "HSK1"),
            level_btn("hsk2", "HSK2"),
            level_btn("hsk3", "HSK3"),
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
