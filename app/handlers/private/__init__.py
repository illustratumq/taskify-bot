from aiogram import Dispatcher

from app.handlers.private import start, settings


def setup(dp: Dispatcher):
    start.setup(dp)
    settings.setup(dp)
