from db_models.UserAuth import UserAuth
from objects.globals import dp

from aiogram.types import (
    Message, InlineKeyboardMarkup, 
    InlineKeyboardButton
    )

from db_models.User import User

from datetime import datetime as dt
from formats.dateTime import datetime_format

@dp.message_handler(lambda message:message.text == "👤Мой профиль")
async def my_profile_ru(message: Message):
    """ My profile (RU)

    :param: message
    :type: Message
    :return: Bot answer message
    :rtype: Message

    """

    web_user_data = await UserAuth.objects.get(login=message.from_user.id)
    user_data = await User.objects.filter(user_id=message.from_user.id).all()
    user_data = user_data[0]

    date = datetime_format(user_data.created)

    buttons_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Пополнить баланс", callback_data="top_up_balance")], 
            [InlineKeyboardButton(text="Изменить язык", callback_data="change_language")], 
            [InlineKeyboardButton(text="Информация о последней атаке", callback_data="info_about_the_last_attack")],
            [InlineKeyboardButton(text="Вывести историю активаций", callback_data="get_history_activations")]
            ]
    )

    return await message.answer(
        text=f"🌐<b>Язык:</b> {user_data.language}\n"
        f"➖\n"
        f"📍<b>User ID:</b> {user_data.user_id}\n"
        f"➖\n"
        f"📅<b>Дата регистрации:</b> <i>{date}</i>\n"
        f"➖\n"
        f"💰<b>Баланс:</b> <code>{float(user_data.balance)}₽</code>\n\n"
        f"Данные от аккаунта:\n"
        f"Логин: <code>{web_user_data.login}</code>\n"
        f"Пароль: <code>{web_user_data.password}</code>", 
        reply_markup=buttons_markup
    )

@dp.message_handler(lambda message:message.text == "👤My profile")
async def my_profile_eng(message: Message):
    """ My profile (ENG)

    :param: message
    :type: Message
    :return: Bot answer message
    :rtype: Message

    """

    user_data = await User.objects.filter(user_id=message.from_user.id).all()
    user_data = user_data[0]

    date = dt.strftime(dt.now(), "%Y-%m-%d %H:%M:%S")

    buttons_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Top up balance", callback_data="top_up_balance")], 
            [InlineKeyboardButton(text="Change language", callback_data="change_language")], 
            [InlineKeyboardButton(text="Information about the last attack", callback_data="info_about_the_last_attack")],
            [InlineKeyboardButton(text="Get activation history", callback_data="get_history_activations")]
            ]
    )

    return await message.answer(
        text=f"🌐<b>Язык:</b> {user_data.language}\n"
        f"➖\n"
        f"📍<b>User ID:</b> {user_data.user_id}\n"
        f"➖\n"
        f"📅<b>Date registration:</b> <i>{date}</i>\n"
        f"➖\n"
        f"💰<b>Balance:</b> <code>{float(user_data.balance)}₽</code>", 
        reply_markup=buttons_markup
    )