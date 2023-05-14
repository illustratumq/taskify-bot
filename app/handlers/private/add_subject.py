from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.services.repos import SubjectRepo, TaskRepo
from app.handlers.private.my_subjects import view_subjects_cmd
from app.keyboards.inline.back import back_kb
from app.keyboards.inline.menu import menu_cb
from app.keyboards.inline.settings import confirm_moderate_kb
from app.states.states import AddSubjectSG

cancel_kb = back_kb('◀ Відмінити')


async def add_subject_cmd(call: CallbackQuery, callback_data: dict, state: FSMContext):
    text = (
        '📚 [Додати предмет]\n\n'
        '<b>1)</b> Напиши назву предмету, який бажаєш додати 👇'
    )
    msg = await call.message.edit_text(text, reply_markup=cancel_kb)
    await state.update_data(last_msg_id=msg.message_id)
    await AddSubjectSG.Name.set()


async def save_subject_name(msg: Message, state: FSMContext):
    subject_name = msg.text
    if len(subject_name) > 255:
        error_text = (
            'Упс, назва предмету занадто велика, максимальна к-ть символів 255, '
            f'замість {len(subject_name)}, спробуй ще раз.'
        )
        await msg.answer(error_text)
        return
    await delete_previous_message(msg, state)
    text = (
        '📚 [Додати предмет]\n\n'
        f'<b>Назва предмету:</b> {subject_name}\n\n'
        f'<b>2)</b> Напиши опис, до цього предмету 👇'
    )
    msg = await msg.answer(text, reply_markup=cancel_kb)
    await state.update_data(name=subject_name, last_msg_id=msg.message_id)
    await AddSubjectSG.Description.set()


async def save_subject_description(msg: Message, state: FSMContext):
    subject_description = msg.text
    if len(subject_description) > 500:
        error_text = (
            'Упс, опис предмету занадто великий, максимальна к-ть символів 500, '
            f'замість {len(subject_description)}, спробуй ще раз.'
        )
        await msg.answer(error_text)
        return
    await delete_previous_message(msg, state)
    data = await state.get_data()
    text = (
        '📚 [Додати предмет]\n\n'
        f'<b>Назва предмету:</b> {data["name"]}\n'
        f'<b>Опис предмету:</b> {subject_description}\n\n'
        f'<b>3)</b> Напиши максимальний бал яким буде оцінюватись цей предмет (від 1 до 100) 👇'
    )
    msg = await msg.answer(text, reply_markup=cancel_kb)
    await state.update_data(description=subject_description, last_msg_id=msg.message_id)
    await AddSubjectSG.Grade.set()


async def save_subject_grade(msg: Message, state: FSMContext):
    subject_grade: str = msg.text
    if not subject_grade.isnumeric():
        error_text = (
            'Упс, здаєтся це не число, спробуй ще раз.'
        )
        await msg.answer(error_text)
        return
    elif int(subject_grade) > 100:
        error_text = (
            'Упс, максимальний бал може бути від 1 до 100, спробуй ще раз.'
        )
        await msg.answer(error_text)
        return
    await delete_previous_message(msg, state)
    data = await state.get_data()
    text = (
        '📚 [Додати предмет]\n\n'
        f'<b>Назва предмету:</b> {data["name"]}\n'
        f'<b>Опис предмету:</b> {data["description"]}\n'
        f'<b>Максимальна оцінка:</b> {subject_grade}\n\n'
        f'<b>4)</b> Напиши тег для цього предмету. Декілька предметів можуть мати '
        f'спільний тег, за яким їх можна буде відсорторувати 👇'
    )
    msg = await msg.answer(text, reply_markup=cancel_kb)
    await state.update_data(grade=int(subject_grade), last_msg_id=msg.message_id)
    await AddSubjectSG.Tag.set()


async def save_subject_tag(msg: Message, state: FSMContext):
    subject_tag = msg.text
    if len(subject_tag) > 100:
        error_text = (
            'Упс, здаєтся цей тег занадто великий, спробуй ще раз.'
        )
        await msg.answer(error_text)
        return
    await state.update_data(tag=subject_tag)
    data = await state.get_data()
    await delete_previous_message(msg, state)
    text = (
        f'📚 [Додати предмет]\n\n'
        f'Ура, майже все готово, будь-ласка перевір чи все вірно\n\n'
        f'<b>Предмет</b>: {data["name"]}\n'
        f'<b>Опис предмету:</b> {data["description"]}\n'
        f'<b>Максимальний бал:</b> {data["grade"]}\n\n'
        f'#{data["tag"]}\n\n'
        f'Якщо все окей, підтверди додавання 👇'
    )
    msg = await msg.answer(text, reply_markup=confirm_moderate_kb('add_subject'))
    await AddSubjectSG.Confirm.set()


async def create_subject_cmd(call: CallbackQuery, state: FSMContext, subject_db: SubjectRepo, task_db: TaskRepo):
    data = await state.get_data()
    tag = data['tag']
    name = data['name']
    grade = data['grade']
    description = data['description']
    subject = await subject_db.add(
        name=name, description=description, grade=grade, tag=tag, user_id=call.from_user.id)
    callback_data = dict(subject_id=subject.subject_id)
    await view_subjects_cmd(call, callback_data, subject_db, task_db)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(add_subject_cmd, menu_cb.filter(action='add_subject'), state='*')
    dp.register_message_handler(save_subject_name, state=AddSubjectSG.Name)
    dp.register_message_handler(save_subject_description, state=AddSubjectSG.Description)
    dp.register_message_handler(save_subject_grade, state=AddSubjectSG.Grade)
    dp.register_message_handler(save_subject_tag, state=AddSubjectSG.Tag)
    dp.register_callback_query_handler(create_subject_cmd, menu_cb.filter(action='conf_add_subject'),
                                       state=AddSubjectSG.Confirm)


async def delete_previous_message(msg: Message, state: FSMContext, chat_id: int = None):
    try:
        data = await state.get_data()
        await msg.bot.delete_message(msg.from_user.id if not chat_id else chat_id, data['last_msg_id'])
    except:
        pass
