from globals import dp

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from db_models.User import session, User

@dp.message_handler(lambda message: message.text == "👤Мой профиль")
async def my_profile_ru(message: Message):

    profile_data= session.query(User).filter_by(user_id=message.from_user.id).first() #Get data user
    #username = f"@{profile_data.username}" if profile_data.username != 'None' else 'Unknow' #Set format username

    get_phones_stat = InlineKeyboardMarkup(
        inline_keyboard= [
            [InlineKeyboardButton(text="Вывести историю активаций(xlsx)", callback_data=f"phone_stat_{message.chat.id}")], 
            [InlineKeyboardButton(text="Пополнить счёт", callback_data=f"payment_{message.chat.id}")]
        ]
    )

    await message.answer(
            text=f"🌐<b>Язык:</b> {profile_data.language}\n\n"
            f"📍<b>User ID:</b> {profile_data.user_id}\n\n"
            f"📅<b>Дата регистрации:</b> <i>{profile_data.date_registration}</i>\n\n"
            f"💰<b>Баланс:</b> <code>{float(profile_data.balance)}₽</code>", 
            reply_markup=get_phones_stat
            )

@dp.message_handler(lambda message: message.text == "👤My profile")
async def my_profile_eng(message: Message):
    profile_data = session.query(User).filter_by(user_id=message.from_user.id).first() #Get data user
    #username = f"@{profile_data.username}" if profile_data.username != 'None' else 'Unknow'

    get_phones_stat = InlineKeyboardMarkup(
        inline_keyboard= [
            [InlineKeyboardButton(text="Display activation history(xlsx)", callback_data=f"phone_stat_{message.chat.id}")]
        ]
    )
    
    await message.answer(
            text=f"🌐<b>Language:</b> {profile_data.language}\n\n"
            f"📍<b>User ID:</b> {profile_data.user_id}\n\n"
            f"📅<b>Date registration:</b> <i>{profile_data.date_registration}</i>\n\n"
            f"💰<b>Balance:</b> <code>{float(profile_data.balance)}₽</code>",
            reply_markup=get_phones_stat
            )