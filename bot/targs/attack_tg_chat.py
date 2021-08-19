SESSIONS_PATH = "../sessions"

from os import listdir, path
from asyncio import sleep

from loguru import logger
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.errors.rpcerrorlist import (UserBannedInChannelError, ChatWriteForbiddenError,
                                          ChannelPrivateError)
@logger.catch
class Attack:

    link:str
    text:str

    def __init__(self, link, text):
        self.link = link
        self.text = text
        self.sessions:dict = {}
        self.client:TelegramClient = None

    async def start(self):
        sessions_dir = listdir(SESSIONS_PATH)

        for session in sessions_dir:
            session_data = listdir(path.join(r"%s/%s" % (SESSIONS_PATH, session)))

            session_name = (session_data[0]).replace(".session", "")
            session_config = open(r"%s/%s/%s" % (SESSIONS_PATH, session, session_data[1])).readlines()

            api_id:int = (session_config[0]).replace("\n", "")
            api_hash:str = session_config[1]

            self.cache_completed_session(session_name, int(api_id), api_hash)

            async with TelegramClient(r"%s/%s/%s" % (SESSIONS_PATH, session, session_name,), int(api_id), api_hash) as self.client:
                await self.client.connect()

                try:
                    await self.client(JoinChannelRequest(self.link))
                except ChannelPrivateError:
                    pass

                try:
                    await self.client.send_message(self.link, self.text)
                except (UserBannedInChannelError, ChatWriteForbiddenError, ChannelPrivateError,):
                    pass

                await sleep(2)

    async def leave_from_chat(self):
        for session_name, session_value in self.sessions.items():

            async with TelegramClient(r"%s/%s/%s" % (SESSIONS_PATH, session_name, session_name), session_value[0], session_value[1]) as client:
                await client.connect()
                try:
                    await client(LeaveChannelRequest(self.link))
                except ChannelPrivateError:pass

    def cache_completed_session(self, session_name:str, api_id:int, api_hash:str) -> dict:
        self.sessions[session_name] = [api_id, api_hash]
        return self.sessions
