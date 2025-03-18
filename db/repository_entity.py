from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models import Gift


class BaseEntity:
    def __init__(self, session: AsyncSession):
        self.session = session


class GiftEntity(BaseEntity):
    async def save_gift(self, gift_data: dict):
        """ Сохраняем подарок в БД
        :param gift_data:
        :return:
        """
        gift = Gift(**gift_data)
        self.session.add(gift)
        await self.session.commit()
        await self.session.refresh(gift)
        return gift

    async def get_gift_by_user(self, user_id: int):
        """ Получаем подарок пользователя
        :param user_id:
        :return:
        """
        result = await self.session.execute(select(Gift).where(Gift.user_id == user_id))
        return result.scalars().first()
