import json
import requests
from globals import dp, bot, username_bot
from aiogram.types import Message
from bs4 import BeautifulSoup as bs

@dp.message_handler(commands=("btc", f"btc@{username_bot}"))
async def get_currency_btc(message: Message):
    '''
    Функция получает последнюю инфомарцию о валюте(Биткоин)
    '''

    try:
        btc_url = requests.get(timeout=0.5, url=
        "https://www.binance.com/en/trade/BTC_USDT")
        btc_soup = str(bs(btc_url.text, "html.parser").find(id="__APP_DATA"))
        btc = json.loads(btc_soup.replace("</script>", "").replace('<script id="__APP_DATA" type="application/json">', ""))
        btc = btc["pageData"]["redux"]["products"]["currentProduct"]

        symbol = btc["symbol"]
        close_price = btc["close"]
        low_price = btc["low"]
        high_price = btc["high"]

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