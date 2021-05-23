import os 
import asyncio
from loguru import logger

import globals

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logger.add("debug/debug.log", format="{time} {level} {message}", 
    level="DEBUG", rotation="1 week", compression="zip")

globals.dp = Dispatcher(globals.bot, storage=MemoryStorage())

send_mess_PATH = os.getcwd()  #Main path

async def main():
    
    from commands import (
            statistics, start, 
            my_profile, admin, 
            send_message, change_language, 
            help, mailing, 
            get_numbers, attack_phone, 
            all_queries
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