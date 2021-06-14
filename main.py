from os import path, mkdir
import asyncio
from json import dumps, loads
from loguru import logger

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from databases import Database
from sqlalchemy import MetaData, create_engine

from objects import globals

async def main():

    if not path.exists(r"config"):
        mkdir(r"config")
        with open(r"config/config.json", "w") as add_cfg:
            add_cfg.write(dumps({
                "token":"", 
                "admins":[], 
                "chat_id":None,
                "super_groups":[], 
                
                "api_key":"", 
                "host_site_api":"", 
                "host_site_main":"", 

                "qiwi_private_key":"", 
                "qiwi_phone":""
                }, indent=4)
            )
            add_cfg.close()
    
    with open(r"config/config.json", "r", encoding="utf-8") as load_cfg:
        globals.config = loads(load_cfg.read())
        logger.info("[+] Configuration loaded!")
    
    if not path.exists(r"debug"):
        mkdir(r"debug")
    
    logger.add(
            r"debug/debug.log", format="{time} {level} {message}", 
            level="DEBUG",      rotation="1 week", 
            compression="zip"
            )

    #Connect to database
    globals.db = Database(r"sqlite:///db/UBI.sqlite")
    globals.metadata = MetaData()

    globals.db_engine = create_engine(str(globals.db.url))
    globals.metadata.create_all(globals.db_engine)

    #Connect to Telegram API
    globals.bot = Bot(token=globals.config["token"], parse_mode="HTML")
    globals.dp = Dispatcher(globals.bot, storage=MemoryStorage())

    import commands
    
    await globals.dp.start_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:pass
