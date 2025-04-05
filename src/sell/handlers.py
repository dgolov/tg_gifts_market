from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from config import CHANNEL_ID, logger, dp, bot
from db.models import Gift
from src.buttons import colors_menu, models_menu, patterns_menu, public_menu, main_menu, cancel_button
from src.patterns import Menu
from src.gifts import SellGift
from src.sell.logic import GiftSaverLogic
from src.sell.parser import GiftParser

import asyncio


async def sell_gift_start(message: Message, state: FSMContext):
    """ Начало процесса продажи подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.sell] Start command from user: {username} (id: {user_id})")

    await message.answer("📝 Укажите ссылку на подарок:", reply_markup=cancel_button)
    await state.set_state(SellGift.waiting_for_url)


async def set_gift_url(message: Message, state: FSMContext):
    """ Пользователь выбрал узор, теперь запрашиваем цену
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.sell] Set gift price {message.text} command from user: {username} (id: {user_id})")

    await state.update_data(url=message.text)
    await message.answer("💰 Укажите цену подарка в TON:", reply_markup=cancel_button)
    await state.set_state(SellGift.waiting_for_price)


async def set_gift_price(message: Message, state: FSMContext):
    """ Завершаем процесс продажи подарка
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id

    try:
        price = float(message.text)
    except ValueError:
        await message.answer("#️⃣ Цена подарка должна быть числом:", reply_markup=cancel_button)
        await state.set_state(SellGift.waiting_for_price)
        return

    await state.update_data(price=price)

    logger.debug(f"[Handlers.sell] Set gift pattern {message.text} command from user: {username} (id: {user_id})")

    await asyncio.sleep(1)

    data = await state.get_data()
    logger.debug(f"[Handlers.sell] Set gift final data - {data} from user: {username} (id: {user_id})")
    parser = GiftParser(url=data.get('url'))
    parser.parse_html()
    gift: Gift = parser.gift
    gift.price = price
    gift.username = username
    gift.user_id = user_id

    await state.update_data(gift=gift)

    await message.answer(
        f"✅ Ваш подарок готов к продаже!\n\n"
        f"🎁 Ссылка: {gift.url}\n"
        f"🎁 Название: {gift.name}\n"
        f"#️⃣ Номер: {gift.number}\n"
        f"📦 Модель: {gift.model}\n"
        f"🖼 Фон: {gift.background}\n"
        f"🌟 Символ: {gift.symbol}\n\n"
        f"💰 Цена: {gift.price}\n\n"
        f"🔄 Опубликовать или вернуться главное в меню?",
        reply_markup=public_menu
    )

    await state.set_state(SellGift.waiting_for_public)


async def public_gift(message: Message, state: FSMContext):
    """ Завершаем процесс продажи подарка и публикуем в канал
    :param message:
    :param state:
    :return:
    """
    username = message.from_user.username
    user_id = message.from_user.id
    data = await state.get_data()

    gift: Gift = data.get('gift')

    logger.info(f"[Handlers.sell] New gift for sell from {username} (id: {user_id}): {data}")

    post_text = (
        f"🎁 *Новый подарок на продажу!*\n\n"
        f"🎁 *Ссылка:* {gift.url}\n"
        f"💰 *Цена:* {gift.price} TON\n\n"
        f"💬 Свяжитесь с продавцом в ЛС: @{username}\n\n"
    )

    try:
        if "gift_screenshot" in data:
            sent_message = await bot.send_photo(
                CHANNEL_ID,
                photo=data["gift_screenshot"],
                caption=post_text,
                parse_mode="Markdown"
            )
        else:
            sent_message = await bot.send_message(CHANNEL_ID, post_text, parse_mode="Markdown")

        post_id = sent_message.message_id
        gift.post_id = post_id
        logger.debug(f"[Handlers.sell] Post id - {post_id}")

        await GiftSaverLogic().save_post_to_db(gift=gift)
        logger.info(f"[Handlers.sell] Public gift in channel {CHANNEL_ID} successfully")
    except Exception as e:
        logger.error(f"[Handlers.sell] Public gift in channel {CHANNEL_ID} error: {e}")
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
    dispatcher.message.register(set_gift_url, SellGift.waiting_for_url)
    dispatcher.message.register(set_gift_price, SellGift.waiting_for_price)
    dispatcher.message.register(public_gift, SellGift.waiting_for_public)
