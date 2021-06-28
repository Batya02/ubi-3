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

        with open(r"temp/blocked_users.txt", "r", encoding="utf-8") as load_blocked_users:
            blocked_users = load_blocked_users.read()
        
        return await message.answer(
                text=f"📊Статистика:\n"
                f"⚔️Общее количество: {len(all_users)}\n"
                f"💣Активировали бомбер: {len(activate_bomber)}\n"
                f"💎С приоритетным статусом: {len(prioritety_status)}\n"
                f"🪔Заблокировали: {int(blocked_users)}"
        )