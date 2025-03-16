from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import CHANNEL_ID, logger, dp, bot
from src.buttons import (
    main_menu, top_up_menu, profile_menu, cancel_button, colors_menu, backgrounds_menu, models_menu, patterns_menu,
    public_menu
)
from src.gifts import SellGift
from src.helpers import check_subscription

import asyncio


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


async def sell_gift_start(message: Message, state: FSMContext):
    """ Начало процесса продажи подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Sell gift Start command from user: {username} (id: {user_id})")
    await message.answer("📝 Укажите название подарка:", reply_markup=cancel_button)
    await state.set_state(SellGift.gift_name)


async def set_gift_name(message: Message, state: FSMContext):
    """ Получаем название подарка и запоминаем
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Sell gift name {message.text} command from user: {username} (id: {user_id})")
    await state.update_data(gift_name=message.text)
    await message.answer("📦 Выберите модель подарка:", reply_markup=models_menu)
    await state.set_state(SellGift.gift_model)


async def set_gift_model(message: Message, state: FSMContext):
    """ Получаем модель подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Sell gift model {message.text} command from user: {username} (id: {user_id})")
    await state.update_data(gift_model=message.text)
    await message.answer("🖼 Выберите фон подарка (цветовая категория):", reply_markup=backgrounds_menu)
    await state.set_state(SellGift.gift_background)


async def set_gift_background(message: Message, state: FSMContext):
    """ Получаем фон подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Sell gift background {message.text} command from user: {username} (id: {user_id})")
    await state.update_data(gift_background=message.text)
    await message.answer("🎨 Выберите цвет подарка:", reply_markup=colors_menu)
    await state.set_state(SellGift.gift_color)


async def set_gift_color(message: Message, state: FSMContext):
    """ Получаем цвет подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers] Sell gift color {message.text} command from user: {username} (id: {user_id})")
    await state.update_data(gift_color=message.text)
    await message.answer("🌟 Выберите узор подарка:", reply_markup=patterns_menu)
    await state.set_state(SellGift.gift_pattern)


async def set_gift_pattern(message: Message, state: FSMContext):
    """ Завершаем процесс продажи подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    await state.update_data(gift_pattern=message.text)

    logger.debug(f"[Handlers] Sell gift pattern {message.text} command from user: {username} (id: {user_id})")

    await asyncio.sleep(1)

    data = await state.get_data()
    logger.debug(f"[Handlers] Sell gift final data - {data} from user: {username} (id: {user_id})")

    await message.answer(
        f"✅ Ваш подарок готов к продаже!\n\n"
        f"🎁 Название: {data.get('gift_name')}\n"
        f"📦 Модель: {data.get('gift_model')}\n"
        f"🖼 Фон: {data.get('gift_background')}\n"
        f"🎨 Цвет: {data.get('gift_color')}\n"
        f"🌟 Узор: {data.get('gift_pattern')}\n\n"
        f"🔄 Опубликовать или вернуться главное в меню?",
        reply_markup=public_menu
    )
    await state.set_state(SellGift.gift_public)


async def public_gift(message: Message, state: FSMContext):
    """ Завершаем процесс продажи подарка и публикуем в канал
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    data = await state.get_data()

    logger.info(f"Новый подарок на продажу от {username} (id: {user_id}): {data}")

    post_text = (
        f"🎁 *Новый подарок на продажу!*\n\n"
        f"👤 Продавец: @{username}  \n"
        f"🎁 *Название:* {data['gift_name']}\n"
        f"📦 *Модель:* {data['gift_model']}\n"
        f"🖼 *Фон:* {data['gift_background']}\n"
        f"🎨 *Цвет:* {data['gift_color']}\n"
        f"🌟 *Узор:* {data['gift_pattern']}\n\n"
        f"💬 Свяжитесь с продавцом в ЛС: @{username}"
    )

    try:
        await bot.send_message(CHANNEL_ID, post_text, parse_mode="Markdown")
        logger.info(f"Подарок опубликован в канале {CHANNEL_ID}")
    except Exception as e:
        logger.error(f"Ошибка при публикации в канал: {e}")

    await message.answer(
        f"✅ Ваш подарок опубликован в канале! 🎉\n\n"
        f"Вы можете проверить публикацию в нашем канале: {CHANNEL_ID}",
        reply_markup=main_menu
    )

    await state.clear()


async def cancel_process(message: Message, state: FSMContext):
    """ Отмена процесса
    :param message:
    :param state:
    :return:
    """
    await state.clear()
    await message.answer("🚫 Процесс отменен. Возвращаем в главное меню.", reply_markup=main_menu)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.message.register(start_command, CommandStart())
    dispatcher.message.register(top_up_balance, lambda msg: msg.text == "💰 Пополнить баланс")
    dispatcher.message.register(show_profile, lambda msg: msg.text == "👤 Профиль")
    dispatcher.message.register(back_to_main, lambda msg: msg.text == "⬅️ Назад")
    dispatcher.message.register(sell_gift_start, lambda msg: msg.text == "🎁 Продать подарок")
    dispatcher.message.register(cancel_process, lambda msg: msg.text == "❌ Отмена")
    dispatcher.message.register(set_gift_pattern, SellGift.gift_pattern)
    dispatcher.message.register(set_gift_name, SellGift.gift_name)
    dispatcher.message.register(set_gift_model, SellGift.gift_model)
    dispatcher.message.register(set_gift_background, SellGift.gift_background)
    dispatcher.message.register(set_gift_color, SellGift.gift_color)
    dispatcher.message.register(public_gift, SellGift.gift_public)
