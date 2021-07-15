from flask import Flask

from databases import Database
from sqlalchemy import MetaData

ip_adress:str = ""
app:Flask = None

db:Database = None
metadata:MetaData = None
db_engine = None

in_users:bool = False
users:list = []
count_users:int = 0

admin_password:str = ""