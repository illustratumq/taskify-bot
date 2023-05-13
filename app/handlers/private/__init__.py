from aiogram import Dispatcher

from app.handlers.private import start, settings, back, help, my_subjects


def setup(dp: Dispatcher):
    start.setup(dp)
    settings.setup(dp)
    back.setup(dp)
    help.setup(dp)
    my_subjects.setup(dp)



