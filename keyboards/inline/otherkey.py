from aiogram.types import *
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import *
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types.web_app_info import WebAppInfo
from utils.misc_func.otherfunc import find_link




def postKey(keyboards: str = None) -> InlineKeyboardMarkup:
    if keyboards is None or keyboards == 'None':
        return None
    
    else:
        keyboardsList = keyboards.split('\n')

        buttons = []

        for keys in keyboardsList:
            timeListKey = []
            btnList = keys.split('|')

            for btn in btnList:
                linkInBtn = find_link(btn)
                timeListKey.append(InlineKeyboardButton(text=str(btn).replace(linkInBtn, ''), url=linkInBtn))

            buttons.append(timeListKey)
            
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard
