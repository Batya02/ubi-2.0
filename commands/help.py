from globals import dp
from aiogram.types import Message

from db_models.User import session, User

@dp.message_handler(commands="help")
async def help(message: Message) -> str:
    language = session.query(User.language).filter_by(user_id=message.from_user.id).first()[0]

    with open(r"temp/help_%s.txt" % language, "r", encoding="utf-8") as help_text_read:
        help_text = help_text_read.read()
    
    return await message.reply(help_text, parse_mode="Markdown")