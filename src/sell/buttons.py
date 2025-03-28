from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


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


public_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Опубликовать"), KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )
