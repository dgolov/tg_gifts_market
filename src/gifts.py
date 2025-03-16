from aiogram.fsm.state import StatesGroup, State


class SellGift(StatesGroup):
    gift_name = State()
    gift_model = State()
    gift_background = State()
    gift_color = State()
    gift_pattern = State()
    waiting_for_price = State()
    gift_public = State()
