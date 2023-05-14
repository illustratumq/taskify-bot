from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.database.services.enums import TaskStatusEnum
from app.database.services.repos import UserRepo, SubjectRepo, TaskRepo
from app.keyboards import buttons
from app.keyboards.inline.menu import menu_cb

from app.keyboards.inline.subjects import my_subjects_kb, subject_cb, sort_kb


async def sort_cmd(call: CallbackQuery, callback_data: dict, subject_db: SubjectRepo):
    subjects = await subject_db.get_subject_user(call.from_user.id)
    subjects.sort(key=lambda s: s.created_at)

    subject_id = int(callback_data['subject_id']) if 'subject_id' in callback_data.keys() else subjects[0].subject_id
    sorted = callback_data['sorted']

    #
    # text = (
    #     f'{buttons.menu.my_subjects[0]} [Мої предмети]\n\n'
    #     f'{create_subjects_list(subjects, subject_id)}\n'
    #     f'{await create_subject_text(subject_id, subject_db, task_db)}'
    # )

    text = 'ffg'

    await call.message.edit_text(text, reply_markup=sort_kb(subject_id, sorted))


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(sort_cmd, subject_cb.filter(action='sort'), state='*')
