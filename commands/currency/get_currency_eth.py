import json
import requests
from globals import dp, bot, username_bot
from aiogram.types import Message
from bs4 import BeautifulSoup as bs

@dp.message_handler(commands=("eth", f"eth@{username_bot}"))
async def get_currency_eth(message: Message):
    '''
    Функция получает последнюю инфомарцию о валюте(Эфир)
    '''

    try:
        await bot.delete_message(message.chat.id, message.message_id)
    except:await bot.delete_message(message.from_user.id, message.message_id)

    try:
        eth_url = requests.get(timeout=0.5, url=
        "https://www.binance.com/en/trade/ETH_USDT")
        eth_soup = str(bs(eth_url.text, "html.parser").find(id="__APP_DATA"))
        eth = json.loads(eth_soup.replace("</script>", "").replace('<script id="__APP_DATA" type="application/json">', ""))
        eth = eth["pageData"]["redux"]["products"]["currentProduct"]

        symbol = eth["symbol"]
        close_price = eth["close"]
        low_price = eth["low"]
        high_price = eth["high"]

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