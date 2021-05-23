import re 
from datetime import datetime as dt
from asyncio import sleep

from aiogram.utils.exceptions import InlineKeyboardExpected

import globals
from sites import Bomber
from globals import dp
from config import config

from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_models.User import session, User, DataUser

from payment.payment import Payment

cfg = config.Config()

@dp.message_handler(lambda message: message.text == "💣Атаковать номер")
async def ru_attack_phone(message: Message):
    '''
    Функция, выводящую информацию при нажатии на кнопку "Атаковать"

    Основные данные:
        1. Дата и время
        2. Номер телефона
        3. Количество кругов

    Рускоязычные пользователи.
    '''

    user_data = session.query(DataUser).filter_by(user_id=message.from_user.id).first()

    if user_data == None:
        user_data = DataUser(
                user_id=message.from_user.id, date=dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S"), 
                status=30, last_phone="None", 
                last_date="None"
        )
        session.add(user_data)
        session.commit()

        await message.answer(
                f"📄Информация о последней атаке ➜\n\n"
                f"📌Вы еще не совершали атаку!\n\n"
                f"☎️Введите номер телефона жертвы(без +)⤵️", 
                )
    else:
        date  = dt.strptime(user_data.date, "%d-%m-%Y %H:%M:%S") if user_data.date != "None" else "Неизвестно" #Time
        date  = dt.strftime(date, "%d-%m-%Y %H:%M:%S") if date != "Неизвестно" else "Неизвестно"
        phone = f"<code>{user_data.last_phone}</code>" if user_data.last_phone != "None" else "<b>Неизвестно</b>"
        
        await message.answer(
                f"📄Информация о последней атаке ➜\n\n"
                f"🕰Время: <b>{date}</b>\n"
                f"📌Номер: {phone}\n"
                f"⏱Осталось кругов: <b>{user_data.status}</b>\n\n"
                f"☎️Введите номер телефона жертвы(без +)⤵️"
                )

@dp.message_handler(lambda message: message.text == "💣Attack number")
async def eng_attack_phone(message: Message):
    '''
    Функция, выводящую информацию при нажатии на кнопку "Атаковать"

    Основные данные:
        1. Дата и время
        2. Номер телефона
        3. Количество кругов

    Англоязычные пользователи.
    '''

    user_data = session.query(DataUser).filter_by(user_id=message.from_user.id).first()

    if user_data == None:
        user_data = DataUser(
                user_id=message.from_user.id, date=dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S"), 
                status=30, last_phone="None", 
                last_date="None"
        )
        session.add(user_data)
        session.commit()

        await message.answer(
                f"📄Information about the last attack ➜\n\n"
                f"📌You haven't made an attack yet!\n\n"
                f"☎️Enter the victim's phone number (no +)⤵️", 
                )
    else:
        date  = dt.strptime(user_data.date, "%d-%m-%Y %H:%M:%S") if user_data.date != "None" else "Unknown"
        date  = dt.strftime(date, "%d-%m-%Y %H:%M:%S") if date != "Unknown" else "Unknown"
        phone = f"<code>{user_data.last_phone}</code>" if user_data.last_phone != "None" else "<b>Unknown</b>"
        
        await message.answer(
                f"📄Information about the last attack ➜\n\n"
                f"🕰Time: <b>{date}</b>\n"
                f"📌Phone number: {phone}\n"
                f"⏱Circles left: <b>{user_data.status}</b>\n\n"
                f"☎️Enter the victim's phone number (no +)⤵️"
                )

@dp.message_handler(lambda message: not message.text.startswith((
        "/msg", "/help",
         "/usd", "/btc", 
         "/bnb", "/eth", 
         "/stat", "/mail", 
         "📲Купить виртуальный номер"))
         )
async def take_phone(message: Message):
    if not message.chat.id in cfg.super_groups:     #Not super groups
        if globals.state_data != []:                #Not attack phone number
            if globals.state_data[0] == "payment":  #If this is payment

                try:                   
                    qiwi_data = Payment(count=float(message.text)).create_invoice() #Create invoice and get data

                    if not qiwi_data:
                        globals.state_data = [] #Reset array (qiwi data)
                        return await message.answer("Error")

                    r_url = qiwi_data["payUrl"]     #Url for payment
                    billId = qiwi_data["billId"]    #Id payment
                    user_id = globals.state_data[1] #User id 

                    continue_payment = InlineKeyboardMarkup(
                        inline_keyboard = [
                            [InlineKeyboardButton(text="Продолжить оплату", url=r_url)]
                        ]
                    )
                    await message.answer(
                        text="Нажмите кнопоку для продолжения оплаты", 
                        reply_markup=continue_payment
                    )

                    globals.state_data = [] #Reset array (qiwi data)

                    while True:
                        value_status = Payment(count=None).check_payment(last_id=billId)["status"]["value"] #Get payment status

                        await sleep(2) #Time-out 

                        if value_status == "WAITING":pass
                        elif value_status == "PAID":
                            #Update balance, insert new amount 
                            update_balance = session.query(User).filter_by(user_id=user_id).first()
                            update_balance.balance = float(update_balance.balance) + float(message.text)
                            session.commit()

                            await message.answer(f"✅ Баланс успешно пополнен на {float(message.text)}₽")
                            break
                    
                except ValueError:await message.answer("Нужно вводить число!")
                except KeyError:pass
        else:
            
            if message.text.isalpha() and message.text.isdigit():return False

            phone = re.sub("[^0-9]", "", message.text) #Only digital value

            if phone.startswith("7") or phone.startswith("8"): #Russia country
                #Phone format
                phone = f"7{phone[1:]}"

                globals.attack_country = "ru" #Set country name for attack

            elif phone.startswith("38"): #Ukraine country
                #Phone format
                arr_phone = phone.split("0")[1]
                phone = f"38{arr_phone}"

                globals.attack_country = "uk" #Set country name for attack
            
            else: #Unknow country or wrong value
                return await message.answer("🔁Не удалось определить страну. Проверьте номер на корректность!", reply=True)

            #Update data (last phone and last date)
            update_data = session.query(DataUser).filter_by(user_id=message.from_user.id).first()
            
            update_data.last_phone = phone
            update_data.last_date = dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S")

            session.commit()

            usl = InlineKeyboardMarkup(
                    inline_keyboard = [
                            [InlineKeyboardButton(
                                    text="⏹Остановить", callback_data=f"Остановить_{message.from_user.id}")]
                    ])

            await message.answer(
                    text="▶️Атака началась!\nНажмите кнопку для остановки атаки.", 
                    reply_markup = usl
                    )

            globals.start_attack = Bomber(user_id=str(message.from_user.id))
            await globals.start_attack.start(message.text, message.from_user.id)