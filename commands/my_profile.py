from globals import dp, conn

from aiogram.types import Message

from sqlalchemy import select
from db_models.User import all_users_table, data_users_table

@dp.message_handler(lambda message: message.text == "👤Мой профиль")
async def my_profile_ru(message: Message):
    profile_data = select([all_users_table]).where(all_users_table.c.user_id==message.from_user.id)
    profile_data = conn.execute(profile_data).fetchone()
    username = f"@{profile_data[1]}" if profile_data[1] != 'None' else 'Unknow'

    await message.answer(
            text=f"🌐<b>Язык:</b> {profile_data[3]}\n\n"
            f"📍<b>User ID:</b> {profile_data[0]}\n\n"
            f"📌<b>Username:</b> {username}\n\n"
            f"📅<b>Дата регистрации:</b> <i>{profile_data[2]}</i>\n"
            )

@dp.message_handler(lambda message: message.text == "👤My profile")
async def my_profile_eng(message: Message):
    profile_data = select([all_users_table]).where(all_users_table.c.user_id==message.from_user.id)
    profile_data = conn.execute(profile_data).fetchone()
    username = f"@{profile_data[1]}" if profile_data[1] != 'None' else 'Unknow'

    await message.answer(
            text=f"🌐<b>Language:</b> {profile_data[3]}\n\n"
            f"📍<b>User ID:</b> {profile_data[0]}\n\n"
            f"📌<b>Username:</b> {username}\n\n"
            f"📅<b>Date registration:</b> <i>{profile_data[2]}</i>\n"
            )