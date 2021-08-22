from datetime import datetime as dt
from orm import Model, DateTime, String, Integer

from objects.globals import db, metadata


class UserData(Model):
    __tablename__ = "attack_data"
    __database__ = db
    __metadata__ = metadata

    id = Integer(primary_key=True)

    user_id = Integer()
    created = DateTime(default=dt.now())
    status = String(max_length=255)
    last_phone = String(max_length=50, default=None)
    last_created = DateTime(default=None)