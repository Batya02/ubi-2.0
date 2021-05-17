import json
from aiohttp import ClientSession
from globals import dp, data_numbers_kv
from config import config
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

cfg = config.Config()

@dp.message_handler(lambda message: message.text=="📲Купить виртуальный номер")
async def get_numbers_list(message: Message):   
    async with ClientSession() as session:
        data_numbers = await session.get(f"https://{cfg.host_site_main}/v1/guest/products/russia/any")
        data_numbers = json.loads(await data_numbers.text())
        await session.close()

        data_numbers_values = [data_numbers["telegram"], data_numbers["vkontakte"], data_numbers["whatsapp"]]
        data_numbers_keys = ["telegram", "vkontakte", "whatsapp"]
        data_numbers_kv = dict(zip(data_numbers_keys, data_numbers_values))
        
        tg_price = int(data_numbers["telegram"]["Price"]) + 1
        vk_price = int(data_numbers["vkontakte"]["Price"]) + 1
        wa_price = int(data_numbers["whatsapp"]["Price"]) + 1
        
        numbers_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"Telegram {tg_price}₽", callback_data=f"num_telegram_{tg_price}")],
                [InlineKeyboardButton(text=f"Vkontakte {vk_price}₽", callback_data=f"num_vkontakte_{vk_price}")],
                [InlineKeyboardButton(text=f"WhatsApp {wa_price}₽", callback_data=f"num_whatsapp_{wa_price}")]
            ]
        )

        await message.answer(
            text="🇷🇺Выберите сервис👇", 
            reply_markup=numbers_markup
        )        