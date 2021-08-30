from datetime import timedelta
from datetime import datetime as dt

from db_models.UserAuth import UserAuth

async def last_day_users() -> int:
    return await UserAuth.objects.filter(last_active__gt = (dt.now() - timedelta(days=1))).count()