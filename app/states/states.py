from app.states.base import *


class AddSubjectSG(StatesGroup):
    Name = State()
    Description = State()
    Grade = State()
    Tag = State()

