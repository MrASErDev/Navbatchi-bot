from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from loader import dp, bot
from keyboards.default.menu import menu
from states.password import password
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Password for authentication
PASSWORD = "target1"

# Start Command Handler
@dp.message_handler(CommandStart())
async def start_authentication(message: Message):
    """
    Start the authentication process by asking the user for a password.
    """
    await message.answer(
        f"Salom, {message.from_user.full_name}\n🤖 Telegram botga xush kelibsiz!\n"
        "Iltimos, maxfiy kodni kiriting:"
    )
    await password.kod.set()  # Set the state to wait for the password

# Password Input Handler
@dp.message_handler(state=password.kod)
async def check_password(message: Message, state: FSMContext):
    """
    Check if the entered password is correct.
    """
    user_password = message.text.strip()  # Get the user's input and remove any extra spaces
    logging.info(f"{message.from_user.full_name} is trying to authenticate.")

    if user_password == PASSWORD:
        # Password is correct
        await state.finish()  # Clear the state
        await message.answer("✅ Maxfiy kod to'g'ri! Botdan foydalanishga ruxsat berildi.")
        await bot_start(message)  # Start the bot
    else:
        # Password is incorrect
        await message.answer(
            "❌ Noto'g'ri maxfiy kod! Iltimos, qayta urinib ko'ring.\n"
            "Yoki /cancel buyrug'ini yuboring va jarayonni bekor qiling."
        )

# Cancel Command Handler
@dp.message_handler(commands="cancel", state="*")
async def cancel_authentication(message: Message, state: FSMContext):
    """
    Allow the user to cancel the authentication process.
    """
    current_state = await state.get_state()
    if current_state is None:
        return  # No active state to cancel

    await state.finish()  # Clear the state
    await message.answer(
        "❌ Autentifikatsiya jarayoni bekor qilindi.\n"
        "Qaytadan boshlash uchun /start buyrug'ini yuboring."
    )

# Bot Start Function
async def bot_start(message: Message):
    """
    Send a welcome message and show the main menu after successful authentication.
    """
    await message.answer_photo(
        photo="https://storage.kun.uz/source/thumbnails/_medium/3/kB1i_5Y31ptP0iHYHHWKApR_D3nXbiZw_medium.jpg",
        caption=(
            f"Assalomu aleykum, {message.from_user.full_name}!\n\n"
            "🎯<b> Targetlash va xavflarni monitoring qilish boshqarmasi</b>\n\n"
            "Botdan foydalanish:\n"
            "📅 <b>Navbatchilik jadvali</b> - Xodimlarning navbatchilik kuni ro'yxati.\n"
            "📝 <b>Yangi jadval</b> - Navbatchilik ro'yxatini yangilash\n"
            "✍️ <b>Yangi xabar</b>- guruhga yangi xabar yoki e'lon yozish.\n\n"
            "✅ Dastur bo'yicha avtorskiy huquqlar himoyalangan.\n\n"
            "🧑‍💻 E'tiroz va takliflar uchun murojaat: <a href='https://t.me/MrASErDev'>Admin</a>"
        ),
        reply_markup=menu,
        parse_mode="HTML"
    )