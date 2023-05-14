from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.services.repos import SubjectRepo
from app.handlers.private.add_subject import delete_previous_message
from app.keyboards import buttons
from app.keyboards.inline.back import back_kb
from app.keyboards.inline.subjects import subject_cb, edit_subjects_kb
from app.states.states import EditSubjectSG


async def edit_subject_cmd(call: CallbackQuery | Message, callback_data: dict, subject_db: SubjectRepo):
    subject_id = int(callback_data['subject_id'])
    subject = await subject_db.get_subject(subject_id)
    subject_sorted = callback_data['sorted']
    text = (
        f'{buttons.menu.my_subjects[0]} [Редагувати предмет]\n\n'
        f'Назва: {subject.name}\n'
        f'Опис: {subject.description}\n'
        f'Максимальний бал: {subject.grade}\n\n'
        f'Обери, що хочеш редагувати'
    )
    msg = call.message if isinstance(call, CallbackQuery) else call
    try:
        await msg.edit_text(text, reply_markup=edit_subjects_kb(subject_id, subject_sorted))
    except:
        await msg.answer(text, reply_markup=edit_subjects_kb(subject_id, subject_sorted))


async def edit_name_cmd(call: CallbackQuery, callback_data: dict, state: FSMContext):
    text = (
        '📚 [Змінити назву]\n\n'
        'Напиши назву предмету,на яку бажаєш змінити 👇'
    )

    msg = await call.message.edit_text(text,
                                       reply_markup=back_kb(to='edit_subject', subject_id=callback_data['subject_id']))
    await state.update_data(subject_id=callback_data['subject_id'], last_msg_id=msg.message_id)
    await EditSubjectSG.Name.set()


async def edit_description_cmd(call: CallbackQuery, callback_data: dict, state: FSMContext):
    text = (
        '📚 [Змінити назву]\n\n'
        'Напиши опис предмету,на який бажаєш змінити 👇'
    )

    msg = await call.message.edit_text(text,
                                       reply_markup=back_kb(to='edit_subject', subject_id=callback_data['subject_id']))
    await state.update_data(subject_id=callback_data['subject_id'], last_msg_id=msg.message_id)
    await EditSubjectSG.Description.set()


async def edit_grade_cmd(call: CallbackQuery, callback_data: dict, state: FSMContext):
    text = (
        '📚 [Змінити назву]\n\n'
        'Напиши максимальний бал предмету,на який бажаєш змінити 👇'
    )

    msg = await call.message.edit_text(text,
                                       reply_markup=back_kb(to='edit_subject', subject_id=callback_data['subject_id']))
    await state.update_data(subject_id=callback_data['subject_id'], last_msg_id=msg.message_id)
    await EditSubjectSG.Grade.set()


async def edit_subject_name(msg: Message, state: FSMContext, subject_db: SubjectRepo):
    subject_name = msg.text
    data = await state.get_data()
    if len(subject_name) > 255:
        error_text = (
            'Упс, назва предмету занадто велика, максимальна к-ть символів 255, '
            f'замість {len(subject_name)}, спробуй ще раз.'
        )
        await msg.answer(error_text)
        return
    await delete_previous_message(msg, state)
    await subject_db.update_subject(subject_id=int(data['subject_id']), name=subject_name)
    await edit_subject_cmd(msg, dict(subject_id=data['subject_id'], sorted='None'), subject_db)
    await state.finish()


async def edit_subject_description(msg: Message, state: FSMContext, subject_db: SubjectRepo):
    subject_description = msg.text
    data = await state.get_data()
    if len(subject_description) > 500:
        error_text = (
            'Упс, назва предмету занадто велика, максимальна к-ть символів 500, '
            f'замість {len(subject_description)}, спробуй ще раз.'
        )
        await msg.answer(error_text)
        return
    await delete_previous_message(msg, state)
    await subject_db.update_subject(subject_id=int(data['subject_id']), description=subject_description)
    await edit_subject_cmd(msg, dict(subject_id=data['subject_id'], sorted='None'), subject_db)
    await state.finish()


async def edit_subject_grade(msg: Message, state: FSMContext, subject_db: SubjectRepo):
    subject_grade: str = msg.text
    data = await state.get_data()
    if not subject_grade.isnumeric():
        error_text = (
            'Упс, схоже це не число'
        )
        await msg.answer(error_text)
        return
    if int(subject_grade) > 100:
        error_text = (
            'Упс, назва предмету занадто велика, максимальна к-ть символів 500, '
            f'замість {len(subject_grade)}, спробуй ще раз.'
        )
        await msg.answer(error_text)
        return
    await delete_previous_message(msg, state)
    await subject_db.update_subject(subject_id=int(data['subject_id']), grade=int(subject_grade))
    await edit_subject_cmd(msg, dict(subject_id=data['subject_id'], sorted='None'), subject_db)
    await state.finish()


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(edit_subject_cmd, subject_cb.filter(action='edit'), state='*')
    dp.register_callback_query_handler(edit_name_cmd, subject_cb.filter(action='edit_name'), state='*')
    dp.register_callback_query_handler(edit_description_cmd, subject_cb.filter(action='edit_description'), state='*')
    dp.register_callback_query_handler(edit_grade_cmd, subject_cb.filter(action='max_grade'), state='*')
    dp.register_message_handler(edit_subject_name, state=EditSubjectSG.Name)
    dp.register_message_handler(edit_subject_description, state=EditSubjectSG.Description)
    dp.register_message_handler(edit_subject_grade, state=EditSubjectSG.Grade)