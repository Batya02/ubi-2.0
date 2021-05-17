import globals
from config import config
from globals import dp, bot, conn, eng_keyboards, ru_keyboards
from aiogram.types import (
        CallbackQuery, ReplyKeyboardMarkup, 
        InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, ChatNotFound

from db_models.User import session, User, Orders

from datetime import datetime as dt
from aiohttp import ClientSession
import pandas as pd
from io import BytesIO

cfg = config.Config()

@dp.callback_query_handler(lambda query: query.data.startswith(("change-lang")))
async def ad_callback(query: CallbackQuery):
    change_data = query.data.replace("_", " ").split()

    changer = session.query(User).filter_by(user_id=change_data[2]).first()
    changer.language = change_data[1]
    session.commit()

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

    language = session.query(User).filter_by(user_id=user_id).first().language
    
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
    all_users = session.query(User).all()

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
    service_name, service_price = query.data.replace("_", " ").split()[1:] #Service data (array)

    async with ClientSession() as client_session:
        res = await client_session.get(f"http://{cfg.host_site_api}/stubs/handler_api.php?api_key={cfg.api_key}&action=getNumber&service={service_name}&operator=any&country=russia")
        res = await res.text()

        #If not found numbers
        if res == "NO_NUMBERS":
            await query.answer(text="Номера отсутствуют!")

        #If ended balance
        elif res == "NO_BALANCE":
            await bot.send_message(
                cfg.chat_id, 
                text=f"Нужно пополнить счет! https://{cfg.host_site_main}"
            )

            await query.answer(text="Неизвестная ошибка!")

        #If all true
        else:
            my_balance = float(session.query(User.balance).filter_by(user_id=query.message.chat.id).first()[0])
            new_balance = my_balance - float(service_price)
            if new_balance < 0:
                return await bot.send_message(
                        query.message.chat.id, 
                        text="Недостаточно средств на балансе!"
                )
            else:
                #UPDATE BALANCE
                update_balance = session.query(User).filter_by(user_id=query.message.chat.id).first()
                update_balance.balance = new_balance
                session.commit()

                #CREATE NEW ORDER
                create_new_order = Orders(
                        user_id=query.message.chat.id, created=dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S"), 
                        service = service_name, price = service_price)
                session.add(create_new_order)
                session.commit()
            
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

                #GET ID ORDER
                get_id = await client_session.get(f"http://{cfg.host_site_api}/stubs/handler_api.php?api_key={cfg.api_key}&action=getStatus&id={id_number}")
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

        #CANCEL ORDER
        res = await session.post(f"http://{cfg.host_site_api}/stubs/handler_api.php?api_key={cfg.api_key}&action=setStatus&status=-1&id={cancel_id_number}")
        res = await res.text()

        if res == "ACCESS_CANCEL":
            await query.answer(text="Номер успешно отменен.")
            await bot.delete_message(query.message.chat.id, query.message.message_id)

@dp.callback_query_handler(lambda query: query.data.startswith(("phone_stat")))
async def get_phone_stat(query: CallbackQuery):
    user_id = query.data.split("_")[2]

    data_orders = session.query(Orders).filter_by(user_id=user_id).all()
    language = session.query(User.language).filter_by(user_id=user_id).first()[0]

    if data_orders == []:
        return await query.answer(
                text= "У вас нет активированных номеров!" if language == "RU" else "You have no activated numbers!"
        )
    
    columns = Orders.__table__.columns.keys()

    all_data = []
    all_data.append([id.id for id in data_orders])
    all_data.append([created.created for created in data_orders])
    all_data.append([service.service for service in data_orders])
    all_data.append([price.price for price in data_orders])

    columns.remove("user_id")

    towrite = BytesIO()
    data_dct = dict(zip(columns, all_data))
    df = pd.DataFrame(data_dct)
    df.to_excel(towrite)

    await bot.send_document(
        query.message.chat.id, 
        document=("activation.xlsx",towrite.getvalue())
    )