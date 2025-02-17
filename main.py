import asyncio
from config import dp, bot, logger
from src.handlers import register_handlers


async def main():
    """ Основная асинхронная функция
    :return:
    """
    logger.debug("Bot is online")
    register_handlers(dispatcher=dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
