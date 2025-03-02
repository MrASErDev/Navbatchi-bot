from loader import dp, bot
from aiogram.types import Message, ContentTypes, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from pathlib import Path
import shutil
import pandas as pd
import logging

from keyboards.default.menu import menu
from keyboards.inline.inlinekeyboards import xabarnoma, scheduler, accept
from states.file_data import files
from data.config import GROUPS, ADMINS

download_path = Path("downloads") / "fayllar"
download_path.mkdir(parents=True, exist_ok=True)
data_path = Path("data") / "jadval"
data_path.mkdir(parents=True, exist_ok=True)

# Navbatchilik jadvali bo'limi
@dp.message_handler(text="📅 Navbatchilik jadvali")
async def show_menu(message: Message):
    try:
        df = pd.read_excel(data_path / "jadval.xlsx", index_col=0)

        fish = df["FISH"]
        sana = pd.to_datetime(df["sana"]).dt.strftime("%d.%m.%Y")

        output_message = f"📊 Navbatchilik jadvali:\n\n"
        for day, full_name in zip(sana, fish):
            output_message += f" 🗓 Sana: <b>{day}</b>\n 👮‍♂️ Navbatchi: <b>{full_name}</b>\n\n"
        await message.answer(output_message, reply_markup=accept)

    except Exception as error:
        logging.exception("Jadvalni o'qishda xatolik yuz berdi:")
        await message.answer("Yangi jadval hali shakllantirilmagan!")

# Yangil jadval bo'limi
@dp.message_handler(text="📝 Yangi jadval")
async def show_menu(message: Message):
    if str(message.from_user.id) not in ADMINS:
        await message.answer(f"Kechirasiz, Yangi jadvalni yaratish vakolati faqat admin uchun berilgan!\n🧑‍💻E'tiroz va takliflar uchun <a href='https://t.me/MrASErDev'>Admin</a>ga murojaat qiling ",parse_mode="HTML") 
    else:
        await message.answer(f"Hurmatli ADMIN, {message.from_user.full_name} yangi jadval yaratish uchun excel faylni yuklang:", reply_markup=ReplyKeyboardRemove())
        await files.file.set()
        

@dp.message_handler(content_types=ContentTypes.DOCUMENT, state=files.file)
async def file_download(message: Message, state: FSMContext):
    doc = message.document
    if not doc.file_name.endswith(('.xlsx', '.xls')):
        await message.answer("Iltimos faqat excel faylni yuklang:")
        return
    
    # faylni saqlash
    await message.document.download(destination_file=download_path / doc.file_name)
    await message.reply(f"✅ Siz yuborgan excel fayl muvaffaqiyatli saqlandi!")
    shutil.copy(download_path / doc.file_name, data_path / "jadval.xlsx")
    
    # fayl ma'lumotlarini ishlatish
    try:
        df = pd.read_excel(data_path / "jadval.xlsx", index_col=0)
        user_idi = df["user_id"]
        tg_name = df["tg_name"]
        fish = df["FISH"]
        sana = pd.to_datetime(df["sana"]).dt.strftime("%d.%m.%Y")
        output_message = "📊 Excel ma'lumotlari:\n\n"
        for day, full_name in zip(sana, fish):
            output_message += f" 🗓 Sana: <b>{day}</b>\n 👮‍♂️ Navbatchi: <b>{full_name}</b>\n\n"
        await message.answer(output_message, reply_markup=menu)
    except Exception as error:
        logging.exception("Jadvalni o'qishda xatolik yuz berdi:")
        await message.answer("Jadval tog'ri shakllantirilmagan!")  
    
    await state.finish()