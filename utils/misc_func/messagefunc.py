from aiogram import Bot
from aiogram.types import*
from loguru import logger
from keyboards.inline.otherkey import *
from typing import Any, Dict, Union
from utils.bot_database import BotDB
from utils.misc_func.otherfunc import *


async def messageFunction(msg: Message, bot: Bot, text: str = None, media: str = None, keyboards: str= None):

    # try:
        print(media, text, keyboards)
        if media != None:
            type_, file_id = media.split('|')

            match type_:
                case 'PHOTO':
                    await bot.send_photo(msg.from_user.id, file_id, caption=str(text).format(name=msg.from_user.first_name), reply_markup=postKey(keyboards), parse_mode='HTML')
                
                case 'VIDEO':
                    await bot.send_video(msg.from_user.id, file_id, caption=str(text).format(name=msg.from_user.first_name), reply_markup=postKey(keyboards), parse_mode='HTML')
                
                case 'ANIMATION':
                    await bot.send_animation(msg.from_user.id, file_id, caption=str(text).format(name=msg.from_user.first_name), reply_markup=postKey(keyboards), parse_mode='HTML')
                
                case 'VIDEO_NOTE':
                    await bot.send_video_note(msg.from_user.id, file_id, reply_markup=postKey(keyboards), parse_mode='HTML')
                
                case 'VOICE':
                    await bot.send_voice(msg.from_user.id, file_id, caption=str(text).format(name=msg.from_user.first_name), reply_markup=postKey(keyboards), parse_mode='HTML')

        else:
            await bot.send_message(msg.from_user.id, str(text).format(name=msg.from_user.first_name), reply_markup=postKey(keyboards), parse_mode='HTML')

        return True



async def spamUsers(user_id: int, name_user: str, bot: Bot, text: str = None, media: str = None, keyboards: str= None):

    try:
        if media is not None:
            type_, file_id = media.split('|')

            match type_:
                case 'PHOTO':
                    await bot.send_photo(user_id, file_id, caption=str(text).format(name=name_user), reply_markup=postKey(keyboards), parse_mode='HTML')
                
                case 'VIDEO':
                    await bot.send_video(user_id, file_id, caption=str(text).format(name=name_user), reply_markup=postKey(keyboards), parse_mode='HTML')
                
                case 'ANIMATION':
                    await bot.send_animation(user_id, file_id, caption=str(text).format(name=name_user), reply_markup=postKey(keyboards), parse_mode='HTML')
                
                case 'VIDEO_NOTE':
                    await bot.send_video_note(user_id, file_id, reply_markup=postKey(keyboards), parse_mode='HTML')

                case 'VOICE':
                    await bot.send_voice(user_id, file_id, caption=str(text).format(name=name_user), reply_markup=postKey(keyboards), parse_mode='HTML')

        else:
            await bot.send_message(user_id, str(text).format(name=name_user), reply_markup=postKey(keyboards), parse_mode='HTML')

        return True

    except Exception as e:
        logger.error(e)
        return False


async def errorMessage(error: str, user: Union[Message, CallbackQuery], bot: Bot):
    
    text = f'''
❗️ Пользователь хотел обратится в техническую поддержку, но что то пошло не так, ошибка: 
<code>{error}</code>

👤 Пользователь:
🆔 юзера: <code>{user.from_user.id}</code>
👁 Имя: <code>{user.from_user.first_name}</code>
👁 Юзернейм: @{user.from_user.username}'''
        
    for id_ in await getAdmins():
        try:
            await bot.send_message(id_, text)
        except:
            pass