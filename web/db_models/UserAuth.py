from datetime import datetime as dt

from orm import Model,  DateTime, String, Integer, Float

from objects.globals import db, metadata


class UserAuth(Model):
    __tablename__ = "user_auth"
    __database__ = db
    __metadata__ = metadata

    id = Integer(primary_key=True)
    login = String(max_length=255)
    password = String(max_length=255)
    username = String(max_length=255)
    last_name = String(max_length=255)
    first_name = String(max_length=255)
    last_password = String(max_length=255)
    last_active = DateTime(default=dt.now())
    date_joined = DateTime(default=dt.now())
    language = String(max_length=32)
    balance = Float()
    ip_address = String(max_length=15)