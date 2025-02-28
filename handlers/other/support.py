from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import *
from utils.misc_func.bot_models import *
from loader import *
from datetime import datetime
from keyboards.inline.adminkeyinline import *
from keyboards.inline.otherkey import *
from utils.bot_database import BotDB

from aiogram.methods.create_forum_topic import CreateForumTopic

from states.other_state import *
from utils.misc_func.filters import *

from keyboards.reply.adminkey import *
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from loguru import logger
from utils.misc_func.messagefunc import messageFunction
from states.admin_state import *
from utils.misc_func.otherfunc import *

from utils.bot_database import BotDB


@moderRouter.message(IsChat(), F.media_group_id)
async def album_handler_moder(msg: Message, album: List[Message], state: FSM):

    await state.clear()

    if msg.from_user.is_bot == True:
        return None

    replyUserID = msg.message_thread_id

    async with BotDB() as db:
        settings = await db.getSettings()

    logger.warning('до проверки')

    if replyUserID not in [settings['flood_message_thread_id'], settings['notification_message_thread_id']]:
        async with BotDB() as db:
            user = await db.getUserThread(replyUserID)
        mediaGroup = await createMediaGroup(album)

        logger.warning('чекнул базу')
        

        try:
            await bot.send_media_group(user['user_id'], media = mediaGroup.build())
            logger.warning('отправил')

        except Exception as e:
            text = f'''⚠️ Не уадлось отправить сообщение пользователю, причина:\n{e}'''
            await msg.answer(text)


@moderRouter.message(IsChat())
async def sendUserMessageFunc(msg: Message, state: FSM):
    await state.clear()

    if msg.from_user.is_bot == True:
        return None
    logger.info(msg.from_user.is_bot)

    replyUserID = msg.message_thread_id

    async with BotDB() as db:
        settings = await db.getSettings()

    if replyUserID not in [settings['flood_message_thread_id'], settings['notification_message_thread_id']]:

        async with BotDB() as db:
            user = await db.getUserThread(replyUserID)

        try:
            await bot.copy_message(user['user_id'], msg.chat.id, msg.message_id)  

        except Exception as e:
            text = f'''⚠️ Не уадлось отправить сообщение пользователю, причина:\n{e}'''
            await msg.answer(text)


@moderRouter.callback_query(IsChat(), F.data.startswith('usban_'))
async def mute_Func(call: CallbackQuery, state: FSM):

    _, user_id, status = call.data.split('_')

    async with BotDB() as db:
        await db.updateUserStatus(user_id, int(status), 'ban')
        user = await db.getUser(user_id)

    await call.message.edit_reply_markup(reply_markup=userMute(user_id, user['ban']))