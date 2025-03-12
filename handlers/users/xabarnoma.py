from loader import dp, bot
from aiogram.types import Message,CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.default.menu import menu
from keyboards.inline.inlinekeyboards import confirmation, xabar_callback
from states.new_message import new_message
from data.config import GROUPS, ADMINS

import logging

# Yangi xabar bo'limi 
@dp.message_handler(text = "✍️ Yangi xabar")
async def show_menu(message: Message):
    await message.answer("Yangi xabar matnini kiriting:")
    await new_message.msg.set()
    logging.info(f"{message.from_user.full_name} is typing to post!")

@dp.message_handler(state = new_message.msg)
async def new_msg(message: Message, state: FSMContext):
    await state.update_data({"user": f"{message.from_user.get_mention()}"})
    await state.update_data({"message": f"{message.html_text}"})

    await message.answer(f"<b>{ message.from_user.full_name} ushbu postni <a href='tg://user?id={ADMINS[0]}'>Admin</a>ga tekshirishdan o'tkazishga yuborasizmi?</b>\n"
                        , reply_markup=confirmation)
    await new_message.confirm.set()
    
@dp.callback_query_handler(xabar_callback.filter(natija="post"), state = new_message.confirm)
async def send_admin(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user = data.get("user") 
    msg = data.get("message")

    await call.message.answer(f"✅ Xabar <a href='tg://user?id={ADMINS[0]}'>Admin</a>ga muvaffaqiyatli yuborildi.")
    await bot.send_message(ADMINS[0], f"Foydalanuvchi {user} quyidagi xabarni chop etmoqchi:")
    await bot.send_message(ADMINS[0], f"{msg}", parse_mode="HTML", reply_markup=confirmation)
    await state.finish()

@dp.callback_query_handler(xabar_callback.filter(natija="cancel"), state = new_message.confirm )
async def send_admin(call: CallbackQuery, state: FSMContext):
    await call.message.answer("🚫 Xabar bekor qilindi.")
    await state.finish()

@dp.callback_query_handler(xabar_callback.filter(natija="post"), user_id=ADMINS  )
async def approve_post(call: CallbackQuery):
    await call.answer("✅ Chop etishga ruxsat berdingiz.", show_alert=True)
    target_group = GROUPS[1]
    message = await call.message.edit_reply_markup()
    await message.send_copy(chat_id=target_group)

@dp.callback_query_handler(xabar_callback.filter(natija='cancel'), user_id=ADMINS)
async def decline_post(call: CallbackQuery):
    await call.answer("🚫 Post rad etildi.", show_alert=True)
    await call.message.edit_reply_markup()
