from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.database.services.repos import UserRepo
from app.keyboards.inline.menu import menu_cb
from app.keyboards.inline.subjects import my_subjects_kb


async def view_subjects_cmd(call: CallbackQuery, callback_data: dict, user_db: UserRepo):
    user = await user_db.get_user(call.from_user.id)
    text = (
        '📚 [Мої предмети]\n\n'
         'Тут ви можете побачити ваші предмети'
    )
    await call.message.edit_text(text, reply_markup=my_subjects_kb())


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(view_subjects_cmd, menu_cb.filter(action='my_subjects'), state='*')
