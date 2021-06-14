from orm import (
        Model,  DateTime, 
        String, Integer
        ) 
from objects.globals import db, metadata
from datetime import datetime as dt

class FAO(Model):
    __tablename__ = "phone_all_orders"
    __database__ = db
    __metadata__ = metadata

    id = Integer(primary_key=True)
    user_id = Integer()
    created = DateTime(default=dt.now())
    service = String(max_length=50)
    price = String(max_length=20)