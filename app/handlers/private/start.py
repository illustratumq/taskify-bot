from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.config import Config
from app.database.services.repos import UserRepo


async def start_cmd(msg: Message, user_db: UserRepo):
    user = await user_db.get_user(msg.from_user.id)
    await msg.answer(f'Мої вітаннячка, #{user.user_id}')


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
