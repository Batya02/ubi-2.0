import globals
from config import config
from globals import dp, bot, conn, eng_keyboards, ru_keyboards
from aiogram.types import (
        Message, CallbackQuery,
        ReplyKeyboardMarkup, InlineKeyboardMarkup, 
        InlineKeyboardButton)
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, ChatNotFound

from db_models.User import all_users_table
from sqlalchemy import select

from datetime import datetime as dt
from aiohttp import ClientSession

cfg = config.Config()

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

@dp.callback_query_handler(lambda query: query.data.startswith(("num")))
async def numbers_service(query: CallbackQuery):
    service = query.data.replace("_", " ").split()[1]

    async with ClientSession() as session:
        res = await session.get(f"http://{cfg.host_site_api}/stubs/handler_api.php?api_key={cfg.api_key}&action=getNumber&service={service}&operator=any&country=russia")
        res = await res.text()
        if res == "NO_NUMBERS":
            await query.answer(text="Номера отсутствуют!")
        else:
            res = res.split(":")
            status_number = res[0]
            id_number = res[1]
            self_number = res[2]

            number_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Отменить", callback_data=f"cancelnum_{id_number}")]
                ]
            )

            await bot.edit_message_text(
                    chat_id = query.message.chat.id, 
                    message_id = query.message.message_id, 
                    text=f"Status: <b>{status_number}</b>\n"
                    f"ID: <code>{id_number}</code>\n"
                    f"Number: <code>{self_number}</code>", 
                    reply_markup=number_markup
            )

            while True:
                get_id = await session.get(f"http://{cfg.host_site_api}/stubs/handler_api.php?api_key={cfg.api_key}&action=getStatus&id={id_number}")
                get_id = await get_id.text()
                if get_id == "STATUS_WAIT_CODE":pass
                elif get_id.startswith(("STATUS_OK")):
                    code = get_id.split(":")[1]
                    return await bot.send_message(
                        query.message.chat.id, 
                        text=f"Code: <code>{code}</code>"
                    )

@dp.callback_query_handler(lambda query: query.data.startswith(("cancelnum")))
async def cancel_number(query: CallbackQuery):
    cancel_id_number = query.data.replace("_", " ").split()[1]
    async with ClientSession() as session:
        res = await session.post(f"http://{cfg.host_site_api}/stubs/handler_api.php?api_key={cfg.api_key}&action=setStatus&status=-1&id={cancel_id_number}")
        res = await res.text()
        if res == "ACCESS_CANCEL":
            await query.answer(text="Номер успешно отменен.")
            await bot.delete_message(query.message.chat.id, query.message.message_id)


    