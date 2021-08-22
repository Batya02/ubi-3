from datetime import datetime as dt
from orm import Model, DateTime, String, Integer, Float

from objects.globals import db, metadata


class UserAuth(Model):
    __tablename__ = "user_auth"
    __database__ = db
    __metadata__ = metadata

    id = Integer(primary_key=True)
    login = Integer()
    password = String(max_length=10)
    username = String(max_length=255, allow_null=True)
    last_name = String(max_length=150, allow_null=True)
    first_name = String(max_length=150, allow_null=True)
    last_password = String(max_length=10)
    last_active = DateTime(default=dt.now())
    date_joined = DateTime(default=dt.now())
    language = String(max_length=32, default=None)
    balance = Float(default=0.0)
    ip_address = String(max_length=15, default=None)