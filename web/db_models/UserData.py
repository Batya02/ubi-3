from orm import (
        Model,  DateTime, 
        String, Integer
        ) 
from objects.globals import db, metadata
from datetime import datetime as dt

class UserData(Model):
    __tablename__ = "data_users"
    __database__ = db
    __metadata__ = metadata

    id = Integer(primary_key=True)

    user_id = Integer()
    date = DateTime(default=dt.now())
    status = String(max_length=255)
    last_phone = String(max_length=50, default=None)
    last_date = DateTime(default=None)