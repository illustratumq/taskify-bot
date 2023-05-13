from app.keyboards.inline.base import *

back_cb = CallbackData('bk', 'to')


def back_bt(text: str = buttons.menu.back, to: str = 'menu'):
    return InlineKeyboardButton(text, callback_data=back_cb.new(to=to))


def back_kb(text: str = buttons.menu.back, to: str = 'menu'):
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[[back_bt(text, to)]])
