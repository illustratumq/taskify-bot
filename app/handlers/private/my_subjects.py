from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.database.services.enums import TaskStatusEnum
from app.database.services.repos import SubjectRepo, TaskRepo
from app.keyboards import buttons
from app.keyboards.inline.menu import menu_cb
from app.keyboards.inline.subjects import my_subjects_kb, subject_cb


async def view_subjects_cmd(call: CallbackQuery, callback_data: dict, subject_db: SubjectRepo, task_db: TaskRepo):
    subjects = await subject_db.get_subject_user(call.from_user.id)

    if not subjects:
        await call.answer('Упс, ти не додав жодного предмету', show_alert=True)
        return

    subjects.sort(key=lambda s: s.created_at)
    subject_id = int(callback_data['subject_id']) if 'subject_id' in callback_data.keys() else subjects[0].subject_id
    subject_sorted = callback_data['sorted'] if 'sorted' in callback_data.keys() else 'None'

    text = (
        f'{buttons.menu.my_subjects[0]} [Мої предмети]\n\n'
        f'{create_subjects_list(subjects, subject_id)}\n'
        f'{await create_subject_text(subject_id, subject_db, task_db)}'
    )

    await call.message.edit_text(text, reply_markup=my_subjects_kb(subjects, subject_id, subject_sorted))


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(view_subjects_cmd, menu_cb.filter(action='my_subjects'), state='*')
    dp.register_callback_query_handler(view_subjects_cmd, subject_cb.filter(action='pag'), state='*')


def create_subjects_list(subjects: list[SubjectRepo.model], subject_id: int, is_tag: bool = True):
    text = ''
    for subject, num in zip(subjects, range(1, len(subjects) + 1)):
        brackets = ('<b>[', f']</b> {"#" + subject.tag if is_tag else ""}') if subject.subject_id == subject_id else ('', '')
        text += f'{num}. {brackets[0]}{subject.name}{brackets[-1]}\n'
    return text


async def create_subject_text(subject_id: int, subject_db: SubjectRepo, task_db: TaskRepo):
    subject = await subject_db.get_subject(subject_id)
    tasks = await task_db.get_task_subject(subject_id)
    return (
        f'Опис предмету: {subject.description}\n'
        f'📘 Завдання для цьго предмету: {create_tasks_list(tasks)}'
    )


def create_tasks_list(tasks: list[TaskRepo.model]):
    text = ''
    if not tasks:
        return 'Немає завдань'
    text += '\n'
    for task, num in zip(tasks, range(1, len(tasks) + 1)):
        marker = ' ✔' if task.status == TaskStatusEnum.COMPLETE else ''
        text += f'  {num}. {task.name}{marker}\n'
    return text
