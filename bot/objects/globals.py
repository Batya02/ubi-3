from aiogram import Dispatcher, Bot
from databases import Database
from sqlalchemy import MetaData
from targs.attack import Attack

# Bot
dp:Dispatcher = None
bot:Bot = None
config:dict = {}

# DB
db:Database = None
metadata:MetaData = None
db_engine = None

# Other
client_session_object:Attack = None
UserData = None