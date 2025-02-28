from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = '' # обязательно берем токен у @BotFather и вставляем его сюда
DOMAIN = '' # если желаете подключить вебхуки укажите сюда ваш домен, например: https://example.com
ADMIN = [] #сюда через запятую можно перечислить администраторов, например: [23423525, 456456456, 2525235]
BOT_TIMEZONE = "Europe/Moscow" 
BOT_SCHEDULER = AsyncIOScheduler(timezone=BOT_TIMEZONE)