from aiogram.types import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import *
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types.web_app_info import WebAppInfo
from typing import *


settingsInlineKey = InlineKeyboardBuilder()
settingsInlineKey.row(InlineKeyboardButton(text='💭 Чат персонала', callback_data='chat_support'))
settingsInlineKey.row(InlineKeyboardButton(text='✍🏻 Контакты', callback_data='contact_edit'),
                      InlineKeyboardButton(text='✍🏻 Правила', callback_data='reluse_edit'))
settingsInlineKey = settingsInlineKey.as_markup()

setChatKey = InlineKeyboardBuilder()
setChatKey.row(InlineKeyboardButton(text='🔑 Задать чат', callback_data='set_chat_support'))
setChatKey = setChatKey.as_markup()

spamKey = InlineKeyboardBuilder()
spamKey.row(InlineKeyboardButton(text='👨🏻‍💻 Создать пост', callback_data='createPostSpam'))
spamKey.row(InlineKeyboardButton(text='📑 Просмотреть посты', callback_data='spamlist'))
spamKey = spamKey.as_markup()

backSpam = InlineKeyboardBuilder()
backSpam.row(InlineKeyboardButton(text='↩️ Назад', callback_data='spamsetting'))
backSpam = backSpam.as_markup()



waitKey = InlineKeyboardBuilder()
waitKey.row(InlineKeyboardButton(text='⏳ Ожидайте', callback_data=f'wait'))
waitKey = waitKey.as_markup()




backSpam= InlineKeyboardBuilder()
backSpam.row(InlineKeyboardButton(text='↩️ К посту', callback_data=f'back_spam'))
backSpam=backSpam.as_markup()


spamMainKey = InlineKeyboardBuilder()
spamMainKey.row(InlineKeyboardButton(text='🎬 Медиа', callback_data=f'spam_media'),
        InlineKeyboardButton(text='🔗 URL Кнопки', callback_data=f'spam_keyboards'))
spamMainKey.row(InlineKeyboardButton(text='↩️ Назад', callback_data='spamsetting'),
        InlineKeyboardButton(text='📄 Текст', callback_data=f'spam_text'),)
spamMainKey = spamMainKey.as_markup()



def contentKeyFunc(voice: int, photo: int, video: int, document: int, video_note: int, link: int):
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text=f"{'✅' if voice == 1 else '🔴'} Голосовые", callback_data=f'cont_voice_{"1" if voice == 0 else "0"}'),
            InlineKeyboardButton(text=f"{'✅' if photo == 1 else '🔴'} Фото", callback_data=f'cont_photo_{"1" if photo == 0 else "0"}'))
    key.row(InlineKeyboardButton(text=f"{'✅' if video == 1 else '🔴'} Видео", callback_data=f'cont_video_{"1" if video == 0 else "0"}'),
            InlineKeyboardButton(text=f"{'✅' if document == 1 else '🔴'} Документы", callback_data=f'cont_document_{"1" if document == 0 else "0"}'))
    key.row(InlineKeyboardButton(text=f"↩️ Назад", callback_data=f'backsettings'),
            InlineKeyboardButton(text=f"{'✅' if video_note == 1 else '🔴'} Кружки", callback_data=f'cont_videonote_{"1" if video_note == 0 else "0"}'))
    return key.as_markup()



def settingsKey(work: int, sleep: int, captcha: int):
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text=f"{'✅' if work == 1 else '🔴'} Тех.работы", callback_data=f'workbot_{"1" if work == 0 else "0"}'),
            InlineKeyboardButton(text=f"{'✅' if captcha == 1 else '🔴'} Капча", callback_data=f'capthca_{"1" if captcha == 0 else "0"}'))
    key.row(InlineKeyboardButton(text=f"{'✅' if sleep == 1 else '🔴'} Работа", callback_data=f'sleepbot_{"1" if sleep == 0 else "0"}'),
            InlineKeyboardButton(text='📷 Контент', callback_data=f'succontent'))
    return key.as_markup()


def userMute(user_id, status: str):
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text=f"{'✅' if status == 1 else '🔴'} Бан", callback_data=f'usban_{user_id}_{"1" if status == 0 else "0"}'))
    return key.as_markup()


def backContent(type_, type_content: str = None):
    key= InlineKeyboardBuilder()
    if type_content == 'media':
        key.row(InlineKeyboardButton(text='🗑 Удалить медиа', callback_data=f'{type_}_delete_media'))
    elif type_content == 'key':
        key.row(InlineKeyboardButton(text='🗑 Удалить кнопки', callback_data=f'{type_}_delete_key'))
    else:
        pass

    key.row(InlineKeyboardButton(text='↩️ К посту', callback_data=f'{type_}_edit'))
    key=key.as_markup()
    return key

def contentMainKey(type_):
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text='🎬 Медиа', callback_data=f'post_media_{type_}'),
            InlineKeyboardButton(text='🔗 URL Кнопки', callback_data=f'post_keyboards_{type_}'))
    key.row(InlineKeyboardButton(text='📄 Текст', callback_data=f'post_text_{type_}'),)
    if type_ == 'spam':
        key.row(InlineKeyboardButton(text='▶️ Начать рассылку', callback_data=f'startspam'),)

    key = key.as_markup()
    return key


def addBotInChat(link: str):
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text='↗️ Добавить бота в чат', url=link))
    key.row(InlineKeyboardButton(text='👁 Проверить', callback_data=f'check_bot_in_chat'))
    key.row(InlineKeyboardButton(text='↩️ Назад', callback_data='chat_support'))    
    return key.as_markup()        


def addChatKey(chat_id: int):
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text='✅ Задать', callback_data=f'addchat_{chat_id}'))
    key.row(InlineKeyboardButton(text='↩️ Назад', callback_data='set_chat_support'))
    return key.as_markup()


backChat = InlineKeyboardBuilder()
backChat.row(InlineKeyboardButton(text='↩️ Назад', callback_data='chat_support'))
backChat = backChat.as_markup()


userAdminKey = InlineKeyboardBuilder()
userAdminKey.row(InlineKeyboardButton(text='🔎 Поиск', switch_inline_query_current_chat='user '))
userAdminKey = userAdminKey.as_markup()

def userOpenKey(user_id: int, admin: int, moder: int, ban: int):
    key = InlineKeyboardBuilder()

    key.row(InlineKeyboardButton(text=f'{"✅" if admin == 1 else "❌"} Админ', callback_data=f'usadmin_{user_id}_{"0" if admin == 1 else "1"}'),
            InlineKeyboardButton(text=f'{"✅" if moder == 1 else "❌"} Модератор', callback_data=f'usmoder_{user_id}_{"0" if moder == 1 else "1"}'),
            InlineKeyboardButton(text=f'{"✅" if ban == 1 else "❌"} Бан', callback_data=f'usban_{user_id}_{"0" if ban == 1 else "1"}'))

    return key.as_markup()


def backUserProfileAdmin(user_id: int):
    key = InlineKeyboardBuilder()
    key.row(InlineKeyboardButton(text='↩️ Назад', callback_data=f'useropen_{user_id}'))
    return key.as_markup()

