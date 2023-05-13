from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from app.database.services.repos import UserRepo
from app.keyboards.inline.menu import menu_cb

from app.keyboards.inline.settings import settings_kb


async def settings_cmd(call: CallbackQuery, callback_data: dict, user_db: UserRepo):
    user = await user_db.get_user(call.from_user.id)

    if callback_data['action'] == 'switch':
        notify = False if user.notify else True
    else:
        notify = user.notify

    await user_db.update_user(user.user_id, notify=notify)

    text = (
        '⚙️ [Налаштування]\n\n'
        'Тут ви можете включити або виключити сповіщення.'
    )

    await call.message.edit_text(text, reply_markup=settings_kb(notify))


def setup(dp: Dispatcher):
    dp.register_callback_query_handler(settings_cmd, menu_cb.filter(action='settings'), state='*')
    dp.register_callback_query_handler(settings_cmd, menu_cb.filter(action='switch'), state='*')
