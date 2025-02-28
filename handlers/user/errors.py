from aiogram.handlers import ErrorHandler
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
from aiogram.filters import ExceptionMessageFilter, ExceptionTypeFilter
from aiogram.exceptions import *


@userRouter.error(ExceptionTypeFilter(TelegramBadRequest), F.update.message.as_("message"))
async def handle_my_custom_exception(event: ErrorEvent):
    # do something with error
    logger.info(event.update.message.from_user.id)
    logger.info(type(event.exception))
    logger.info(event.exception)

    async with BotDB() as db:
        settings = await db.getSettings()

    match str(event.exception):
        case 'Telegram server says - Bad Request: message thread not found':
            await bot.send_message(event.update.message.from_user.id, 
                                   'Пожалуйста, подождите, создаем обращение в техничскую поддержку ⏳')
            add = await createTopicUser(bot, event.update.message, settings)
            if add:
                await bot.send_message(event.update.message.from_user.id, 
                                   '✅ Готово, можете обратиться в техничскую поддержку')
            else:
                await bot.send_message(event.update.message.from_user.id, 
                                   'Что то пошло не так...\nПопробуйте снова через некоторое время...')

@userRouter.error(ExceptionTypeFilter(TelegramRetryAfter))
async def TelegramRetryAfterFunc(event: ErrorEvent):
    
    logger.warning(event)

    await bot.send_message(event.update.message.from_user.id,
                           f'⚠️ Сработал флуд контроль со стороны телеграма, пожалуйста, подождите <i>{event.exception.retry_after} секнуд</i> и повторите прошлое действие, спасибо за понимание 🙏')