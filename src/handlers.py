from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import CHANNEL_ID, logger
from src.buttons import main_menu, top_up_menu, profile_menu
from src.helpers import check_subscription


async def start_command(message: Message):
    """
    :param message:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Start command from user: {username} (id: {user_id})")
    is_subscribed = await check_subscription(user_id)

    if is_subscribed:
        await message.answer("✅ Вы подписаны на канал! Добро пожаловать!", reply_markup=main_menu)
    else:
        logger.debug(f"[Handlers] {username} (id: {user_id}) is not subscribed")
        await message.answer(
            f"⚠️ Вы не подписаны на канал!\n"
            f"Подпишитесь: {CHANNEL_ID}\n"
            f"После подписки нажмите /start"
        )


async def top_up_balance(message: Message):
    """ Обработчик кнопки 'Пополнить баланс'
    :param message:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Top up balance command from user: {username} (id: {user_id})")
    await message.answer("Выберите способ пополнения:", reply_markup=top_up_menu)


async def show_profile(message: Message):
    """ Обработчик кнопки 'Профиль'
    :param message:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Show profile command from user: {username} (id: {user_id})")
    await message.answer("👤 Профиль:", reply_markup=profile_menu)


async def back_to_main(message: Message):
    """ Обработчик кнопки 'Назад'
    :param message:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Back to main command from user: {username} (id: {user_id})")
    await message.answer("🔙 Возвращаем вас в главное меню", reply_markup=main_menu)


def register_main_handlers(dispatcher: Dispatcher):
    dispatcher.message.register(start_command, CommandStart())
    dispatcher.message.register(top_up_balance, lambda msg: msg.text == "💰 Пополнить баланс")
    dispatcher.message.register(show_profile, lambda msg: msg.text == "👤 Профиль")
    dispatcher.message.register(back_to_main, lambda msg: msg.text == "⬅️ Назад")
