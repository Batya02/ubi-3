from orm import (
        Model,  DateTime, 
        String, Integer, 
        Float
        ) 
from objects.globals import db, metadata
from datetime import datetime as dt

class User(Model):
    __tablename__ = "all_users"
    __database__ = db
    __metadata__ = metadata

    id = Integer(primary_key=True)

    user_id  = Integer()
    username = String(max_length=255)
    created  = DateTime(default=dt.now())
    language = String(max_length=4)
    balance  = Float()