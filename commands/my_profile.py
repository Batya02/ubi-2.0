from globals import dp, conn

from aiogram.types import Message
from db_models.User import session, User

@dp.message_handler(lambda message: message.text == "👤Мой профиль")
async def my_profile_ru(message: Message):
    profile_data= session.query(User).filter_by(user_id=message.from_user.id).first()
    username = f"@{profile_data.username}" if profile_data.username != 'None' else 'Unknow'
    await message.answer(
            text=f"🌐<b>Язык:</b> {profile_data.language}\n\n"
            f"📍<b>User ID:</b> {profile_data.user_id}\n\n"
            f"📅<b>Дата регистрации:</b> <i>{profile_data.date_registration}</i>\n\n"
            f"💰<b>Баланс:</b> <code>{float(profile_data.balance)}</code>"
            )

@dp.message_handler(lambda message: message.text == "👤My profile")
async def my_profile_eng(message: Message):
    profile_data= session.query(User).filter_by(user_id=message.from_user.id).first()
    profile_data = conn.execute(profile_data).fetchone()
    username = f"@{profile_data.username}" if profile_data.username != 'None' else 'Unknow'

    await message.answer(
            text=f"🌐<b>Language:</b> {profile_data.language}\n\n"
            f"📍<b>User ID:</b> {profile_data.user_id}\n\n"
            f"📅<b>Date registration:</b> <i>{profile_data.date_registration}</i>\n"
            f"💰<b>Balance:</b> <code>{float(profile_data.balance)}</code>"
            )