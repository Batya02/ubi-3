import threading
from typing import Any
import pandas as pd
from io import BytesIO
from asyncio import sleep
from datetime import timedelta
from aiohttp import ClientSession
from datetime import datetime as dt

from qiwipyapi import Wallet
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import (CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton, ReplyKeyboardMarkup,
                           Message)

from objects import globals
from formats import dateTime
from db_models.FAO import FAO
from states.states import States
from db_models.UserAuth import UserAuth
from db_models.UserData import UserData
from temp.select_lang import select_lang
from objects.globals import dp, bot, config
from temp.lang_keyboards import lang_keyboard

WALLET: Wallet = Wallet(
    globals.config["qiwi_phone"], p2p_sec_key=globals.config["qiwi_private_key"])


@dp.callback_query_handler(lambda query: query.data.startswith(("language")))
async def select_language(query: CallbackQuery):
    """ Select language

    :param: query
    :type: CallbackQuery
    :return: Bot message
    :rtype: Message

    """

    change_language: UserAuth = await UserAuth.objects.get(login=query.from_user.id)
    await change_language.update(language=query.data.split("_")[1])

    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id,)

    return await bot.send_message(chat_id=query.from_user.id,
                                  text=select_lang[query.data.split("_")[1]],
                                  reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=lang_keyboard[query.data.split("_")[1]]))


@dp.callback_query_handler(lambda query: query.data == "change_language")
async def change_language(query: CallbackQuery):
    """ Change language

    :param: query
    :type: CallbackQuery
    :return: Bot edit message
    :rtype: Message

    """

    languages_markup: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇬🇧ENG", callback_data="language_ENG")],
            [InlineKeyboardButton(text="🇷🇺RU", callback_data="language_RU")]
        ])

    await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                text="🌐Select the language", reply_markup=languages_markup)


@dp.callback_query_handler(lambda query: query.data == "stoped_attack")
async def stoped_attack(query: CallbackQuery):
    """ Stoped attack

    :param: query
    :type: CallbackQuery
    :return: Bot edit message
    :rtype: Message

    """

    await globals.client_session_object.stop()
    #thread = threading.Thread(target=globals.client_session_object.stop, args=())
    #await thread.start()
    main_user_data: UserAuth = await UserAuth.objects.get(login=query.from_user.id)

    if main_user_data == "RU":
        text: str = "✅Атака остановлена"
    else:
        text: str = "✅Attack stopped"

    await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                text=text)


@dp.callback_query_handler(lambda query: query.data == "info_about_the_last_attack")
async def get_info_about_the_last_attack(query: CallbackQuery):
    """ Get info about the last attack

    :param: query
    :type: CallbackQuery
    :return: Bot edit message
    :rtype: Message

    """

    main_user_data: UserAuth = await UserAuth.objects.get(login=query.from_user.id)
    user_data: UserData = await UserData.objects.filter(user_id=query.from_user.id).all()

    if not user_data:
        if main_user_data.language == "RU":
            have_not_attack_text: str = "Вы еще не совершали атаку!"
        else:
            have_not_attack_text: str = "You haven't made an attack yet"

        return await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                           text=have_not_attack_text)

    user_data = user_data[0]

    if main_user_data.language == "RU":
        unknow_msg: str = "Неизвестно"
    else:
        unknow_msg: str = "Unknow"

    phone: Any = user_data.last_phone if user_data.last_phone != None else unknow_msg
    date: Any = dateTime.datetime_format(
        user_data.last_created) if user_data.last_created != None else unknow_msg

    return await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                       text=f"📄Информация о последней атаке ➜\n\n"
                                       f"💎Статус: {user_data.status} кругов\n"
                                       f"〰️\n"
                                       f"☎️Номер телефона: {phone}\n"
                                       f"〰️\n"
                                       f"📅Дата и время: {date}")


@dp.callback_query_handler(lambda query: query.data == "top_up_balance")
async def top_up_balance(query: CallbackQuery):
    """ Set the amount to top up ()

    :param: query
    :type: CallbackQuery
    :return: Bot edit message
    :rtype: Message

    """

    main_user_data: UserAuth = await UserAuth.objects.get(login=query.from_user.id)

    if main_user_data.language == "RU":
        top_up_text: str = "Введите сумму для пополения:"
    else:
        top_up_text: str = "Enter the amount to top up:"

    await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                text=top_up_text)

    await States.get_amount_balance_targ.set()


@dp.message_handler(state=States.get_amount_balance_targ)
async def get_amount_balance(message: Message, state: FSMContext):
    """ Get the amount to top up

    :param: message
    :type: Message
    :param: state
    :type: FSMContext
    :return: Bot edit message
    :rtype: Message

    """

    await state.finish()

    try:
        amount: float = float(message.text)
        invoice = WALLET.create_invoice(
            value=amount, expirationDateTime=dateTime.datetime_format(dt.now()+timedelta(hours=3)))

        main_user_data: UserAuth = await UserAuth.objects.get(login=message.from_user.id)

        if main_user_data.language == "RU":
            payment_text_button: str = "Продолжить оплату"
            payment_text_message: str = "Продолжить оплату?"
            successfull_payment: str = "Ваш баланс успешно пополнен на %.2f₽"
            correct_input_msg: str = "Правильный формат ввода суммы - 10 или 10.0"
        else:
            payment_text_button: str = "Continue"
            payment_text_message: str = "Continue?"
            successfull_payment: str = "Your balance has been successfully credited to %.2f₽"
            correct_input_msg: str = "The correct format for entering the amount - 10 or 10.0"

        payment_url: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text=payment_text_button, url=invoice["payUrl"])]
            ])

        await message.answer(text=payment_text_message, reply_markup=payment_url)

        while True:
            status = WALLET.invoice_status(bill_id=invoice["billId"])
            if status["status"]["value"] == "PAID":
                update_balance: UserAuth = await UserAuth.objects.get(login=message.from_user.id)
                new_value_to_balance: float = float(
                    update_balance.balance) + amount
                await update_balance.update(balance=new_value_to_balance)
                return await message.answer(successfull_payment % amount)

            await sleep(5)

    except ValueError:
        return await message.answer(text=correct_input_msg)


