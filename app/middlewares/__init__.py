import logging

from aiogram import Dispatcher
from sqlalchemy.orm import sessionmaker

from app.middlewares.databse import DatabaseMiddleware
from app.middlewares.environment import EnvironmentMiddleware
from app.middlewares.acl import ACLMiddleware


log = logging.getLogger(__name__)


def setup(dp: Dispatcher, session_pool: sessionmaker, environments: dict):
    dp.setup_middleware(EnvironmentMiddleware(environments))
    dp.setup_middleware(DatabaseMiddleware(session_pool))
    dp.setup_middleware(ACLMiddleware())
    log.info('Мідлварі успішно встановлені...')
