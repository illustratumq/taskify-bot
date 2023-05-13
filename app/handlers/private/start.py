from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.keyboards import buttons
from app.keyboards.inline.menu import menu_kb


async def start_cmd(msg: Message, state: FSMContext):
    await state.finish()
    text = (
        f'{buttons.menu.my_subjects[0]} {buttons.menu.my_subjects.split(" ")[-1]}\n'
        'Додати або редагувати предмети\n\n'
        f'{buttons.menu.my_task[0]} {buttons.menu.my_task.split(" ")[-1]}\n'
        'Додати або редагувати завдання для предметів\n\n'
        f'{buttons.menu.help[0]} {buttons.menu.help.split(" ")[-1]}\n'
        'Гайд, як користуватися ботом\n\n'
        f'{buttons.menu.settings[0]} {buttons.menu.settings.split(" ")[-1]}\n'
        'Вимкнути або увікнути сповіщення про дедлайни'

    )
    await msg.answer(text, reply_markup=menu_kb())


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
