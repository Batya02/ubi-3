from aiogram.dispatcher.filters.state import StatesGroup, State

class Mailing(StatesGroup):
    mailing_text_targ = State()