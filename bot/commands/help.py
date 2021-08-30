from aiogram.types import Message

from objects.globals import dp
from db_models.UserAuth import UserAuth
from decorators.updates import update_time

@dp.message_handler(commands="help")
@update_time
async def help(message: Message):
    message: Message = message[0]
    main_user_data = await UserAuth.objects.get(login=message.from_user.id)
    # Load help text (.txt)
    with open(r"temp/help_%s.txt" % main_user_data.language, "r", encoding="utf-8") as load_help_text:
        help_text = load_help_text.read()
        
    return await message.answer(text=help_text)