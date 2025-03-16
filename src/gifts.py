from aiogram.fsm.state import StatesGroup, State


class SellGift(StatesGroup):
    gift_name = State()
    gift_model = State()
    gift_background = State()
    gift_color = State()
    gift_pattern = State()
    gift_public = State()
