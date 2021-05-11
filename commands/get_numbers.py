import json
from aiohttp import ClientSession
from globals import dp, data_numbers_kv
from config import config
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

cfg = config.Config()

@dp.message_handler(lambda message: message.text=="📲Купить виртуальный номер")
async def get_numbers_list(message: Message):
    if message.from_user.id == cfg.chat_id:
        async with ClientSession() as session:
            data_numbers = await session.get(f"https://{cfg.host_site_main}/v1/guest/products/russia/any")
            data_numbers = json.loads(await data_numbers.text())
            await session.close()

            data_numbers_values = [data_numbers["telegram"], data_numbers["vkontakte"], data_numbers["whatsapp"]]
            data_numbers_keys = ["telegram", "vkontakte", "whatsapp"]
            data_numbers_kv = dict(zip(data_numbers_keys, data_numbers_values))
            
            
            numbers_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Telegram", callback_data="num_telegram")],
                    [InlineKeyboardButton(text="Vkontakte", callback_data="num_vkontakte")],
                    [InlineKeyboardButton(text="WhatsApp", callback_data="num_whatsapp")]
                ]
            )

            await message.answer(
                text="🇷🇺Выберите сервис👇", 
                reply_markup=numbers_markup
            )
    else:
        await message.answer(text="Скоро будет доступно!")

    