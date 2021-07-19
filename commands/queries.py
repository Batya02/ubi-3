from aiogram.types import (
        CallbackQuery,        InlineKeyboardMarkup, 
        InlineKeyboardButton, ReplyKeyboardMarkup, 
        Message
        )

from objects.globals import dp, bot, config
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
from aiohttp import ClientSession

from datetime import datetime as dt 
from datetime import timedelta

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
        text=f"📄Информация о последней атаке ➜\n\n"
        f"💎Статус: {user_data.status} кругов\n"
        f"〰️\n"
        f"☎️Номер телефона: {user_data.last_phone}\n"
        f"〰️\n"
        f"📅Дата и время: {dateTime.datetime_format(user_data.last_date)}"
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
        invoice = WALLET.create_invoice(value=amount, expirationDateTime=dateTime.datetime_format(dt.now()+timedelta(hours=6)))

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

@dp.callback_query_handler(lambda query: query.data.startswith(("num")))
async def pay_number(query: CallbackQuery):
    metadata_service = query.data.split("_")
    del metadata_service[0]
    
    service, price = metadata_service
    
    balance = await User.objects.get(user_id=query.from_user.id)
    host_site_api = config["host_site_api"] 
    api_key = config["api_key"]
    
    if int(balance.balance) < int(price):
        return await bot.edit_message_text(
            chat_id=query.from_user.id, 
            message_id=query.message.message_id, 
            text="У вас недостаточно средств!"
        )
    
    async with ClientSession() as client_session:
        async with client_session.get(f"http://{host_site_api}/stubs/handler_api.php?api_key={api_key}&action=getNumber&service={service}&operator=any&country=russia") as resp:
            phone = await resp.text()
            await client_session.close()

    if phone == "NO_NUMBERS":
        return await query.answer("Номера отсутствуют!")
    
    elif phone == "NO_BALANCE":
        host_site_main = config["host_site_main"]
        await bot.send_message(
            config["chat_id"], 
            text=f"Нужно пополнить счет! https://{host_site_main}"
            )

        await query.answer(text="Неизвестная ошибка!")
    
    else:

        status_phone, id_phone, self_phone = phone.split(":")

        cancel_phone = InlineKeyboardMarkup(
            inline_keyboard = [
                [InlineKeyboardButton(text="Отменить", callback_data=f"cancel-num_{id_phone}")]
            ]
        )

        await bot.edit_message_text(
                chat_id = query.message.chat.id, 
                message_id = query.message.message_id, 
                text=f"Status: <b>{status_phone}</b>\n"
                f"ID: <code>{id_phone}</code>\n"
                f"Number: <code>{self_phone}</code>", 
                reply_markup=cancel_phone
                )
        
        while True:
            #GET ID ORDER
            async with ClientSession() as client_session:
                async with client_session.get(f"http://{host_site_api}/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id_phone}") as get_id:
                    get_id = await get_id.text()

            if get_id == "STATUS_WAIT_CODE":pass
            elif get_id.startswith(("STATUS_OK")):
                #UPDATE BALANCE
                new_balance = float(balance.balance) - float(price) 
                await balance.update(balance=new_balance)

                #CREATE NEW ORDER
                await FAO.objects.create(
                        user_id=query.from_user.id, 
                        service=service, 
                        price=price
                )

                code = get_id.split(":")[1]
                return await bot.send_message(
                    query.message.chat.id, 
                    text=f"Code: <code>{code}</code>"
                )

@dp.callback_query_handler(lambda query: query.data.startswith(("cancel-num")))
async def cancel_number(query: CallbackQuery):
    cancel_id_number = query.data.replace("_", " ").split()[1]

    host_site_api = config["host_site_api"] 
    api_key = config["api_key"]

    async with ClientSession() as session:

        #CANCEL ORDER
        async with session.post(f"http://{host_site_api}/stubs/handler_api.php?api_key={api_key}&action=setStatus&status=-1&id={cancel_id_number}") as resp:
            resp = await resp.text()

        if resp == "ACCESS_CANCEL":
            await query.answer(text="Номер успешно отменен.")
            await bot.delete_message(query.message.chat.id, query.message.message_id)