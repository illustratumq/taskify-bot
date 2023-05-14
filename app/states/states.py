from app.states.base import *


class AddSubjectSG(StatesGroup):
    Name = State()
    Description = State()
    Grade = State()
    Tag = State()
    Confirm = State()


class EditSubjectSG(StatesGroup):
    Name = State()
    Description = State()
    Grade = State()


class AddTaskSG(StatesGroup):
    Name = State()
    Description = State()
    Deadline = State()
    Confirm = State()
