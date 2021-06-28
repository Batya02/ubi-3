from objects.globals import dp

from aiogram.types import Message

@dp.message_handler(commands="help")
async def help(message:Message):
    with open(r"temp/help.txt", "r", encoding="utf-8") as load_help_text:
        help_text = load_help_text.read()

    return await message.answer(text=help_text)