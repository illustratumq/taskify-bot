from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from app.database.services.repos import SubjectRepo, TaskRepo
from app.handlers.private.add_subject import delete_previous_message
from app.handlers.private.my_subjects import view_subjects_cmd
from app.keyboards import buttons
from app.keyboards.inline.back import back_kb
from app.keyboards.inline.menu import menu_cb
from app.keyboards.inline.settings import confirm_moderate_kb
from app.keyboards.inline.subjects import subject_cb, add_task_subject
from app.misc.times import now
from app.states.states import AddTaskSG


async def add_task_cmd(call: CallbackQuery, callback_data: dict, subject_db: SubjectRepo, state: FSMContext):
    subject_id = int(callback_data['subject_id'])
    await state.update_data(subject_id=subject_id)
    subject = await subject_db.get_subject(subject_id)
    text = (
        f'➕{buttons.menu.my_task[0]} [Додати завдання]\n\n'
        f'Ти бажаєш додати завднання для твого предмету {subject.name}, '
        f'давай поченмо з назви завдання 👇'
    )
    msg = await call.message.edit_text(text, reply_markup=back_kb(to='subject', subject_id=subject_id))
    await state.update_data(last_msg_id=msg.message_id, subject_id=subject_id,
                            description=None, dealline=None)
    await AddTaskSG.Name.set()


async def save_task_name(msg: Message, state: FSMContext):
    task_name = msg.text
    if len(task_name) > 255:
        error_text = (
            f'Упс, максиамльна к-ть символів 255, замість {len(task_name)}'
        )
        await msg.answer(error_text)
        return
    data = await state.get_data()
    await delete_previous_message(msg, state)
    text = (
        f'➕{buttons.menu.my_task[0]} [Додати завдання]\n\n'
        f'Назва завдання: {task_name}\n\n'
        f'Додай опис, якщо він потрібний, або пропусти цей крок 👇'
    )
    msg = await msg.answer(text, reply_markup=add_task_subject(data['subject_id'], 'description'))
    await state.update_data(name=task_name, last_msg_id=msg.message_id)
    await AddTaskSG.Description.set()


async def save_task_description(msg: Message, state: FSMContext):
    task_description = msg.text
    if task_description == 'skip':
        task_description = None
    elif len(task_description) > 1500:
        error_text = (
            f'Упс, максиамльна к-ть символів 255, замість {len(task_description)}'
        )
        await msg.answer(error_text)
        return
    data = await state.get_data()
    await delete_previous_message(msg, state)
    text = (
        f'➕{buttons.menu.my_task[0]} [Додати завдання]\n\n'
        f'Назва завдання: {data["name"]}\n'
        f'Опис завдання: {data["description"] if task_description else "Немає"}\n\n'
        f'Додай дедлайн у форматі день.місяць.рік (наприклад 24.08.2023), якщо він потрібний, або пропусти цей крок 👇'
    )
    msg = await msg.answer(text, reply_markup=add_task_subject(data['subject_id'], 'deadline'))
    await state.update_data(description=task_description, last_msg_id=msg.message_id)
    await AddTaskSG.Deadline.set()


async def save_task_deadline(msg: Message, state: FSMContext):
    task_deadline = msg.text
    if task_deadline == 'skip':
        task_deadline = None
    else:
        if not check_deadline_correct(task_deadline):
            error_text = (
                'Упс, схоже щось не так. Зауваж, формат дедлайну має бути день.місяць.рік (наприклад 24.08.2023), '
                'спробуй ще раз'
            )
            await msg.answer(error_text)
            return
    data = await state.get_data()
    await delete_previous_message(msg, state)
    text = (
        f'➕{buttons.menu.my_task[0]} [Додати завдання]\n\n'
        f'Ура майже все готово, перевір чи все правильно\n\n'
        f'Назва завдання: {data["name"]}\n'
        f'Опис завдання: {data["description"] if data["description"] else "Немає"}\n'
        f'Дедлайн: {task_deadline if task_deadline else "Немає"}\n\n'
        f'Якщо все окей, підвтерди довання 👇'
    )
    msg = await msg.answer(text, reply_markup=confirm_moderate_kb('add_task'))
    await state.update_data(deadline=task_deadline, msg=msg.message_id)
    await AddTaskSG.Confirm.set()


async def create_task_cmd(call: CallbackQuery, callback_data: dict, task_db: TaskRepo, subject_db: SubjectRepo,
                          state: FSMContext):
    print('here')
    data = await state.get_data()
    subject_id = data['subject_id']
    name = data['name']
    description = data['description']
    deadline = data['deadline']

    task = await task_db.add(
        subject_id=subject_id, name=name, description=description, deadline=deadline
    )
    task.is_deadline_wasted(task_db)
    callback_data.update(subject_id=subject_id)
    await view_subjects_cmd(call, callback_data, subject_db, task_db)
    await state.finish()


async def skip_description(call: CallbackQuery, state: FSMContext):
    call.message.text = 'skip'
    await delete_previous_message(call.message, state, chat_id=call.from_user.id)
    await save_task_description(call.message, state)


async def skip_deadline(call: CallbackQuery, state: FSMContext):
    call.message.text = 'skip'
    await delete_previous_message(call.message, state, chat_id=call.from_user.id)
    await save_task_deadline(call.message, state)


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(add_task_cmd, subject_cb.filter(action='add_task'), state='*')
    dp.register_message_handler(save_task_name, state=AddTaskSG.Name)

    dp.register_callback_query_handler(skip_description, subject_cb.filter(action='skip_description'), state='*')
    dp.register_message_handler(save_task_description, state=AddTaskSG.Description)

    dp.register_callback_query_handler(skip_deadline, subject_cb.filter(action='skip_deadline'), state='*')
    dp.register_message_handler(save_task_deadline, state=AddTaskSG.Deadline)

    dp.register_callback_query_handler(create_task_cmd, menu_cb.filter(action='conf_add_task'), state='*')


def check_deadline_correct(deadline: str):
    try:
        return now().strptime(deadline, '%d.%m.%Y')
    except:
        pass
