from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import *
from utils.misc_func.bot_models import *
from loader import *
from datetime import datetime
from keyboards.inline.adminkeyinline import *
from utils.bot_database import BotDB

from aiogram.methods.create_forum_topic import CreateForumTopic

from states.other_state import *
from utils.misc_func.filters import *

from keyboards.reply.adminkey import *
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from loguru import logger

from states.admin_state import *
from typing import List
import random
from aiogram.exceptions import TelegramBadRequest



@adminRouter.message(F.text=='👤 Клиенты')
async def clientMSG(msg: Message, state: FSM):

    text = f'''
<b>👁 Поиск клиентов</b>

Здесь Вы можете найти пользователей, воспользуйтесь кнопкой ниже и начните вводить данные о пользователе (например, ID пользователя, или его имя, произойдет поиск по базе и Вам вернуться доступные варианты)
'''

    await msg.answer(text, reply_markup=userAdminKey)




@adminRouter.inline_query(F.query.startswith('user '))
async def queryFunc(query: InlineQuery, state: FSMContext):

    q = query.query.replace('user ', '')

    print(q)

    async with BotDB() as db:
        list_ = await db.gerAllUsers()

    clearList = []

    for i in list_:
        if q.lower() in str(i['user_id']).lower() or q.lower() in str(i['name']).lower() or q.lower() in str(i['username']).lower():
            clearList.append(i)

    results = []    

    for dd in clearList:
        id_ = random.randint(0, 9999999999999999999)
        results.append(InlineQueryResultArticle(
            id=str(id_),  # индекс элемента в list   
            title=f"🔰 Имя: {dd['name']}",
            description=f"🆔: {dd['user_id']}\n💠 Юзернейм: {dd['username']}",
            input_message_content=InputTextMessageContent(message_text=f"/user {dd['user_id']}"),

        ))
    # Важно указать is_personal=True!
    await query.answer(results, is_personal=True)


@adminRouter.message(Command('user'))
async def openUserFunc(msg: Message, state: FSMContext):

    user_id = msg.text.split(' ')[1]

    async with BotDB() as db:
        user = await db.getUser(user_id)
    if user is not None:
        text = f'''
👤 Пользователь:
🆔 юзера: <code>{user['user_id']}</code>
👁 Имя: <code>{user['name']}</code>
👁 Юзернейм: @{user['username']}'''
        
        key = userOpenKey(user_id, user['admin'], user['moderator'], user['ban'])
    else:
        text = f'👁‍🗨 Пользователь не найден'
        key = None

    await msg.answer(text, reply_markup=key)



@adminRouter.callback_query(F.data.startswith('usadmin_'))
async def usadmin_Func(call: CallbackQuery, state: FSM, bot: Bot):

    user_id, status = call.data.split('_')[1], call.data.split('_')[2]

    async with BotDB() as db:
        await db.updateUserStatus(user_id, status, 'admin')
        user = await db.getUser(user_id)

    key = userOpenKey(user_id, user['admin'], user['moderator'], user['ban'])
    await call.message.edit_reply_markup(reply_markup=key)

    

@adminRouter.callback_query(F.data.startswith('usmoder_'))
async def usmoder_Func(call: CallbackQuery, state: FSM, bot: Bot):

    user_id, status = call.data.split('_')[1], call.data.split('_')[2]

    async with BotDB() as db:
        await db.updateUserStatus(user_id, status, 'moder')
        user = await db.getUser(user_id)

    key = userOpenKey(user_id, user['admin'], user['moderator'], user['ban'])
    await call.message.edit_reply_markup(reply_markup=key)


@adminRouter.callback_query(F.data.startswith('usban_'))
async def usban__Func(call: CallbackQuery, state: FSM, bot: Bot):

    user_id, status = call.data.split('_')[1], call.data.split('_')[2]

    async with BotDB() as db:
        await db.updateUserStatus(user_id, status, 'ban')
        user = await db.getUser(user_id)

    key = userOpenKey(user_id, user['admin'], user['moderator'], user['ban'])
    await call.message.edit_reply_markup(reply_markup=key)

