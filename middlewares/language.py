# - *- coding: utf- 8 - *-
from aiogram import BaseMiddleware
from utils.bot_database import BotDB
from utils.misc_func.otherfunc import get_date
from aiogram.filters.command import CommandObject



# Проверка юзера в БД и его добавление
class ExistsUserMiddleware(BaseMiddleware):

    async def __call__(self, handler, event, data):
        
        this_user = data.get("event_from_user")
                
        if not this_user.is_bot:

            user_id = this_user.id
            user_login = this_user.username
            user_name = this_user.first_name

            dateRegister = get_date(True)

            async with BotDB() as db:
                add = await db.addUser(user_id, user_name, user_login, dateRegister)  
                

        return await handler(event, data)