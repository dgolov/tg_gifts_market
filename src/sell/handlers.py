from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config import CHANNEL_ID, logger, dp, bot
from src.buttons import colors_menu, backgrounds_menu, models_menu, patterns_menu, public_menu, main_menu, cancel_button
from src.patterns import Menu
from src.gifts import SellGift
from src.sell.logic import GiftLogic

import asyncio


async def sell_gift_start(message: Message, state: FSMContext):
    """ Начало процесса продажи подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.sell] Sell gift Start command from user: {username} (id: {user_id})")
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
    logger.debug(f"[Handlers.sell] Sell gift name {message.text} command from user: {username} (id: {user_id})")
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
    logger.debug(f"[Handlers.sell] Sell gift model {message.text} command from user: {username} (id: {user_id})")
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
    logger.debug(f"[Handlers.sell] Sell gift background {message.text} command from user: {username} (id: {user_id})")
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
    logger.debug(f"[Handlers.sell] Sell gift color {message.text} command from user: {username} (id: {user_id})")
    await state.update_data(gift_color=message.text)
    await message.answer("🌟 Выберите узор подарка:", reply_markup=patterns_menu)
    await state.set_state(SellGift.waiting_for_price)


@dp.message(SellGift.waiting_for_price)
async def set_gift_price(message: Message, state: FSMContext):
    """ Пользователь выбрал узор, теперь запрашиваем цену
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.sell] Sell gift price {message.text} command from user: {username} (id: {user_id})")
    await state.update_data(gift_pattern=message.text)
    await message.answer("💰 Укажите цену подарка в TON:", reply_markup=cancel_button)
    await state.set_state(SellGift.gift_pattern)


async def set_gift_pattern(message: Message, state: FSMContext):
    """ Завершаем процесс продажи подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    await state.update_data(price=message.text)

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
        f"💰 Цена: {data.get('price')}\n\n"
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
        f"🎁 *Название:* {data.get('gift_name')}\n"
        f"📦 *Модель:* {data.get('gift_model')}\n"
        f"🖼 *Фон:* {data.get('gift_background')}\n"
        f"🎨 *Цвет:* {data.get('gift_color')}\n"
        f"🌟 *Узор:* {data.get('gift_pattern')}\n\n"
        f"💰 *Цена:* {data.get('price')} TON\n\n"
        f"💬 Свяжитесь с продавцом в ЛС: @{username}"
    )

    try:
        sent_message = await bot.send_message(CHANNEL_ID, post_text, parse_mode="Markdown")
        post_id = sent_message.message_id
        logger.debug(f"Post id - {post_id}")
        await GiftLogic().save_post_to_db(data=data, user=message.from_user, post_id=post_id)
        logger.info(f"Подарок опубликован в канале {CHANNEL_ID}")
    except Exception as e:
        logger.error(f"Ошибка при публикации в канал: {e}")
        await message.answer(f"❌ Ошибка публикации подарка", reply_markup=main_menu)
        return

    await message.answer(
        f"✅ Ваш подарок опубликован в канале! 🎉\n\n"
        f"Вы можете проверить публикацию в нашем канале: {CHANNEL_ID}",
        reply_markup=main_menu
    )

    await state.clear()


def register_sell_handlers(dispatcher: Dispatcher):
    dispatcher.message.register(sell_gift_start, lambda msg: msg.text == Menu.SELL_GIFT)
    dispatcher.message.register(set_gift_pattern, SellGift.gift_pattern)
    dispatcher.message.register(set_gift_name, SellGift.gift_name)
    dispatcher.message.register(set_gift_model, SellGift.gift_model)
    dispatcher.message.register(set_gift_background, SellGift.gift_background)
    dispatcher.message.register(set_gift_color, SellGift.gift_color)
    dispatcher.message.register(public_gift, SellGift.gift_public)
