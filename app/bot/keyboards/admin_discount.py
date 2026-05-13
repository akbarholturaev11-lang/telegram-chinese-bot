from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def discount_panel_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Yangi chegirma", callback_data="disc:new")],
            [InlineKeyboardButton(text="📋 Oxirgi chegirmalar", callback_data="disc:list")],
        ]
    )


def discount_duration_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1 kun", callback_data="disc:duration:24"),
                InlineKeyboardButton(text="3 kun", callback_data="disc:duration:72"),
                InlineKeyboardButton(text="7 kun", callback_data="disc:duration:168"),
            ],
            [InlineKeyboardButton(text="✍️ Boshqa muddat", callback_data="disc:duration:custom")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="disc:cancel")],
        ]
    )


def discount_status_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Hamma", callback_data="disc:status:all"),
                InlineKeyboardButton(text="Free", callback_data="disc:status:free"),
                InlineKeyboardButton(text="Trial", callback_data="disc:status:trial"),
            ],
            [
                InlineKeyboardButton(text="Active", callback_data="disc:status:active"),
                InlineKeyboardButton(text="Expired", callback_data="disc:status:expired"),
            ],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="disc:cancel")],
        ]
    )


def discount_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Hamma", callback_data="disc:lang:all"),
                InlineKeyboardButton(text="UZ", callback_data="disc:lang:uz"),
                InlineKeyboardButton(text="RU", callback_data="disc:lang:ru"),
                InlineKeyboardButton(text="TJ", callback_data="disc:lang:tj"),
            ],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="disc:cancel")],
        ]
    )


def discount_payment_method_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Hamma", callback_data="disc:method:all"),
                InlineKeyboardButton(text="Visa", callback_data="disc:method:visa"),
            ],
            [
                InlineKeyboardButton(text="Alipay", callback_data="disc:method:alipay"),
                InlineKeyboardButton(text="WeChat", callback_data="disc:method:wechat"),
            ],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="disc:cancel")],
        ]
    )


def discount_plan_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Hamma", callback_data="disc:plan:all"),
                InlineKeyboardButton(text="10 kun", callback_data="disc:plan:10_days"),
                InlineKeyboardButton(text="1 oy", callback_data="disc:plan:1_month"),
            ],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="disc:cancel")],
        ]
    )


def discount_start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Hozir", callback_data="disc:start:now"),
                InlineKeyboardButton(text="Belgilangan vaqt", callback_data="disc:start:scheduled"),
            ],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="disc:cancel")],
        ]
    )


def discount_usage_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Bir marta", callback_data="disc:usage:once"),
                InlineKeyboardButton(text="Takror", callback_data="disc:usage:repeat"),
            ],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="disc:cancel")],
        ]
    )


def discount_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Ishga tushirish", callback_data="disc:confirm"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="disc:cancel"),
            ]
        ]
    )


def discount_list_keyboard(campaigns) -> InlineKeyboardMarkup:
    rows = []
    for campaign in campaigns:
        if campaign.is_active:
            rows.append([
                InlineKeyboardButton(
                    text=f"⛔ #{campaign.id} o'chirish",
                    callback_data=f"disc:disable:{campaign.id}",
                )
            ])
    rows.append([InlineKeyboardButton(text="➕ Yangi chegirma", callback_data="disc:new")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
