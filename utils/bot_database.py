import aiosqlite, time
from data.config import *
from loguru import logger
from datetime import datetime


def dict_factory(cursor, row):
    save_dict = {}

    for idx, col in enumerate(cursor.description):
        save_dict[col[0]] = row[idx]

    return save_dict


class BotDB(object):
    def __init__(self, db_fp='data/bot.db'):
        self.db_fp = db_fp
        self.conn = None
        self.cur = None

    async def __aenter__(self):
        self.conn = await aiosqlite.connect(self.db_fp)
        self.cur = await self.conn.cursor()
        self.cur.row_factory = dict_factory
        await self.create_tables()
        await self.createSettings()
        await self.createContent()
        return self

    async def __aexit__(self, type, value, traceback):
        await self.conn.commit()
        await self.cur.close()
        await self.conn.close()


    async def create_tables(self):
        
        await self.cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    username TEXT,
                    date_registered TEXT,
                    ban BOOLEAN DEFAULT False,
                    admin BOOLEAN DEFAULT False,
                    moderator BOOLEAN DEFAULT False,
                    thread_id INTEGER DEFAULT NULL,
                    captcha BOOLEAN DEFAULT False)""")
        
        await self.cur.execute("""CREATE TABLE IF NOT EXISTS settings(
                    default_id INTEGER PRIMARY KEY,
                    chat_id INTEGER DEFAULT NULL,
                    chat_name TEXT DEFAULT NULL,
                    wait_chat_id TEXT DEFAULT 'None',
                    flood_message_thread_id INTEGER DEFAULT NULL,
                    notification_message_thread_id INTEGER DEFAULT NULL,
                    hello_post TEXT DEFAULT 'None',
                    hello_media TEXT DEFAULT NULL,
                    hello_keyboard TEXT DEFAULT NULL,
                    spam_post TEXT DEFAULT 'None',
                    spam_media TEXT DEFAULT NULL,
                    spam_keyboard TEXT DEFAULT NULL,
                    faq_post TEXT DEFAULT 'None',
                    faq_media TEXT DEFAULT NULL,
                    faq_keyboard TEXT DEFAULT NULL,
                    technical_work BOOLEAN DEFAULT False,
                    workbot BOOLEAN DEFAULT True,
                    captcha BOOLEAN DEFAULT True,
                    time_work TEXT DEFAULT NULL)""")
        

        await self.cur.execute("""CREATE TABLE IF NOT EXISTS content(
                    default_id INTEGER PRIMARY KEY,
                    voice BOOLEAN DEFAULT True,
                    photo BOOLEAN DEFAULT True,
                    video BOOLEAN DEFAULT True,
                    document BOOLEAN DEFAULT True,
                    videonote BOOLEAN DEFAULT True,
                    link BOOLEAN DEFAULT True)""")

    async def updateCaptcha(self, user_id: int, status: bool):
        await self.cur.execute('UPDATE users SET captcha = ? WHERE user_id = ?', [status, user_id])


    async def updateStatusBot(self, type_: str, status: int):
        await self.cur.execute(f'UPDATE settings SET {type_} = ? WHERE default_id = ?', [status, 1])

        
    async def nullContent(self, type_: str, content_type: str):
        await self.cur.execute(f'UPDATE settings SET {type_}_{content_type} = ? WHERE default_id = ?', [None, 1])


    async def updateUserStatus(self, user_id, status, type_):
        match type_:
            case 'moder':
                await self.cur.execute('UPDATE users SET moderator = ? WHERE user_id = ?', [status, user_id]) 
            case 'admin':
                await self.cur.execute('UPDATE users SET admin = ? WHERE user_id = ?', [status, user_id]) 
            case 'ban':
                await self.cur.execute('UPDATE users SET ban = ? WHERE user_id = ?', [status, user_id]) 


    async def getUsers(self):
        return await (await self.cur.execute('SELECT * FROM users')).fetchall()


    async def updateMedia(self, media: str, type_: str):
        try:
            match type_:
                case 'hello':
                    await self.cur.execute('UPDATE settings SET hello_media = ? WHERE default_id = ?', [media, 1])
                    
                case 'faq':
                    await self.cur.execute('UPDATE settings SET faq_media = ? WHERE default_id = ?', [media, 1])

                case 'spam':
                    await self.cur.execute('UPDATE settings SET spam_media = ? WHERE default_id = ?', [media, 1])

            return True
        
        except Exception as e:
            logger.error(e)
            return False
        
    
    async def updateKeyboard(self, keyboards: str, type_: str):
        try:
            match type_:
                case 'hello':
                    await self.cur.execute('UPDATE settings SET hello_keyboard = ? WHERE default_id = ?', [keyboards, 1])
                    
                case 'faq':
                    await self.cur.execute('UPDATE settings SET faq_keyboard = ? WHERE default_id = ?', [keyboards, 1])

                case 'spam':
                    await self.cur.execute('UPDATE settings SET spam_keyboard = ? WHERE default_id = ?', [keyboards, 1])

            return True
        
        except Exception as e:
            logger.error(e)
            return False
        
    
    async def updateText(self, text: str, type_: str):
        try:
            match type_:
                case 'hello':
                    await self.cur.execute('UPDATE settings SET hello_post = ? WHERE default_id = ?', [text, 1])
                    
                case 'faq':
                    await self.cur.execute('UPDATE settings SET faq_post = ? WHERE default_id = ?', [text, 1])

                case 'spam':
                    await self.cur.execute('UPDATE settings SET spam_post = ? WHERE default_id = ?', [text, 1])

            return True
        
        except Exception as e:
            logger.error(e)
            return False
        



    async def setChat(self, chat_id: int, chat_name: str):
        await self.cur.execute('UPDATE settings SET chat_id = ? WHERE default_id = ?', [chat_id, 1])
        await self.cur.execute('UPDATE settings SET chat_name = ? WHERE default_id = ?', [chat_name, 1])


    async def setMessagesThread(self, flood_message_thread_id: int, notification_message_thread_id: int):
        await self.cur.execute('UPDATE settings SET flood_message_thread_id = ? WHERE default_id = ?', [flood_message_thread_id, 1])
        await self.cur.execute('UPDATE settings SET notification_message_thread_id = ? WHERE default_id = ?', [notification_message_thread_id, 1])


    async def getWaitChat(self):
        return await (await self.cur.execute('SELECT wait_chat_id FROM settings WHERE default_id = ?', [1])).fetchone()


    async def updateWaitChat(self, chat_id: str):
        await self.cur.execute('UPDATE settings SET wait_chat_id = ? WHERE default_id = ?', [chat_id, 1])


    async def getSettings(self):
        return await (await self.cur.execute('SELECT * FROM settings WHERE default_id = ?', [1])).fetchone()


    async def updateContent(self, type_: str, status: int):
        await self.cur.execute(f'UPDATE content SET {type_} = ? WHERE default_id = ?', [status, 1])


    async def getContent(self):
        return await (await self.cur.execute('SELECT * FROM content WHERE default_id = ?', [1])).fetchone()

    async def createContent(self):
        try:
            await self.cur.execute('INSERT INTO content(default_id) VALUES(?)', [1])
        except:
            pass

    async def createSettings(self):
        try:
            await self.cur.execute('INSERT INTO settings(default_id) VALUES(?)', [1])
        except:
            pass


    async def addUser(self, user_id: int, name: str, username: str, register_date: str):
        try:
            await self.cur.execute('INSERT INTO users(user_id, name, username, date_registered) VALUES(?, ?, ?, ?)', 
                                   [user_id, name, username, register_date])
            return True
        except Exception as e:
            await self.cur.execute('UPDATE users SET name = ?, username = ? WHERE user_id = ?', [name, username, user_id])
            logger.error(e)
            return False
            
    async def getUser(self, user_id: int):
        return await (await self.cur.execute('SELECT * FROM users WHERE user_id = ?', [user_id])).fetchone()
    
    async def getUserThread(self, thread_id: int):
        return await (await self.cur.execute('SELECT * FROM users WHERE thread_id = ?', [thread_id])).fetchone()

    async def getAdminsDB(self):
        return await (await self.cur.execute('SELECT * FROM users WHERE admin = ?', [1])).fetchall()

    async def updateThreadIDUser(self, user_id: int, thread_id: int):
        await self.cur.execute('UPDATE users SET thread_id = ? WHERE user_id = ?', [thread_id, user_id])

        
    async def gerAllUsers(self):
        return await (await self.cur.execute('SELECT * FROM users')).fetchall()