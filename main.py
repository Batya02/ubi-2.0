import os 
import re
import json
import asyncio
import sqlite3
from loguru import logger
from aiohttp import ClientSession
from datetime import datetime as dt

import commands
import globals
from sites import Bomber
from config.config import Config

from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ( 
        ReplyKeyboardMarkup, KeyboardButton, 
        InlineKeyboardMarkup, InlineKeyboardButton, 
        Message
        )

#from db_models.User import session, User
from sqlalchemy import select

logger.add("debug/debug.log", format="{time} {level} {message}", 
    level="DEBUG", rotation="1 week", compression="zip")

globals.dp = Dispatcher(globals.bot, storage=MemoryStorage())

send_mess_PATH = os.getcwd()  #Main path


async def main():
    
    from commands import (
            statistics, start, 
            my_profile, admin, 
            send_message, change_language, 
            all_queries, help, 
            attack_phone, mailing,
            get_numbers
            )

    from commands.currency import (
            get_currency_usd, get_currency_btc,
            get_currency_eth, get_currency_bnb
            )
     
    info_bot = await globals.bot.get_me() #Get Bot Data
    globals.username_bot = info_bot.username #Set bot username
 
    await globals.dp.start_polling()

if __name__ == '__main__':
    #executor.start_polling(globals.dp, skip_updates = True)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except RuntimeError:pass 