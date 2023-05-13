from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.keyboards import buttons
from app.keyboards.inline.back import back_bt
from app.keyboards.inline.menu import menu_cb


def my_subjects_kb():

    def button_cb(actions: str):
        return dict(callback_data=menu_cb.new(action=actions))

    inline_keyboard = [
        [InlineKeyboardButton(buttons.sub_menu.add_subject, **button_cb('add_subject')),
         InlineKeyboardButton(buttons.sub_menu.rates, **button_cb('rates'))],
        [InlineKeyboardButton(buttons.sub_menu.edit, **button_cb('edit')),
         InlineKeyboardButton(buttons.sub_menu.sort, **button_cb('sort'))],
        [back_bt()]
    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)
