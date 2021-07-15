from flask import Flask

from databases import Database
from sqlalchemy import MetaData

ip_adress:str = ""
app:Flask = None

db:Database = None
metadata:MetaData = None
db_engine = None

first_count = 0
last_count = 15