# - *- coding: utf- 8 - *-

from data.config import TOKEN, BOT_TIMEZONE
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.token import TokenValidationError, validate_token
from typing import Any, Dict, Union
from aiogram import Bot, Dispatcher, F, Router

import random
import time
import uuid
from datetime import datetime
from typing import Union

from loguru import logger

import pickle
import pytz
import re
from aiogram import Bot
from aiogram.types import InlineKeyboardButton, KeyboardButton, WebAppInfo, Message, InlineKeyboardMarkup, \
    ReplyKeyboardMarkup

from data.config import BOT_TIMEZONE
from utils.bot_database import BotDB
from data.config import ADMIN
from captcha.image import ImageCaptcha
from io import BytesIO
from aiogram.types import *
from aiogram.utils.media_group import MediaGroupBuilder
from typing import *
from keyboards.inline.adminkeyinline import userMute

from aiogram.exceptions import TelegramRetryAfter
import asyncio

async def createTopicUser(bot: Bot, msg: Message, settings: dict):

    try:
        await createTopic(bot, msg, settings)

        return True    
            
    except Exception as e:
        logger.error(e)
        return False



async def createTopic(bot: Bot, msg: Message, settings: dict):
    
    titleThread = f'👤 {msg.from_user.first_name}'

    thread_user = await bot.create_forum_topic(settings['chat_id'], name=titleThread)
    key = userMute(msg.from_user.id, 0)

    text = f'''
👤 Пользователь:
🆔 юзера: <code>{msg.from_user.id}</code>
👁 Имя: <code>{msg.from_user.first_name}</code>
👁 Юзернейм: @{msg.from_user.username}
'''
    await bot.send_message(settings['chat_id'], text, message_thread_id=thread_user.message_thread_id, reply_markup=key)
    
    async with BotDB() as db:
        await db.updateThreadIDUser(msg.from_user.id, thread_user.message_thread_id)

    return True




async def createMediaGroup(album: List[Message]) -> MediaGroupBuilder:
    mediaGroup = MediaGroupBuilder()

    for m in album:

        if await success_content(m.content_type) == False:

            match m.content_type:
                case ContentType.PHOTO:
                    mediaGroup.add_photo(
                        media=m.photo[-1].file_id,
                        caption=m.caption,
                        caption_entities=m.caption_entities,
                    )
                    
                case ContentType.VIDEO:
                    mediaGroup.add_video(
                        media=m.video.file_id,
                        caption=m.caption,
                        caption_entities=m.caption_entities,
                    )
                
                case ContentType.DOCUMENT:
                    mediaGroup.add_document(
                        media=m.document.file_id,
                        caption=m.caption,
                        caption_entities=m.caption_entities,
                    )
        else:
            return False
    return mediaGroup




async def success_content(content_type: ContentType) -> bool:

    async with BotDB() as db:
        content = await db.getContent()

    match content_type:
        case ContentType.PHOTO:
            if content['photo'] == 1:
                return False
            else:
                return True
            
        case ContentType.VIDEO:
            if content['video'] == 1:
                return False
            else:
                return True
            
        case ContentType.VOICE:
            if content['voice'] == 1:
                return False
            else:
                return True
            
        case ContentType.DOCUMENT:
            if content['document'] == 1:
                return False
            else:
                return True
            
        case ContentType.VIDEO_NOTE:
            if content['videonote'] == 1:
                return False
            else:
                return True
                
        case _:
            return False
                
  
            


def generate_capthcat():
    image = ImageCaptcha(fonts=['data/captchacode.otf'])

    randInt = random.randint(1000, 9999)
    data = image.generate(str(randInt))

    return {'bytes': data.getvalue(), 'success': str(randInt)}


async def getAdmins():
    async with BotDB() as db:
        admins = await db.getAdminsDB()

    adminlist = []

    for i in admins:
        adminlist.append(int(i['user_id']))

    for i in ADMIN:
        adminlist.append(i)

    return adminlist






