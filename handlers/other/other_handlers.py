from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import *
from utils.misc_func.bot_models import *
# from aiogram.utils.token import TokenValidationError, validate_token
from aiogram.exceptions import TelegramUnauthorizedError
from loader import *
from datetime import datetime

from keyboards.inline.otherkey import *
from utils.bot_database import BotDB

from data.config import DOMAIN
from states.other_state import *
from utils.misc_func.otherfunc import validate_token
from utils.misc_func.filters import *


@other.message(Command('start'))
async def startOtherFunc(msg: Message, state: FSM, bot: Bot):
    
    await state.clear()
    await state.set_state(setTokenState.token)
    await msg.answer('Добро пожаловать!\nПожалуйста, введите токен от бота')
    



    