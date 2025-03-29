import asyncio
from config import dp, bot, logger
from src.handlers import register_main_handlers
from src.buy.handlers import register_buy_handlers
from src.sell.handlers import register_sell_handlers


async def main():
    """ Основная асинхронная функция
    :return:
    """
    logger.debug("Bot is online")
    register_main_handlers(dispatcher=dp)
    register_sell_handlers(dispatcher=dp)
    register_buy_handlers(dispatcher=dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
