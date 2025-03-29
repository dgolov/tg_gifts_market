from aiogram.types.user import User
from config import logger
from datetime import datetime
from db.engine import AsyncSessionLocal
from db.repository_entity import GiftEntity
from typing import Dict, Union, Optional


class GiftLogic:
    def __init__(self, data: Dict[str, str]):
        self.gift_name = self._prepare_str_field(field_str=data.get('gift_name', "-"))
        self.gift_model = self._prepare_str_field(field_str=data.get('gift_model', "-"))
        self.gift_background = self._prepare_str_field(field_str=data.get('gift_background', "-"))
        self.gift_pattern = self._prepare_str_field(field_str=data.get('gift_pattern', "-"))
        self.gift_number = self._prepare_str_field(field_str=data.get('gift_number', "-"))
        if self.gift_number:
            self.gift_number = int(self.gift_number)

    async def get_filtered_gifts(self):
        """ Получаем список подарков, отфильтрованных по параметрам
        """
        async with AsyncSessionLocal() as session:
            result = await GiftEntity(session=session).get_filtered_gifts(
                gift_name=self.gift_name,
                gift_model=self.gift_model,
                gift_background=self.gift_background,
                gift_pattern=self.gift_pattern,
                gift_number=self.gift_number,
            )
        logger.info(f"[get_filtered_gifts] Got {len(result)} gifts")
        return result

    async def get_average_price(self):
        logger.info("Get average price")

        async with AsyncSessionLocal() as session:
            average = await GiftEntity(session=session).get_average_price(
                gift_name=self.gift_name,
                gift_model=self.gift_model,
                gift_background=self.gift_background,
                gift_pattern=self.gift_pattern,
                gift_number=self.gift_number,
            )
        logger.info(f"[get_filtered_gifts] Got average price - {average}")
        return average

    @staticmethod
    def _prepare_str_field(field_str: str) -> Optional[str]:
        if field_str == "-":
            return None
        return field_str
