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

@adminRouter.my_chat_member(
                            ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR),
                            F.chat.type.in_({"group", "supergroup"}))
async def addedBotChannel(event: ChatMemberUpdated, bot: Bot):
    logger.info(event.chat.type)
    logger.info(event.from_user.id)
    
    async with BotDB() as db:
        await db.updateWaitChat(event.chat.id)
    
    

@adminRouter.message(F.text == '💭 Чат')
@adminRouter.callback_query(F.data == 'chat_support')
async def chat_supportFunc(upd: Union[Message, CallbackQuery], state: FSM, bot: Bot):

    await state.clear()

    async with BotDB() as db:
        settings = await db.getSettings()

    if settings['chat_id'] == None:
        text = f'''
❗️ У вас не добавлен чат для технической поддержки! Скорее добавьте его для корректной работы бота по кнопке ниже 👇🏻.
'''
    
    else:
        try:
            checkChat = await bot.get_chat(int(settings['chat_id']))

            text = f'''

🆔: <code>{settings['chat_id']}</code>
🔰 Имя чата: <b>{checkChat.title}</b>

<i>Что бы сменить чат воспользуйтесь кнопкой ниже 👇🏻</i>
'''
        except:
            text = f'''

❗️ Внимание ❗️ Чат, который Вы добавили ранее по какой то причине не работает, возможно, Вы удалили бота из чата, или сам чат был удален.
Срочно смените чат или если Вы по ошибке удалили бота из чата добавьте его обратно!

🆔: <code>{settings['chat_id']}</code>
🔰 Имя чата: <b>{settings['chat_name']}</b>
'''

    title = '<b>💭 Чат персонала</b>'

    finishText = title + text

    try:
        await upd.message.edit_text(text, reply_markup=setChatKey)
    except:
        await upd.answer(finishText, reply_markup=setChatKey)


@adminRouter.callback_query(F.data == 'set_chat_support')
async def set_chat_supportFunc(call: CallbackQuery, state: FSM, bot: Bot):

    thisBot = await bot.get_me()
    usernameBot = thisBot.username

    await state.clear()

    text = f'''
ℹ️ Для того что бы добавить бота в чат: 

1. <b>С помощью кнопки</b> "<i>↗️ Добавить бота в чат</i>" <b>добавьте бота в чат, не выключая никакие права.</b>
2. Нажмите на кнопку "<i>👁 Проверить</i>"

Если все было выполнено по инструкции Вы задали чат персонала для бота.
'''
    await call.message.edit_text(text, reply_markup=addBotInChat(f'https://t.me/{usernameBot}?startgroup=true&admin=change_info+edit_messages+post_messages+delete_messages+restrict_members+invite_users+pin_messages+manage_topics+promote_members+anonymous+manage_chat'))



@adminRouter.callback_query(F.data == 'check_bot_in_chat')
async def check_bot_in_chatFunc(call: CallbackQuery, state: FSM, bot: Bot):

    async with BotDB() as db:
        waitChat = await db.getWaitChat()

    if waitChat['wait_chat_id'] != 'None':
        chat_id = waitChat['wait_chat_id']
        
        try:
            checkChat = await bot.get_chat(int(chat_id))

            text = f'''
👁 Был обнаружен чат: <b>{checkChat.title}</b>

<i>Задать этот чат как чат персонала?</i>
'''

            await call.message.edit_text(text, reply_markup=addChatKey(checkChat.id))

        except Exception as e:
            logger.error(e)
            await call.answer('💭 Кажется, что то пошло не так...\nВозможно, такого чата не существует или он был удален')
    
    else:
        await call.answer('💭 Кажется, Вы не добавили никакой чат', True)

    
@adminRouter.callback_query(F.data.startswith('addchat_'))
async def addchat_Func(call: CallbackQuery, state: FSM, bot: Bot):

    chat_id = call.data.split('_')[1]

    try:
        checkChat = await bot.get_chat(int(chat_id))

        await call.message.edit_reply_markup(reply_markup=waitKey)

        try:
            flood = await bot.create_forum_topic(checkChat.id, name='Общение')
            await bot.send_message(checkChat.id, 'Проверка темы "Общение"', message_thread_id=flood.message_thread_id)

            notification = await bot.create_forum_topic(checkChat.id, name='Технические уведомления')
            await bot.send_message(checkChat.id, 'Проверка темы "Технические уведомления"\n\nСюда будут приходить все уведомления о изменениях в боте', message_thread_id=notification.message_thread_id)


            async with BotDB() as db:
                await db.setChat(checkChat.id, checkChat.title)
                await db.setMessagesThread(flood.message_thread_id, notification.message_thread_id)

            await call.message.edit_text('✅ Чат был успешно задан!\nВ чате были созданы темы: <b>Общение, Технические уведомления</b>', reply_markup=backChat)

        except TelegramBadRequest as e:
            logger.error(e.message)

            if e.message == 'Bad Request: the chat is not a forum':
                await call.message.edit_reply_markup(reply_markup=addChatKey(chat_id))
                await call.answer('Включите темы в чате', True)

            elif e.message == 'Bad Request: not enough rights to create a topic':
                await call.message.edit_reply_markup(reply_markup=addChatKey(chat_id))
                await call.answer('Выдайте боту право управлять темами', True)

            else:
                await call.message.edit_reply_markup(reply_markup=addChatKey(chat_id))
                await call.answer('Кажется, Вы либо не добавили бота в чат, либо выдали не все права боту.', True)

    except Exception as e:
        logger.error(e)
        await call.message.edit_reply_markup(reply_markup=addChatKey(chat_id))

        await call.answer('Кажется, Вы либо не добавили бота в чат, либо не включили темы в чатах либо выдали не все права боту.', True)