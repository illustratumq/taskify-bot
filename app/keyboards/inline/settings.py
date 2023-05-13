from app.keyboards.inline.base import *

settings_cb = CallbackData('stt', 'action')


def settings_kb(notify: bool):

    value = 'Вкл.' if notify else 'Викл.'

    def button_kb(action: str):
        return dict(callback_data=settings_cb.new(action=action))

    inline_keyboard = [
        [InlineKeyboardButton(buttons.menu.notify.format(value), **button_kb('notify'))],
    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)

