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

cancel_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Отмена")]],
    resize_keyboard=True
)

models_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 Стандарт"), KeyboardButton(text="🎁 Премиум")],
        [KeyboardButton(text="🎁 Уникальный"), KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)

backgrounds_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔵 Синий"), KeyboardButton(text="🔴 Красный")],
        [KeyboardButton(text="🟢 Зеленый"), KeyboardButton(text="⚫️ Черный")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)

colors_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔵 Голубой"), KeyboardButton(text="🟡 Желтый")],
        [KeyboardButton(text="🟠 Оранжевый"), KeyboardButton(text="🟣 Фиолетовый")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)

patterns_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✨ Блестки"), KeyboardButton(text="🌀 Вихрь")],
        [KeyboardButton(text="📸 Полосы"), KeyboardButton(text="🖼 Градиент")],
        [KeyboardButton(text="❌ Отмена")]
    ],
    resize_keyboard=True
)
