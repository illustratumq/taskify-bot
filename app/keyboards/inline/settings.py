from app.keyboards.inline.back import back_bt
from app.keyboards.inline.base import *
from app.keyboards.inline.menu import menu_cb


def settings_kb(notify: bool):

    value = 'Вкл.' if notify else 'Викл.'

    def button_kb(action: str):
        return dict(callback_data=menu_cb.new(action=action))

    inline_keyboard = [
        [InlineKeyboardButton(buttons.menu.notify.format(value), **button_kb('settings'))],
        [back_bt()]

    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)

