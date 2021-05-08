import json
import requests
from globals import dp, bot
from aiogram.types import Message
from bs4 import BeautifulSoup as bs

@dp.message_handler(commands="usd")
async def get_currency_usd(message: Message):
    '''
    Функция получает последнюю инфомарцию о валюте(Доллар)

    '''
    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except:await bot.delete_message(message.from_user.id, message.message_id)

    try:
        usd_url = requests.get(timeout=0.5, url=
        "https://www.binance.com/en/trade/USDT_RUB")
        usd_soup = str(bs(usd_url.text, "html.parser").find(id="__APP_DATA"))
        usd = json.loads(usd_soup.replace("</script>", "").replace('<script id="__APP_DATA" type="application/json">', ""))
        usd = usd["pageData"]["redux"]["products"]["currentProduct"]

        symbol = usd["symbol"]
        close_price = usd["close"]
        low_price = usd["low"]
        high_price = usd["high"]

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