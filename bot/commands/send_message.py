from aiogram.types import Message
from aiogram.dispatcher.storage import FSMContext

from db_models.UserAuth import UserAuth
from states.states import SendMessage
from objects.globals import dp, bot, config 
from temp.lang_keyboards import lang_keyboard
from targs.updates import update_time 

@dp.message_handler(lambda message: message.text == "✉️Отправить сообщение" or message.text == "✉️Send message")
@update_time
async def send_message(message: Message):
    message: Message = message[0]

    global main_data_user
    main_data_user = await UserAuth.objects.get(login=message.from_user.id)

    if main_data_user.language == "RU":
        msg: str = "\nОтменить отправку сообщения -> /start\nНапишите сообщение администратору.\nОтвет поступит через некоторое время:"
    else:
        msg: str = "\nCancel message sending -> /start\nWrite a message to the administrator.\nThe answer will come after a while:"

    await message.answer(text=msg)
    await SendMessage.send_message_targ.set()

@dp.message_handler(lambda message: message.text not in [k[0] for k in lang_keyboard["RU"]], 
                    state=SendMessage.send_message_targ)
async def send_message_process(message: Message, state: FSMContext):

    await state.finish()

    if main_data_user.language == "RU":
        successful_send: str = "✅Сообщение успешно доставлено!"
        cancel_msg: str = "Отмена"
    else:
        successful_send: str = "✅Message successfully delivered!"
        cancel_msg: str = "Cancel"

    if message.text == "/start":
        return await message.answer(text=cancel_msg)

    username = f"@{message.from_user.username}" if message.from_user.username != None else "Unknow"

    await bot.send_message(
        chat_id=config["chat_id"], 
        text=f"UserId: <code>{message.from_user.id}</code>\n"
        f"Username: {username}\n"
        f"Message: {message.text}\n"
        f"Reply message (admin command): <code>/msg</code>")

    return await message.answer(text=successful_send)

@dp.message_handler(commands="msg")
async def reply_admin_message(message: Message):

    if message.from_user.id == int(config["chat_id"]):
        is_not_my_message: Message = message.reply_to_message
        format_user_id:int = int(is_not_my_message.text.split("\n")[0].split(" ")[1])
        format_user_message:str = is_not_my_message.text.split("\n")[2].split(" ")[1]
        my_message = message.text.split(" ")[1]
        main_user_data = await User.objects.get(user_id=format_user_id)

        if main_user_data.language == "RU":
            reply_page = f"📫Новое сообщение ➔\n\n" +\
            f"📍[От]: Admin\n" +\
            f"✔️[Ваше сообщение]: {format_user_message}\n" +\
            f"✔️[Сообщение от админа]: {my_message}\n"
        else:
            reply_page = f"📫New message ➔\n\n" +\
            f"📍[From]: Admin\n" +\
            f"✔️[Your message]: {format_user_message}\n" +\
            f"✔️[Admin message]: {my_message}\n"

        await bot.send_message(chat_id = format_user_id, text=reply_page)

        return await message.answer(text="✔️Сообщение успешно отправлено пользователю")
