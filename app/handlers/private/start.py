from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.database.services.repos import UserRepo
from app.keyboards.inline.menu import menu_kb


async def start_cmd(msg: Message):
    text = (
        ''
    )
    await msg.answer(text, reply_markup=menu_kb())


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
