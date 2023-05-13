from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from app.keyboards.inline.menu import menu_kb


async def start_cmd(msg: Message):
    text = (
        '📚 Мої предмети\n'
        'Додати або редагувати предмети\n\n'
        '📒 Мої завдання\n'
        'Додати або редагувати завдання для предметів\n\n'
        '⚙ Налаштування\n'
        'Вимкнути або увікнути сповіщення про дедлайни\n\n'
        '💭 Питання\n'
        'Гайд, як користуватися ботом'
    )
    await msg.answer(text, reply_markup=menu_kb())


def setup(dp: Dispatcher):
    dp.register_message_handler(start_cmd, CommandStart(), state='*')
