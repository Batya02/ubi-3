from aiogram.types import (
        Message, InlineKeyboardMarkup, 
        InlineKeyboardButton
        )

from objects.globals import dp, config

from aiohttp import ClientSession

from json import loads

@dp.message_handler(lambda message: message.text == "📲Купить виртуальный номер")
async def get_numbers(message:Message):

    host_site_main = config["host_site_main"] # Host main

    # Get all data from services
    async with ClientSession() as client_session:
        async with client_session.get(f"https://{host_site_main}/v1/guest/products/russia/any") as all_services:
            data_services = loads(await all_services.text())
            await client_session.close()
        
        # Add percent
        tg_price = int(data_services["telegram"]["Price"])  + 1 # Telegram price
        vk_price = int(data_services["vkontakte"]["Price"]) + 1 # Vkontakte price
        wa_price = int(data_services["whatsapp"]["Price"])  + 1 # Whats app price
        
        prices_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=f"Telegram {tg_price}", callback_data=f"num_telegram_{tg_price}")], 
                [InlineKeyboardButton(text=f"Vkontakte {vk_price}", callback_data=f"num_vkontakte_{tg_price}")], 
                [InlineKeyboardButton(text=f"Whatsapp {wa_price}", callback_data=f"num_whatsapp_{tg_price}")]
            ]
        )

        return await message.answer(
            text="🇷🇺Выберите сервис👇", 
            reply_markup=prices_markup
        )