from objects.globals import dp, bot

from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BotBlocked, UserDeactivated, ChatNotFound

from states.states import Mailing

from db_models.User import User
from asyncio import sleep
from datetime import datetime as dt

from temp.lang_keyboards import lang_keyboard

@dp.message_handler(commands="mail")
async def mailing(message: Message):
    await message.answer(
        text="Отмена рассылки -> /start\nВведите текст для рассылки:"
    )

    await Mailing.mailing_text_targ.set()

@dp.message_handler(
        lambda message: message.text not in [k[0] for k in lang_keyboard["RU"]], 
        state=Mailing.mailing_text_targ)
async def get_mailing_text(message: Message, state:FSMContext):
    if message.text == "/start":
        await state.finish()
        return await message.answer("Рассылка отменена!")

    users = await User.objects.all()
    
    start_time = dt.now()

    blocked:int = 0

    for i, user in enumerate(users):
        if i % 5 == 0:
            await sleep(1)
        try:
            await bot.send_message(
                user.user_id, 
                text=message.text
            )
        except (BotBlocked, UserDeactivated, ChatNotFound):
            blocked += 1
    
    with open(r"temp/blocked_users.txt", "w") as add_blocked_count_users:
        add_blocked_count_users.write(str(blocked))
        add_blocked_count_users.close()

    end_time = int((dt.now() - start_time).total_seconds())
    
    await message.answer(
        text=f"Рассылка заврешена!\n"
        f"Минут: {end_time // 60} Секунд: {end_time % 60}"
    )

    await state.finish()