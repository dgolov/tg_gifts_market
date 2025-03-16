from aiogram.types.user import User
from config import logger
from datetime import datetime
from db.engine import AsyncSessionLocal
from db.repository_entity import GiftEntity
from typing import Dict, Union


class GiftLogic:
    async def save_post_to_db(self, data: Dict[str, str], user: User, post_id: int) -> None:
        """ Запись публикации подарка в бд
        :param data:
        :param user:
        :param post_id:
        :return:
        """
        logger.info(f"Save gift to db - {data}")
        prepared_data = self._prepare_data(data=data, user=user, post_id=post_id)
        async with AsyncSessionLocal() as session:
            await GiftEntity(session=session).save_gift(gift_data=prepared_data)

    @staticmethod
    def _prepare_data(data: Dict[str, str], user: User, post_id: int) -> Dict[str, Union[int, str, float, datetime]]:
        """ Подготовка данных для записи в бд
        :param data:
        :param user:
        :param post_id:
        :return:
        """
        return {
            "user_id": user.id,
            "username": user.username,
            "gift_name": data.get('gift_name'),
            "gift_model": data['gift_model'],
            "gift_background": data['gift_background'],
            "gift_color": data['gift_color'],
            "gift_pattern": data['gift_pattern'],
            "price": float(data['price']),
            "created_at": datetime.now(),
            "post_id": post_id,
        }