@dp.callback_query_handler(lambda query: query.data == "get_history_activations")
async def get_history_activation(query: CallbackQuery):
    """ Get history activation

    :param: query
    :type: CallbackQuery
    :return: Bot document
    :rtype: Message

    """

    main_user_data: UserAuth = await UserAuth.objects.get(login=query.from_user.id)
    fao_data: FAO = await FAO.objects.filter(user_id=query.from_user.id).all()

    if main_user_data.language == "RU":
        wait_loading_text: str = "Дождитесь загрузки..."
        columns: list = ["ID", "Дата и время", "Сервис", "Цена"]
    else:
        wait_loading_text: str = "Wait for loading ..."
        columns: list = ["ID", "Date and time", "Service", "Price"]

    all_data: list = []
    all_data.append([id.id for id in fao_data])
    all_data.append([created.created for created in fao_data])
    all_data.append([service.service for service in fao_data])
    all_data.append([price.price for price in fao_data])

    to_write: BytesIO = BytesIO()
    data_dict: dict = dict(zip(columns, all_data))
    df = pd.DataFrame(data_dict)
    df.to_excel(to_write)

    await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                text=wait_loading_text)
    return await bot.send_document(query.message.chat.id, document=("activation.xlsx", to_write.getvalue()))


@dp.callback_query_handler(lambda query: query.data.startswith(("num")))
async def pay_number(query: CallbackQuery):
    """ Pay number virtual phone

    :param: query
    :type: CallbackQuery
    :return: Bot message or bot edit message
    :rtype: Message

    """

    metadata_service: list = query.data.split("_")
    del metadata_service[0]

    service, price = metadata_service
    balance: UserAuth = await UserAuth.objects.get(login=query.from_user.id)
    host_site_api, api_key = config["host_site_api"], config["api_key"]

    if int(balance.balance) < int(price):
        return await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
                                           text="У вас недостаточно средств!")

    # Get virtual phone request
    async with ClientSession() as client_session:
        url_format: str = (f"http://{host_site_api}/stubs/handler_api.php?api_key={api_key}"
                           f"&action=getNumber&service={service}&operator=any&country=russia")

        async with client_session.get(url_format) as resp:
            phone = await resp.text()
            await client_session.close()

    if phone == "NO_NUMBERS":
        return await query.answer("Номера отсутствуют!")
    elif phone == "NO_BALANCE":
        host_site_main: str = config["host_site_main"]
        await bot.send_message(config["chat_id"], text=f"Нужно пополнить счет! https://{host_site_main}")
        await query.answer(text="Неизвестная ошибка!")
    else:
        status_phone, id_phone, self_phone = phone.split(":")

        cancel_phone: InlineKeyboardMarkup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="Отменить", callback_data=f"cancel-num_{id_phone}")]
            ])

        # Found virtual phone page
        await bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                    text=f"Status: <b>{status_phone}</b>\n"
                                    f"ID: <code>{id_phone}</code>\n"
                                    f"Number: <code>{self_phone}</code>", reply_markup=cancel_phone)

        while True:
            # GET ID ORDER request
            async with ClientSession() as client_session:
                url_format: str = (f"http://{host_site_api}/stubs/handler_api.php?"
                                   f"api_key={api_key}&action=getStatus&id={id_phone}")

                async with client_session.get(url_format) as get_id:
                    get_id = await get_id.text()

            if get_id.startswith(("STATUS_OK")):
                # UPDATE BALANCE
                new_balance: float = float(balance.balance) - float(price)
                await balance.update(balance=new_balance)
                # CREATE NEW ORDER
                await FAO.objects.create(user_id=query.from_user.id, service=service, price=price)
                # Code
                code: str = get_id.split(":")[1]
                # Return code
                return await bot.send_message(query.message.chat.id, text=f"Code: <code>{code}</code>")


@dp.callback_query_handler(lambda query: query.data.startswith(("cancel-num")))
async def cancel_number(query: CallbackQuery):
    """ Cancel number

    :param: query
    :type: CallbackQuery
    :return: Bot answer message
    :rtype: Message

    """

    cancel_id_number: str = query.data.replace("_", " ").split()[1]
    host_site_api: str = config["host_site_api"]
    api_key: str = config["api_key"]

    async with ClientSession() as session:
        # CANCEL ORDER request
        url_format: str = (f"http://{host_site_api}/stubs/handler_api.php?"
                           f"api_key={api_key}&action=setStatus&status=-1&id={cancel_id_number}")

        async with session.post(url_format) as resp:
            resp = await resp.text()

        if resp == "ACCESS_CANCEL":
            await query.answer(text="Номер успешно отменен.")
            await bot.delete_message(query.message.chat.id, query.message.message_id)
