from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hlink

from app.keyboards.inline.back import back_kb
from app.keyboards.inline.menu import menu_cb


async def help_cmd(call: CallbackQuery):
    text = '⁉ [Допомога]\n\n' + hlink(
        'Нажавши на це повідомлення ви побачите інструкцію по користуванню',
        'https://telegra.ph/%D0%86nstrukc%D1%96ya-po-vikoristannyu-05-13-3'
    )
    await call.message.edit_text(text, reply_markup=back_kb())


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(help_cmd, menu_cb.filter(action='help'), state='*')
