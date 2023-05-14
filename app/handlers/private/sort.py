from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.database.services.repos import SubjectRepo, TaskRepo
from app.handlers.private.my_subjects import view_subjects_cmd
from app.keyboards import buttons
from app.keyboards.inline.subjects import subject_cb, sort_kb


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

    text = (f'{buttons.subject.sort[0]} [Сортування]\n\n'
            'Обери за яким параметром ти хочеш відсортувати свої предмети')

    await call.message.edit_text(text, reply_markup=sort_kb(subject_id, sorted))


async def by_tag_cmd(call: CallbackQuery, callback_data: dict, subject_db: SubjectRepo, task_db: TaskRepo):
    callback_data.update(sorted='tag')



    await view_subjects_cmd(call, callback_data, subject_db, task_db)


async def by_deadline_cmd(call: CallbackQuery, callback_data: dict, subject_db: SubjectRepo, task_db: TaskRepo):
    callback_data.update(sorted='deadline')

    await view_subjects_cmd(call, callback_data, subject_db, task_db)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(by_tag_cmd, subject_cb.filter(action='tags'), state='*')
    dp.register_callback_query_handler(by_deadline_cmd, subject_cb.filter(action='deadline'), state='*')
    dp.register_callback_query_handler(sort_cmd, subject_cb.filter(action='sort'), state='*')
