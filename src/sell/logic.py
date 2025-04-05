from config import logger
from db.engine import AsyncSessionLocal
from db.models import Gift
from db.repository_entity import GiftEntity


class GiftSaverLogic:
    @staticmethod
    async def save_post_to_db(gift: Gift) -> None:
        """ Запись публикации подарка в бд
        :param gift:
        :return:
        """
        logger.info(f"Save gift to db - {gift.dict()}")

        async with AsyncSessionLocal() as session:
            await GiftEntity(session=session).save_gift(gift=gift)
