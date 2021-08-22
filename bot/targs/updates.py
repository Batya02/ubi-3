from datetime import datetime as dt

from db_models.UserAuth import UserAuth

def update_time(main):
    async def wrapper_function(*args):
        user_id = (args[0]).from_user.id
        user = await UserAuth.objects.get(login=user_id)
        await user.update(last_active=dt.now())
        return await main(args)
    return wrapper_function