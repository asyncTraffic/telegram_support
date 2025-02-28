from aiogram.fsm.state import StatesGroup,State


class createPostFaq(StatesGroup):
    text = State()
    media = State()
    keyboard = State()

class createPostHi(StatesGroup):
    text = State()
    media = State()
    keyboard = State()

class createPostSpam(StatesGroup):
    text = State()
    media = State()
    keyboard = State()

class setTimePost(StatesGroup):
    uniq_id = State()
    timeSet = State()

class autoSpamState(StatesGroup):
    uniq_id = State()
    timeSet = State()

class sendMsgUser(StatesGroup):
    user_id = State()
    msg = State()

