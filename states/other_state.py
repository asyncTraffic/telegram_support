from aiogram.fsm.state import StatesGroup,State

class setTokenState(StatesGroup):
    token = State()

class capthcaState(StatesGroup):
    uniq = State()
    reply = State()