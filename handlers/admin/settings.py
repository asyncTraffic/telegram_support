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
from aiogram.exceptions import TelegramBadRequest

@adminRouter.callback_query(F.data=='backsettings')
@adminRouter.message(F.text=='🔧 Работа бота')
async def settingsBotFunc(upd: Union[CallbackQuery, Message], state: FSM):

    await state.clear()

    async with BotDB() as db:
        settings = await db.getSettings() 

    text = f'''
<b>🔧 Работа бота</b>

💭 Здесь Вы можете включить/выключить технические работы, включить/выключить капчу, включить/выключить работу бота и настроить время работы

<i>Воспользуйтесь кнопками ниже 👇🏻</i>
'''
    key = settingsKey(settings['technical_work'], settings['workbot'], settings['captcha'])

    try:
        await upd.message.edit_text(text, reply_markup=key)
    except:
        await upd.answer(text, reply_markup=key)

@adminRouter.callback_query(F.data.startswith('sleepbot_'))
async def sleepbot_Func(call: CallbackQuery, state: FSM):

    status = int(call.data.split('_')[1])

    async with BotDB() as db:
        await db.updateStatusBot('workbot', status)
        settings = await db.getSettings() 

    key = settingsKey(settings['technical_work'], settings['workbot'], settings['captcha'])

    await call.message.edit_reply_markup(reply_markup=key)


@adminRouter.callback_query(F.data.startswith('workbot_'))
async def workbot_Func(call: CallbackQuery, state: FSM):

    status = int(call.data.split('_')[1])

    async with BotDB() as db:
        await db.updateStatusBot('technical_work', status)
        settings = await db.getSettings() 

    key = settingsKey(settings['technical_work'], settings['workbot'], settings['captcha'])

    await call.message.edit_reply_markup(reply_markup=key)


@adminRouter.callback_query(F.data.startswith('capthca_'))
async def capthca_Func(call: CallbackQuery, state: FSM):

    status = int(call.data.split('_')[1])

    async with BotDB() as db:
        await db.updateStatusBot('captcha', status)
        settings = await db.getSettings() 

    key = settingsKey(settings['technical_work'], settings['workbot'], settings['captcha'])

    await call.message.edit_reply_markup(reply_markup=key)



@adminRouter.callback_query(F.data=='succontent')
async def succontentFunc(call: CallbackQuery, state: FSM):

    await state.clear()

    async with BotDB() as db:
        content = await db.getContent()

    key = contentKeyFunc(content['voice'], content['photo'], content['video'], content['document'], content['videonote'], content['link'])

    text = f'''
<b>📷 Разрешенный контент</b>

<b>✅ — разрешено</b>
<b>🔴 — запрещено</b>

Здесь Вы можете настроить контент, который могут присылать в тех.поддержку, по умолчания включены все виды контента, но Вы можете что нибудь запретить, например, голосовые сообщени, тогда пользователи не смогут отправлять голосовые сообщения
'''
    await call.message.edit_text(text, reply_markup=key)


@adminRouter.callback_query(F.data.startswith('cont_'))
async def cont_Func(call: CallbackQuery, state: FSM):

    _, type_, value_ = call.data.split('_')

    async with BotDB() as db:
        await db.updateContent(type_, int(value_))
        content = await db.getContent()

    key = contentKeyFunc(content['voice'], content['photo'], content['video'], content['document'], content['videonote'], content['link'])

    await call.message.edit_reply_markup(reply_markup=key)
