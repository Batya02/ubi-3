from aiogram.types import Message

from objects.globals import dp
from db_models.User import User

@dp.message_handler(commands="help")
async def help(message:Message):

    main_user_data = await User.objects.get(user_id=message.from_user.id)

    # Load help text (.txt)
    with open(r"temp/help_%s.txt" % main_user_data.language, "r", encoding="utf-8") as load_help_text:
        help_text = load_help_text.read()

    return await message.answer(text=help_text)