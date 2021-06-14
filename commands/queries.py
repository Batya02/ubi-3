from aiogram.types import (
        CallbackQuery,        InlineKeyboardMarkup, 
        InlineKeyboardButton, ReplyKeyboardMarkup)

from objects.globals import dp, bot
from objects import globals

from db_models.User import User
from db_models.UserData import UserData

from temp.select_lang import select_lang
from temp.lang_keyboards import lang_keyboard


@dp.callback_query_handler(lambda query: query.data.startswith(("language")))
async def select_language(query: CallbackQuery):

    change_language = await User.objects.get(user_id=query.from_user.id)
    await change_language.update(language=query.data.split("_")[1])

    await bot.delete_message(
        chat_id = query.from_user.id, 
        message_id = query.message.message_id,
    )

    return await bot.send_message(
        query.from_user.id, 
        text=select_lang[query.data.split("_")[1]], 
        reply_markup=ReplyKeyboardMarkup(
                    resize_keyboard=True,
                    keyboard=lang_keyboard[query.data.split("_")[1]]
                    )
    )

@dp.callback_query_handler(lambda query: query.data == "change_language")
async def change_language(query: CallbackQuery):
    languages_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇬🇧ENG", callback_data="language_ENG")], 
            [InlineKeyboardButton(text="🇷🇺RU", callback_data="language_RU")]
        ]
    )

    await bot.edit_message_text(
        chat_id = query.from_user.id, 
        message_id = query.message.message_id,
        text="🌐Select the language", 
        reply_markup=languages_markup
    )

@dp.callback_query_handler(lambda query: query.data == "stoped_attack")
async def stoped_attack(query: CallbackQuery):
    await globals.client_session_object.stop()

    await bot.edit_message_text(
        chat_id = query.from_user.id, 
        message_id = query.message.message_id,
        text="✅Атака остановлена")

@dp.callback_query_handler(lambda query: query.data == "info_about_the_last_attack")
async def get_info_about_the_last_attack(query: CallbackQuery):
    user_data = await UserData.objects.filter(user_id=query.from_user.id).all()
    user_data = user_data[0]

    return await bot.edit_message_text(
        chat_id=query.from_user.id, 
        message_id=query.message.message_id, 
        text=f"Статус: {user_data.status}\n"
        f"Номер телефона: {user_data.last_phone}\n"
        f"Дата и время: {user_data.last_date}"
    )