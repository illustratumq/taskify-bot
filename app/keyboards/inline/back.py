from app.keyboards.inline.base import *

back_cb = CallbackData('bk', 'to', 'subject_id')


def back_bt(text: str = buttons.menu.back, to: str = 'menu', subject_id: int = 0):
    return InlineKeyboardButton(text, callback_data=back_cb.new(to=to, subject_id=subject_id))


def back_kb(text: str = buttons.menu.back, to: str = 'menu', subject_id: int = 0):
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[[back_bt(text, to, subject_id)]])