def validate_date(date_str: str) -> bool:
    """
    Проверяет валидность введенной даты в формате "день.месяц.год часы:минуты"
    """
    pattern = r'^(\d{1,2})\.(\d{1,2})\.(\d{4}) (\d{1,2})\:(\d{2})$'
    match = re.match(pattern, date_str)

    if match:
        day, month, year, hour, minute = match.groups()

        # Проверка дня и месяца
        if int(day) < 1 or int(day) > 31:
            return False
        if int(month) < 1 or int(month) > 12:
            return False

        # Проверка года
        if int(year) < 1:
            return False

        # Проверка часов и минут
        if int(hour) < 0 or int(hour) > 23:
            return False
        if int(minute) < 0 or int(minute) > 59:
            return False

        return True
    else:
        return False


def check_format_keys(text):
    '''Проверка формата кнопок'''
    pattern = r'.*https?://[^ ]+' # Шаблон для проверки

    if re.match(pattern, text):
        return True
    else:
        return False


def find_link(text):
    '''Поиск ссылки в тексте'''
    link = re.search(r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    if link:
        return link.group()
    return None


def is_bot_token(value: str) -> Union[bool, Dict[str, Any]]:
    '''Проерка на валид ботов'''
    try:
        validate_token(value)
    except TokenValidationError:
        return False
    return True


def get_unix(full: bool = False) -> int:
    '''Получение текущего unix времени (True - время в наносекундах, False - время в секундах)'''
    if full:
        return time.time_ns()
    else:
        return int(time.time())
    
    
def get_date(full: bool = True) -> str:
    '''Получение текущей даты (True - дата с временем, False - дата без времени)'''
    if full:
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
    else:
        return datetime.now(pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")


def convert_date(from_time, full=True, second=True) -> Union[str, int]:
    '''Конвертация unix в дату и даты в unix'''
    if "-" in str(from_time):
        from_time = from_time.replace("-", ".")

    if str(from_time).isdigit():
        if full:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M:%S")
        elif second:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y %H:%M")
        else:
            to_time = datetime.fromtimestamp(from_time, pytz.timezone(BOT_TIMEZONE)).strftime("%d.%m.%Y")
    else:
        if " " in str(from_time):
            cache_time = from_time.split(" ")

            if ":" in cache_time[0]:
                cache_date = cache_time[1].split(".")
                cache_time = cache_time[0].split(":")
            else:
                cache_date = cache_time[0].split(".")
                cache_time = cache_time[1].split(":")

            if len(cache_date[0]) == 4:
                x_year, x_month, x_day = cache_date[0], cache_date[1], cache_date[2]
            else:
                x_year, x_month, x_day = cache_date[2], cache_date[1], cache_date[0]

            x_hour, x_minute, x_second = cache_time[0], cache_time[2], cache_time[2]

            from_time = f"{x_day}.{x_month}.{x_year} {x_hour}:{x_minute}:{x_second}"
        else:
            cache_date = from_time.split(".")

            if len(cache_date[0]) == 4:
                x_year, x_month, x_day = cache_date[0], cache_date[1], cache_date[2]
            else:
                x_year, x_month, x_day = cache_date[2], cache_date[1], cache_date[0]

            from_time = f"{x_day}.{x_month}.{x_year}"

        if " " in str(from_time):
            to_time = int(datetime.strptime(from_time, "%d.%m.%Y %H:%M:%S").timestamp())
        else:
            to_time = int(datetime.strptime(from_time, "%d.%m.%Y").timestamp())

    return to_time


def gen_id(len_id: int = 16) -> int:
    '''Генерация уникального айди'''
    mac_address = uuid.getnode()
    time_unix = int(str(time.time_ns())[:len_id])

    return mac_address + time_unix


def gen_password(len_password: int = 16, type_password: str = "default") -> str:
    '''Генерация пароля | default, number, letter, onechar'''
    if type_password == "default":
        char_password = list("1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ")
    elif type_password == "letter":
        char_password = list("abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ")
    elif type_password == "number":
        char_password = list("1234567890")
    elif type_password == "onechar":
        char_password = list("1234567890")

    random.shuffle(char_password)
    random_chars = "".join([random.choice(char_password) for x in range(len_password)])

    if type_password == "onechar":
        random_chars = f"{random.choice('abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ')}{random_chars[1:]}"

    return random_chars


def convert_times(get_time: int, get_type: str = "day") -> str:
    '''Дополнение к числу корректного времени (1 -> 1 день, 3 -> 3 дня)'''
    get_time = int(get_time)
    if get_time < 0: get_time = 0

    if get_type == "second":
        get_list = ['секунда', 'секунды', 'секунд']
    elif get_type == "minute":
        get_list = ['минута', 'минуты', 'минут']
    elif get_type == "hour":
        get_list = ['час', 'часа', 'часов']
    elif get_type == "day":
        get_list = ['день', 'дня', 'дней']
    elif get_type == "month":
        get_list = ['месяц', 'месяца', 'месяцев']
    else:
        get_list = ['год', 'года', 'лет']

    if get_time % 10 == 1 and get_time % 100 != 11:
        count = 0
    elif 2 <= get_time % 10 <= 4 and (get_time % 100 < 10 or get_time % 100 >= 20):
        count = 1
    else:
        count = 2

    return f"{get_time} {get_list[count]}"



def snum(amount: Union[int, float], remains: int = 2) -> str:
    '''Преобразование экспоненциальных чисел в читаемый вид (1e-06 -> 0.000001)'''
    format_str = "{:." + str(remains) + "f}"
    str_amount = format_str.format(float(amount))

    if remains != 0:
        if "." in str_amount:
            remains_find = str_amount.find(".")
            remains_save = remains_find + 8 - (8 - remains) + 1

            str_amount = str_amount[:remains_save]

    if "." in str(str_amount):
        while str(str_amount).endswith('0'): str_amount = str(str_amount)[:-1]

    if str(str_amount).endswith('.'): str_amount = str(str_amount)[:-1]

    return str(str_amount)



def to_float(get_number, remains: int = 2) -> Union[int, float]:
    '''Конвертация любого числа в вещественное, с удалением нулей в конце (remains - округление)'''
    if "," in str(get_number):
        get_number = str(get_number).replace(",", ".")

    if "." in str(get_number):
        get_last = str(get_number).split(".")

        if str(get_last[1]).endswith("0"):
            while True:
                if str(get_number).endswith("0"):
                    get_number = str(get_number)[:-1]
                else:
                    break

        get_number = round(float(get_number), remains)

    str_number = snum(get_number)
    if "." in str_number:
        if str_number.split(".")[1] == "0":
            get_number = int(get_number)
        else:
            get_number = float(get_number)
    else:
        get_number = int(get_number)

    return get_number



def to_int(get_number: float) -> int:
    '''Конвертация вещественного числа в целочисленное'''
    if "," in get_number:
        get_number = str(get_number).replace(",", ".")

    get_number = int(round(float(get_number)))

    return get_number



def is_number(get_number: Union[str, int, float]) -> bool:
    '''Проверка ввода на число'''
    if str(get_number).isdigit():
        return True
    else:
        if "," in str(get_number): get_number = str(get_number).replace(",", ".")

        try:
            float(get_number)
            return True
        except ValueError:
            return False


def format_rate(amount: Union[float, int], around: int = 2) -> str:
    '''Преобразование числа в читаемый вид (123456789 -> 123 456 789)'''
    if "," in str(amount): amount = float(str(amount).replace(",", "."))
    if " " in str(amount): amount = float(str(amount).replace(" ", ""))
    amount = str(round(amount, around))

    out_amount, save_remains = [], ""

    if "." in amount: save_remains = amount.split(".")[1]
    save_amount = [char for char in str(int(float(amount)))]

    if len(save_amount) % 3 != 0:
        if (len(save_amount) - 1) % 3 == 0:
            out_amount.extend([save_amount[0]])
            save_amount.pop(0)
        elif (len(save_amount) - 2) % 3 == 0:
            out_amount.extend([save_amount[0], save_amount[1]])
            save_amount.pop(1)
            save_amount.pop(0)
        else:
            print("Error 4388326")

    for x, char in enumerate(save_amount):
        if x % 3 == 0: out_amount.append(" ")
        out_amount.append(char)

    response = "".join(out_amount).strip() + "." + save_remains

    if response.endswith("."):
        response = response[:-1]

    return response
