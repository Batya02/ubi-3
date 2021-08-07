from objects.globals import dp, bot, config 

from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from states.states import SendMessage

from temp.lang_keyboards import lang_keyboard

@dp.message_handler(lambda message: message.text == "✉️Отправить сообщение")
async def send_message(message: Message):
    await message.answer("\nОтменить отправку сообщения -> /start\nНапишите сообщение администратору.\nОтвет поступит через некоторое время:")
    await SendMessage.send_message_targ.set()

@dp.message_handler(
    lambda message: message.text not in [k[0] for k in lang_keyboard["RU"]], 
    state=SendMessage.send_message_targ
    )
async def send_message_process(message: Message, state:FSMContext):

    if message.text == "/start":
        await state.finish()
        return await message.answer("Отмена")
    
    await state.finish()
    username = f"@{message.from_user.username}" if not None else "Unknow"
    await bot.send_message(
        chat_id=config["chat_id"], 
        text=f"User Id: <code>{message.from_user.id}</code>\n"
        f"Username: {username}\n"
        f"Message: {message.text}"
    )

    await message.answer(text="✅Сообщение успешно доставлено!")