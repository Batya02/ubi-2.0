from globals import dp, bot, config
from db_models.User import session, User

from aiogram.types import Message

@dp.message_handler(commands=["msg"])
async def ru_send_message(message: Message):

    data = session.query(User).filter_by(user_id=message.from_user.id).first() #My data

    if data.language == "ENG":message_form="📫Message sent successfully. Wait for an answer ..."
    elif data.language == "RU":message_form="📫Сообщение успешно отправлено. Ожидайте ответа ..."
    
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
        user_data = session.query(User).filter_by(user_id=user_id).first() #Reply data

        if user_data == None: return await message.answer("⚠️Нельзя пересылать сообщения!" if data.language == "RU" else "⚠️No forwarding messages!")
        await bot.send_message(
            user_id, 
            text=f"📬Сообщение от админа: <code>{msg}</code>" if user_data.language == "RU" else f"📬Message from admin: <code>{msg}</code>"
        )

        await bot.send_message(
                message.chat.id, 
                text=message_form
        )    