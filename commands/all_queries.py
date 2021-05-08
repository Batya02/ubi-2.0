import globals
from globals import dp, bot, conn, eng_keyboards, ru_keyboards
from aiogram.types import (
        Message, CallbackQuery,
        ReplyKeyboardMarkup, InlineKeyboardMarkup, 
        InlineKeyboardButton)
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, ChatNotFound

from db_models.User import all_users_table
from sqlalchemy import select

from datetime import datetime as dt

@dp.callback_query_handler(lambda query: query.data.startswith(("change-lang")))
async def ad_callback(query: CallbackQuery):
    change_data = query.data.replace("_", " ").split()
    
    update_data = all_users_table.update().values(
            language=change_data[1]
    ).where(all_users_table.c.user_id==change_data[2])
    conn.execute(update_data)

    await bot.edit_message_text(
                chat_id = query.message.chat.id, 
                message_id = query.message.message_id, 
                text = f"➜ <b>{change_data[1]}</b>",        
                )

    await bot.send_message(
        change_data[2],
        text="Меню👇" if change_data[1] == "RU" else "Menu👇",
        reply_markup=ReplyKeyboardMarkup(
                            keyboard=eng_keyboards,
                            resize_keyboard = True) if change_data[1] == "ENG" else ReplyKeyboardMarkup(
                                                                                            keyboard=ru_keyboards, 
                                                                                            resize_keyboard = True)
    )

@dp.callback_query_handler(lambda query: query.data.startswith(("Остановить", "Stop")))
async def stop_attack(query: CallbackQuery):
    user_id = query.data.replace("_", " ").split()[1]
    language = select([all_users_table]).where(all_users_table.c.user_id==user_id)
    language = conn.execute(language).fetchone()[3]
    
    if language == "ENG": message = "✔️Attack stopped!"
    else: message = "✔️Атака остановлена!"
    try:
        await globals.start_attack.stop(str(user_id))
        await bot.edit_message_text(
                chat_id = query.message.chat.id, 
                message_id = query.message.message_id, 
                text =  message
                )
    except UnboundLocalError:
        await globals.start_attack.stop(str(user_id))
        await bot.edit_message_text(
                chat_id = query.message.chat.id, 
                message_id = query.message.message_id, 
                text =  message
                )

@dp.callback_query_handler(lambda query: query.data.startswith(("mail")))
async def on_mailing(query: CallbackQuery):
    all_users = select([all_users_table])
    all_users = conn.execute(all_users).fetchall()

    if query.data.split("_")[1] == "send":
        start_time = dt.utcnow()
        if len(globals.mail_markup.inline_keyboard) > 1:
            send_inline_data = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=globals.mail_button[0], url=globals.mail_button[1])]])

            for user in all_users:
                try:
                    await bot.send_message(user.user_id, 
                            text=globals.mail_content, 
                            reply_markup=send_inline_data
                            )
                    globals.mail_count+=1
                except (BotBlocked, UserDeactivated, ChatNotFound):pass
        else:
            for user in all_users:
                try:
                    await bot.send_message(user.user_id, 
                            text=globals.mail_content
                            )
                    globals.mail_count+=1
                except (BotBlocked, UserDeactivated, ChatNotFound):pass

        end_time = (dt.utcnow() - start_time).total_seconds()
        await bot.send_message(query.message.chat.id,
                f"✅Рассылка завершена! (Count: {globals.mail_count})\n"+\
                "⏱Время(sec): {:.2f}".format(end_time))

    elif query.data.split("_")[1] == "cancel": 
        await query.answer("Рассылка отменена!")
        await bot.delete_message(query.message.chat.id, query.message.message_id)
    
    