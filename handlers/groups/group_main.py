from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ContentType
from aiogram.dispatcher.filters import Command
from loader import dp

from keyboards.default.menu import menu
from keyboards.inline.inlinekeyboards import accept
from data.config import GROUPS
from filters.groups import isGroup

@dp.message_handler(isGroup())
async def get_group_id(message: Message):
    chat_id = message.chat.id
    chat_idi = GROUPS[0]
    await message.answer(f"Group ID: {chat_id}")
    await message.answer(f"Guruhhi idisi: {chat_idi}")
    await message.answer(f"Guruhhi idisi: {chat_idi==chat_id}")