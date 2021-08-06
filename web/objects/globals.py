from flask import Flask

from databases import Database
from sqlalchemy import MetaData

config:dict = {}   # Configures data

ip_adress:str = "" # Ip address
app:Flask = None   # Flask app

db:Database = None       # Db 
metadata:MetaData = None # Metadata
db_engine = None         # Db engine

users:list = []          # All users
count_users:int = 0      # Count users

admin_password:str = ""  # Admin password