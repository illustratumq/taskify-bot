from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards import buttons
from app.keyboards.inline.back import back_bt
from app.keyboards.inline.menu import menu_cb


def help_kb():

    def button_kb(action: str):
        return dict(callback_data=menu_cb.new(action=action))

    inline_keyboard = [
            [back_bt()]

    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)
