from aiogram.dispatcher.filters.state import StatesGroup, State

class Mailing(StatesGroup):
    mailing_text_targ = State()

class SendMessage(StatesGroup):
    send_message_targ = State()