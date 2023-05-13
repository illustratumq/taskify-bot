from app.keyboards.inline.base import *


menu_cb = CallbackData('mn', 'action')


def menu_kb():

    def button_cb(action: str):
        return dict(callback_data=menu_cb.new(action=action))

    inline_keyboard = [
        [InlineKeyboardButton(buttons.menu.new_subject, **button_cb('new_subject'))],
        [InlineKeyboardButton(buttons.menu.my_subjects, **button_cb('my_subjects')),
         InlineKeyboardButton(buttons.menu.my_task, **button_cb('my_task'))],
        [InlineKeyboardButton(buttons.menu.settings, **button_cb('settings')),
         InlineKeyboardButton(buttons.menu.question, **button_cb('question'))]

    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)
