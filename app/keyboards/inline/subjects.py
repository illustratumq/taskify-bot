from app.database.models import Subject
from app.keyboards.inline.base import *

from app.keyboards import buttons
from app.keyboards.inline.back import back_bt


subject_cb = CallbackData('sb', 'subject_id', 'action', 'sorted')


def my_subjects_kb(subjects: list[Subject], subject_id: int, sorted: str):
    subjects_ids = [subject.subject_id for subject in subjects]
    current_subject_index = subjects_ids.index(subject_id)
    next_subject_cb = subject_cb.new(subject_id=subjects_ids[(current_subject_index + 1) % len(subjects)], action='pag',
                                     sorted=sorted)
    prev_subject_cb = subject_cb.new(subject_id=subjects_ids[(current_subject_index - 1) % len(subjects)], action='pag',
                                     sorted=sorted)

    def button_cb(action: str, sub_id: int = subject_id):
        return dict(callback_data=subject_cb.new(subject_id=sub_id, action=action, sorted=sorted))

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


def edit_subjects_kb(subject_id: int, subject_sorted: str):

    def button_cb(action: str, sub_id: int = subject_id):
        return dict(callback_data=subject_cb.new(subject_id=sub_id, action=action, sorted=subject_sorted))

    inline_keyboard = [
        [InlineKeyboardButton(buttons.edit_subject.extra_grade, **button_cb('extra_grade'))],
        [InlineKeyboardButton(buttons.edit_subject.edit_name, **button_cb('edit_name')),
         InlineKeyboardButton(buttons.edit_subject.edit_max_grade, **button_cb('max_grade'))],
        [InlineKeyboardButton(buttons.edit_subject.edit_description, **button_cb('edit_description')),
         InlineKeyboardButton(buttons.edit_subject.delete_subject, **button_cb('delete_subject'))],
        [back_bt(to='subject', subject_id=subject_id)]
    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)


def sort_kb(subject_id: int, subject_sorted: str):

    def button_cb(action: str, sub_id: int = subject_id):
        return dict(callback_data=subject_cb.new(subject_id=sub_id, action=action, sorted=subject_sorted))

    inline_keyboard = [
        [InlineKeyboardButton(buttons.sort.tags, **button_cb('tags')),
         InlineKeyboardButton(buttons.sort.deadline, **button_cb('deadline'))],
        [back_bt(to='subject', subject_id=subject_id)]
    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)


def add_task_subject(subject_id: int, attribute: str):

    def button_cb(action: str, sub_id: int = subject_id):
        return dict(callback_data=subject_cb.new(subject_id=sub_id, action=action, sorted='None'))

    inline_keyboard = [
        [back_bt(to='subject', subject_id=subject_id),
         InlineKeyboardButton(buttons.confirm.skip, **button_cb(f'skip_{attribute}'))],
    ]

    return InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_keyboard)