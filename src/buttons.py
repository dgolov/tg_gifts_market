from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from src.patterns import Menu, Gift, Color, Pattern, Profile


models_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Gift.DEFAULT), KeyboardButton(text=Gift.PREMIUM)],
        [KeyboardButton(text=Gift.UNIQUE), KeyboardButton(text=Menu.CANCEL)]
    ],
    resize_keyboard=True
)

colors_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Color.BLUE), KeyboardButton(text=Color.RED), KeyboardButton(text=Color.GREEN)],
        [KeyboardButton(text=Color.ORANGE), KeyboardButton(text=Color.YELLOW), KeyboardButton(text=Color.VIOLET)],
        [KeyboardButton(text=Color.BLACK), KeyboardButton(text=Color.WHILE), KeyboardButton(text=Color.VIOLET)],
        [KeyboardButton(text=Menu.CANCEL)]
    ],
    resize_keyboard=True
)

patterns_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✨ Блестки"), KeyboardButton(text="🌀 Вихрь")],
        [KeyboardButton(text="📸 Полосы"), KeyboardButton(text="🖼 Градиент")],
        [KeyboardButton(text=Menu.CANCEL)]
    ],
    resize_keyboard=True
)


public_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=Menu.PUBLIC), KeyboardButton(text=Menu.CANCEL)]
        ],
        resize_keyboard=True
    )


main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=Menu.BALANCE), KeyboardButton(text=Menu.PROFILE)],
        [KeyboardButton(text=Menu.SELL_GIFT), KeyboardButton(text=Menu.BUY_GIFT)],
        [KeyboardButton(text=Menu.FAQ)]
    ],
    resize_keyboard=True
)

top_up_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="TON"), KeyboardButton(text="⭐️ Звезды")],
        [KeyboardButton(text=Menu.BACK)]
    ],
    resize_keyboard=True
)

profile_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎁 Мои подарки"), KeyboardButton(text="💰 Мой баланс")],
        [KeyboardButton(text=Menu.BACK)]
    ],
    resize_keyboard=True
)

cancel_button = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=Menu.CANCEL)]],
    resize_keyboard=True
)
