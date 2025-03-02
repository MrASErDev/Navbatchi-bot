from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


xabarnoma = InlineKeyboardMarkup(
    inline_keyboard=[
        [
        InlineKeyboardButton(text="🗓 Avtomat eslatma", callback_data = "scheduler")
        ],
        [
        InlineKeyboardButton(text="⬅️ Ortga", callback_data = "remove")
        ]
    ]
)

control_call = CallbackData("komanda", "status")
scheduler = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="⏹️ Yoqish", callback_data = control_call.new(status="start_scheduler")),
            InlineKeyboardButton(text="🛑 O'chirish", callback_data = control_call.new(status="stop_scheduler"))
        ],
        [
        InlineKeyboardButton(text="⬅️ Ortga", callback_data = "back2"),
        InlineKeyboardButton(text="⬅️ Boshiga", callback_data = "remove")
        ]
    ], resize_keyboard=True
)


xabar_callback = CallbackData("xabar", "natija")
confirmation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="🖨 Post qilish", callback_data= xabar_callback.new(natija="post")),
            InlineKeyboardButton(text="❌ Bekor qilish", callback_data= xabar_callback.new(natija="cancel"))
        ]
    ]
)

accept = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Yopish", callback_data="accept")
        ]
    ], resize_keyboard=True
)