from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.keyboards.inline.subjects import subject_cb, edit_subjects_kb


async def edit_subject_cmd(call: CallbackQuery, callback_data: dict):
    subject_id = int(callback_data['subject_id'])
    sorted = callback_data['sorted']
    text = (
        'test'
    )
    await call.message.edit_text(text, reply_markup=edit_subjects_kb(subject_id, sorted))


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(edit_subject_cmd, subject_cb.filter(action='edit'), state='*')

