from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Пополнить баланс"), KeyboardButton(text="👤 Профиль")],
        [KeyboardButton(text="🎁 Продать подарок"), KeyboardButton(text="🛍 Купить подарок")],
        [KeyboardButton(text="❓ Как это работает?")]
    ],
    resize_keyboard=True
)

top_up_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="TON"), KeyboardButton(text="⭐️ Звезды")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

profile_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 Мои подарки"), KeyboardButton(text="💰 Мой баланс")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)
