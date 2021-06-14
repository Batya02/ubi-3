from aiogram.types import (
        CallbackQuery,        InlineKeyboardMarkup, 
        InlineKeyboardButton, ReplyKeyboardMarkup, 
        Message
        )

from objects.globals import dp, bot
from objects import globals

from db_models.User import User
from db_models.UserData import UserData
from db_models.FAO import FAO

from temp.select_lang import select_lang
from temp.lang_keyboards import lang_keyboard

from formats import dateTime

from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from qiwipyapi import Wallet

from asyncio import sleep
from io import BytesIO

import pandas as pd

WALLET = Wallet(globals.config["qiwi_phone"], p2p_sec_key=globals.config["qiwi_private_key"])

class States(StatesGroup):
    get_amount_balance_targ = State()

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
        f"Дата и время: {dateTime.datetime_format(user_data.last_date)}"
    )

@dp.callback_query_handler(lambda query: query.data == "top_up_balance")
async def top_up_balance(query: CallbackQuery):
    await bot.edit_message_text(
        chat_id = query.from_user.id, 
        message_id=query.message.message_id, 
        text="Введите сумму для пополения:"
    )

    await States.get_amount_balance_targ.set()

@dp.message_handler(state=States.get_amount_balance_targ)
async def get_amount_balance(message: Message, state:FSMContext):
    await state.finish()

    try:
        amount = float(message.text)
        invoice = WALLET.create_invoice(value=amount)

        payment_url = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Продолжить оплату", url=invoice["payUrl"])]
            ]
        )

        await message.answer(
            text="Продолжить оплату?", 
            reply_markup=payment_url
        )

        while True:
            status = WALLET.invoice_status(bill_id=invoice["billId"])
            if status["status"]["value"] == "WAITING":pass
            elif status["status"]["value"] == "PAID":
                update_balance = await User.objects.get(user_id=message.from_user.id)
                new_value_to_balance = float(update_balance.balance) + amount
                await update_balance.update(balance=new_value_to_balance)
                return await message.answer(f"Ваш баланс успешно пополнен на {amount}₽")
            await sleep(5)

    except ValueError:
        return await message.answer(
            text="Правильный формат ввода суммы - 10 или 10.0"
        ) 

@dp.callback_query_handler(lambda query: query.data == "get_history_activations")
async def get_history_activation(query: CallbackQuery):
    fao_data = await FAO.objects.filter(user_id=query.from_user.id).all()
    
    columns = ["ID", "Дата покупки", "Сервис", "Цена"]
    all_data = []

    all_data.append([id.id for id in fao_data])
    all_data.append([created.created for created in fao_data])
    all_data.append([service.service for service in fao_data])
    all_data.append([price.price for price in fao_data])

    to_write = BytesIO()
    data_dict = dict(zip(columns, all_data))
    df = pd.DataFrame(data_dict)
    df.to_excel(to_write)
    
    await bot.edit_message_text(
        chat_id = query.from_user.id, 
        message_id = query.message.message_id, 
        text="Дождитесь загрузки..."
    )
    return await bot.send_document(
        query.message.chat.id, 
        document=("activation.xlsx",to_write.getvalue())
    )