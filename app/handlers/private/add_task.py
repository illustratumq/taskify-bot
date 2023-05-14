from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from app.database.services.repos import SubjectRepo
from app.keyboards import buttons
from app.keyboards.inline.back import back_kb
from app.keyboards.inline.subjects import subject_cb


async def add_task_cmd(call: CallbackQuery, callback_data: dict, subject_db: SubjectRepo, state: FSMContext):
    subject_id = int(callback_data['subject_id'])
    await state.update_data(subject_id=subject_id)
    subject = await subject_db.get_subject(subject_id)
    text = (
        f'➕{buttons.menu.my_task[0]} [Додати завдання]\n\n'
        f'Ти бажаєш додати завднання для твого предмету {subject.name}, '
        f'давай поченмо з назви завдання 👇'
    )
    await call.message.edit_text(text, reply_markup=back_kb(to='subject', subject_id=subject_id))


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(add_task_cmd, subject_cb.filter(action='add_task'), state='*')