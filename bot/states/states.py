from aiogram.dispatcher.filters.state import StatesGroup, State

class States(StatesGroup):
    get_amount_balance_targ = State()
    
class Mailing(StatesGroup):
    mailing_text_targ = State()

class SendMessage(StatesGroup):
    send_message_targ = State()

class Phone(StatesGroup):
    get_phone_targ = State()