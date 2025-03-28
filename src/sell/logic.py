from aiogram.types.user import User
from config import logger
from datetime import datetime
from db.engine import AsyncSessionLocal
from db.repository_entity import GiftEntity
from typing import Dict, Union, Optional


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

    def _prepare_data(
            self,
            data: Dict[str, Optional[str]],
            user: User,
            post_id: int
    ) -> Dict[str, Union[int, str, float, datetime]]:
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
            "gift_model": data.get('gift_model'),
            "gift_background": data.get('gift_background'),
            "gift_color": data.get('gift_color'),
            "gift_pattern": data.get('gift_pattern'),
            "price": float(data.get('price')),
            "created_at": datetime.now(),
            "post_id": post_id,
        }

    def get_gift_name(self, gift_name: Optional[str]) -> Optional[str]:
        ...

    def get_gift_model(self, gift_model: Optional[str]) -> Optional[str]:
        ...

    def get_gift_background(self, gift_background: Optional[str]) -> Optional[str]:
        ...

    def get_gift_color(self, gift_color: Optional[str]) -> Optional[str]:
        ...

    def get_gift_pattern(self, gift_pattern: Optional[str]) -> Optional[str]:
        ...

    def get_gift_price(self, gift_price: Optional[str]) -> Optional[str]:
        ...
