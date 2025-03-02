from aiogram import Dispatcher

from loader import dp
from . groups import isGroup


if __name__ == "filters":
    dp.filters_factory.bind(isGroup)
    pass
