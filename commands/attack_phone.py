from aiogram.types import (
        Message, InlineKeyboardMarkup, 
        InlineKeyboardButton
        )

from objects.globals import dp
from objects import globals

from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from targs.attack import Attack

from formats.phone import phone_format

from db_models.UserData import UserData

class Phone(StatesGroup):
    get_phone_targ = State()

@dp.message_handler(lambda message: message.text == "💣Атаковать номер")
async def attack_phone(message: Message):
    user_data = await UserData.objects.filter(user_id=message.from_user.id).all()
    
    if user_data == []:
        await UserData.objects.create(
            user_id=message.from_user.id, 
            status="30"
        )
        await message.answer(
            text="При 1-ом запуске дается 30 кругов!"
        )

    await message.answer(
        text="Введите номер телефона:"
    )

    await Phone.get_phone_targ.set()

@dp.message_handler(state=Phone.get_phone_targ)
async def get_phone_targ(message: Message, state:FSMContext):
    await state.finish()

    if not message.text.isdigit():
        return await message.answer(
            text="Неккоректный ввод! Номер должен содержать только цфиры."
        )
        
    globals.client_session_object = Attack(
            phone=phone_format(message.text),
            user_id=message.from_user.id)
    globals.UserData = UserData

    stoped_attack = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(
            text="⏹Остановить", callback_data="stoped_attack"
        )]]
    )

    await message.answer(
        "Остановить атаку?", 
        reply_markup=stoped_attack
    )

    await globals.client_session_object.start(message)   