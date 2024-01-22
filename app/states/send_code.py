from aiogram.fsm.state import State, StatesGroup


class SendCode(StatesGroup):
    agreement = State()
    city = State()
    phone = State()
