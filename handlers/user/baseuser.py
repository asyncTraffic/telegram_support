from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import *
from typing import Any, Dict, Union
from loader import *
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from datetime import datetime
from keyboards.reply.usermainkey import *
from keyboards.inline.userinlinekey import *
from loguru import logger
from utils.misc_func.bot_models import *
from aiogram_media_group import media_group_handler

from utils.misc_func.messagefunc import *
from typing import *
from keyboards.inline.adminkeyinline import *
from random import randint
from utils.misc_func.otherfunc import generate_capthcat
import io
from aiogram.utils.media_group import MediaGroupBuilder

from aiogram.exceptions import TelegramBadRequest

@userRouter.message(Command('start'))
async def startFunc(msg: Message, state: FSM, bot: Bot):

    await state.clear()

    msg_id = await msg.answer(f'Добро пожаловать, {msg.from_user.first_name}!', reply_markup=menuReply)

    async with BotDB() as db:
        settings = await db.getSettings()
    
    await messageFunction(msg, bot, settings['hello_post'], settings['hello_media'], settings['hello_keyboard'])


@userRouter.message(F.text=='📄 Частые вопросы')
async def faqFunc(msg: Message, state: FSM):

    await state.clear()

    async with BotDB() as db:
        settings = await db.getSettings()

    randname= randint(0, 999)

    await messageFunction(msg, bot, settings['faq_post'], settings['faq_media'], settings['faq_keyboard'])


@userRouter.message(IsWork(), SuccessContentType(), F.media_group_id)
async def album_handler(msg: Message, album: List[Message]):


    async with BotDB() as db:
        settings = await db.getSettings()
        user = await db.getUser(msg.from_user.id)

    if settings['chat_id'] == None:

        await errorMessage('не привязан чат', msg, bot)

        return msg.answer('🔴 Сейчас техническа поддержка недоступна, попробуйте позже')

    if user['thread_id'] == None:

        await createTopicUser(bot, msg, settings)

    async with BotDB() as db:
        user = await db.getUser(msg.from_user.id)

    mediaGroup = await createMediaGroup(album)

    if mediaGroup == False:
        return msg.answer('🔴 В сообщении присутствует запрещенный тип контента, сообщние небыло отправлено администрации')
    
    await bot.send_media_group(settings['chat_id'], media = mediaGroup.build(), message_thread_id=user['thread_id'])


@userRouter.message(IsWork(), SuccessContentType())
async def sendMessageUser(msg: Message, bot: Bot):

    async with BotDB() as db:
        user = await db.getUser(msg.from_user.id)
        settings = await db.getSettings()

    if settings['chat_id'] == None:

        await errorMessage('не привязан чат', msg, bot)

        return msg.answer('🔴 Сейчас техническа поддержка недоступна, попробуйте позже')

    if user['thread_id'] == None:
        await createTopicUser(bot, msg, settings)

    async with BotDB() as db:
        user = await db.getUser(msg.from_user.id)

    await bot.copy_message(settings['chat_id'], msg.from_user.id, msg.message_id, user['thread_id'])       
