import globals
from globals import dp, bot, conn, ru_keyboards, eng_keyboards
from aiogram.types import Message

from sqlalchemy import select
from db_models.User import all_users_table

from aiogram.types import (
        InlineKeyboardMarkup, InlineKeyboardButton, 
        ReplyKeyboardMarkup
        )

from datetime import datetime as dt

@dp.message_handler(commands="start")
async def start(message: Message):

    data = select([all_users_table]).where(all_users_table.c.user_id==message.from_user.id)
    data = conn.execute(data).fetchall()

    if data == []:

        date_reg = dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S")

        insert_data = all_users_table.insert().values(
            user_id=message.from_user.id, 
            username=str(message.from_user.username), 
            date_registration=date_reg, 
            language="None"
        )

        globals.conn.execute(insert_data)

        lang_usl = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🇬🇧ENG", callback_data=f"change-lang_ENG_{message.from_user.id}")],
                [InlineKeyboardButton(text="🇷🇺RU", callback_data=f"change-lang_RU_{message.from_user.id}")]
            ]
        )

        await message.answer(
                    text=f"🌐Select the language\n"
                    f"🌐Выберите язык",
                    reply_markup=lang_usl
                    )

    else:
        language = data[0][3]

        if language == "None":
            lang_usl = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🇬🇧ENG", callback_data=f"change-lang_ENG_{message.from_user.id}")], 
                    [InlineKeyboardButton(text="🇷🇺RU", callback_data=f"change-lang_RU_{message.from_user.id}")]
                ]
            )

            await message.answer(
                    text=f"🌐Select the language\n"
                    f"🌐Выберите язык",
                    reply_markup=lang_usl
            )
        
        else:
            await message.answer(
                    text="🤖Universal Bot\n\nВыберите действие👇🏼" if language == "RU" else "🤖Universal Bot\n\nSelect an action👇🏼", 
                    reply_markup=ReplyKeyboardMarkup(
                                        keyboard=ru_keyboards, 
                                        resize_keyboard=True) if language == "RU" else ReplyKeyboardMarkup(
                                                                                                keyboard=eng_keyboards, 
                                                                                                resize_keyboard=True)
                    )