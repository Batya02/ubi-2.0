from aiogram.types import Message

from globals import config, dp
from db_models.User import session, User, DataUser

@dp.message_handler(commands="stat")
async def statistics(msg: Message):
    if msg.from_user.id in config.admins:

        all_users_ids = session.query(User.id).all() #All users
        data_users_ids = session.query(DataUser.id).all() #Data users
        endless_status = session.query(DataUser).filter_by(status="∞").all() #Endless status (∞)

        await msg.answer(
            f"📊Статистика:\n"
            f"Общее количество: {len(all_users_ids)}\n"
            f"Активировали бомбер: {len(data_users_ids)}\n"
            f"Приоритетный статус (∞): {len(endless_status)}"
        )