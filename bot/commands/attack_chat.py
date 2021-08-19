from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.storage import FSMContext

from states.states import AttackChat
from targs.attack_tg_chat import Attack
from objects.globals import dp, bot, config

@dp.message_handler(lambda message: message.text == "🚀Атаковать TG Chat")
async def attack_chat(message:Message):
    if message.from_user.id in config["admins"]:
        await message.answer(text="Введите username чата:")
        await AttackChat.get_link_chat_targ.set()

@dp.message_handler(state=AttackChat.get_link_chat_targ)
async def get_username_chat(message:Message, state:FSMContext):
    await state.update_data(link=message.text)
    await message.answer(text="Введите текст:")
    await AttackChat.get_text_targ.set()

@dp.message_handler(state=AttackChat.get_text_targ)
async def get_text_chat(message:Message, state:FSMContext):
    await state.update_data(text_chat=message.text)
    data = await state.get_data()
    
    link = data["link"]
    text_chat = data["text_chat"]

    leave_from_chat_markup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Выйти из чата", callback_data="leave-from-chat")]])
    
    global attack_tg_chat
    attack_tg_chat = Attack(link, text_chat) 

    await state.finish()

    try:
        await attack_tg_chat.start()
    except ValueError:
        return await message.answer(text="Чат не найден")

    await message.answer(text=f"Атака завершена!\n"f"Канал: {link}", reply_markup=leave_from_chat_markup)

@dp.callback_query_handler(lambda query: query.data == "leave-from-chat")
async def leave_from_chat(query:CallbackQuery):

    await attack_tg_chat.leave_from_chat()

    return await bot.edit_message_text(chat_id=query.from_user.id, message_id=query.message.message_id,
            text="Выход из чата окончен.")