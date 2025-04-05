from aiogram import Dispatcher
from aiogram import types
from aiogram.fsm.context import FSMContext
from config import logger
from src.buy.logic import GiftLogic
from src.helpers import prepare_gift_list_message, check_gift_number_for_buy_logic
from src.gifts import BuyGift
from src.buttons import colors_menu, models_menu, patterns_menu, main_menu, cancel_button
from src.patterns import Menu


async def buy_gift_start(message: types.Message, state: FSMContext):
    """ Начало процесса покупки подарка
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.buy] Start command from user: {username} (id: {user_id})")

    await message.answer("📝 Укажите название подарка:", reply_markup=cancel_button)
    await state.set_state(BuyGift.gift_name)


async def set_gift_name(message: types.Message, state: FSMContext):
    """ Получаем название подарка и продолжаем выбор модели
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.buy] Set gift name {message.text} command from user: {username} (id: {user_id})")

    await state.update_data(gift_name=message.text)
    await message.answer(
        text="📦 Выберите модель подарка (если не важно, ставите -):",
        reply_markup=models_menu
    )
    await state.set_state(BuyGift.gift_model)


async def set_gift_model(message: types.Message, state: FSMContext):
    """ Получаем модель подарка и продолжаем выбор фона
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.buy] Set gift model {message.text} command from user: {username} (id: {user_id})")

    await state.update_data(gift_model=message.text)
    await message.answer(
        text="🖼 Выберите фон подарка (если не важно, ставите -):",
        reply_markup=colors_menu
    )
    await state.set_state(BuyGift.gift_background)


async def set_gift_background(message: types.Message, state: FSMContext):
    """ Получаем цвет подарка и продолжаем выбор узора
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.buy] Set gift color {message.text} command from user: {username} (id: {user_id})")

    await state.update_data(gift_color=message.text)
    await message.answer(
        text="🌟 Выберите узор подарка (если не важно, ставите -):",
        reply_markup=patterns_menu
    )
    await state.set_state(BuyGift.gift_symbol)


async def set_gift_symbol(message: types.Message, state: FSMContext):
    """ Получаем узор подарка и продолжаем выбор номера
    """
    username = message.from_user.username
    user_id = message.from_user.id
    logger.debug(f"[Handlers.buy] Set gift price {message.text} command from user: {username} (id: {user_id})")

    await state.update_data(gift_symbol=message.text)
    await message.answer(
        text="🔢 Укажите номер подарка (если не важно, ставите -):",
        reply_markup=cancel_button
    )
    await state.set_state(BuyGift.gift_number)


async def set_gift_number(message: types.Message, state: FSMContext):
    """ Получаем номер подарка и показываем результаты
    """
    username = message.from_user.username
    user_id = message.from_user.id
    try:
        check_gift_number_for_buy_logic(gift_number=message.text)
    except ValueError:
        await message.answer("#️⃣ Номер подарка должен быть числом:", reply_markup=cancel_button)
        await state.set_state(BuyGift.gift_number)
        return
    logger.debug(f"[Handlers.buy] Set gift number {message.text} command from user: {username} (id: {user_id})")

    await state.update_data(gift_number=message.text)
    data = await state.get_data()
    logger.debug(f"[Handlers.buy] Sell gift final data - {data} from user: {username} (id: {user_id})")
    gift_service = GiftLogic(data=data)

    await state.set_state(BuyGift.show_results)

    try:
        gifts = await gift_service.get_filtered_gifts()
    except Exception as e:
        logger.error(f"[Handlers.buy] Get filtered gifts error - {e}")
        await message.answer("❌ Ошибка поиска подарков.", reply_markup=main_menu)
        await state.clear()
        return

    if not gifts:
        await message.answer("❌ Подарков с такими параметрами не найдено.", reply_markup=main_menu)
        await state.clear()
        return

    average = await gift_service.get_average_price()

    try:
        response = prepare_gift_list_message(gifts=gifts, average=average)
        await message.answer(response, reply_markup=main_menu, parse_mode="MarkdownV2")
        await state.clear()
    except Exception as e:
        logger.error(f"[Handlers.buy] Get filtered gifts error - {e}")
        await message.answer("❌ Ошибка поиска подарков.", reply_markup=main_menu)
        await state.clear()
        return


def register_buy_handlers(dispatcher: Dispatcher):
    dispatcher.message.register(buy_gift_start, lambda msg: msg.text == Menu.BUY_GIFT)
    dispatcher.message.register(set_gift_name, BuyGift.gift_name)
    dispatcher.message.register(set_gift_model, BuyGift.gift_model)
    dispatcher.message.register(set_gift_background, BuyGift.gift_background)
    dispatcher.message.register(set_gift_symbol, BuyGift.gift_symbol)
    dispatcher.message.register(set_gift_number, BuyGift.gift_number)
