from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from loader import dp

from keyboards.default.menu import menu
from keyboards.inline.inlinekeyboards import xabarnoma, scheduler, accept, confirmation, xabar_callback
from data.config import GROUPS

@dp.callback_query_handler(text="accept")
async def show_menu(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("<b>Ushbu menyudan yana foydalanishingiz mumkin:</b>", reply_markup=menu)

@dp.message_handler(text="⚙️ Sozlamalar")
async def show_menu(message: Message):
    await message.answer("<b>Sozlamalar</b> bo'limi tanlandi:", reply_markup=ReplyKeyboardRemove())
    await message.answer("🗓 Avtomat eslatma - Navbatchilikni xodimga avtomatik eslatish bo'limi\n📝 Yangi xabarnoma - Guruhga yangi xabar qoldirish bo'limi\n⬅️ ortga - bosh menyuga qaytish", reply_markup=xabarnoma)

@dp.callback_query_handler(Text(contains="scheduler"))
async def show_menu(call: CallbackQuery):
    await call.message.answer("Kunlik navbat eslatmalarni sozlang:", reply_markup=scheduler)

@dp.callback_query_handler(Text(contains="back2"))
async def show_menu(call: CallbackQuery):
    await call.message.answer("<b>Sozlamalar</b> bo'limi\n🗓 Avtomat eslatma - Navbatchilikni xodimga avtomatik eslatish bo'limi:",reply_markup=xabarnoma)
    
@dp.callback_query_handler(Text(contains="remove"))
async def show_menu(call: CallbackQuery):
    await call.message.answer("Asosiy sahifaga qaytdingiz:",reply_markup=menu)






