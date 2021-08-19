from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from objects.globals import dp, config
from temp.lang_keyboards import admin_keyboard

@dp.message_handler(commands="admin")
async def admin(message:Message):

    if message.from_user.id in config["admins"]:
        buttons = list(zip([KeyboardButton(admin_keyboard[k]) for k in range(len(admin_keyboard)) if k % 2 == 0],
                    [KeyboardButton(admin_keyboard[k]) for k in range(len(admin_keyboard)) if k % 2 != 0]))

        return await message.answer(text="Меню", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, keyboard=buttons))