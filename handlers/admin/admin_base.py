from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import *

from utils.bot_database import BotDB
from utils.misc_func.bot_models import *

from keyboards.reply.adminkey import *

from loader import *


@adminRouter.callback_query(F.data == 'adminmenu')
async def adminMenu(call: CallbackQuery, state: FSM, bot: Bot):

    await state.clear()

    await call.message.delete()

    text = f'''
<b>{call.from_user.first_name}, добро пожаловать в панель администратора!</b>

Панель администратора предназначена для управления ботом. 

<i>Для взаимодействия с ботом используйте кнопки ниже 👇🏻</i>'''

    await bot.send_message(call.from_user.id, text, reply_markup=kbMainAdmin)
    
    
@adminRouter.message(F.text=='↩️ Назад')
@adminRouter.message(Command('admin'))
async def startAdmin(msg: Message, state: FSM):
    
    await state.clear()
    
    text = f'''
<b>{msg.from_user.first_name}, добро пожаловать в панель администратора!</b>

Панель администратора предназначена для управления ботом.

<i>Для взаимодействия с ботом используйте кнопки ниже 👇🏻</i>'''

    await msg.answer(text, reply_markup=keyReplayAdmin)
    
   
@adminRouter.message(F.text=='⚙️ Настройки')
async def settingsOpenFunc(msg: Message, state: FSM):

    await state.clear()

    text = f'''
<b>⚙️ Настройки</b>

Здесь Вы можете изменить приветственный текст, FAQ, подключить/отключить чат, поставить бота в технические работы или поставить бота в спячку

<i>Для взаимодействия с ботом используйте кнопки ниже 👇🏻</i>'''

    await msg.answer(text, reply_markup=keySettingsAdmin)