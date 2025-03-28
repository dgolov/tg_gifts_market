from aiogram import Dispatcher
from aiogram import types
from aiogram.fsm.context import FSMContext
from config import logger
from src.gifts import BuyGift
from src.buttons import colors_menu, backgrounds_menu, models_menu, patterns_menu, main_menu, cancel_button
from src.patterns import Menu


async def buy_gift_start(message: types.Message, state: FSMContext):
    """ Начало процесса покупки подарка
    """
    await message.answer("📝 Укажите название подарка:", reply_markup=cancel_button)
    await state.set_state(BuyGift.gift_name)


async def set_gift_name(message: types.Message, state: FSMContext):
    """ Получаем название подарка и продолжаем выбор модели
    """
    await state.update_data(gift_name=message.text)
    await message.answer(
        text="📦 Выберите модель подарка (если не важно, ставите -):",
        reply_markup=models_menu
    )
    await state.set_state(BuyGift.gift_model)


async def set_gift_model(message: types.Message, state: FSMContext):
    """ Получаем модель подарка и продолжаем выбор фона
    """
    await state.update_data(gift_model=message.text)
    await message.answer(
        text="🖼 Выберите фон подарка (если не важно, ставите -):",
        reply_markup=backgrounds_menu
    )
    await state.set_state(BuyGift.gift_background)


async def set_gift_background(message: types.Message, state: FSMContext):
    """ Получаем цвет подарка и продолжаем выбор цвета
    """
    await state.update_data(gift_background=message.text)
    await message.answer(
        text="🎨 Выберите цвет подарка (если не важно, ставите -):",
        reply_markup=colors_menu
    )
    await state.set_state(BuyGift.gift_color)


async def set_gift_color(message: types.Message, state: FSMContext):
    """ Получаем цвет подарка и продолжаем выбор узора
    """
    await state.update_data(gift_color=message.text)
    await message.answer(
        text="🌟 Выберите узор подарка (если не важно, ставите -):",
        reply_markup=patterns_menu
    )
    await state.set_state(BuyGift.gift_pattern)


async def set_gift_pattern(message: types.Message, state: FSMContext):
    """ Получаем узор подарка и продолжаем выбор номера
    """
    await state.update_data(gift_pattern=message.text)
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

    await state.update_data(gift_number=message.text)
    await message.answer("Теперь мы покажем вам доступные подарки:", reply_markup=cancel_button)

    data = await state.get_data()
    logger.debug(f"[Handlers] Sell gift final data - {data} from user: {username} (id: {user_id})")

    await state.set_state(BuyGift.show_results)


def register_buy_handlers(dispatcher: Dispatcher):
    dispatcher.message.register(buy_gift_start, lambda msg: msg.text == Menu.BUY_GIFT)
    dispatcher.message.register(set_gift_name, BuyGift.gift_name)
    dispatcher.message.register(set_gift_model, BuyGift.gift_model)
    dispatcher.message.register(set_gift_background, BuyGift.gift_background)
    dispatcher.message.register(set_gift_color, BuyGift.gift_color)
    dispatcher.message.register(set_gift_pattern, BuyGift.gift_pattern)
    dispatcher.message.register(set_gift_number, BuyGift.gift_number)
