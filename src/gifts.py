from aiogram.fsm.state import StatesGroup, State


class SellGift(StatesGroup):
    waiting_for_url = State()
    waiting_for_price = State()
    waiting_for_public = State()


class BuyGift(StatesGroup):
    gift_name = State()
    gift_model = State()
    gift_background = State()
    gift_symbol = State()
    gift_number = State()
    show_results = State()
