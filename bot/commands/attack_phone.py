from aiogram.types import (
    Message, InlineKeyboardMarkup, 
    InlineKeyboardButton
    )

from aiogram.dispatcher.storage import FSMContext

from objects.globals import dp
from objects import globals

from targs.attack import Attack
from formats.phone import phone_format
from temp.lang_keyboards import lang_keyboard
from states.states import Phone

from db_models.UserData import UserData
from db_models.User import User

@dp.message_handler(lambda message: message.text == "💣Атаковать номер")
async def attack_phone_RU(message: Message):

    user_data = await UserData.objects.filter(user_id=message.from_user.id).all()

    # User not in database
    if len(user_data) == 0:
        await UserData.objects.create(
            user_id=message.from_user.id, 
            status="30"
        )
        
        await message.answer(
            text="🟢При 1-ом запуске дается 30 кругов!"
        )

    await message.answer(
        text=f"Отмена /start\n"
        f"Введите номер телефона(without +):"
    )

    await Phone.get_phone_targ.set()

@dp.message_handler(lambda message: message.text == "💣Attack number")
async def attack_phone_ENG(message: Message):
    user_data = await UserData.objects.filter(user_id=message.from_user.id).all()

    # User not in database
    if len(user_data) == 0:
        await UserData.objects.create(
            user_id=message.from_user.id, 
            status="30"
        )

        await message.answer(
            text="🟢At the 1st start, 30 laps are given!"
        )
    
    await message.answer(
        text=f"Cancel /start\n"
        f"Input phone number(without +):"
    )

    await Phone.get_phone_targ.set()

@dp.message_handler(
    lambda message: message.text not in [k[0] for k in lang_keyboard["RU"]],
    state=Phone.get_phone_targ
    )
async def get_phone_targ(message: Message, state:FSMContext):
    await state.finish()

    main_user_data = await User.objects.get(user_id=message.from_user.id)

    if message.text == "/start":
        if main_user_data.language == "RU":
            cancel_text = "Отмена"
        else:
            cancel_text = "Cancel"
        
        return await message.answer(text=cancel_text)

    elif not message.text.isdigit():
        if main_user_data.language == "RU":
            incorrect_input_text = "Неккоректный ввод! Номер должен содержать только цфиры."
        else:
            incorrect_input_text = "Incorrect input! The number should contain only numbers."

        return await message.answer(
            text=incorrect_input_text
        )
    
    # Create new attack object.
    # params: user phone and user id
    globals.client_session_object = Attack(
        phone=phone_format(message.text),
        user_id=message.from_user.id)
    
    # set new object in variable
    globals.UserData = UserData

    # Attack stopped button

    if main_user_data.language == "RU":
        stop_text_message = "Остановить атаку?"
        stop_text_button = "⏹Остановить"
    else:
        stop_text_message = "Stop attack?"
        stop_text_button = "⏹Stop"

    stoped_attack = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text=stop_text_button, callback_data="stoped_attack")]
        ]
    )

    await message.answer(
        text=stop_text_message, 
        reply_markup=stoped_attack
    )

    await globals.client_session_object.start(message)   