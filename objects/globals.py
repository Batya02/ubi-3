from aiogram import Dispatcher, Bot
from databases import Database
from sqlalchemy import MetaData
from targs.attack import Attack

dp:Dispatcher = None
bot:Bot = None
config:dict = {}

db:Database = None
metadata:MetaData = None
db_engine = None
client_session_object:Attack = None
UserData = None