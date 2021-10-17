import asyncio
from os import path
from json import dumps, loads
from loguru import logger
from requests import get

from flask import Flask

from databases import Database
from sqlalchemy import MetaData, create_engine

from objects import globals

async def main():

    if not path.isfile(r"config.json"):
        with open(r"config.json", "w") as add_config:
            add_config.write(
                dumps({
                    "SECRET_KEY":"", 
                    "DEBUG":False
                    },indent=4)
            )
            add_config.close()
    
    with open(r"config.json", "r", encoding="utf-8") as load_config:
        globals.config = loads(load_config.read())

    if not globals.config["SECRET_KEY"]:
        return logger.error("Not found SECRET KEY!")

    globals.ip_adress = get("https://api.ipify.org").text
    globals.app = Flask(__name__)
    globals.app.config['SECRET_KEY'] = globals.config["SECRET_KEY"]

    #Database
    globals.db = Database("sqlite:///../db/db.sqlite")
    globals.metadata = MetaData()

    globals.db_engine = create_engine(str(globals.db.url))
    globals.metadata.create_all(globals.db_engine)

    from db_models.AdminAuth import AdminAuth

    #Set admin password
    admin_data = await AdminAuth.objects.all()
    globals.admin_password = admin_data[0].password

    import commands

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    try:
        globals.app.run(host="0.0.0.0", port="5002", debug=globals.config["DEBUG"])
    except AttributeError:pass