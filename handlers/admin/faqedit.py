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

@adminRouter.message(F.text=='✍🏻 FAQ')
@adminRouter.callback_query(F.data == 'faq_edit')
async def Faq_editFunc(upd: Union[Message, CallbackQuery], state: FSM, bot: Bot):

    await state.clear()
    try:
        await upd.message.delete()
    except:
        await upd.delete()

    async with BotDB() as db:
        settings = await db.getSettings()
    
    await messageFunction(upd, bot, settings['faq_post'], settings['faq_media'], settings['faq_keyboard'])

    await bot.send_message(upd.from_user.id, 'Что бы изменить пост на кнопке <b>"📄 Частые вопросы"</b> воспользуйтесь ккнопками ниже', reply_markup=contentMainKey('faq'))


@adminRouter.callback_query(F.data == 'post_media_faq')
async def post_media_Func(call: CallbackQuery, state: FSM, bot: Bot):

    await state.clear()

    await state.set_state(createPostFaq.media)

    text = f'''
Смена медиафайла на кнопке <b>"📄 Частые вопросы"</b>

<b>Что бы сменить медиафайл отправьте его, бот принимает: 
1. Фотографии
2. Видео
3. Видеосообщения
4. Гифки
5. Голосовые сообщения</b>

<i>Бот принимает по одному медиафайлу! Отправлять медиаконтент обязательно сжатым!</i>
'''

    await call.message.edit_text(text, reply_markup=backContent('faq', 'media'))


@adminRouter.callback_query(F.data.startswith('faq_delete_'))
async def faq_delete_Func(call: CallbackQuery, state: FSM):
    await state.clear()

    type_ = call.data.split('_')[2]

    match type_:
        case 'media':
            content_type = 'media'
            text = '<b>⌨️ Медиа файл был успешно удален</b>'

        case 'key':
            content_type = 'keyboard'
            text = '<b>⌨️ Клавиатура была успешно удалено</b>'
            
    async with BotDB() as db:
        await db.nullContent('faq', content_type)

    await call.message.edit_text(text, reply_markup=backContent('faq'))


@adminRouter.message(createPostFaq.media, F.content_type.in_({'photo', 'video', 'animation', 'video_note', 'voice'}))
async def setMediaPostFaq(msg: Message, state: FSM, bot: Bot):

    if str(msg.content_type) == 'ContentType.VIDEO':
        type_ = 'VIDEO'
        document_id = msg.video.file_id

    elif str(msg.content_type) == 'ContentType.PHOTO':
        type_ = 'PHOTO'
        document_id = msg.photo[-1].file_id
    
    elif str(msg.content_type) == 'ContentType.VIDEO_NOTE':
        type_ = 'VIDEO_NOTE'
        document_id = msg.video_note.file_id

    elif str(msg.content_type) == 'ContentType.ANIMATION':
        type_ = 'ANIMATION'
        document_id = msg.animation.file_id
    
    elif str(msg.content_type) == 'ContentType.VOICE':
        type_ = 'VOICE'
        document_id = msg.voice.file_id
    
    file_info = await bot.get_file(document_id)
    file_id = file_info.file_id

    media = f'{type_}|{file_id}'

    async with BotDB() as db:
        await db.updateMedia(media, 'faq')

    await msg.answer('✅ Медиафайл для кнопки <b>"📄 Частые вопросы"</b> успешно настроен, вернитесь назад', reply_markup=backContent('faq'))
    

@adminRouter.callback_query(F.data == 'post_keyboards_faq')
async def keyboards_Func(call: CallbackQuery, state: FSM, bot: Bot):

    await state.set_state(createPostFaq.keyboard)
    text = f'''
Отправьте боту название кнопки и адрес ссылки. Например, так: 

Telegram https://telegram.org

Чтобы отправить несколько кнопок за раз, используйте разделитель «|». Каждый новый ряд – с новой строки. Например, так: 

<i>Telegram https://telegram.org | Новости https://telegram.org/blog
FAQ https://telegram.org/faq | Скачать https://telegram.org/apps</i>
'''
    await call.message.answer(text, reply_markup=backContent('faq', 'key'), disable_web_page_preview=True)


@adminRouter.message(createPostFaq.keyboard)
async def setKeyboardPostFaq(msg: Message, state: FSM, bot: Bot):

    try:
        keysList = msg.text.split('\n')

        formatStatus=True

        for key in keysList:
            logger.info(key)
            keys = key.split('|')
            
            for btn in keys:
                logger.info(btn)
                if check_format_keys(btn) == False:
                    formatStatus = False
                break

            if formatStatus==False:
                break

        if formatStatus==False:
            await state.set_state(createPostFaq.keyboard)
            await msg.answer('⚠️ Кажется, введенные Вами кнопки не соответсвуют формату, попробуйте снова:', reply_markup=backContent('faq', 'key'))
        
        else:
            async with BotDB() as db:
                await db.updateKeyboard(msg.text, 'faq')

            await msg.answer('✅ Кнопки успешно заданы, вернитесь к посту', reply_markup=backContent('faq'))

    except Exception as e:
        logger.error(e)
        await state.set_state(createPostFaq.keyboard)
        await msg.answer('⚠️ Кажется, введенные Вами кнопки не соответсвуют формату, попробуйте снова:', reply_markup=backContent('faq', 'key'))


@adminRouter.callback_query(F.data == 'post_text_faq')
async def text_Func(call: CallbackQuery, state: FSM, bot: Bot):
    await state.set_state(createPostFaq.text)
    await call.message.edit_text('Отправьте боту текст для кнопки <b>"📄 Частые вопросы"</b>', reply_markup=backContent('faq'))


@adminRouter.message(createPostFaq.text)
async def setTextPostFaq(msg: Message, state: FSM, bot: Bot):

    async with BotDB() as db:
        await db.updateText(msg.html_text, 'faq')

    await msg.answer('✅ Текст успешно задан, вернитесь к посту', reply_markup=backContent('faq'))