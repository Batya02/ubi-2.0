import globals
from globals import dp
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@dp.message_handler(commands="mail")
async def mailing(message: Message):
    if message.text.split("/mail")[1] != '':
        if "\nКнопка:" in message.text.split("/mail")[1]:
            globals.mail_content = (message.text.split("/mail")[1].split("\nКнопка:")[0]).strip()
            globals.mail_button = (message.text.split("/mail")[1]).replace("\nКнопка: ", "").split(" | ")
            globals.mail_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=globals.mail_button[0].strip(), url=globals.mail_button[1].strip())], 
                    [InlineKeyboardButton(text="Send", callback_data="mail_send"), 
                    InlineKeyboardButton(text="Cancel", callback_data="mail_cancel")]
                ]
            )

            await message.answer(text=globals.mail_content[0], reply_markup=globals.mail_markup)
        else: 
            globals.mail_content = (message.text.split("/mail")[1]).strip()
            globals.mail_markup = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Send", callback_data="mail_send"), 
                    InlineKeyboardButton(text="Cancel", callback_data="mail_cancel")]
                ]
            )

            await message.answer(text=globals.mail_content, reply_markup=globals.mail_markup)

    else:await message.answer("Нужно вводить сообщение!")