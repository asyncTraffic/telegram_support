from loader import *

from data.config import *
import logging, asyncio
from aiohttp import web

from middlewares.throttling import *
from middlewares.language import *
from middlewares.album import *

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    TokenBasedRequestHandler,
    setup_application,
)

from services.api_session import *

from handlers.admin import admin_base
from handlers.admin import appendchat
from handlers.admin import faqedit
from handlers.admin import spam
from handlers.admin import helloedit
from handlers.admin import settings
from handlers.admin import openuser

from handlers.user import baseuser
from handlers.user import errors

from handlers.other import support
from handlers.other import defaultfilter


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.set_webhook(f"{DOMAIN}/webhook/main/{TOKEN}/")       


def main_webhook():
    arSession = AsyncRequestSession()

    logging.basicConfig(level=logging.INFO)
    
    main_dispatcher = Dispatcher(storage=storage)
    main_dispatcher.include_router(adminRouter)
    main_dispatcher.include_router(userRouter)
    main_dispatcher.include_router(moderRouter)
    main_dispatcher.startup.register(on_startup)
    main_dispatcher.message.middleware(ThrottlingMiddleware())
    main_dispatcher.message.middleware(ExistsUserMiddleware())
    main_dispatcher.message.middleware(MediaGroupMiddleware())

    app = web.Application()
    SimpleRequestHandler(dispatcher=main_dispatcher, bot=bot).register(app, path=f'/webhook/main/{TOKEN}/')

    setup_application(app, main_dispatcher, bot=bot)

    web.run_app(app, host='localhost', port=8080)

async def main_longpool():
    arSession = AsyncRequestSession()

    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    dp.include_router(adminRouter)
    dp.include_router(userRouter)
    dp.include_router(moderRouter)
    dp.message.middleware(ThrottlingMiddleware())
    dp.message.middleware(ExistsUserMiddleware())
    dp.message.middleware(MediaGroupMiddleware())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if DOMAIN == '':
        asyncio.run(main_longpool())
    else:
        main_webhook()
    