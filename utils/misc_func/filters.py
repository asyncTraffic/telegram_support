# - *- coding: utf- 8 - *-
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from data.config import ADMIN
from aiogram import Bot, Dispatcher, F, Router
from utils.bot_database import BotDB
from loguru import logger
from utils.misc_func.bot_models import *
from utils.misc_func.otherfunc import success_content
from typing import *


class NotSuccessContentType(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return await success_content(message.content_type)

class SuccessContentType(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        status = await success_content(message.content_type)
        return False if status else True



# Проверка на админа
class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async with BotDB() as db:
            user = await db.getUser(message.from_user.id)

        if user is None:
            return True

        if message.from_user.id in ADMIN or user['admin'] == 1:
            return True
        else:
            return False
        

# Проверка на админа
class IsNotAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user.id in ADMIN:
            return False
        else:
            return True
        

class IsNotWork(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async with BotDB() as db:
            settings = await db.getSettings()

        if settings['workbot'] == 1:
            return False
        else:
            return True

class IsNotCaptcha(BaseFilter):
    async def __call__(self, message: Message, state: FSM) -> bool:

        data = await state.get_data()

        if data.get('uniq') is None:

            async with BotDB() as db:
                settings = await db.getSettings()
                user = await db.getUser(message.from_user.id)

            if (settings['captcha'] == 1) and user['captcha'] != 1:
                return True
            else:
                return False
        else:
            return False
        

class IsWork(BaseFilter):
    async def __call__(self, message: Message) -> bool:

        async with BotDB() as db:
            settings = await db.getSettings()
            user = await db.getUser(message.from_user.id)

        if message.from_user in ADMIN:
            return True

        if settings['workbot'] == 1 and settings['technical_work'] == 0 and (user['captcha'] == 1 or settings['captcha'] == 0):
            return True
        
        else:
            return False
        



class IsTechWork(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async with BotDB() as db:
            settings = await db.getSettings()
            user = await db.getUser(message.from_user.id)

        if settings['technical_work'] == 0 or message.from_user.id in ADMIN or user['admin'] == 1:
            return False
        else:
            return True


class IsChat(BaseFilter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:

        async with BotDB() as db:
            settings = await db.getSettings()

        try:
            type_ = message.chat.type
            chat_id = message.chat.id
        except:
            type_ = message.message.chat.type
            chat_id = message.message.chat.id

        if str(type_) != 'private' and chat_id == settings['chat_id']:
            return True
        else:
            return False


class IsModer(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async with BotDB() as db:
            user = await db.getUser(message.from_user.id)

        if user is None:
            return True

        if message.from_user.id in ADMIN or user['moderator'] == 1:
            return True
        else:
            return False


class IsPrivate(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        
        if message.chat.type == 'private':
            return True
        else:
            return False
      

class IsBan(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        async with BotDB() as db:
            user = await db.getUser(message.from_user.id)

        if user is None:
            return True

        if message.from_user.id in ADMIN or user['ban'] != 1:
            return True
        else:
            return False


    
