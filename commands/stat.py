from objects.globals import dp, config

from aiogram.types import Message

from db_models.User import User
from db_models.UserData import UserData

@dp.message_handler(commands="stat")
async def stat(message: Message):
    if message.from_user.id in config["admins"]:
        all_users = await User.objects.all()
        activate_bomber = await UserData.objects.all()
        prioritety_status = await UserData.objects.filter(status="∞").all()
        
        return await message.answer(
                text=f"Общее количество: {len(all_users)}\n"
                f"Активировали бомбер: {len(activate_bomber)}\n"
                f"С приоритетным статусом: {len(prioritety_status)}"
        )