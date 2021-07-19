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

@dp.message_handler(lambda message: message.text == "💣Атаковать номер")
async def attack_phone(message: Message):
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
        text=f"Отменить /start\n"
        f"Введите номер телефона(без +):"
    )

    await Phone.get_phone_targ.set()

@dp.message_handler(
    lambda message: message.text not in [k[0] for k in lang_keyboard["RU"]],
    state=Phone.get_phone_targ
    )
async def get_phone_targ(message: Message, state:FSMContext):
    await state.finish()

    if message.text == "/start":
        return await message.answer(text="Отмена")

    elif not message.text.isdigit():
        return await message.answer(
            text="Неккоректный ввод! Номер должен содержать только цфиры."
        )
    
    # Create new attack object.
    # params: user phone and user id
    globals.client_session_object = Attack(
            phone=phone_format(message.text),
            user_id=message.from_user.id)
    
    # set new object in variable
    globals.UserData = UserData

    # Attack stopped button
    stoped_attack = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text="⏹Остановить", callback_data="stoped_attack"
                    )
            ]
        ]
    )

    await message.answer(
        "Остановить атаку?", 
        reply_markup=stoped_attack
    )

    await globals.client_session_object.start(message)   