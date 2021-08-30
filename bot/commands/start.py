from hashlib import md5
from datetime import datetime as dt

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

from objects.globals import dp
from db_models.UserAuth import UserAuth
from temp.lang_start import lang_start
from temp.lang_keyboards import lang_keyboard
from decorators.updates import update_time

@dp.message_handler(commands="start")
@update_time
async def start(message:Message):
    """ Start function

    :param: message
    :type: Message
    :return: Bot message answer
    :rtype: Message

    """
    message: Message = message[0]

    data: UserAuth = await UserAuth.objects.filter(login=message.from_user.id).all()

    if not data:
        hash_pass: str = md5(str(message.from_user.id).encode("utf-8")).hexdigest()[:10]
        await UserAuth.objects.create(login=message.from_user.id, password=hash_pass,
                username=message.from_user.username, last_name=message.from_user.last_name,
                first_name=message.from_user.first_name, last_password=hash_pass)

    data: UserAuth = await UserAuth.objects.get(login=message.from_user.id)

    if not data.language:
        select_language_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🇬🇧ENG", callback_data="language_ENG")], 
                [InlineKeyboardButton(text="🇷🇺RU", callback_data="language_RU")]
                ])

        return await message.answer(text=f"👾Hey\n"f"🌐Select the language", reply_markup=select_language_markup)

    return await message.answer(text=lang_start[data.language],
            reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,keyboard=lang_keyboard[data.language]))