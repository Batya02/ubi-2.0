from globals import dp, conn, bot, config

from sqlalchemy import select
from db_models.User import all_users_table

from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State

from commands import change_language, attack_phone
from aiogram.utils.exceptions import ChatNotFound

@dp.message_handler(commands=["msg"])
async def ru_send_message(message: Message):
    data = select([all_users_table]).where(all_users_table.c.user_id==message.from_user.id)
    data = conn.execute(data).fetchone()

    if data[3] == "ENG":message_form="📫Message sent successfully. Wait for an answer ..."
    elif data[3] == "RU":message_form="📫Сообщение успешно отправлено. Ожидайте ответа ..."
    
    msg:str = message.text.replace("/msg", "").strip()
    if msg == "":
        return await message.answer("⚠️Нужно воодить сообщение!" if data[3] == "RU" else "⚠️You need to enter a message!")

    if message.reply_to_message == None:
        await bot.send_message(
                config.chat_id, 
                text=f"User_ID: <code>{message.from_user.id}</code>\n"
                     f"Username: @{message.from_user.username}\n"
                     f"Message: <code>{msg}</code>\n"
        )

        await bot.send_message(
                message.chat.id, 
                text=message_form
        )
    else:
        user_id = message.reply_to_message.text.replace(":", " ").split()[1]
        user_data = select([all_users_table]).where(all_users_table.c.user_id==user_id)
        user_data = conn.execute(user_data).fetchone()
        if user_data == None: return await message.answer("⚠️Нельзя пересылать сообщения!" if data[3] == "RU" else "⚠️No forwarding messages!")
        await bot.send_message(
            user_id, 
            text=f"📬Сообщение от админа: <code>{msg}</code>" if user_data[3] == "RU" else f"📬Message from admin: <code>{msg}</code>"
        )

        await bot.send_message(
                message.chat.id, 
                text=message_form
        )
    