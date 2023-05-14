from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.services.repos import SubjectRepo
from app.handlers.private.add_subject import delete_previous_message
from app.keyboards.inline.back import back_kb
from app.keyboards.inline.subjects import subject_cb, edit_subjects_kb
from app.states.states import AddSubjectSG, EditSubjectSG


async def edit_subject_cmd(call: CallbackQuery | Message, callback_data: dict):
    subject_id = int(callback_data['subject_id'])
    sorted = callback_data['sorted']
    text = (
        'test'
    )
    msg = call.message if isinstance(call, CallbackQuery) else call
    try:
        await msg.edit_text(text, reply_markup=edit_subjects_kb(subject_id, sorted))
    except:
        await msg.answer(text, reply_markup=edit_subjects_kb(subject_id, sorted))


async def edit_name_cmd(call: CallbackQuery, callback_data: dict, state: FSMContext):
    print(callback_data)
    text = (
        '📚 [Змінити назву]\n\n'
        'Напиши назву предмету,на яку бажаєш змінити 👇'
    )

    msg = await call.message.edit_text(text,
                                       reply_markup=back_kb(to='edit_subject', subject_id=callback_data['subject_id']))
    await state.update_data(subject_id=callback_data['subject_id'], last_msg_id=msg.message_id)
    await EditSubjectSG.Name.set()


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

    # msg = await msg.answer(text, reply_markup=cancel_kb)
    subject = await subject_db.update_subject(subject_id=int(data['subject_id']), name=subject_name)
    await edit_subject_cmd(msg, dict(subject_id=data['subject_id'], sorted='None'))


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(edit_subject_cmd, subject_cb.filter(action='edit'), state='*')
    dp.register_callback_query_handler(edit_name_cmd, subject_cb.filter(action='edit_name'), state='*')
    dp.register_message_handler(edit_subject_name, state=EditSubjectSG.Name)
