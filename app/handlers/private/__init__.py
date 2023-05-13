from aiogram import Dispatcher

from app.handlers.private import start, settings, back


def setup(dp: Dispatcher):
    start.setup(dp)
    settings.setup(dp)
    back.setup(dp)


