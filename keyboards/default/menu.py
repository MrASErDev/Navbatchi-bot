from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📅 Navbatchilik jadvali")],
        [
            KeyboardButton(text="📝 Yangi jadval"),
            KeyboardButton(text="✍️ Yangi xabar")
        ],
        [KeyboardButton(text="⚙️ Sozlamalar")]
    ],resize_keyboard=True
)