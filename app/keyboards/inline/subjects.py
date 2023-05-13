from app.database.models import Subject
from app.keyboards.inline.base import *


from app.keyboards import buttons
from app.keyboards.inline.back import back_bt


subject_cb = CallbackData('sb', 'subject_id', 'action')


def my_subjects_kb(subjects: list[Subject], subject_id: int):
    subjects_ids = [subject.subject_id for subject in subjects]
    current_subject_index = subjects_ids.index(subject_id)
    next_subject_cb = subject_cb.new(subject_id=subjects_ids[(current_subject_index + 1) % len(subjects)], action='pag')
    prev_subject_cb = subject_cb.new(subject_id=subjects_ids[(current_subject_index - 1) % len(subjects)], action='pag')

    def button_cb(action: str, sub_id: int = subject_id):
        return dict(callback_data=subject_cb.new(subject_id=sub_id, action=action))

    inline_keyboard = [
        [InlineKeyboardButton(buttons.subject.add_task, **button_cb('add_task')),
         InlineKeyboardButton(buttons.subject.rates, **button_cb('rates'))],
        [InlineKeyboardButton(buttons.subject.edit, **button_cb('edit')),
         InlineKeyboardButton(buttons.subject.sort, **button_cb('sort'))],
        [
            InlineKeyboardButton('◀', callback_data=prev_subject_cb),
            back_bt('Назад'),
            InlineKeyboardButton('▶', callback_data=next_subject_cb)
        ]
    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)
