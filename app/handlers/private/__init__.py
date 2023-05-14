from aiogram import Dispatcher

from app.handlers.private import (
    start,
    settings,
    back,
    help,
    my_subjects,
    add_subject,
    edit_subject,
    add_task,
    sort
)


def setup(dp: Dispatcher):
    start.setup(dp)
    settings.setup(dp)
    back.setup(dp)
    help.setup(dp)
    my_subjects.setup(dp)
    add_subject.setup(dp)
    edit_subject.setup(dp)
    add_task.setup(dp)
    sort.setup(dp)





