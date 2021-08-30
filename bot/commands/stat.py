import inspect
from aiogram.types import Message

from objects.globals import dp, config
from db_models.UserAuth import UserAuth
from db_models.UserData import UserData
from decorators.updates import update_time
from targs.users import last_day_users

@dp.message_handler(commands="stat")
@dp.message_handler(lambda message: message.text=="📊Статистика")
@update_time
async def stat(message: Message):
    """Show statistics

    :param: message
    :type: Message
    :return: Bot message answer
    :rtype: Message

    """

    message: Message = message[0]

    if message.from_user.id in config["admins"]:
        all_users: UserAuth = await UserAuth.objects.all()
        activate_bomber: UserData = await UserData.objects.all()
        prioritety_status: UserData = await UserData.objects.all(status="∞")
        web_url: str = config["web_url"]

        with open(r"temp/blocked_users.txt", "r", encoding="utf-8") as load_blocked_users:
            blocked_users = load_blocked_users.read()

        return await message.answer(
            text=f"📊Статистика:\n"
            f"⚔️Общее количество: {len(all_users)}\n"
            f"👀Активные за день: {await last_day_users()}\n"
            f"💣Активировали бомбер: {len(activate_bomber)}\n"
            f"💎С приоритетным статусом: {len(prioritety_status)}\n"
            f"🪔Заблокировали: {int(blocked_users)}\n\n"
            f"Узнать больше: {web_url}")