from objects.globals import dp, bot

from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from states.states import Mailing

from db_models.User import User
from asyncio import sleep
from datetime import datetime as dt

@dp.message_handler(commands="mail")
async def mailing(message: Message):
    await message.answer(
        text="Введите текст для рассылки:"
    )

    await Mailing.mailing_text_targ.set()

@dp.message_handler(state=Mailing.mailing_text_targ)
async def get_mailing_text(message: Message, state:FSMContext):
    users = await User.objects.all()
    
    start_time = dt.now()

    for i, user in enumerate(users):
        if i % 5 == 0:
            await sleep(1)

        await bot.send_message(
            user.user_id, 
            text=message.text
        )
    
    end_time = int((dt.now() - start_time).total_seconds())
    
    await message.answer(
        text=f"Рассылка заврешена!\n"
        f"Минут: {end_time // 60} Секунд: {end_time % 60}"
    )

    await state.finish()
