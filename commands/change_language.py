from globals import dp
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

@dp.message_handler(lambda message: message.text == "🌐Изменить язык" or message.text == "🌐Change the language")
async def ru_send_message(message: Message):
    '''
    Функция изменения языка
    Дается выбор: 
        1. Английский(ENG)
        2. Русский(RUS)
    '''

    change_language_usl = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text="🇬🇧ENG", callback_data=f"change-lang_ENG_{message.from_user.id}")],
            [InlineKeyboardButton(text="🇷🇺RU", callback_data=f"change-lang_RU_{message.from_user.id}")]
        ]
    )

    await message.answer(
            text = f"🌐Select the language\n"
            f"🌐Выберите язык", 
            reply_markup=change_language_usl
    )