from globals import conn, dp, all_users_table
from aiogram.types import Message

from sqlalchemy import select

@dp.message_handler(commands="help")
async def help(message: Message) -> str:
    language = select([all_users_table]).where(all_users_table.c.user_id==message.from_user.id)
    language = conn.execute(language).fetchone()

    with open(r"temp/help_%s.txt" % language[3], "r", encoding="utf-8") as help_text_read:
        help_text = help_text_read.read()
    
    return await message.reply(help_text, parse_mode="Markdown")