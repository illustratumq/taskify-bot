from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.handlers.private.start import start_cmd
from app.keyboards.inline.back import back_cb


async def back_cmd(call: CallbackQuery, callback_data: dict):
    to = callback_data['to']
    if to == 'menu':
        await call.message.delete()
        await start_cmd(call.message)
        return


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(back_cmd, back_cb.filter(), state='*')
