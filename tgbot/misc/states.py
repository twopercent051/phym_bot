from aiogram.fsm.state import State, StatesGroup


class AdminFSM(StatesGroup):
    home = State()
    edit = State()
    users = State()


class UserFSM(StatesGroup):
    home = State()
    year = State()
    height = State()
    weight = State()
    trainer = State()
