from globals import dp, config
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

@dp.message_handler(commands="adm")
async def adm(message: Message):
    """
    Admin function 
    message -- data user 
    """

    if str(message.from_user.id) == str(config.chat_id):
        usl = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                        text = "📣Рассылка", callback_data = "Рассылка")],
                [InlineKeyboardButton(
                        text = "📧Отправить сообщение(ID)", callback_data= "Отправить сообщение(ID)")]
            ]
        )

        await message.answer(
                text="🤖Universal Bot\n\nВыберите действие👇🏼", 
                reply_markup = usl)
    else:pass