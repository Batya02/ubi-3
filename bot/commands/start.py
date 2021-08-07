from db_models.User import User
from objects.globals import dp

from aiogram.types import (
        Message,              InlineKeyboardMarkup, 
        InlineKeyboardButton, ReplyKeyboardMarkup
        )

from datetime import datetime as dt

from temp.lang_start import lang_start
from temp.lang_keyboards import lang_keyboard

@dp.message_handler(commands="start")
async def start(message: Message):
    data = await User.objects.filter(user_id=message.from_user.id).all()
    
    if len(data) == 0:
        await User.objects.create(
            user_id=message.from_user.id, 
            username=str(message.from_user.username), 
            created=dt.now(), 
            language="None", 
            balance=0.0
        )
    
    lang = await User.objects.filter(user_id=message.from_user.id).all()
    lang = lang[0]

    if lang.language == "None":
        select_language_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🇬🇧ENG", callback_data="language_ENG")], 
                [InlineKeyboardButton(text="🇷🇺RU", callback_data="language_RU")]
                ]
        )

        return await message.answer(
            text=f"👾Hey\n"
            f"🌐Select the language",
            reply_markup=select_language_markup
            )
    
    return await message.answer(
        text=lang_start[lang.language],
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard=True,
            keyboard=lang_keyboard[lang.language]
        )
    )