from data.config import TOKEN 
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from typing import Any, Dict, Union
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, F, Router
from services.api_session import *
from utils.misc_func.filters import *


other = Router()

userRouter = Router()
userRouter.message.filter(IsPrivate())
userRouter.message.filter(IsBan())

adminRouter = Router()
adminRouter.message.filter(IsAdmin())
adminRouter.message.filter(IsPrivate())

moderRouter = Router()
moderRouter.message.filter(IsModer())
moderRouter.message.filter(IsBan())

session = AiohttpSession()
bot_settings = {"session": session, "parse_mode": "HTML"}

bot = Bot(token=TOKEN, **bot_settings)

storage = MemoryStorage()
