import json
import requests
from globals import dp, bot, username_bot
from aiogram.types import Message
from bs4 import BeautifulSoup as bs

@dp.message_handler(commands=("bnb", f"bnb@{username_bot}"))
async def get_currency_bnb(message: Message):
    '''
    Функция получает последнюю инфомарцию о валюте(Доллар)
    '''

    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except:await bot.delete_message(message.from_user.id, message.message_id)
    
    try:
        bnb_url = requests.get(timeout=0.5, url=
        "https://www.binance.com/en/trade/BNB_USDT")
        bnb_soup = str(bs(bnb_url.text, "html.parser").find(id="__APP_DATA"))
        bnb = json.loads(bnb_soup.replace("</script>", "").replace('<script id="__APP_DATA" type="application/json">', ""))
        bnb = bnb["pageData"]["redux"]["products"]["currentProduct"]

        symbol = bnb["symbol"]
        close_price = bnb["close"]
        low_price = bnb["low"]
        high_price = bnb["high"]

        await message.answer(
                text=f"*{symbol}*\n"
                f"_Now_: `{close_price}`\n"
                f"_Min_: *{low_price}*\n"
                f"_Max_: *{high_price}*", 
                parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(
                text=f"⚠️Ошибка при отправке запроса...\n"
                f"Информация об ошибке ➔ {e}"
        )