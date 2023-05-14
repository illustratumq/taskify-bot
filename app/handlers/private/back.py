from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.database.services.repos import SubjectRepo, TaskRepo
from app.handlers.private.edit_subject import edit_subject_cmd
from app.handlers.private.my_subjects import view_subjects_cmd
from app.handlers.private.start import start_cmd
from app.keyboards.inline.back import back_cb


async def back_cmd(call: CallbackQuery, callback_data: dict, state: FSMContext,
                   subject_db: SubjectRepo, task_db: TaskRepo):
    to = callback_data['to']
    if to == 'menu':
        await call.message.delete()
        await start_cmd(call.message, state)
    elif to == 'subject':
        await view_subjects_cmd(call, callback_data, subject_db, task_db)
    elif to == 'edit_subject':
        callback_data.update(sorted='None')
        await edit_subject_cmd(call, callback_data)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(back_cmd, back_cb.filter(), state='*')
