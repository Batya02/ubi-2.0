from globals import dp, ru_keyboards, eng_keyboards
from db_models.User import session, User

from aiogram.types import (
        InlineKeyboardMarkup, InlineKeyboardButton, 
        ReplyKeyboardMarkup, Message
        )

from datetime import datetime as dt

@dp.message_handler(commands="start")
async def start(message: Message):

    data_user = session.query(User).filter_by(user_id=message.from_user.id).first()
    
    if data_user == None:
        new_user = User(
                user_id=message.from_user.id, username=message.from_user.username, 
                date_registration=dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S"), language="None", 
                balance="0.0"

        )
        session.add(new_user)
        session.commit()

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
        language = data_user.language

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